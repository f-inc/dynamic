import asyncio
from dataclasses import dataclass
from typing import Union, Dict, Optional

from fastapi import WebSocket

# dyanmic
from dynamic.runners.runner import Runner
from dynamic.classes.agent import DynamicAgent

# langchain
from langchain.agents import Agent, AgentExecutor, initialize_agent


@dataclass
class AgentRunnerConfig:
    agent_input: Union[str, Dict[str, str]]
    streaming: bool = False

class AgentRunner(Runner):
    def __init__(self, handle: Union[DynamicAgent, Agent, AgentExecutor], config: AgentRunnerConfig, websocket: Optional[WebSocket] = None):
        self.streaming = False
        self.config = config

        if self.config.streaming:
            # mark runner as streaming
            self.streaming = True

            if not isinstance(handle, DynamicAgent):
                raise ValueError(f"A streaming Agent needs to a DynamicAgent, recieved {type(handle)}.")

            handle = handle._initialize_agent(websocket)

        if not (isinstance(handle, Agent) or isinstance(handle, AgentExecutor)):
            raise ValueError(f"AgentRunner requires handle to be a Langchain Agent or AgentExecutor. Instead got {type(handle)}.")
        
        super(AgentRunner, self).__init__(handle, config)

    async def run(self):
        agent_input = self.config.agent_input
        if self.streaming:
            return await self.handle.arun(agent_input)

        return self.handle.run(agent_input)




