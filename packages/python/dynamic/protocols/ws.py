from fastapi import WebSocket, WebSocketDisconnect
import uuid
import orjson

handlers = {}


def update_ws_routes(routes):
    handlers = routes
    print(f"Updated websocket routes {handlers}")


def setup_websocket(app, routes):
    update_ws_routes(routes)
