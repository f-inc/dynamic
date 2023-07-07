import typing
import logging

from fastapi import Request

from dynamic import dynamic

@dynamic(methods=["GET", "PUT", "POST"])
async def handler(req: Request) -> typing.Any:
    if req.method == "GET":
        return get()
    elif req.method == "POST" or req.method == "PUT":
        return await put_or_post(req)
    else:
        return handle_all()


def get() -> typing.Dict[str, str]:
    return dict(message="foo")

async def put_or_post(req: Request) -> typing.Dict[str, str]:
    data = await req.json()

    message = data.get("message")

    if message:
        return dict(message=message)
    
    return dict(message="foo, called PUT/POST")

def handle_all() -> typing.Dict[str, str]:
    return dict(message="handle all")