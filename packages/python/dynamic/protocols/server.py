import os
import uuid
import orjson
import traceback
import logging
from typing import Any, Callable, Union

# fastapi
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
import uvicorn

# dynamic
from dynamic.classes.message import BaseMessage, ErrorMessage, ClientMessage, ServerMessage
from dynamic.router import Router, Route
from dynamic.runners.utils import get_runner
from dynamic.protocols.ws import ConnectionManager

# Exceptions
class RouteNotFound(Exception):
    pass

parent_dir_path = os.path.dirname(os.path.realpath(__file__))

class Server:
    app = FastAPI(debug=True)
    routes = {}

    def __init__(
            self,
            router: Router,
            host: str ="0.0.0.0",
            port: int = 8000,
            static_dir: Any = None
        ):
        self.host = host
        self.port = port
        self.connection_manager = ConnectionManager()
        self.router = router

        for route in router.routes:
            logging.info(f"Adding route /{route.path}")
            self.add_route(route)
        

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

    def add_route(self, route: Route) -> None:
        """Dynamically add static routes"""
        handle = route.handle
        path = route.path
        api_path = f"/{path}"
        runner, runner_config_type = get_runner(handle)

        self.routes[api_path] = dict(
            handle=handle,
            runner=runner,
            runner_config_type=runner_config_type,
            streaming=route.streaming,
        )

        async def run_route(req: Request):
            """Non-streaming simple route"""
            # collect data
            data = await req.json()

            # setup runner config
            config_dict = data.get("config")

            # run runner and return output
            config = runner_config_type(**config_dict)
            output = runner(handle, config, streaming=False).run()
            return dict(
                message="Ran subroute successfully!",
                output=output
            )
        
        self.app.add_api_route(api_path, run_route, methods=["GET", "POST"])

    def start(self):
        logging.info(f"Starting server on host:port {self.host}:{self.port}")
        uvicorn.run(
            self.app,
            host=self.host,
            port=self.port,
            log_level="info",
        )

    async def websocket_handler(self, websocket: WebSocket):
        async def handle_msg(recieved_message: ClientMessage) -> Union[ServerMessage, ErrorMessage]:
            logging.info(f"Processing message(id={recieved_message.id}) for route {recieved_message.route_path}")
            try:
                # TODO: Remove self.routes and route data

                # build runner and run incoming input
                route_data = self.routes[recieved_message.route_path]
                handle = route_data.get("handle")
                runner = route_data.get("runner")
                streaming = route_data.get("streaming")
                runner_config_type = route_data.get("runner_config_type")
                config = runner_config_type(**recieved_message.config)
                
                output = await runner(handle, config, websocket=websocket, streaming=streaming).run()

                # return processed message
                return ServerMessage(
                    content=output,
                    route_path=recieved_message.route_path
                )
            except ValueError as e:
                err_content = f"ERROR: ValueError while processing Message(id={recieved_message.id}) on route path ({recieved_message.route_path})."
                logging.error(err_content)
                traceback.print_exc()
                return ErrorMessage(
                    content=err_content,
                    route_path=recieved_message.route_path,
                    error=e
                )
            except Exception as e:
                err_content = f"ERROR: Unknown Error while processing Message(id={recieved_message.id}) on route path ({recieved_message.route_path})."
                logging.error(err_content)
                traceback.print_exc()
                return ErrorMessage(
                    content=err_content,
                    route_path=recieved_message.route_path,
                    error=e
                )

        async def send_msg(message: BaseMessage, broadcast: bool = False) -> None:
            logging.info(f"Sending message {message}")
            if broadcast:
                await self.connection_manager.broadcast(message)
            else:
                await self.connection_manager.send_message(message, websocket)

        await self.connection_manager.connect(websocket)
        while True:
            try:
                received_json = await websocket.receive_json()
                incoming_message = ClientMessage(**received_json)
                logging.info(f"Received message: {incoming_message}")

                route_path = incoming_message.route_path

                if route_path is None:
                    err_message = f"Recieved a message without a route. Message - {incoming_message}"
                    logging.error(err_message)
                    raise RouteNotFound(err_message)
                
                if route_path in self.routes:
                    logging.info(f"Found handler for route {route_path}")
                    outgoing_message = await handle_msg(incoming_message)
                    await send_msg(outgoing_message)
                else:
                    err_message = f"Route ({route_path}) not defined on the server."
                    logging.error(err_message)
                    raise RouteNotFound(err_message)
            except WebSocketDisconnect as e:
                logging.info("WebSocketDisconnect")
                await self.connection_manager.disconnect(websocket)
                break
            # TODO: Update error messaging
            except orjson.JSONDecodeError as e:
                err_content = f"ERROR: failed to handle recieve_json. {e.__class__.__name__} Recieved."
                logging.error(err_content)
                await send_msg(ErrorMessage(error=e, content=err_content))
            except KeyError as e:
                err_content = f"ERROR: failed to handle recieve_json. {e.__class__.__name__} Recieved."
                logging.error(err_content)
                await send_msg(ErrorMessage(error=e, content=err_content))
            except RouteNotFound as e:
                err_content = f"ERROR: failed to handle recieve_json. {e.__class__.__name__} Recieved."
                logging.error(err_content)
                await send_msg(ErrorMessage(error=e, content=err_content))
            except Exception as e:
                err_content = f"ERROR: Unknown failure to handle recieve_json. {e.__class__.__name__} Recieved."
                logging.error(err_content)
                await send_msg(ErrorMessage(error=e, content=err_content))

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
                    <p id='messages'>
                    </p>
                    <script>
                        var ws = new WebSocket("ws://localhost:8000/ws");
                        ws.onmessage = function(event) {
                            var messages = document.getElementById('messages')
                            data = JSON.parse(event.data)
                            var content = document.createTextNode(data.content)
                            messages.appendChild(content)
                        };
                        function sendMessage(event) {
                            var input = document.getElementById("messageText")
                            var content = input.value
                            var config = { input: input.value }
                            var value = { content: content, config: config,  route_path: "/agent" }
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
        