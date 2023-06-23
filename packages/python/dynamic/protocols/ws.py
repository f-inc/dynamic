import logging
from typing import Any, Dict, List

from fastapi import WebSocket

from dynamic.classes.message import IncomingMessage

handlers = {}


def update_ws_routes(routes):
    handlers = routes
    logging.info(f"Updated websocket routes {handlers}")


def setup_websocket(app, routes):
    update_ws_routes(routes)


class ConnectionManager:
    """WebSocket connection manager."""

    # TODO: Add logs
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: IncomingMessage, websocket: WebSocket):
        await websocket.send_json(message.to_dict())

    async def broadcast(self, message: IncomingMessage):
        for connection in self.active_connections:
            await connection.send_json(message.to_dict())
