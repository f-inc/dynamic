import { type DynamicAgent } from '../dync/langchain/agent';

// fastify
import type { Resource } from 'fastify-autoroutes';
import type { FastifyInstance } from 'fastify';

const getDyncHandler = (dync: DynamicAgent) => {
  return async () => dync;
};

const routeTemplate = (wsHandler: any) => {
  return (fastify: FastifyInstance) =>
    ({
      get: {
        handler: () => null,
        wsHandler,
      },
    }) as Resource;
};

type wsRouteType = (w: any) => (f: FastifyInstance) => Resource;

const wsRouteBuilder: wsRouteType = (dync: DynamicAgent) => {
  return routeTemplate(getDyncHandler(dync));
};

export default wsRouteBuilder;
