import asyncio
from dataclasses import dataclass
from typing import Any, Union, Dict, Optional
import logging

from fastapi import WebSocket

# dyanmic
from dynamic.runners.runner import Runner

# langchain
from langchain.agents import Agent, AgentExecutor, initialize_agent
from langchain.callbacks.base import AsyncCallbackHandler
from langchain.agents import load_tools


@dataclass
class AgentRunnerConfig:
    agent_input: Union[str, Dict[str, str]]
    streaming: bool = True

class AgentRunner(Runner):
    def __init__(self, handle: Union[Agent, AgentExecutor], config: AgentRunnerConfig, websocket: Optional[WebSocket] = None):
        self.streaming = False

        if config.streaming:
            # mark Runner as streaming
            self.streaming = True

            # Setup LLM for streaming
            llm = handle.kwargs.get("llm")
            llm.streaming = True
            llm.verbose = True
            llm.callbacks = [WebsocketCallbackHandler(websocket)]

            # Update Handle
            handle.kwargs["llm"] = llm
            handle.kwargs["tools"] = load_tools(["google-serper"], llm=llm)

            # Init AgentExecutor
            logging.info(f"Initializing agent with following kwargs: \n{handle.kwargs}")
            handle = initialize_agent(**handle.kwargs)

        if not (isinstance(handle, Agent) or isinstance(handle, AgentExecutor)):
            raise ValueError(f"AgentRunner requires handle to be a Langchain Agent or AgentExecutor. Instead got {type(handle)}.")
        
        super(AgentRunner, self).__init__(handle, config)

    async def run(self):
        agent_input = self.config.agent_input
        if self.streaming:
            return await self.handle.arun(agent_input)

        return self.handle.run(agent_input)



class WebsocketCallbackHandler(AsyncCallbackHandler):
    def __init__(self, websocket: WebSocket):
        super().__init__()
        self.websocket = websocket

    async def on_llm_new_token(self, token: str, **kwargs) -> None:
        logging.info(f"on new token {token}")
        await self.websocket.send_json(dict(data=token))
