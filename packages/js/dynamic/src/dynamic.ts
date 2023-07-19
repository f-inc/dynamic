import Fastify, { FastifyInstance } from "fastify";
import FastifyWebsocket from "@fastify/websocket";

const dynamic: FastifyInstance = Fastify({
  logger: true,
});

dynamic.register(FastifyWebsocket);

export default dynamic;