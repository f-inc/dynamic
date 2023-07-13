import logging

from fastapi import Request

from dynamic import dynamic

@dynamic
async def get(req: Request):
    return dict(message="Ran get")

@dynamic(methods=["PUT", "POST"])
async def put_or_post(req: Request):
    return dict(message="Ran put_or_post")