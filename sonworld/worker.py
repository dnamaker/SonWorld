import logging
import time
import traceback
from os import getpid
from typing import Any, Callable, Dict, Optional


import sdnotify

from sonworld import __version__
from sonworld.sonworld import SonWorld
from sonworld.enums.enums import State
from sonworld.constants import PROCESS_THROTTLE_SECS, RETRY_TIMEOUT
from sonworld.exceptions import OperationalException, TemporaryError


logger = logging.getLogger(__name__)


class Worker:
    def __init__(self, args: Dict[str, Any], config: Optional[dict] = None) -> None:
        """
        Init all variables and objects the bot needs to work
        """
        logger.info(f"Starting worker {__version__}")

        self._args = args
        self._config = config
        self._init(False)

        self._heartbeat_msg: float = 0

        # Tell systemd that we completed initialization phase
        self._notify("READY=1")

    def _init(self, reconfig: bool) -> None:
        # Init the instance of the bot
        self.sonworld = SonWorld(self._config, args=self._args)

        internals_config = self._config.get("internals", {})
        self._throttle_secs = internals_config.get(
            "process_throttle_secs", PROCESS_THROTTLE_SECS
        )
        self._heartbeat_interval = internals_config.get("heartbeat_interval", 60)

        self._sd_notify = (
            sdnotify.SystemdNotifier()
            if self._config.get("internals", {}).get("sd_notify", False)
            else None
        )

    def _notify(self, message: str) -> None:
        """
        Removes the need to verify in all occurrences if sd_notify is enabled
        :param message: Message to send to systemd if it's enabled.
        """
        if self._sd_notify:
            logger.debug(f"sd_notify: {message}")
            self._sd_notify.notify(message)

    def run(self) -> None:
        state = None
        while True:
            state = self._worker(old_state=state)
            if state == State.RELOAD_CONFIG:
                self._reconfigure()

    def _worker(self, old_state: Optional[State]) -> State:
        state = self.sonworld.state

        if state != old_state:
            if old_state != State.RELOAD_CONFIG:
                self.sonworld.notify_status(f"{state.name.lower()}")

            logger.info(
                f"Changing state{f' from {old_state.name}' if old_state else ''} to: {state.name}"
            )
            if state == State.RUNNING:
                self.sonworld.startup()

            self._heartbeat_msg = 0

        if state == State.STOPPED:
            # Ping systemd watchdog before sleeping in the stopped state
            self._notify("WATCHDOG=1\nSTATUS=State: STOPPED.")

            self._throttle(
                func=self._process_stopped, throttle_secs=self._throttle_secs
            )

        elif state == State.RUNNING:
            # Ping systemd watchdog before throttling
            self._notify("WATCHDOG=1\nSTATUS=State: RUNNING.")

            # Use an offset of 1s to ensure a new candle has been issued
            self._throttle(
                func=self._process_running, throttle_secs=self._throttle_secs
            )

        if self._heartbeat_interval:
            now = time.time()
            if (now - self._heartbeat_msg) > self._heartbeat_interval:
                version = __version__
                logger.info(
                    f"World heartbeat. PID={getpid()}, "
                    f"version='{version}', state='{state.name}'"
                )
                self._heartbeat_msg = now

        return state

    def _throttle(
        self, func: Callable[..., Any], throttle_secs: float, *args, **kwargs
    ) -> Any:
        """
        Throttles the given callable that it
        takes at least `min_secs` to finish execution.
        :param func: Any callable
        :param throttle_secs: throttling interation execution time limit in seconds
        :return: Any (result of execution of func)
        """
        last_throttle_start_time = time.time()
        logger.debug("========================================")
        result = func(*args, **kwargs)
        time_passed = time.time() - last_throttle_start_time
        sleep_duration = throttle_secs - time_passed

        sleep_duration = max(sleep_duration, 0.0)
        # next_iter = datetime.now(timezone.utc) + timedelta(seconds=sleep_duration)

        logger.debug(
            f"Throttling with '{func.__name__}()': sleep for {sleep_duration:.2f} s, "
            f"last iteration took {time_passed:.2f} s."
            #  f"next: {next_iter}"
        )
        self._sleep(sleep_duration)
        return result

    @staticmethod
    def _sleep(sleep_duration: float) -> None:
        """Local sleep method - to improve testability"""
        time.sleep(sleep_duration)

    def _process_stopped(self) -> None:
        self.sonworld.process_stopped()

    def _process_running(self) -> None:
        try:
            self.sonworld.process()
        except TemporaryError as error:
            logger.warning(f"Error: {error}, retrying in {RETRY_TIMEOUT} seconds...")
            time.sleep(RETRY_TIMEOUT)
        except OperationalException:
            tb = traceback.format_exc()
            hint = "Issue `/start` if you think it is safe to restart."


            logger.exception("OperationalException. Stopping trader ...")
            self.sonworld.state = State.STOPPED

    def _reconfigure(self) -> None:
        """
        Cleans up current sonagentbot instance, reloads the configuration and
        replaces it with the new instance
        """
        # Tell systemd that we initiated reconfiguration
        self._notify("RELOADING=1")

        # Clean up current sonagent modules
        self.sonworld.cleanup()

        # Load and validate config and create new instance of the bot
        self._init(True)

        self.sonworld.notify_status("config reloaded")
        
        # Tell systemd that we completed reconfiguration
        self._notify("READY=1")

    def exit(self) -> None:
        # Tell systemd that we are exiting now
        self._notify("STOPPING=1")

        if self.sonworld:
            self.sonworld.notify_status("process died")
            self.sonworld.cleanup()
    