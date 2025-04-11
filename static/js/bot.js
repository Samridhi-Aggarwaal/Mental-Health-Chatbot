function updateTime() {
  var now = new Date();
  var hours = now.getHours();
  var minutes = now.getMinutes();
  var seconds = now.getSeconds();
  var timeString = hours + ':' + (minutes < 10 ? '0' + minutes : minutes);
  document.getElementById('clock').textContent = timeString;
}
setInterval(updateTime, 1000);

// Chatbot toggle logic
var running = false;
document.getElementById("chatbot_toggle").onclick = function () {
  const chatbot = document.getElementById("chatbot");
  const toggleIcons = document.getElementById("chatbot_toggle").children;

  if (chatbot.classList.contains("collapsed")) {
    chatbot.classList.remove("collapsed");
    toggleIcons[0].style.display = "none";
    toggleIcons[1].style.display = "";
    setTimeout(() => appendMessage(BOT_NAME, "left", "Hi"), 1000);
  } else {
    chatbot.classList.add("collapsed");
    toggleIcons[0].style.display = "";
    toggleIcons[1].style.display = "none";
  }
};

// Constants
const BOT_IMG = "static/img/mhcicon.png";
const PERSON_IMG = "static/img/person.png";
const BOT_NAME = "Psychiatrist Bot";
const PERSON_NAME = "You";

// DOM Elements
const form = document.querySelector(".msger-inputarea");
const inputField = document.querySelector(".msger-input");
const chat = document.querySelector(".msger-chat");

// Form Submit Listener
form.addEventListener("submit", async function (e) {
  e.preventDefault();
  const msgText = inputField.value.trim();
  if (!msgText) return;

  appendMessage(PERSON_NAME, "right", msgText, PERSON_IMG);
  inputField.value = "";

  const response = await fetch(`/get?msg=${encodeURIComponent(msgText)}`);
  const data = await response.text();

  appendMessage(BOT_NAME, "left", data, BOT_IMG);
});

// Append message function
function appendMessage(name, side, text, img) {
  const time = formatDate(new Date());
  const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-img" style="background-image: url(${img})"></div>
      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${time}</div>
        </div>
        <div class="msg-text">${text}</div>
      </div>
    </div>
  `;
  chat.insertAdjacentHTML("beforeend", msgHTML);
  chat.scrollTop = chat.scrollHeight;
}

// Time formatting helper
function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();
  return `${h.slice(-2)}:${m.slice(-2)}`;
}
