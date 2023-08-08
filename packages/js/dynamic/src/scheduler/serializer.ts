/**
 * Serializing Logic for Dynamic Serverless
 */
import { Plugin } from '../types';

import type { FastifyPluginCallback, FastifyPluginAsync } from 'fastify';

interface SerializedPlugin {
  callback: string;
  options?: any;
}

const serialize = (plugins: Plugin[]): string[] => {
  const output: string[] = [];
  plugins.map((plugin) => {
    const serializedCallback = plugin.callback.toString();
    const serializedPlugin: SerializedPlugin = {
      ...plugin,
      callback: serializedCallback,
    };

    output.push(JSON.stringify(serializedPlugin));
  });

  return output;
};

const deserialize = (stringPlugins: string[]): Plugin[] => {
  const plugins: Plugin[] = [];
  stringPlugins.map((stringPlugin) => {
    const sPlugin: SerializedPlugin = JSON.parse(stringPlugin);
    const callback = deserializeCallback(sPlugin.callback);
    const plugin: Plugin = {
      ...sPlugin,
      callback,
    };

    plugins.push(plugin);
  });

  return plugins;
};

const deserializeCallback = (
  sFunc: string
): FastifyPluginCallback | FastifyPluginAsync => {
  sFunc = JSON.parse(sFunc).function;
  const func = new Function('return ' + sFunc)();

  return func;
};

export { serialize, deserialize };
