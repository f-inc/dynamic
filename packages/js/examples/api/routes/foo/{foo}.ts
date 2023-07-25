// route - /foo/:foo
import type { FastifyInstance, FastifyRequest, FastifyReply } from "fastify";
import { Resource } from "fastify-autoroutes";

interface FooParams {
  foo: string;
}

interface FooBody {
  data: string;
}

interface FooRequest extends FastifyRequest {
  params: FooParams;
  body: FooBody;
}
export default (fastify: FastifyInstance) =>
  <Resource>{
    get: {
      handler: async (request: FooRequest, reply: FastifyReply) =>
        `Foo Foo ${request.params.foo}!`,
    },
    put: {
      handler: async (request: FooRequest, reply: FastifyReply) =>
        `put body: ${request.body.data}! \nput params: ${request.params.foo}\n`,
    },
  };
