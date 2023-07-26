import type { FastifyInstance, FastifyRequest, FastifyReply } from "fastify";
import { Resource } from "fastify-autoroutes";

const exampleWSHandler = async () => "Hello, this is your custom WS logic.";

export default (fastify: FastifyInstance) =>
  <Resource>{
    get: {
      handler: async (request: FastifyRequest, reply: FastifyReply) =>
        "Hello, Route!",
      wsHandler: exampleWSHandler,
    },
  };
