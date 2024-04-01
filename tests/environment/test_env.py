from copy import deepcopy
from pathlib import Path
from unittest.mock import MagicMock, PropertyMock

import pytest
from sonworld.environment.env import SonEnv


class TestEnv:
    def test_init(self):
        config = {
        }
        env = SonEnv(config)
        assert env.config == config

