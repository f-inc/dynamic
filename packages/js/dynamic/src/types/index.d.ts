import type { FastifyRequest } from "fastify";
import { RouteOptions, RouteOptions } from "@fastify/websocket";

// dynamic
// import { DynamicRouteOptions } from "./resource";
import { WebsocketHandler } from "@fastify/websocket";

interface DynamicRouteOptions extends <RouteOptions> {
  runnerHandler?: any;
  wsHandler?: WebsocketHandler;
}

interface DynamicRequest extends FastifyRequest {
  routeOptions: DynamicRouteOptions;
}

// interface DynamicWebSocketHandler extends WebsocketHandler {
//     req
// }

export { DynamicRequest, DynamicRouteOptions };
