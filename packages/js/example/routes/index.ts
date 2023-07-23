import { FastifyPluginCallback, FastifyInstance } from "fastify";
import fp from "fastify-plugin";

export interface HomeOpts {
  foo?: string;
}

const homeRoute: FastifyPluginCallback = (
  dynamic: FastifyInstance,
  opts: HomeOpts,
  done
) => {
  dynamic.get("/", (request, reply) => {
    reply.send("Hello World");
  });

  dynamic.get("/foo", (_, reply) => {
    reply.send(`Foo value from opts: ${opts.foo ?? "foo"}`);
  });

  done();
};

export default fp(homeRoute);
