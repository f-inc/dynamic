// fastify
import { FastifyPluginCallback, FastifyPluginAsync } from "fastify";


// dynamic
import dynamic from "./dynamic";

const host: string = process.env.HOST || "0.0.0.0"
const port: number = parseInt(process.env.PORT || '8000')

interface Plugins {
    callback: FastifyPluginCallback | FastifyPluginAsync,
    options?: any
}

const startServer = (plugins?: Plugins[]): void => {
    dynamic.get("/", {websocket: false}, (request, reply) => {
        reply.send("Hello World!")
    })
    
    if (plugins) {

        // adding plugins - includes routes
        plugins.forEach(({ callback, options }) => {
            dynamic.register(callback, options)
        })
    }

    // Run the server!
    dynamic.listen({ host: host, port: port }, function (err, address) {
        if (err) {
            dynamic.log.error(err);
            process.exit(1);
        }
        console.log(`Server is now listening on ${address}`)
    });
}

export default startServer;