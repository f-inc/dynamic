import startServer, { Plugins, Server } from "../dynamic/src/startServer";

// route plugins
import home, { HomeOpts } from "./routes";

const homeOptions: HomeOpts = { foo: "bar" };

const routes: Plugins[] = [{ callback: home, options: homeOptions }];

const server: Server = {
  plugins: routes,
};

startServer(server);
