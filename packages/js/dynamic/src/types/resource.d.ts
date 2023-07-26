import { RouteOptions } from "@fastify/websocket";
import { GetRoute } from "fastify-autoroutes";

export interface DynamicRouteOptions {
  runnerHandler?: any;
}
