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
from dynamic.classes.agent import DynamicAgent
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
        """Dynamically add routes"""
        handle = route.handle
        path = route.path
        runner = route.runner
        runner_config_type = route.runner_config_type

        async def run_inline_route(req: Request):
            """Non-streaming simple route"""
            # collect data
            data = await req.json()

            # setup runner config
            config_dict = data.get("config")

            # run runner and return output
            config = runner_config_type(**config_dict)
            output = runner(handle, config, streaming=False).run()
            return dict(
                message="Ran inline route successfully!",
                output=output
            )
        if route.streaming and isinstance(route.handle, DynamicAgent):
            logging.info(f"Adding websocket route {route.path}")
            self.app.websocket(route.path)(self.websocket_handler)
        elif route.inline:
            logging.info(f"Adding inline route {route.path}")
            self.app.add_api_route(path, run_inline_route, methods=["GET", "POST"])
        else:
            logging.info(f"Adding route {route.path}")
            self.app.add_api_route(path, handle, methods=["GET", "PUT", "POST", "DELETE"])

    def start(self):
        logging.info(f"Starting server on host:port {self.host}:{self.port}")
        uvicorn.run(
            self.app,
            host=self.host,
            port=self.port,
            log_level="info",
        )

    async def websocket_handler(self, websocket: WebSocket):
        path = websocket.scope.get("path")
        if path is None:
            raise RouteNotFound("Websocket recieved a request without a path declared.")
        async def handle_msg(recieved_message: ClientMessage) -> Union[ServerMessage, ErrorMessage]:
            logging.info(f"Processing message(id={recieved_message.id}) for route {path}")
            try:
                # TODO: Remove self.routes and route data

                # build runner and run incoming input
                route = self.router.get_route(path)
                if not route:
                    err_message = f"Server's router does not have path, {path}"
                    logging.error(err_message)
                    raise RouteNotFound(err_message)
                logging.info(f"Route path {path}")
                logging.info(f"Route {route}")
                
                handle = route.handle
                runner = route.runner
                streaming = route.streaming
                runner_config_type = route.runner_config_type
                config = runner_config_type(**recieved_message.config)
                
                output = await runner(handle, config, websocket=websocket, streaming=streaming).arun()

                # return processed message
                return ServerMessage(content=output)
            except ValueError as e:
                err_content = f"ERROR: ValueError while processing Message(id={recieved_message.id}) on route path ({path})."
                logging.error(err_content)
                traceback.print_exc()
                return ErrorMessage(content=err_content, error=e)
            except Exception as e:
                err_content = f"ERROR: Unknown Error while processing Message(id={recieved_message.id}) on route path ({path})."
                logging.error(err_content)
                traceback.print_exc()
                return ErrorMessage(content=err_content, error=e)

        async def send_msg(message: BaseMessage, broadcast: bool = False) -> None:
            logging.info(f"Sending message {message.to_json_dump()}")
            if broadcast:
                await self.connection_manager.broadcast(message)
            else:
                await self.connection_manager.send_message(websocket, message)

        websocket_id = await self.connection_manager.connect(websocket)
        while True:
            try:
                received_json = await websocket.receive_json()
                incoming_message = ClientMessage(**received_json)
                logging.info(f"Received message: {incoming_message.to_json_dump()}")

                outgoing_message = await handle_msg(incoming_message)

                logging.info(f"Outgoing message: {outgoing_message.to_json_dump()}")
                await send_msg(outgoing_message)

            except WebSocketDisconnect as e:
                logging.info("WebSocketDisconnect")
                self.connection_manager.disconnect(websocket_id)
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
            except TypeError as e:
                err_content = f"ERROR - {e.__class__.__name__}: the recieved client message was formatted in correctly. \n Recieved: {received_json}"
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
                        var ws = new WebSocket("ws://localhost:8000/agent");
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
                            var value = { content: content, config: config }
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
        