// fastify
import Fastify, { type FastifyInstance } from "fastify";
import FastifyWebsocket from "@fastify/websocket";

// default plugins
import autoRoute from "fastify-autoroutes";

type DynamicOptions = {
  fileBased?: boolean;
};

const dynamic = (options?: DynamicOptions) => {
  const app: FastifyInstance = Fastify({
    logger: true,
  });

  app.register(FastifyWebsocket);

  app.register(autoRoute, {
    dir: "./../routes",
  });

  return app;
};

export default dynamic;
