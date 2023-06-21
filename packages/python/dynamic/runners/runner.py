"""
Runner Abstraction - executes an endpoint's functionality
"""
from abc import ABC, abstractmethod

class Runner(ABC):
    def __init__(self, handle, config):
        self.handle = handle
        self.config = config
    
    @abstractmethod
    def run(self):
        pass