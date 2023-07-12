const websocket = new WebSocket("ws://localhost:9801");

websocket.addEventListener("open", () => {
  console.log("WebSocket connection is open!");
});

websocket.addEventListener("message", (event: any) => {
  console.log("Received message from server:", event.data);
});

websocket.addEventListener("close", (event: any) => {
  console.log("WebSocket connection closed:", event.code, event.reason);
});

websocket.addEventListener("error", (event: any) => {
  console.error("WebSocket error:", event);
});
