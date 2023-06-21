from dataclasses import dataclass
from typing import Any, Callable

# dyanmic imports
from dynamic.runners.runner import Runner


@dataclass
class CallableRunnerConfig:
    params: Any

    

class CallableRunner(Runner):
    def __init__(self, handle: Callable, config: CallableRunnerConfig):
        if not callable(handle):
            raise ValueError(f"CallableRunner requires handle to be a Callable. Instead got {type(handle)}.")
        
        super(CallableRunner, self).__init__(handle, config)
    
    def run(self):
        return self.handle(**self.config.params)
    
if __name__ == "__main__":
    print("Testing class...")

    def hello(msg):
        return msg
    
    config = CallableRunnerConfig(params=dict(msg="Hello World!\n-from Runner"))

    runner = CallableRunner(hello, config)

    print("Runner created and running...")
    print(runner.run())