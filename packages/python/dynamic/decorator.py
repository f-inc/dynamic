from functools import wraps

def dynamic(streaming=False):
    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            output = func(*args, **kwargs)

            if streaming:
                if not isinstance(output, DynamicAgent):
                    raise Exception("Streaming endpoints must return DynamicAgents")

            return output
        return wrapper
    return decorator

