from dynamic.protocols.server import Server
import os
from dynamic.classes.logger import setup_logging
import logging

host = os.environ.get("HOST", "0.0.0.0")
port = int(os.environ.get("PORT", 8000))


setup_logging()


def start_server(routes, static_dir=None):
    logging.info(f"Starting server on {host}:{port}")
    server = Server(routes, host=host, port=port, static_dir=static_dir)
    server.start()

    return server
