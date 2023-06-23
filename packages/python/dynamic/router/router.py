from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Callable

class RouteType(Enum):
    AGENT = "agent"
    CHAIN = "chain"
    CALLABLE = "callable"

@dataclass
class Route:
    handle: Callable
    streaming: bool = False
    path: str
    # TODO: Implement type
    type: Optional[RouteType] = None

@dataclass
class Router:
    routes: List[Route]
