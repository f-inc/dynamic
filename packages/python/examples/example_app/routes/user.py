from fastapi import Request

def handler(req: Request):
    if req.method == "GET":
        return get_user()
    return all_user()

def get_user():
    return dict(message="Ran get_user()")

def all_user():
    return dict(message="Ran all_user()")