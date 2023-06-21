from typing import Any

from dynamic.runners.runner import Runner
from dynamic.runners.callable import CallableRunner
from dynamic.runners.langchain import AgentRunner, ChainRunner

from langchain.agents import Agent, AgentExecutor
from langchain.chains.base import Chain

def get_runner(handle: Any) -> Runner:
    if callable(handle):
        return CallableRunner
    elif isinstance(handle, Chain):
        return ChainRunner
    elif isinstance(handle, Agent) or isinstance(handle, AgentExecutor):
        return AgentRunner
    
    raise ValueError(f"Dynamic does not support your handler type. Type: {type(handle)}")