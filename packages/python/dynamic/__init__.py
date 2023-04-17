from dynamic.protocols.server import Server
import os

host = os.environ.get("HOST", "0.0.0.0")
port = int(os.environ.get("PORT", 8000))


def start_server(routes):
    print(f"Starting server on {host}:{port}")
    server = Server(routes, host=host, port=port)
    server.start()

    return server
