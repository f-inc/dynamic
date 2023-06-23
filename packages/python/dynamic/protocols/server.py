import os
import uuid
import orjson
import traceback
import logging
from typing import Any, Callable

# fastapi
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
import uvicorn

# dynamic
from dynamic.runners.utils import get_runner
from dynamic.protocols.ws import ConnectionManager

# Exceptions
class RouteNotFound(Exception):
    pass

parent_dir_path = os.path.dirname(os.path.realpath(__file__))


def parse_json_string(json_string):
    try:
        parsed_json = orjson.loads(json_string)
        return parsed_json
    except orjson.JSONDecodeError as e:
        raise e


def error_response(message="Unexpected Error", e=None):
    # TODO: Remove
    error_response = {"error": message, "details": str(e)}
    return orjson.dumps(error_response).decode("utf-8")


def run_agent(agent_func, json_data, send_msg):
    logging.info(f"Running agent... {json_data}")
    # look up if agent is already running
    # might need to check what kind of agent


class Server:
    app = FastAPI(debug=True)
    routes = {}

    def __init__(self, routes, host="0.0.0.0", port=8000, static_dir=None):
        self.host = host
        self.port = port
        self.connection_manager = ConnectionManager()

        for route in routes:
            handle = routes[route]
            logging.info(f"Adding route {route}")
            self.add_route(route, handle)
            
            async def run_route(req: Request):
                # collect data
                data = await req.json()

                # setup runner config
                config_dict = data.get("config")
                runner = self.routes[route].get("runner")
                runner_config_type = self.routes[route].get("runner_config_type")

                # run runner and return output
                config = runner_config_type(**config_dict)
                output = runner(handle, config).run()
                return dict(
                    message="Ran subroute successfully!",
                    output=output
                )
            
            self.app.add_api_route(route, run_route, methods=["GET", "POST"])

        # Enable CORS for your frontend domain
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        if static_dir:
            logging.info(f"Adding static dir {static_dir}")
            full_path = "{}/{}".format(
                os.path.dirname(os.path.realpath(static_dir)), static_dir
            )
            logging.info(f"Adding static dir {full_path}")
            self.app.mount(
                "/",
                StaticFiles(directory=full_path),
                name="static",
            )
            self.app.add_route("/", FileResponse("{}/index.html".format(full_path)))
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

    def add_route(self, route: str, handle: Callable) -> None:
        # TODO: Create Routes and Route classes
        # check route intance type
        runner, runner_config_type = get_runner(handle)

        self.routes[route] = dict(
            handle=handle,
            runner=runner,
            runner_config_type=runner_config_type,
        )

    def start(self):
        logging.info(f"Starting server on host:port {self.host}:{self.port}")
        uvicorn.run(
            self.app,
            host=self.host,
            port=self.port,
            log_level="info",
        )

    async def websocket_handler(self, websocket: WebSocket):
        async def handle_msg(route, data):
            logging.info(f"Processing handler message for route {route} data {data}")
            try:
                route_data = self.routes[route]
                handle = route_data.get("handle")
                runner = route_data.get("runner")
                runner_config_type = route_data.get("runner_config_type")
                config = runner_config_type(**data)
                
                await runner(handle, config, websocket=websocket).run()
            except ValueError as e:
                logging.error(f"ValueError while processing route {route}")
                return error_response(f"ValueError for route {route}", e=e)
            except Exception as e:
                logging.error(f"Error processing handler message for route {route}")
                traceback.print_exc()
                return error_response(f"Can't handle message for route {route}", e=e)

        async def send_msg(data, original_msg={}, broadcast=False):
            # TODO: Create Message class
            message = dict(
                route=original_msg.get("route"),
                message_id=original_msg.get("message_id"),
                data=data,
            )
            logging.info(f"Sending message {message}")
            if broadcast:
                await self.connection_manager.broadcast(message)
            else:
                await self.connection_manager.send_message(message, websocket)

        await self.connection_manager.connect(websocket)
        while True:
            try:
                message = await websocket.receive_json()
                logging.info(f"Received message {message}")


                if message.get("message_id") is None:
                    message["message_id"] = str(uuid.uuid4())
                route = message.get("route")

                if route is None:
                    err_message = f"Recieved a message without a route. Message - {str(message)}"
                    logging.error(err_message)
                    raise RouteNotFound(err_message)
                
                if route in self.routes:
                    logging.info(f"Found handler for route {route}")
                    response = await handle_msg(route, message.get("data", {}))
                    await send_msg(response, message)
                else:
                    err_message = f"Route ({route}) not defined on the server."
                    logging.error(err_message)
                    raise RouteNotFound(err_message)
            except WebSocketDisconnect as e:
                logging.info("WebSocketDisconnect")
                await self.connection_manager.disconnect(websocket)
                break
            except orjson.JSONDecodeError as e:
                await send_msg(error_response(e=e))
            except KeyError as e:
                await send_msg(error_response(e=e))
            except RouteNotFound as e:
                await send_msg(error_response(e=e))
            except Exception as e:
                logging.error("failed to handle recieve_json")
                traceback.print_exc()

    def _add_test_ws_html(self):
        from fastapi.responses import HTMLResponse
        html = """
            <!DOCTYPE html>
            <html>
                <head>
                    <title>Chat</title>
                </head>
                <body>
                    <h1>WebSocket Testing</h1>
                    <form action="" onsubmit="sendMessage(event)">
                        <input type="text" id="messageText" autocomplete="off"/>
                        <button>Send</button>
                    </form>
                    <ul id='messages'>
                    </ul>
                    <script>
                        var ws = new WebSocket("ws://localhost:8000/ws");
                        ws.onmessage = function(event) {
                            var messages = document.getElementById('messages')
                            var message = document.createElement('li')
                            data = JSON.parse(event.data)
                            var content = document.createTextNode(JSON.stringify(data.data))
                            message.appendChild(content)
                            messages.appendChild(message)
                        };
                        function sendMessage(event) {
                            var input = document.getElementById("messageText")
                            var data = { agent_input: input.value }
                            var value = { data: data,  route: "/agent" }
                            ws.send(JSON.stringify(value))
                            input.value = ''
                            event.preventDefault()
                        }
                    </script>
                </body>
            </html>
            """
        
        async def get_html():
            return HTMLResponse(html)
        
        self.app.add_api_route("/test_ws", get_html)
        