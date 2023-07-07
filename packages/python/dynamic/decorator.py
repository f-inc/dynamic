from functools import wraps

def dynamic(streaming=False):
    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
    
        return wrapper
    return decorator

