// fastify
import Fastify, { type FastifyInstance } from "fastify";
import FastifyWebsocket from "@fastify/websocket";

// default plugins
import { fileRoutes } from "fastify-file-routes";

type DynamicOptions = {
  fileBased?: boolean;
};

const dynamic = (options?: DynamicOptions) => {
  const app: FastifyInstance = Fastify({
    logger: true,
  });

  app.register(FastifyWebsocket);

  return app;
};

export default dynamic;
