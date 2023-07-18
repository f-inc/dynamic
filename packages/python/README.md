# Dynamic ⚡️

![Static Badge](https://img.shields.io/badge/release-0.0.4--alpha-blue)

**Disclaimer:** This documentation is intended for the alpha F.inc Community launch. Some portions of this documentation, such as the setup, are expected to change. Please keep that in mind for future reference.

## What is Dynamic?

Easy-to-use framework to enable building, deploying, and scaling LLM applications.

## Table of Contents

1. [Getting Started](#1-getting-started)

   a. [Installation](#a-installation)

2. [Building Your Application](#2-building-your-application)

   a. [Dynamic Alpha - what can you do?](#a-dynamic-alpha---what-can-you-do)

   b. [Project Structure](#b-project-structure)

   c. [Routing](#c-routing)

   d. [Websockets](#d-websockets)

3. [Concepts](#3-concepts)

   a. [LLM Operators](#a-llm-operators)

## 1. Getting Started

### a. Installation

With python versions 3.6+, run the following to install the `dynamic` module. It is recommended that you have a virtual environment set up in your project as well before doing this.

```bash
pip install dynamic-sh
```

**(optional)** Test that the module is functional in your console by running:

```bash
$ python -c "import dynamic"
```

<!--
These are useful instructions for a developer README.
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
-->

## 2. Building Your Application

### a. Dynamic Alpha - what can you do?

As of right now, the following features for an API built on dynamic are available:

1. Simple, normal `GET`, `PUT`, `POST`, and `DELETE` endpoints are represented by a callable function.

2. Given a langchain chain or agent, a simple endpoint will be generated that will return agent/chain output given a prompt.

3. Given an agent, a websocket endpoint can be generated that will stream all of the agent's output in real-time.

### b. Project Structure

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

### c. Routing

There are two routing options, file-based and non file-based routing. Dynamic does not restrict you from using one or the other or both.

#### File-based routing

This is the **recommended** method of routing.

This routing builds the routes based on the files given under the `routes` folder. Similar to frameworks like [Next.js](https://nextjs.org/docs/pages/building-your-application/routing/api-routes), the endpoint of the route is based on the file name.

`./routes/foo/bar` &rarr; `/foo/bar`

##### Decorator `@dynamic`

Use the decorator in your files to declare which functions will act as your route handlers.

| Parameter | Type      | Default | Description                                                                                                                                                             |
| --------- | --------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| streaming | bool      | False   | Useful for websocket endpoints for LLM Operators (\`DynamicAgent\`). <br /> Handlers with `streaming=True` must return an instance of the LLM Operator in their output. |
| methods   | List[str] | ["GET"] | List all of the HTTP methods that the handler will support.                                                                                                             |

```python
# /example/routes/foo/bar.py
from fastapi import Request

from dynamic import dynamic

@dynamic
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
```
```python
# /example/routes/file_based_agent.py

streaming_agent = DynamicAgent(
    tool_list=tool_list, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True,
)

# this agent will be sitting on the websocket "ws://<host>:<port>/file_based_agent"
@dynamic(streaming=True)
def agent():
    return streaming_agent
```
See [the example app](./example/) for more route examples.

#### Non file-based routing

Simply put, these are routes that are manually defined into `start_server`.

##### Non-streaming/inline

This is how you would declare a chain or non-streaming, or inline, agent.

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

(**Note**: Langchain yet has streaming support for chains, so for the time being only `Agents` are supported)

```python
from dynamic.classes.dynamic_agent  import DynamicAgent

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

#### d. Websockets

##### Security

Most of the server-side websocket setup is done automatically for you with Dynamic ⚡️ (yay 🎉). The rest, that is client-side, depends on the websocket library/client you use to connect to your Dynamic Websocket. Please be **aware** there is one expectation from Dynamic.

Dynamic expects there to be an acknowledge message sent from the client within 10 seconds of connecting. At the moment, there is no expected format, but as a layer of acknowledged connection and security, there is this expectation, otherwise, your connection will be closed.

Here is a simple example:

```javascript
var ws = new WebSocket("ws://localhost:8000/agent");

ws.onopen = function(event) {
    console.log("Sending acknowledge message on connection open...")
    ws.send("ack msg")
}
ws.onmessage = function(event) {
    ...
};
```

## 3. Concepts

### a. LLM Operators

TODO

#### Inline vs Streaming

TODO
