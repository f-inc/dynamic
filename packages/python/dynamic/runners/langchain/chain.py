from dataclasses import dataclass
from typing import Any, Union, Dict

# dyanmic
from dynamic.runners.runner import Runner

# langchain
from langchain.chains.base import Chain


@dataclass
class ChainConfig:
    prompt_inputs: Union[str, Dict[str, str]]

class ChainRunner(Runner):
    def __init__(self, handle: Chain, config: ChainConfig):
        if not isinstance(handle, Chain):
            raise ValueError(f"ChainRunner requires handle to be a Langchain Chain. Instead got {type(handle)}.")
        
        super(ChainRunner, self).__init__(handle, config)
    
    def run(self):
        return self.handle.run(**self.config.prompt_inputs)