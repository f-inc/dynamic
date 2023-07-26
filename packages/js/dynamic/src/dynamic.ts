// @ts-nocheck
// fastify
import Fastify, { type FastifyInstance } from "fastify";
import FastifyWebsocket from "@fastify/websocket";

// default plugins
import autoRoute from "fastify-autoroutes";
import { websocketHandler } from "./protocols/ws";

// dynamic
import { type DynamicRouteOptions } from "./types";

interface DynamicOptions {
  fileBased?: boolean;
}

const dynamic = (options?: DynamicOptions): FastifyInstance => {
  const app: FastifyInstance = Fastify({
    logger: true,
  });

  app.register(FastifyWebsocket);
  app.addHook("onRoute", (routeOptions) => {
    if (routeOptions.wsHandler != null) {
      console.log(routeOptions);
      routeOptions.runnerHandler = routeOptions.wsHandler;
      routeOptions.wsHandler = websocketHandler;
    }

    return routeOptions;
  });

  app.register(autoRoute, {
    dir: "./../routes",
  });

  return app;
};

export default dynamic;
