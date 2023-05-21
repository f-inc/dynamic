import logging

handlers = {}


def update_ws_routes(routes):
    handlers = routes
    logging.info(f"Updated websocket routes {handlers}")


def setup_websocket(app, routes):
    update_ws_routes(routes)
