import type { FastifyInstance, FastifyRequest, FastifyReply } from "fastify";
import { Resource } from "fastify-autoroutes";

export default (fastify: FastifyInstance) =>
  <Resource>{
    get: {
      handler: async (request: FastifyRequest, reply: FastifyReply) =>
        "Hello, Route!",
    },
  };
