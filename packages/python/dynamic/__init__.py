from dynamic.protocols.server import Server
import os

host = os.environ.get("HOST", "0.0.0.0")
port = int(os.environ.get("PORT", 8000))
print(f"Starting server on {host}:{port}")


def start_server():
    server = Server(host=host, port=port)
    server.start()

    return server
