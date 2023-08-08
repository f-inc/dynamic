// fastify
import type { FastifyPluginCallback, FastifyPluginAsync } from 'fastify';

export interface Plugin {
  callback: FastifyPluginCallback | FastifyPluginAsync;
  options?: any;
}

export interface Server {
  plugins: Plugin[];
  host?: string;
  port?: number;
}
