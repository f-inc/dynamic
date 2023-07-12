# Dynamic ⚡️

**Disclaimer:** This documentation is intended for the alpha F.inc Community launch. Some portions of this documentation, such as the setup, are expected to change. Please keep that in mind for future reference.

## What is Dynamic?

Easy-to-use framework to enable building, deploying, and scaling LLM applications.

## Table of Contents

1. [Getting Started](#getting-started)

   a. [Installation](#installation)
   <!-- b. [Concepts](#concepts) -->

2. [Building Your Application](#building-your-application)

   a. [Dynamic Alpha - what can you do?](#dynamic-alpha---what-can-you-do)

   b. [Project Structure](#project-structure)

   c. [Routing](#routing)

   d. [Callables](#callables)

   e. [Langchain Agents](#langchain-agents)

   f. [Langchain Chains](#langchain-chains)

## Getting Started

### Installation

**Note:** There are instructions for the alpha version, these are expected to update once the wheel is released into a public artifactory.

1. Start a virtual environment
2. Given a python wheel provided by Aman, run:

```bash
$ pip install <path_to_wheel>
# example
$ pip install dist/dynamic-0.0.1-py3-none-any.whl
```

3. **(optional)** Test that the module is functional in your console by running:

```bash
$ python -c "import dynamic"
```

<!-- ### Concepts -->

## Building Your Application

### Dynamic Alpha - what can you do?

As of right now, the following features for an API built on dynamic are available:

1. Simple, normal `GET`, `PUT`, `POST`, and `DELETE` endpoints are represented by a callable function.

2. Given a langchain chain or agent, a simple endpoint will be generated that will return agent/chain output given a prompt.

3. Given an agent, a websocket endpoint can be generated that will stream all of the agent's output in real-time.

### Project Structure

Typically your root directory should have a server/app script that initiates your server. And then if you opt for file-based routing, a folder named `routes` in which the endpoint logic is stored. More details on routing will be in the next section.

```bash
# example file structure tree
.
└── my_app/
    ├── routes/
    │   └── foo/
    │       └── bar.py
    └── app.py
```

And `app.py` could look like the following:

```python
from dynamic import start_server

if __name__ == "__main__":
    start_server()
```

Run with `python app.py`.

Besides these details, the project structure has no other requirements or restrictions.

### Routing

There are two routing options, file-based and inline routing. Dynamic does not restrict you from using one or the other or both.

<!-- #### Inline routing (Static)


Here is how you declare your static route.

```python
from dynamic.router import Router, Route

...

"""
Callable Declaration
"""
def foo():
    ...
    return dict(message="/foo output")

...

"""
Start Server
"""
if __name__ == "__main__":
    routes = [
        Route(path="/foo", handle=foo, inline=True),
    ]

    router = Router(routes=routes)

    start_server(router=router)

``` -->

#### Inline routing (Agent and Chains)

Simply put, these are routes that are manually defined into `start_server`.

At the moment, this is the routing type that supports streaming agents. A streaming agent simply means output is streamed out a token at a time. The alternative is a non-streaming agent endpoint that only responds to requests after the agent completes its job.

##### Non-streaming

This is how you would declare a chain or non-streaming agent.

```python
from dynamic import start_server
from dynamic.router import Router, Route

from langchain.agents import AgentType
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain

"""
Initizialize Chain and Agent as usual
"""

llm = OpenAI(
    client=None,
    temperature=0.9,
)
prompt = PromptTemplate(
    input_variables=["product"],
    template="What is a good name for a company that makes {product}?",
)

chain = LLMChain(llm=llm, prompt=prompt)

tools = load_tools(["google-serper"], llm=llm)

agent = initialize_agent(
    tools=tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True,
)

if __name__ == "__main__":
    routes = [
        Routes(path="/chain", handle=chain, inline=True),
        Routes(path="/agent", handle=agent, inline=True),
    ]

    router = Router(routes=routes)

    start_server(router=router)

```

Now, the non-streaming chain and agent will respond to any HTTP method (`GET`, `PUT`, `POST`, `DELETE`), but it expects the prompt to be in the request body as such:

```
{
    "config": {
        "input": <prompt_here>
    }
}
```

So an example request would look like:

```bash
$ curl -X POST localhost:8000/chain \
    -H 'Content-Type: application/json' \
    -d '{"config": {"input": "AC/Heating"}}'
```

##### Streaming

Setting up a streaming agent is nearly identical, except you must also:

- declare `streaming=True` when defining your langchain llms and dynamic `Route`
- declare your agent using `DynamicAgent` rather than `initialize_agent`

(**Note**: Langchain yet has streaming support for chains, so for the time being)

```python
from dynamic.classes.agent import DynamicAgent

llm = OpenAI(temperature=0, verbose=True, streaming=True) # declare llm with streaming

tool_list = ["google-serper"]

# if you want to use streaming over websocket, your agent must be decalared with a DynamicAgent
streaming_agent = DynamicAgent(
    tool_list=tool_list, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True,
)

if __name__ == "__main__":
    routes = [
        ...,
        Route(path="/agent", handle=streaming_agent, streaming=True),
    ]

    router = Router(routes=routes)
    start_server(router=router)
```

This now opens a websocket with path `/agent`: `ws://<host>/agent`

To make a request, just like non-streaming agents, the handle will also expect your request to be sent in json representation that follows this template:

```
{
    "config": {
        "input": <agent_prompt_here>
    }
}
```

#### File-based routing

**Disclaimer**: Streaming agents are not yet supported in file-based routing as this approach to file-based routing may change.

This routing builds the routes based on the files given under the `routes` folder. Similar to frameworks like Next.js, the endpoint of the route is based on the file name.

`./routes/foo/bar` &rarr; `/foo/bar`

For callables, complete all of your API logic under a function named `handler`. Dynamic will support the `handler` by also passing in a request parameter. For example:

```python
# /examples/example_app/routes/foo/bar.py

import typing

from fastapi import Request

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
```

See [`examples/example_app`](./../examples/example_app/) for more route examples.
