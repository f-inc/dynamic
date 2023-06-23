import asyncio
from dataclasses import dataclass
from typing import Any, Union, Dict, Optional
import logging

from fastapi import WebSocket
from langchain.schema import AgentAction, AgentFinish

# dyanmic
from dynamic.runners.runner import Runner

# langchain
from langchain.agents import Agent, AgentExecutor, initialize_agent, AgentOutputParser
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.base import BaseCallbackManager
from langchain.agents import load_tools
from websockets.sync.client import connect


@dataclass
class AgentRunnerConfig:
    agent_input: Union[str, Dict[str, str]]
    streaming: bool = True

class AgentRunner(Runner):
    def __init__(self, handle: Union[Agent, AgentExecutor], config: AgentRunnerConfig, websocket: Optional[WebSocket] = None):

        if config.streaming:
            llm = handle.kwargs.get("llm")
            llm.streaming = True
            llm.verbose = True
            llm.callbacks = [StreamingWebsocketCallbackHandler(websocket)]

            handle.kwargs["llm"] = llm
            handle.kwargs["tools"] = load_tools(["wikipedia"], llm=llm)
            handle.kwargs["output_parser"] = CustomOutputParset()

            logging.info(f"Initializing agent with following kwargs: \n{handle.kwargs}")
            handle = initialize_agent(**handle.kwargs)

        if not (isinstance(handle, Agent) or isinstance(handle, AgentExecutor)):
            raise ValueError(f"AgentRunner requires handle to be a Langchain Agent or AgentExecutor. Instead got {type(handle)}.")
        
        super(AgentRunner, self).__init__(handle, config)

    def run(self):
        agent_input = self.config.agent_input
        return self.handle.run(agent_input)



class AsyncStreamingWebsocketCallbackHandler(StreamingStdOutCallbackHandler):
    def __init__(self, websocket: WebSocket):
        super().__init__()
        self.websocket = websocket
        # self.ws = connect("ws://localhost:8000/ws")

    @property
    def always_verbose(self) -> bool:
        return True

    @property
    def is_async(self) -> bool:
        return True

    async def on_llm_new_token(self, token: str, **kwargs) -> None:
        logging.info(f"on new token {token}")
        await self.websocket.send_json(dict(data=token))

    # async def on_text(self, text: str, **kwargs: Any) -> None:
    #     logging.info(f"on text {text}")
    #     await self.websocket.send_json(dict(data=text))

class StreamingWebsocketCallbackHandler(AsyncStreamingWebsocketCallbackHandler):
    @property
    def is_async(self) -> bool:
        return False

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        logging.info(f"-{token}-")
        # asyncio.run(super().on_llm_new_token(token, **kwargs))

        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(super().on_llm_new_token(token, **kwargs))
        # self.ws.send
        self._sync_execute(super().on_llm_new_token(token, **kwargs))

    def _sync_execute(self, task):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:  # 'RuntimeError: There is no current event loop...'
            loop = None
        
        if loop and loop.is_running():
            loop.create_task(task)
        else:
            asyncio.run(task)

class CustomOutputParset(AgentOutputParser):

    def parse(self, text: str) -> AgentAction | AgentFinish:
        logging.info(f"TESTTEST -{text}-")
        return super().parse(text)

