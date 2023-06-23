import logging
from typing import Any, List, Optional

# fastapi
from fastapi import WebSocket

# langchain
from langchain.agents import load_tools, initialize_agent
from langchain.callbacks.base import AsyncCallbackHandler


class DynamicAgent:
    def __init__(self, llm, **kwargs):
        self.llm = llm
        self.kwargs = kwargs

    def _initialize_agent(self, websocket: WebSocket):
        logging.info("Setting up streaming settings for agent...")
        llm = self.llm

        llm.streaming = True
        llm.verbose = True
        llm.callbacks = [WebsocketCallbackHandler(websocket)]

        # TODO: Setup tools for either list of string or already pre_loaded
        tool_list = self.kwargs.get("tool_list")
        if tool_list:
            self.kwargs["tools"] = load_tools(tool_list, llm=llm)

        logging.info("Initializing agent...")
        return initialize_agent(llm=llm, **self.kwargs)


class WebsocketCallbackHandler(AsyncCallbackHandler):
    def __init__(self, websocket: WebSocket):
        super().__init__()
        self.websocket = websocket

    async def on_llm_new_token(self, token: str, **kwargs) -> None:
        await self.websocket.send_json(dict(data=token))