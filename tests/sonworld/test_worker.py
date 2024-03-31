import logging
import time
from datetime import timedelta
from unittest.mock import MagicMock, PropertyMock


from sonworld.enums import State
from sonworld.worker import Worker
from tests.conftest import get_patched_worker, log_has, log_has_re
import logging
import time
from datetime import timedelta
from unittest.mock import MagicMock, PropertyMock
from sonworld.enums import State
from sonworld.worker import Worker
from tests.conftest import get_patched_worker, log_has, log_has_re
import logging
import time
from datetime import timedelta
from unittest.mock import MagicMock, PropertyMock
from sonworld.enums import State
from sonworld.worker import Worker
from tests.conftest import get_patched_worker, log_has, log_has_re
import logging
from sonworld.enums import State
from sonworld.worker import Worker
from tests.conftest import get_patched_worker, log_has


def test_worker_state() -> None:
    worker = Worker(config={}, args={})
    assert worker.sonworld.state is State.STOPPED


def test_worker_running() -> None:
    worker = Worker(config={}, args={})
    worker.sonworld.state = State.RUNNING
    state = worker._worker(old_state=None)
    assert state is State.RUNNING



def test_throttle() -> None:
    worker = Worker(config={}, args={})
    worker.sonworld.state = State.RUNNING
    worker._throttle_secs = 0
    worker._throttle(func=worker._process_running, throttle_secs=0)
    assert worker._heartbeat_msg == 0
