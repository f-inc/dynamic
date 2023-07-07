from functools import wraps
import logging

from dynamic.classes.agent import DynamicAgent

def dynamic(func=None, streaming=False):
    def decorator(func):
        # logging.info(f"test {func.__name__}")
        @wraps(func)
        def wrapper(*args, **kwargs):
            output = func(*args, **kwargs)

            if streaming:
                if not isinstance(output, DynamicAgent):
                    raise Exception("Streaming endpoints must return DynamicAgents")

            return output

        return wrapper

    if callable(func):
        return decorator(func)    

    return decorator

