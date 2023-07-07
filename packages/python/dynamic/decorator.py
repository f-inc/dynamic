from functools import wraps
from typing import Callable, List, Optional

from dynamic.classes.agent import DynamicAgent

METHODS = ["GET", "PUT", "POST", "DELETE"]

def dynamic(
        func: Optional[Callable] = None,
        streaming: bool = False,
        methods: List[str] = ["GET"]
    ):
    """Dynamic wrapper to declare endpoints"""

    for m in methods:
        if m not in methods:
            raise Exception(f"{m} is not a valid method. Supported methods: {METHODS}")

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            output = func(*args, **kwargs)

            if streaming:
                if not isinstance(output, DynamicAgent):
                    raise Exception(f"Streaming endpoints must return DynamicAgents. {func.__name__} returns {type(func)}.")

            return output
        
        # set dynamic options
        wrapper.streaming = streaming
        wrapper.methods = methods

        return wrapper

    if callable(func):
        return decorator(func)    

    return decorator

