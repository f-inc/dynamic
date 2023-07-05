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
            inline: bool = False,
            streaming: bool = False,
            route_type: Optional[RouteType] = None,
    ):
        self.path = path
        self.handle = handle
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
        self.routes = []

        # error checks routes, duplicate paths are problematic atm
        for route in routes:
            self.add_route(route)
    
    def get_route(self, path: str) -> Union[Route, None]:
        for route in self.routes:
            if route.path == path:
                return route
        
        return None
    
    def add_route(self, route: Route):
        paths = [r.path for r in self.routes]
        if route.path in paths:
            raise Exception(f"Duplicate path found, \"{route.path}\". All routes must have unique path (both http and websocket).")

        self.routes.append(route)

