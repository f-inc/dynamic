// route - /foo/:foo
import type { FastifyInstance, FastifyRequest, FastifyReply } from "fastify";
import { Resource } from "fastify-autoroutes";

interface GetFooParams {
  foo: string;
}

interface GetFooRequest extends FastifyRequest {
  params: GetFooParams;
}
export default (fastify: FastifyInstance) =>
  <Resource>{
    get: {
      handler: async (request: GetFooRequest, reply: FastifyReply) =>
        `Foo Foo ${request.params.foo}!`,
    },
  };
