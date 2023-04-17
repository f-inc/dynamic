from .ws import setup_websocket, register_routes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
import uvicorn


class Server:
    routes = []

    def __init__(self, host="0.0.0.0", port=8000, static_dir=None):
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

        setup_websocket(self.app)
        if static_dir:
            self.app.mount("/static", StaticFiles(directory=static_dir), name="static")
            self.app.add_route("/", FileResponse("static/index.html"))

    def register_routes(self, route, func):
        register_routes(route, func)

    def start(self):
        print(f"Starting server on host:port {self.host}:{self.port}")
        uvicorn.run(self.app, host=self.host, port=self.port)
