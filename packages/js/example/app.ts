import startServer, { Plugins, Server } from "../dynamic/src/startServer";

// route plugins
import route from "./routes";

const routes: Plugins[] = [
    {callback: route}
]

const server: Server = {
    plugins: routes
}

startServer(server)