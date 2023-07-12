from dataclasses import dataclass
from typing import Any, Union, Dict

# dyanmic
from dynamic.runners.runner import Runner
from dynamic.runners.langchain.config import ChainRunnerConfig

# langchain
from langchain.chains.base import Chain


class ChainRunner(Runner):
    def __init__(self, handle: Chain, config: ChainRunnerConfig, **kwargs):
        if not isinstance(handle, Chain):
            raise ValueError(f"ChainRunner requires handle to be a Langchain Chain. Instead got {type(handle)}.")
        
        super(ChainRunner, self).__init__(handle, config, **kwargs)
    
    def run(self):
        prompt_input = self.config.input
        return self.handle.run(prompt_input)
