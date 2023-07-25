// route - /foo/:id/bar
import type { FastifyInstance, FastifyRequest, FastifyReply } from "fastify";
import { Resource } from "fastify-autoroutes";

interface GetParams {
  id: string;
}

interface CustomGetRequest extends FastifyRequest {
  params: GetParams;
}

export default (fastify: FastifyInstance) =>
  <Resource>{
    get: {
      handler: async (request: CustomGetRequest, reply: FastifyReply) =>
        `Hello ${request.params?.id}`,
    },
  };
