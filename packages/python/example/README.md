<h1>Example App</h1>

- [How to run the example server](#how-to-run-the-example-server)
- [How to use the example](#how-to-use-the-example)
  - [Calling the different methods](#calling-the-different-methods)
  - [Streaming](#streaming)
- [How does it work](#how-does-it-work)
  - [The agents in `agent.py`](#the-agents-in-agentpy)
  - [The setup in `app.py`](#the-setup-in-apppy)

This is a simple example dynamic app using file-based routing. At the moment, file-based routing supports `GET`, `PUT`, `POST`, and `DELETE` requests.

## How to run the example server

1. Rename the `.env.example` file to `.env`
2. Fill in the `OPENAI_API_KEY` and `SERPER_API_KEY` keys (You can get a `SERPER_API_KEY` from [here](https://serper.dev/), its free)
3. Install the package

   `pip install dynamic-sh`

   Additional instructions [here](./../dynamic/README.md#installation)

4. Run `python app.py`

## How to use the example

There are a total of 5 different routes on this app:

**CRUD Examples**
They handle any `GET`, `PUT`, `POST`, or `DELETE` request.

- `/foo/bar`
- `/user`

**Non-streaming, or inline, Langchain Objects**
Using HTTP requests, you can communicate to these Langchain LLM operators, `inline` is in reference to non-streaming LLM operators.

- `/chain`
- `/inline_agent`

**Streaming Agent**
Using a websocket client, you can communicate with this endpoint, also retrieving live tokens from this agent as it is responding to your prompt. This is the same agent from `/inline_agent`, but now the content, including the agent self-reflection/explanation, is being outputted as it is generated.

- `/agent`

### Calling the different methods

All non-streaming endpoints are accessible via HTTP requests, using `curl` or any other API tool to communicate with the API server.

```bash
# examples

# GET /foo/bar
$ curl localhost:8000/foo/bar

> {"message":"foo"}

# POST /chain
$ curl -X POST localhost:8000/chain \
-H 'Content-Type: application/json' \
-d '{"config": {"input": "AC/Heating"}}'

> {"message":"Ran inline route successfully!","output":"\n\nAir King Solutions."}

# POST /inline_agent
$ curl -X POST localhost:8000/inline_agent \
-H 'Content-Type: application/json' \
-d '{"config": {"input": "Who is the US president?"}}'

> {"message":"Ran inline route successfully!","output":"Joe Biden is the US president."}
```

### Streaming

TODO

## How does it work

TODO

### The agents in `agent.py`

TODO

### The setup in `app.py`

TODO
