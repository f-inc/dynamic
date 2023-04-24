/*
 * this javascript file will connect a websocket server at /ws
 * the websocket connection will send back html
 * and we'll render that in root
 */

// main.js
const socket = new WebSocket(`ws://${window.location.host}/ws`);

socket.addEventListener("open", (event) => {
  console.log("WebSocket opened:", event);

  setTimeout(() => {
    sendMessage({ route: "chain", data: { product: "cookies" } });
  }, 2000);

  setTimeout(() => {
    sendMessage({ route: "chain", data: { product: "ties" } });
  }, 3000);
});

socket.addEventListener("connected", (event) => {
  console.log("WebSocket connected:", event);
});

socket.addEventListener("message", (event) => {
  console.log("WebSocket message received:", event);
  const receivedHTML = event.data;
  document.querySelector("#root").innerHTML = receivedHTML;
});

socket.addEventListener("close", (event) => {
  console.log("WebSocket disconnected:", event);
});

socket.addEventListener("error", (event) => {
  console.log("WebSocket error:", event);
});

function sendMessage(json) {
  if (socket.readyState === WebSocket.OPEN) {
    //TODO validate it has "route"
    socket.send(JSON.stringify(json));
  } else {
    console.error("WebSocket not connected");
  }
}
