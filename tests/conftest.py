# pragma pylint: disable=missing-docstring
import json
import logging
import re
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional
from unittest.mock import MagicMock, Mock, PropertyMock

import numpy as np
import pytest

from sonworld import constants
from sonworld.worker import Worker

logging.getLogger('').setLevel(logging.INFO)


# Do not mask numpy errors as warnings that no one read, raise the exсeption
np.seterr(all='raise')


def log_has(line, logs):
    """Check if line is found on some caplog's message."""
    return any(line == message for message in logs.messages)


def log_has_when(line, logs, when):
    """Check if line is found in caplog's messages during a specified stage"""
    return any(line == message.message for message in logs.get_records(when))


def log_has_re(line, logs):
    """Check if line matches some caplog's message."""
    return any(re.match(line, message) for message in logs.messages)


def num_log_has(line, logs):
    """Check how many times line is found in caplog's messages."""
    return sum(line == message for message in logs.messages)


def num_log_has_re(line, logs):
    """Check how many times line matches caplog's messages."""
    return sum(bool(re.match(line, message)) for message in logs.messages)


# def get_args(args):
#     return Arguments(args).get_parsed_arg()


def patch_sonworld(mocker, config) -> None:
    """
    This function patch _init_modules() to not call dependencies
    :param mocker: a Mocker object to apply patches
    :param config: Config to pass to the bot
    :return: None
    """
    mocker.patch('sonworld.configuration.config_validation._validate_consumers')


def get_patched_worker(mocker, config) -> Worker:
    """
    This function patches _init_modules() to not call dependencies
    :param mocker: a Mocker object to apply patches
    :param config: Config to pass to the bot
    :return: Worker
    """
    patch_sonworld(mocker, config)
    return Worker(args=None, config=config)
