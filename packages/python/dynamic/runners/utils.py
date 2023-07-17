from typing import Any, Tuple

from dynamic.runners.runner import Runner, RunnerConfig
from dynamic.runners.callable import CallableRunner, CallableRunnerConfig
from dynamic.runners.langchain import AgentRunner, ChainRunner, ChainRunnerConfig
from dynamic.classes.dynamic_agent  import DynamicAgent

from langchain.agents import Agent, AgentExecutor
from langchain.chains.base import Chain


def get_runner(handle: Any) -> Tuple[Runner, RunnerConfig]:
    if isinstance(handle, (Agent, AgentExecutor, DynamicAgent)):
        return AgentRunner, ChainRunnerConfig
    elif isinstance(handle, Chain):
        return ChainRunner, ChainRunnerConfig
    elif callable(handle):
        return CallableRunner, CallableRunnerConfig
    
    # TODO: Return error, don't raise
    raise ValueError(f"Dynamic does not support your handler type. Type: {type(handle)}")