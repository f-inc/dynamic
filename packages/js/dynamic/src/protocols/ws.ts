import type { SocketStream, WebsocketHandler } from "@fastify/websocket";
import { DynamicRequest } from "../types";

const websocketHandler = async (
  connection: SocketStream,
  request: DynamicRequest
) => {
  const runner = request.routeOptions.runnerHandler;
  const { socket } = connection;

  socket.on("connections", (event: any) => {
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
  });
};

export { websocketHandler };
