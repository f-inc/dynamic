// fastify
import Fastify, { type FastifyInstance } from "fastify";
import FastifyWebsocket from "@fastify/websocket";

// default plugins
import autoRoute from "fastify-autoroutes";
import { websocketHandler } from "./protocols/ws";

// dynamic
import { DynamicRouteOptions } from "./types";

interface DynamicOptions {
  fileBased?: boolean;
}

const dynamic = (options?: DynamicOptions): FastifyInstance => {
  const app: FastifyInstance = Fastify({
    logger: true,
  });

  app.register(FastifyWebsocket);
  app.addHook("onRoute", (routeOptions: DynamicRouteOptions) => {
    if (routeOptions.wsHandler) {
      routeOptions.runnerHandler = routeOptions.wsHandler;
      routeOptions.wsHandler = websocketHandler;
      console.log("test", routeOptions);
    }
  });

  app.register(autoRoute, {
    dir: "./../routes",
  });

  return app;
};

export default dynamic;
