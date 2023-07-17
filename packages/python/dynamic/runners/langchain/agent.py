import asyncio
from dataclasses import dataclass
from typing import Union, Dict, Optional

from fastapi import WebSocket

# dyanmic
from dynamic.runners.runner import Runner
from dynamic.classes.dynamic_agent  import DynamicAgent
from dynamic.runners.langchain.config import ChainRunnerConfig

# langchain
from langchain.agents import Agent, AgentExecutor, initialize_agent


class AgentRunner(Runner):
    def __init__(self,
        handle: Union[DynamicAgent, Agent, AgentExecutor],
        config: ChainRunnerConfig,
        websocket: Optional[WebSocket] = None,
        streaming: bool = False,
    ):
        self.streaming = streaming
        self.config = config

        if streaming:
            if not isinstance(handle, DynamicAgent):
                raise ValueError(f"A streaming Agent needs to a DynamicAgent, recieved {type(handle)}.")

            handle = handle._initialize_agent_with_websocket(websocket)

        if not (isinstance(handle, Agent) or isinstance(handle, AgentExecutor)):
            raise ValueError(f"AgentRunner requires handle to be a Langchain Agent or AgentExecutor. Instead got {type(handle)}.")
        
        super(AgentRunner, self).__init__(handle, config)

    async def arun(self):
        input = self.config.input
        if self.streaming:
            return await self.handle.arun(input)

        return self.handle.run(input)
    
    def run(self):
        input = self.config.input
        return self.handle.run(input)




