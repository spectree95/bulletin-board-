const input = document.getElementById("chat_input");
const productId = parseInt(input.dataset.productId);
const productOwnerId = input.dataset.productOwnerId;
const currentUserId = input.dataset.currentUserId

const wsProtocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
const ws = new WebSocket(`${wsProtocol}${window.location.host}/ws/chat_author/${productId}/`);

const messageContainer = document.getElementById("messages");
const sendBtn = document.getElementById("message-send");

ws.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const messageEl = document.createElement("div");
    messageEl.className = "message";
    if (data.sender_name === currentUserId) {
        messageEl.classList.add("my-message")
    }
    else {
        messageEl.classList.add("other-message")
    }
    messageEl.textContent = `${data.message}`
    messageContainer.appendChild(messageEl)
    messageContainer.scrollTop = messageContainer.scrollHeight
}

console.log("productId = ", productId, "typeof:", typeof productId);
sendBtn.onclick = function () {
    const message = input.value;
    if (!message) return;
    ws.send(JSON.stringify({
        "command": "send",
        "message": message,
        "sender_id": currentUserId,
        "product_id": productId,
        
    }));

    input.value = "";

};

input.addEventListener("keyup", function(e){
    if (e.key == "Enter"){
        sendBtn.click()
    }
})

ws.onerror = function(error) {
    console.error("Ошибка WebSocket:", error);
};

ws.onclose = function(e) {
    console.log("Соединение закрыто. Код:", e.code, "Причина:", e.reason);
};