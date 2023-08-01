import { type FastifyRequest } from 'fastify';
import type { RouteOptions, SocketStream } from '@fastify/websocket';

import { ServerMessage, ErrorMessage } from '../types';
import { DynamicAgent } from '../dync/langchain/agent';
import { AgentRunner } from '../runners/langchain';
import { Config } from '../runners/types';

type GetDyncType = () => Promise<DynamicAgent>;

type wsWrapperType = (
  f: GetDyncType
) => (conn: SocketStream, request: FastifyRequest) => Promise<void>;

const websocketWrapper: wsWrapperType = (getDync) => {
  const websocketHandler = async (
    connection: SocketStream,
    request: FastifyRequest
  ): Promise<void> => {
    const { socket } = connection;

    socket.onopen = async (event: any) => {
      console.log('connection event:', event.type);
    };

    socket.onclose = async (event: CloseEvent) => {
      // TODO: Connection Mangager close handling
      console.log(
        `Closing socket (code=${event.code}), (wasClean=${event.wasClean}) 
        ${event.reason ? `\nReason: ${event.reason}` : ''}`
      );
    };

    socket.onmessage = async (event: MessageEvent) => {
      const { data } = event;

      let input = null;
      try {
        input = JSON.parse(data);
      } catch (e: unknown) {
        if (e instanceof SyntaxError) {
          const errMsg =
            'Dynamic Websocket will only take JSON parseable data.';
          const error: ErrorMessage = {
            error: e.toString(),
            content: errMsg,
          };

          console.warn(errMsg);
          socket.send(JSON.stringify(error));
        }
        return;
      }
      console.log('data recieved:', input);

      // socket.send(
      //   JSON.stringify({
      //     output: await func(),
      //   })
      // );
    };
  };

  return websocketHandler;
};

const onRouteOverride = (routeOptions: RouteOptions): void => {
  if (routeOptions.wsHandler != null && 'dynamic' in routeOptions)
    routeOptions.wsHandler = websocketWrapper(
      routeOptions.wsHandler as GetDyncType
    );
};

export { websocketWrapper, onRouteOverride };
