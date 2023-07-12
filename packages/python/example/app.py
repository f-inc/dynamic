from dynamic import start_server
from dynamic.router import Router, Route

from example.agent import inline_agent, streaming_agent
from example.chain import chain

if __name__ == "__main__":

    langchain_routes = [
        Route(path="/inline_agent", handle=inline_agent, inline=True),
        Route(path="/agent", handle=streaming_agent, streaming=True),
        Route(path="/chain", handle=chain, inline=True),
    ]

    start_server(router=Router(routes=langchain_routes), test_ws=True)