import logging
from typing import Any, Dict, List
from uuid import uuid4
import asyncio

from fastapi import WebSocket

from dynamic.classes.message import BaseMessage

class WebSocketAckTimeoutError(Exception):
    pass

DEFAULT_TIMEOUT = 10 # seconds

class ConnectionManager:
    """WebSocket connection manager."""

    # TODO: Add logs
    def __init__(self):
        logging.info("ConnectionManager starting...")
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket) -> str:
        await websocket.accept()
        id = str(uuid4())
        self.active_connections[id] = websocket

        try:
            await asyncio.wait_for(websocket.receive(), timeout=DEFAULT_TIMEOUT)
        except Exception as e:
            await websocket.close()
            err_msg = f"Client acknowledge message exceeded timeout of {DEFAULT_TIMEOUT}s. Please make sure your client is sending a acknowledge message before timeout occurs."
            logging.error(err_msg)
            del self.active_connections[id]
            raise WebSocketAckTimeoutError(err_msg)

        logging.info(f"Websocket with id({id}) is now active.")
        return id

    def disconnect(self, id: str) -> None:
        logging.info(f"Removing Websocket with id({id}).")
        del self.active_connections[id]

    async def send_message(self, websocket: WebSocket, message: BaseMessage) -> None:
        await websocket.send_json(message.to_dict())
    
    async def send_message_by_id(self, id: str, message: BaseMessage) -> None:
        websocket = self.active_connections.get(id)
        if websocket:
            await self.send_message(websocket, message)
        else:
            logging.warn(f"Websocket with id({id}) was not found. Message({message}) was not sent.")

    async def broadcast(self, message: BaseMessage) -> None:
        for connection in self.active_connections.values():
            await connection.send_json(message.to_dict())

    async def _recieve_ack(self, id: str):
        logging.info(f"Waiting for ack for websocket(id={id})...")
        websocket = self.active_connections[id]
        logging.info(f"state {websocket.client_state}")
        await websocket.receive_json()