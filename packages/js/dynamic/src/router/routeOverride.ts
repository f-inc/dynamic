import { RouteOptions } from "@fastify/websocket";
import type { FastifyInstance, FastifyPluginCallback } from "fastify";

const routeOverride: FastifyPluginCallback = (
  dynamic: FastifyInstance,
  options,
  done
) => {
  const _defaultRoute = dynamic.route;
  dynamic.decorate("route", (routeOptions: RouteOptions) => {
    console.log("test", routeOptions);

    return _defaultRoute(routeOptions);
  });

  done();
};

export default routeOverride;
