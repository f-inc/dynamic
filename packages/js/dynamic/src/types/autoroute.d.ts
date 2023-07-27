// fastify
import { type Resource } from 'fastify-autoroutes';
import { type RouteOptions } from '@fastify/websocket';

export declare type DynamicGetRoute = Omit<
  RouteOptions,
  'method' | 'url' | 'body' | 'handler'
> &
  Partial<RouteOptions, 'handler'>;

export interface DynamicResource extends Resource {
  get?: DynamicGetRoute;
}
