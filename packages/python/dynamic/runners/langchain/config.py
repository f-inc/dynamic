from dataclasses import dataclass
from typing import Dict, Union

from dynamic.runners.runner import RunnerConfig

@dataclass
class ChainRunnerConfig(RunnerConfig):
    input: Union[str, Dict[str, str]]