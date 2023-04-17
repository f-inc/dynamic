from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
import uvicorn
import os
import uuid
import orjson
import traceback

parent_dir_path = os.path.dirname(os.path.realpath(__file__))


def parse_json_string(json_string):
    try:
        parsed_json = orjson.loads(json_string)
        return parsed_json
        # return orjson.dumps(parsed_json).decode("utf-8")
    except orjson.JSONDecodeError as e:
        raise e


def error_response(message="Unexpected Error", e=None):
    error_response = {"error": message, "details": str(e)}
    return orjson.dumps(error_response).decode("utf-8")


class Server:
    routes = {}

    def __init__(self, routes, host="0.0.0.0", port=8000, static_dir=None):
        self.routes = routes
        self.host = host
        self.port = port

        self.app = FastAPI()
        # Enable CORS for your frontend domain
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        if static_dir:
            self.app.mount("/", StaticFiles(directory=static_dir), name="static")
            # go through the static directory and add specific routes
        else:
            self.app.mount(
                "/static",
                StaticFiles(directory=parent_dir_path + "/../static"),
                name="static",
            )
            self.app.add_route(
                "/", FileResponse(parent_dir_path + "/../static/index.html")
            )

        self.app.websocket("/ws")(self.websocket_handler)

    def start(self):
        print(f"Starting server on host:port {self.host}:{self.port}")
        uvicorn.run(self.app, host=self.host, port=self.port)

    async def websocket_handler(self, websocket: WebSocket):
        def handle_msg(route, data):
            print(f"Processing handler message for route {route}")
            chain = self.routes[route]
            return chain.handle_msg(data)

        await websocket.accept()
        while True:
            try:
                data = await websocket.receive_text()
                message_id = str(uuid.uuid4())

                parsed_data = parse_json_string(data)
                parsed_data["message_id"] = message_id
                print(f"Received message {parsed_data}")

                route = parsed_data["route"]
                if route in self.routes:
                    print(f"Found handler for route {route}")
                    response = handle_msg(route, parsed_data)
                    await websocket.send_text(orjson.dumps(response).decode("utf-8"))
                else:
                    print(f"route {route} not found in handlers: {self.routes}")
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
