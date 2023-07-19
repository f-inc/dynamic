import dynamic from "./dynamic";

const startServer = (): void => {
    // Run the server!
    dynamic.listen({ port: 9801 }, function (err, address) {
        if (err) {
        dynamic.log.error(err);
        process.exit(1);
        }
        // Server is now listening on ${address}
    });
}

export default startServer;