import type { FastifyRequest } from "fastify";
import { type RequestRouteOptions } from "fastify/types/request";
import { type WebsocketHandler } from "@fastify/websocket";

interface DynamicRouteOptions extends RequestRouteOptions {
  runnerHandler?: any;
  wsHandler?: WebsocketHandler;
}

interface DynamicRequest extends FastifyRequest {
  routeOptions: DynamicRouteOptions;
}

export type { DynamicRequest, DynamicRouteOptions };
