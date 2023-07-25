import startServer, { Plugins, Server } from "../../dynamic/src/startServer";

// route plugins
// import home, { HomeOpts } from "./routes";

// const homeOptions: HomeOpts = { foo: "bar" };

const routes: Plugins[] = [];

const server: Server = {
  plugins: routes,
};

startServer(server);
