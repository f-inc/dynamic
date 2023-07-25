import { FastifyRequest } from "fastify";
import type { SocketStream } from "@fastify/websocket";

const websocketHandler = async (
  connection: SocketStream,
  request: FastifyRequest
) => {
  const { socket } = connection;

  socket.on("connections", (event: any) => {
    console.log("connection event:", event);
  });

  socket.on("message", (data: any) => {
    console.log("data recieved:", data);
  });
};

export { websocketHandler };
