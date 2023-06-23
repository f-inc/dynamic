import os
import logging
from typing import Any, Optional

from dynamic.protocols.server import Server
from dynamic.classes.logger import setup_logging
from dynamic.router import Router, Route

host = os.environ.get("HOST", "0.0.0.0")
port = int(os.environ.get("PORT", 8000))


setup_logging()


def start_server(
        router: Router = Router(routes=[]),
        routes: Any = None,
        static_dir=None,
        test_ws=False
    ):
    if routes:
        routes = [
            Route(handle=handle, path=path) for path, handle in routes.items()
        ]

        if router:
            router.routes += routes
        else:
            Router(routes=routes)

    logging.info(f"Starting server on {host}:{port}")
    server = Server(router, host=host, port=port, static_dir=static_dir)
    if test_ws:
        server._add_test_ws_html()
    server.start()

    return server
