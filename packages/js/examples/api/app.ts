import "dotenv/config";

import { startServer } from "dynamic";
import { Plugins, Server } from "dynamic/src/types";

/**
 * Without Plugins
 *
 * With file-based routing, technically you app.ts you could simply have one line:
 *
 * startServer();
 *
 * For the sake of example, we added a non-filebased route.
 */

import home, { HomeOpts } from "./exampleRoute";

const homeOptions: HomeOpts = { foo: "bar", prefix: "/example" };

const routes: Plugins[] = [{ callback: home, options: homeOptions }];

const server: Server = {
  plugins: routes,
};

startServer(server);
