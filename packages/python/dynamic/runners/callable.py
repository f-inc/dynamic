from dataclasses import dataclass
from typing import Any, Callable

# dyanmic imports
from dynamic.runners.runner import Runner, RunnerConfig

@dataclass
class CallableRunnerConfig(RunnerConfig):
    params: Any  

class CallableRunner(Runner):
    def __init__(self, handle: Callable, config: CallableRunnerConfig):
        if not callable(handle):
            raise ValueError(f"CallableRunner requires handle to be a Callable. Instead got {type(handle)}.")
        
        super(CallableRunner, self).__init__(handle, config)
    
    def run(self):
        return self.handle(**self.config.params)
