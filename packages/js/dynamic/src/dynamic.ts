// fastify
import Fastify, { type FastifyInstance } from 'fastify';
import FastifyWebsocket from '@fastify/websocket';

// default plugins
import autoRoute from 'fastify-autoroutes';

// dynamic
import { onRouteOverride } from './protocols/ws';

interface DynamicOptions {
  fileBased?: boolean;
}

const dynamic = (options?: DynamicOptions): FastifyInstance => {
  const app: FastifyInstance = Fastify({
    logger: true,
  });

  app.addHook('onRoute', onRouteOverride);
  app.register(FastifyWebsocket);

  app.register(autoRoute, {
    dir: './../routes',
  });

  return app;
};

export default dynamic;
