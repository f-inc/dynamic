import Fastify from "fastify";
import FastifyWebsocket from "@fastify/websocket";

const parseRequest = (request: any) => {
  const route = "test_route";
  const data = { test: "test" };
  return { route, data };
};

const checkIfRouteExists = (route: string) => {
  return true;
};

const executeRoute = async (
  route: string,
  data: any,
  sendMessage: (message: any) => void
) => {
  return { route, data };
};

const fastify = Fastify({
  logger: true,
});

fastify.register(FastifyWebsocket);

// Declare a route
fastify.get("/", function (request, reply) {});

fastify.get("/ws", { websocket: true }, async (connection, req) => {
  const sendMessage = (message: any, messageId = null) => {
    if (messageId) {
      message.messageId = messageId;
    }

    connection.socket.send(JSON.stringify(message));
  };

  connection.socket.on("message", async (message: any) => {
    //Parse request
    const { route, data } = parseRequest(message);
    //check if there's a route that's been set
    if (!checkIfRouteExists(route)) {
      connection.socket.send(JSON.stringify({ error: "Route not found" }));
      return;
    }
    //execute route
    const response = await executeRoute(route, data, sendMessage);
    //return response
    sendMessage(response);
  });
});

// Run the server!
fastify.listen({ port: 9801 }, function (err, address) {
  if (err) {
    fastify.log.error(err);
    process.exit(1);
  }
  // Server is now listening on ${address}
});
