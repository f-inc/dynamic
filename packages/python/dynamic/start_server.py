import os
import logging
from typing import Any, List, Optional

from dynamic.classes.logger import setup_logging
from dynamic.protocols.server import Server
from dynamic.router import Router, Route
from dynamic.router.get_file_routes import get_file_routes, has_file_based_routing

host = os.environ.get("HOST", "0.0.0.0")
port = int(os.environ.get("PORT", 8000))


setup_logging()


def start_server(
        router: Router = Router(),
        # TODO: Remove routes in start_server
        routes: Optional[List[Any]] = None,
        static_dir=None,
        test_ws=False
    ):
    
    router = _handle_router(router, routes)

    logging.info(f"Starting server on {host}:{port}")
    server = Server(router, host=host, port=port, static_dir=static_dir)
    if test_ws:
        server._add_test_ws_html()
    server.start()

    return server

def _handle_router(router: Router, routes: Optional[List[Any]]) -> Router:
    # get path of excuting script
    if routes:
        routes = [
            Route(
                path=path,
                handle=handle,
            ) for path, handle in routes.items()
        ]
    else:
        routes = []

    if has_file_based_routing():
        logging.info("Building file based routes...")
        routes += get_file_routes()

    if router:
        router.routes += routes
    else:
        router = Router(routes=routes)

    return router


