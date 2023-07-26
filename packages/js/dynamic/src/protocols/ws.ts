import { type FastifyRequest } from 'fastify';
import type { RouteOptions, SocketStream } from '@fastify/websocket';

type wsWrapperType = (
  f: any
) => (conn: SocketStream, request: FastifyRequest) => Promise<void>;

const websocketWrapper: wsWrapperType = (func: any): any => {
  const websocketHandler = async (
    connection: SocketStream,
    request: FastifyRequest
  ): Promise<void> => {
    const { socket } = connection;

    socket.on('open', (event: any) => {
      console.log('connection event:', event);
    });

    socket.on('message', async (data: any) => {
      console.log('data recieved:', data.toString());
      socket.send(
        JSON.stringify({
          output: await func(),
        })
      );
    });
  };

  return websocketHandler;
};

const onRouteOverride = (routeOptions: RouteOptions): void => {
  if (routeOptions.wsHandler != null)
    routeOptions.wsHandler = websocketWrapper(routeOptions.wsHandler);
};

export { websocketWrapper, onRouteOverride };
