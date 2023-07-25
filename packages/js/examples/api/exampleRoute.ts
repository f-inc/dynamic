import type { FastifyPluginCallback, FastifyInstance } from "fastify";
import fp from "fastify-plugin";

export interface HomeOpts {
  foo?: string;
  prefix?: string;
}

const homeRoute: FastifyPluginCallback<HomeOpts> = (
  dynamic: FastifyInstance,
  opts: HomeOpts,
  done
) => {
  const { prefix } = opts ?? "";
  dynamic.get(prefix + "/", (request, reply) => {
    reply.send("Hello Example!");
  });

  dynamic.get(prefix + "/foo", (_, reply) => {
    reply.send(`Foo value from opts: ${opts.foo ?? "foo"}`);
  });

  done();
};

export default fp(homeRoute);
