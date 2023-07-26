import { FastifyRequest } from "fastify";
import type { RouteOptions, SocketStream } from "@fastify/websocket";

const websocketWrapper = (func: any) => {
  const websocketHandler = async (
    connection: SocketStream,
    request: FastifyRequest
  ) => {
    const { socket } = connection;

    socket.on("open", (event: any) => {
      console.log("connection event:", event);
    });

    socket.on("message", async (data: any) => {
      console.log("data recieved:", data.toString());
      socket.send(
        JSON.stringify({
          output: await func(),
        })
      );
    });
  };

  return websocketHandler;
};

const onRouteWSWrapperOverride = (routeOptions: RouteOptions) => {
  if (routeOptions.wsHandler)
    routeOptions.wsHandler = websocketWrapper(routeOptions.wsHandler);
};

export { websocketWrapper, onRouteWSWrapperOverride };
