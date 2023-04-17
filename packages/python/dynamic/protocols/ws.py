# websocket_handler.py
from fastapi import WebSocket, WebSocketDisconnect
import uuid
import orjson
import traceback

handlers = {}


def register_routes(route, func):
    handlers[route] = func


def error_response(message="Unexpected Error", e=None):
    error_response = {"error": message, "details": str(e)}
    return orjson.dumps(error_response).decode("utf-8")


def parse_json_string(json_string):
    try:
        parsed_json = orjson.loads(json_string)
        return parsed_json
        # return orjson.dumps(parsed_json).decode("utf-8")
    except orjson.JSONDecodeError as e:
        raise e


async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            message_id = str(uuid.uuid4())

            parsed_data = parse_json_string(data)
            parsed_data["message_id"] = message_id
            print(parsed_data)

            route = parsed_data["route"]
            if route in handlers:
                response = handlers[route](parsed_data["data"])
                await websocket.send_text(orjson.dumps(response).decode("utf-8"))
            else:
                await websocket.send_text(error_response("Route not found"))
        except orjson.JSONDecodeError as e:
            await websocket.send_text(error_response(e=e))
        except KeyError as e:
            await websocket.send_text(error_response(e=e))
        except WebSocketDisconnect as e:
            print("WebSocketDisconnect")
            await websocket.close()
            break
        except Exception as e:
            print("failed to handle receive_text")
            traceback.print_exc()


def setup_websocket(app):
    app.websocket("/ws")(websocket_endpoint)
