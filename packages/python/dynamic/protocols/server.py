from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
import uvicorn
import os
import uuid
import orjson
import traceback
import logging
from langchain.chains.base import Chain
from langchain.agents import Agent


parent_dir_path = os.path.dirname(os.path.realpath(__file__))


def parse_json_string(json_string):
    try:
        parsed_json = orjson.loads(json_string)
        return parsed_json
    except orjson.JSONDecodeError as e:
        raise e


def error_response(message="Unexpected Error", e=None):
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

        for route in routes:
            logging.info(f"Adding route {route}")
            self.add_route(route, routes[route])

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

    def add_route(self, route, func):
        # check route intance type
        if isinstance(func, Chain):
            self.routes[route] = {"func": func, "type": "chain"}
        elif isinstance(func, Agent):
            self.routes[route] = {"func": func, "type": "agent"}
        elif callable(func):
            self.routes[route] = {"func": func, "type": "handler"}
        else:
            logging.warning(f"Route {route} is not a valid type")

    def start(self):
        logging.info(f"Starting server on host:port {self.host}:{self.port}")
        uvicorn.run(
            self.app,
            host=self.host,
            port=self.port,
            log_level="info",
        )

    async def websocket_handler(self, websocket: WebSocket):
        def handle_msg(route, data):
            logging.info(f"Processing handler message for route {route} data {data}")
            if route not in self.routes:
                logging.error(f"Route {route} not found")
                return error_response(f"Route {route} not found")
            try:
                chain = self.routes[route]
                if chain["type"] == "chain":
                    return chain["func"].run(data)
                elif chain["type"] == "agent":
                    run_agent(chain["func"], data, send_msg)
                    return chain["func"].run(data)
                elif chain["type"] == "handler":
                    return chain["func"](data)
                else:
                    return error_response(f"Route {route} not found")
            except ValueError as e:
                logging.error(f"Error processing handler message for route {route}")
                return error_response(f"Can't handle message for route {route}")
            except Exception as e:
                logging.error(f"Error processing handler message for route {route}")
                return error_response(f"Can't handle message for route {route}")

        async def send_msg(msg, original_msg={}):
            logging.info(f"Sending message {msg}")
            response = {
                "route": route,
                "message_id": original_msg.get("message_id", "NO_MESSAGE_ID"),
                "data": msg,
            }
            await websocket.send_text(orjson.dumps(response).decode("utf-8"))

        await websocket.accept()
        while True:
            try:
                msg = await websocket.receive_text()
                logging.info(f"Received message {msg}")

                parsed_msg = parse_json_string(msg)

                message_id = str(uuid.uuid4())
                parsed_msg["message_id"] = message_id
                route = parsed_msg["route"]

                if route in self.routes:
                    logging.info(f"Found handler for route {route}")
                    response = handle_msg(route, parsed_msg.get("data", {}))
                    await send_msg(response, parsed_msg)
                else:
                    logging.info(f"route {route} not found in handlers: {self.routes}")
                    await send_msg(error_response("Route not found"), parsed_msg)
            except orjson.JSONDecodeError as e:
                await send_msg(error_response(e=e))
            except KeyError as e:
                await send_msg(error_response(e=e))
            except WebSocketDisconnect as e:
                logging.error("WebSocketDisconnect")
                await websocket.close()
                break
            except Exception as e:
                logging.error("failed to handle receive_text")
                traceback.print_exc()
