from dataclasses import dataclass
from enum import Enum
from typing import Callable, List, Optional, Union

from dynamic.runners.utils import get_runner
from dynamic.runners.callable import CallableRunner
from dynamic.runners.langchain import AgentRunner, ChainRunner

class RouteType(Enum):
    AGENT = "agent"
    CHAIN = "chain"
    CALLABLE = "callable"

_ROUTE_TYPE_TO_RUNNER = {
    RouteType.AGENT: AgentRunner,
    RouteType.CHAIN: ChainRunner,
    RouteType.CALLABLE: CallableRunner,
}

_RUNNER_TO_ROUTE_TYPE = {
    AgentRunner: RouteType.AGENT,
    ChainRunner: RouteType.CHAIN,
    CallableRunner: RouteType.CALLABLE,
}

class Route:
    def __init__(
            self,
            path: str,
            handle: Callable,
            methods: List[str] = ["GET"],
            inline: bool = False,
            streaming: bool = False,
            route_type: Optional[RouteType] = None,
    ):
        self.path = path
        self.handle = handle
        self.methods = methods
        self.inline = inline
        self.streaming = streaming
        self.route_type = route_type

        self.runner, self.runner_config_type = get_runner(self.handle)
        if route_type:
            assert _ROUTE_TYPE_TO_RUNNER[route_type] == self.runner, f"The route_type set {route_type.value} does not match the runner retrieved via handler, {self.runner}."

            self.route_type = route_type
        else:
            self.route_type = _RUNNER_TO_ROUTE_TYPE[self.runner]



class Router:
    def __init__(self, routes: List[Route] = []):
        self.routes: List[Route] = []

        # error checks routes, duplicate paths are problematic atm
        for route in routes:
            self.add_route(route)
    
    def get_route(self, path: str, method: str = "GET") -> Union[Route, None]:
        for route in self.routes:
            if route.path == path and (method in route.methods or route.streaming):
                return route
        
        return None
    
    def add_route(self, route: Route):
        for r in self.routes:
            overlapping_methods = set(r.methods).intersection(set(route.methods))
            # the route path is the same and if one the methods already has an existing handler, then raise exception
            if r.path == route.path and len(overlapping_methods) > 0:
                raise Exception(f"Duplicate path (\"{route.path}\") + method(s) found, {overlapping_methods}. All incoming routes must have unique path (both http and websocket) and methods.")

        self.routes.append(route)

