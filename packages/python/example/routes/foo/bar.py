import typing
import logging

from fastapi import Request

from dynamic import dynamic

@dynamic(methods=["GET"])
def get(req: Request) -> typing.Any:
    if req.method == "GET":
        return dict(message="foo")
    else:
        logging.warn("If you see this message, dynamic decorator method handling is not working correctly")
        return handle_all()


@dynamic(methods=["PUT", "POST"])
async def put_or_post(req: Request) -> typing.Any:
    data = await req.json()

    message = data.get("message")

    if message:
        return dict(message=message)
    
    return dict(message="foo, called PUT/POST")

def handle_all() -> typing.Dict[str, str]:
    return dict(message="handle all")

@dynamic(methods=["DELETE"])
def delete():
    return dict(message="Ran delete()")