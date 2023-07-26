// fastify
import type { FastifyPluginCallback, FastifyPluginAsync } from 'fastify';

export interface Plugins {
  callback: FastifyPluginCallback | FastifyPluginAsync;
  options?: any;
}

export interface Server {
  plugins: Plugins[];
  host?: string;
  port?: number;
}
