import logging
from functools import wraps
from typing import Callable, List, Optional
from inspect import iscoroutinefunction

from dynamic.classes.dynamic_agent  import DynamicAgent

def dynamic(
        func: Optional[Callable] = None,
        streaming: bool = False,
        methods: List[str] = ["GET"]
    ):
    """Dynamic wrapper to declare endpoints"""

    def decorator(func):

        wrapper = None

        @wraps(func)
        async def http_wrapper(*args, **kwargs):
            if _is_async(func):
                return await func(*args, **kwargs)
            return func(*args, **kwargs)

        @wraps(func)
        def dynamic_wrapper(*args, **kwargs):
            dynamic_handler = func(*args, **kwargs)
            if not isinstance(dynamic_handler, DynamicAgent):
                # If any other Dynamic handlers are added, for instance DynamicChat, make sure to type check here
                raise Exception(f"Streaming endpoints must return DynamicAgents. {func.__name__} returns {type(func)}.")
            
            return dynamic_handler
        
        if streaming:
            wrapper = dynamic_wrapper
        else:
            wrapper = http_wrapper
        
        # set dynamic options
        wrapper.streaming = streaming
        wrapper.methods = methods

        return wrapper

    if callable(func):
        return decorator(func)    

    return decorator

def _is_async(func: Callable) -> bool:
    return iscoroutinefunction(func)