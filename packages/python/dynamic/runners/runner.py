"""
Runner Abstraction - executes an endpoint's functionality
"""
from abc import ABC, abstractmethod

class RunnerConfig:
    pass

class Runner(ABC):
    def __init__(self, handle, config, **kwargs):
        self.handle = handle
        self.config = config
    
    @abstractmethod
    def run(self):
        pass