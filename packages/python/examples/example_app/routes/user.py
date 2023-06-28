from fastapi import Request

def handler(req: Request):
    if req.method == "GET":
        return get_foo()
    return all_foo()

def get_foo():
    return 'get-foo'

def all_foo():
    return 'foo'