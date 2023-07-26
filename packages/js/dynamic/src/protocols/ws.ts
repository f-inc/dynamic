import type { SocketStream, WebsocketHandler } from "@fastify/websocket";
import { DynamicRequest } from "../types";

const websocketHandler = async (
  connection: SocketStream,
  request: DynamicRequest
) => {
  const { routeOptions } = request;
  const runner = routeOptions.runnerHandler;
  const { socket } = connection;

  console.log("routeOptions", routeOptions);

  socket.on("connected", (event: any) => {
    console.log("connection event:", event);

    // TODO: Change with LLM Op
    console.log("FOOOOOO", runner());
    socket.send(
      JSON.stringify({
        output: runner(),
      })
    );
  });

  socket.on("message", (data: any) => {
    console.log("data recieved:", data);

    console.log("FOOOOOO", typeof runner);
    // socket.send(
    //   JSON.stringify({
    //     output: runner(),
    //   })
    // );
  });
};

export { websocketHandler };
