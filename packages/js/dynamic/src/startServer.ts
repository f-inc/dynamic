// dynamic
import dynamic from './dynamic';
import type { Server } from './types';

const DEFAULT_HOST: string = process.env.HOST ?? '0.0.0.0';
const DEFAULT_PORT: number = parseInt(process.env.PORT ?? '8000');

const DEFAULT_SERVER: Server = {
  plugins: [],
  host: DEFAULT_HOST,
  port: DEFAULT_PORT,
};

const startServer = (server?: Server): void => {
  server = { ...DEFAULT_SERVER, ...server };
  const { plugins, host, port } = server;

  const app = dynamic();

  if (plugins != null) {
    // adding plugins - includes routes
    plugins.forEach(({ callback, options }) => {
      app.register(callback, options);
    });
  }

  // Run the server!
  app.listen({ host, port }, function (err, address) {
    if (err != null) {
      app.log.error(err);
      process.exit(1);
    }
    console.log(`Server is now listening on ${address}`);
  });
};

export default startServer;
