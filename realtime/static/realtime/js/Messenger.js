let room = null
const input = document.getElementById("chat-input")
const currentUserId = input.dataset.currentUserId
const product = input.dataset.product
const messageContainer = document.getElementById("chat-messages");
const sendBtn = document.getElementById("message-send");

const wsProtocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
const ws = new WebSocket(wsProtocol + window.location.host + `/ws/Messenger/`);

document.querySelectorAll(".chat_item").forEach(el => {
    el.addEventListener("click", e => {
        room = el.dataset.room;
        productId = el.dataset.productId
        const userA = el.dataset.userA
        const userB = el.dataset.userB
        const productImg = el.dataset.productImg
        document.querySelectorAll(".chat_item .chats").forEach(chat => {
            chat.style.backgroundColor = "";
        });
        document.querySelectorAll(".chat-p").forEach(p => {
            p.style.color = "#787878ff";
        })
        document.querySelectorAll(`.chat-username`).forEach(p =>{
            p.style.color = "black"
        })


        el.querySelector(".chats").style.backgroundColor = "#4a6cf7";
        document.getElementById(`chat-${room}-p`).style.color = "#f1f1f1";
        el.querySelector(`.chat-username`).style.color = "#f1f1f1";
        
        const chatHeader = document.getElementById("chat-header");
        chatHeader.textContent = (userA===currentUserId) ? userB : userA;

        const chatImg = document.getElementById("chat-img");
        chatImg.style.display = "flex"
        chatImg.src = productImg 

        document.getElementById("chat-input-container").style.display = "flex"
        if(window.innerWidth<=768){

            document.getElementById("chat-list").style.display="none";

            document.getElementById("chat-window").style.display="block";

        }

        input.dataset.room = room
        input.dataset.productId = productId
        // отправляем join через WS
        ws.send(JSON.stringify({
            "command": "join",
            "room_id": room,
            "product_id": productId
        }));
        messageContainer.innerHTML = ""; // очистка правой колонки
    });
});




ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    const created = new Date(data.created);
    const hours = created.getHours().toString().padStart(2, "0");
    const minutes = created.getMinutes().toString().padStart(2, "0");
    const msgTime = `${hours}:${minutes}`;
    const day = created.toLocaleDateString();
    let dayBlock = document.getElementById(`day-${day}`);
    if (!dayBlock) {
        dayBlock = document.createElement("div");
        dayBlock.classList.add("day-block");
        dayBlock.id = `day-${day}`;

        // заголовок дня
        const dayHeader = document.createElement("div");
        dayHeader.classList.add("day-header");
        dayHeader.textContent = day;

        dayBlock.appendChild(dayHeader);
        messageContainer.appendChild(dayBlock);
    }


    const messageEl = document.createElement("div");
    messageEl.classList.add("message");
    if (data.sender_name == currentUserId) {
        messageEl.classList.add("my-message")
    }
    else {
        messageEl.classList.add("other-message")
    }
    messageEl.innerHTML = `
        <div class = "message-text">${data.message}</div>
        <div class = "message-time">${msgTime}</div>    
    `;


    dayBlock.appendChild(messageEl);
    
    messageContainer.scrollTop = messageContainer.scrollHeight
    
}



sendBtn.onclick = function () {
    const message = input.value;
    if (!message) return;
    ws.send(JSON.stringify({
        "command": "send",
        "room_id": room,
        "message": message,
        "product": product,
        "product_id": productId,
    }));

    input.value = "";

};

input.addEventListener("keyup", function(e){
    if (e.key == "Enter"){
        sendBtn.click()
    }
})

const back=document.getElementById("back-chat");

back.onclick=function(){

    if(window.innerWidth<=768){

        document.getElementById("chat-window").style.display="none";

        document.getElementById("chat-list").style.display="block";

    }

}