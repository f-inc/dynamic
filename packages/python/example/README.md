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

There are a total of 6 different routes on this app:

**CRUD Examples**
Simple CRUD (Create, Read, Update, Delete) endpoints.

- `GET, PUT, POST, or DELETE /foo/bar`
- `GET, PUT, or POST /user`

**Non-streaming, or inline, Langchain Objects**
Using HTTP `POST` requests, you can communicate to these Langchain LLM operators, `inline` is in reference to non-streaming LLM operators.

- `/chain`
- `/inline_agent`

**Streaming Agents**
Using a websocket client, you can communicate with this endpoint, also retrieving live tokens from this agent as it is responding to your prompt. This is the same agent from `/inline_agent`, but now the content, including the agent self-reflection/explanation, is being outputted as it is generated.

- `/agent`
- `/file_based_agent`

**Note:** Both endpoints are the exact agent, one is non file-based route and the other one is.

### CRUD and inline

All non-streaming endpoints are accessible via HTTP requests, using `curl` or any other API tool to communicate with the API server.

**Remember**: As mentioned in the [dynamic README.md](./../dynamic/README.md), inline LLM operators need this template used for their API request to handle prompts:

```
{
    "config": {
        "input": <prompt_here>
    }
}
```

**Examples**

```bash
# GET /foo/bar
$ curl localhost:8000/foo/bar

> {"message":"foo"}

# POST /foo/bar
$ curl -X POST localhost:8000/foo/bar \
-H 'Content-Type: application/json' \
-d '{"message": "foo-ey"}'

> {"message":"foo-ey"}

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

`DyanmicAgent` uses a technology called [websockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) to stream the generated LLM tokens to a client at the moment of generation. In order to take advantage of this, use a [websocket client](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_client_applications) to connect to the `/agent` dynamic endpoint.

Here is an example of a client setup to send and retrieve data to `/agent`:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Chat</title>
  </head>
  <body>
    <h1>WebSocket Testing</h1>
    <form action="" onsubmit="sendMessage(event)">
      <input type="text" id="messageText" autocomplete="off" />
      <button>Send</button>
    </form>
    <p id="messages"></p>
    <script>
      var ws = new WebSocket("ws://localhost:8000/agent");
      ws.onmessage = function (event) {
        var messages = document.getElementById("messages");
        data = JSON.parse(event.data);
        var content = document.createTextNode(data.content);
        messages.appendChild(content);
      };
      function sendMessage(event) {
        var input = document.getElementById("messageText");
        var content = input.value;
        var value = { config: { input: input.value } };
        ws.send(JSON.stringify(value));
        input.value = "";
        event.preventDefault();
      }
    </script>
  </body>
</html>
```

WebSocket testing is available to you on this example app via `localhost:8000/`. Open a browser to access this.

## How does it work

<!-- TODO -->

### The agents in `agent.py`

See [agent.py](./agent.py) for context.

In this example app, the agent is taking prompts and using the `google-serper` tool to answer the prompt via google.

As you can see in `agent.py`, there are two agents defined and exported, `inline_agent` and `streaming_agent`.

All LLM operators, in this case langchain, can be defined as `inline` or `streaming` based on how the Dynamic API server serves its content.

Inline operators are defined as they typically would be, in this case, Langchain Agents that are defined with `initialize_agent`.

Streaming operators will be given a dynamic class wrapper, in this case, `DynamicAgent` that will take identical parameters as the inline operator, but will add the websocket configuration in the middle.

### The chain in `chain.py`

See [chain.py](./chain.py) for context.

Currently, there is no streaming support for Langchain `Chain`, so dynamic only has inline endpoints available for chains.

In this example, it is serving a chain that will take in a prompt input into the template: `What is a good name for a company that makes {product}?`, `product` being the input from API request.

```python
llm = OpenAI(
    client=None,
    temperature=0.9,
)
prompt = PromptTemplate(
    input_variables=["product"],
    template="What is a good name for a company that makes {product}?",
)

chain = LLMChain(llm=llm, prompt=prompt)
```
