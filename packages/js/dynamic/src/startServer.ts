import dynamic from "./dynamic";

const host: string = process.env.HOST || "0.0.0.0"
const port: number = parseInt(process.env.PORT || '8000')

const startServer = (): void => {
    dynamic.get("/", {websocket: false}, (request, reply) => {
        reply.send("Hello World!")
    })


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