import functools
from typing import Any, Dict, List, Callable
from collections import defaultdict
from copy import copy, deepcopy
import numpy as np
from pettingzoo.utils.env import AgentID, ParallelEnv


class SonEnv(ParallelEnv):
    metadata = {'render.modes': ['human'], 'name': 'sonworld-mmo'}

    def __init__(self, config: dict, seed=None):
        self.config = config
        self._np_random = None
        self._np_seed = None
        self._reset_required = True
        self.seed(seed)
        super().__init__()

        self.obs = None
        self._agents = None
        self._dead_agents = set()
        self._dead_this_tick = None
        self.scripted_agents = set()

    def render(self, mode='human'):
        '''For conformity with the PettingZoo API only; rendering is external'''

    @property
    def agents(self) -> List[AgentID]:
        '''For conformity with the PettingZoo API'''
        # returns the list of "current" agents, both alive and dead_this_tick
        return self._agents

    def close(self):
        '''For conformity with the PettingZoo API only; rendering is external'''
  
    def seed(self, seed=None):
        '''Reseeds the environment. reset() must be called after seed(), and before step().
        - self._np_seed is None: seed() has not been called, e.g. __init__() -> new RNG
        - self._np_seed is set, and seed is not None: seed() or reset() with seed -> new RNG

        If self._np_seed is set, but seed is None
            probably called from reset() without seed, so don't change the RNG
        '''
        if self._np_seed is None or seed is not None:
            # self._np_random, self._np_seed = seeding.np_random(seed)
            self._reset_required = True
