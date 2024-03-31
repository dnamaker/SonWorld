# pragma pylint: disable=missing-docstring

from copy import deepcopy
from pathlib import Path
from unittest.mock import MagicMock, PropertyMock

import pytest


def test_init():
    from sonworld.sonworld import SonWorld
    config = {
        'initial_state': 'STOPPED'
    }
    sonworld = SonWorld(config)
    assert sonworld.args is None
    assert sonworld.config == config


def test_sonworld_is_running_correctly():
    from sonworld.sonworld import SonWorld
    config = {
        'initial_state': 'RUNNING'
    }
    sonworld = SonWorld(config)
    print(sonworld.state)
    assert str(sonworld.state) == 'running'
