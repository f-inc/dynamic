/*
 * this javascript file will connect a websocket server at /ws
 * the websocket connection will send back html
 * and we'll render that in root
 */

// main.js
const socket = new WebSocket(`ws://${window.location.host}/agent`);

socket.addEventListener("open", (event) => {
  console.log("WebSocket opened:", event);
});

socket.addEventListener("connected", (event) => {
  console.log("WebSocket connected:", event);
});

socket.addEventListener("message", (event) => {
  console.log("WebSocket message received:", event);
  var messages = document.getElementById("messages");
  data = JSON.parse(event.data);
  var content = document.createTextNode(data.content);
  messages.appendChild(content);
});

socket.addEventListener("close", (event) => {
  console.log("WebSocket disconnected:", event);
});

socket.addEventListener("error", (event) => {
  console.log("WebSocket error:", event);
});

function sendMessage(event) {
  console.log();
  var input = document.getElementById("messageText");
  var content = input.value;
  var config = { input: input.value };
  var value = { content: content, config: config };
  socket.send(JSON.stringify(value));
  input.value = "";
  event.preventDefault();
}
