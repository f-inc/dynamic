from typing import Any, Tuple

from dynamic.runners.runner import Runner
from dynamic.runners.callable import CallableRunner, CallableRunnerConfig
from dynamic.runners.langchain import AgentRunner, AgentRunnerConfig, ChainRunner, ChainRunnerConfig
from dynamic.classes.agent import DynamicAgent

from langchain.agents import Agent, AgentExecutor
from langchain.chains.base import Chain


def get_runner(handle: Any) -> Tuple[Runner, Any]:
    if isinstance(handle, (Agent, AgentExecutor, DynamicAgent)):
        return AgentRunner, AgentRunnerConfig
    elif isinstance(handle, Chain):
        return ChainRunner, ChainRunnerConfig
    elif callable(handle):
        return CallableRunner, CallableRunnerConfig
    
    raise ValueError(f"Dynamic does not support your handler type. Type: {type(handle)}")