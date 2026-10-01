let room = null;

const input = document.getElementById("chat-input");
const currentUserId = input.dataset.currentUserId;
const product = input.dataset.product;

const messageContainer = document.getElementById("chat-messages");
const sendBtn = document.getElementById("message-send");

const wsProtocol = window.location.protocol === "https:" ? "wss://" : "ws://";
const ws = new WebSocket(
    wsProtocol + window.location.host + "/ws/Messenger/"
);


function openChat(el) {
    room = el.dataset.room;

    const userA = el.dataset.userA;
    const userB = el.dataset.userB;
    const productImg = el.dataset.productImg;
    const productId = el.dataset.productId;


    document.querySelectorAll(".chat_item .chat").forEach(chat => {
        chat.style.backgroundColor = "";
    });

    document.querySelectorAll(".chat-p").forEach(p => {
        p.style.color = "#787878ff";
    });

    document.querySelectorAll(".chat-username").forEach(p => {
        p.style.color = "black";
    });


    const chat = el.querySelector(".chat");

    if (chat) {
        chat.style.backgroundColor = "#4a6cf7";
    }

    const chatP = document.getElementById(`chat-${room}-p`);

    if (chatP) {
        chatP.style.color = "#f1f1f1";
    }

    const username = el.querySelector(".chat-username");

    if (username) {
        username.style.color = "#f1f1f1";
    }


    const chatHeader = document.getElementById("chat-header");

    chatHeader.textContent =
        userA === currentUserId ? userB : userA;


    const chatImg = document.getElementById("chat-img");

    chatImg.style.display = "flex";
    chatImg.src = productImg;


    document.getElementById("chat-input-container").style.display = "flex";


    if (window.innerWidth <= 768) {
        document.getElementById("chat-list").style.display = "none";
        document.getElementById("chat-window").style.display = "block";
    }

    
    input.dataset.room = room;
    input.dataset.productId = productId;
    
    messageContainer.innerHTML = "";

    if (ws.readyState === WebSocket.OPEN){
        ws.send(JSON.stringify({
            command: "join",
            room_id: room
        }));
    } 

    
}


function openChatByRoom(roomId) {
    const chat = document.querySelector(
        `.chat_item[data-room="${roomId}"]`
    );

    if (!chat) {
        console.warn(`Чат с room=${roomId} не найден`);
        return;
    }

    openChat(chat);
}


const chatSidebar = document.getElementById("chats-sidebar-list");

if (chatSidebar) {

    chatSidebar.addEventListener("click", function (e) {

        const chat = e.target.closest(".chat_item");

        if (!chat) {
            return;
        }

        e.preventDefault();

        openChat(chat);
    });
}

ws.onmessage = function (event) {

    const data = JSON.parse(event.data);


    if (data.type === "new_message_for_user") {
        const sidebar = document.getElementById("chats-sidebar-list");
        const existingChat = document.querySelector(`[data-room="${data.room_id}"]`);

        if (existingChat) {
            return;
        }

        const newChatHTML = `
            <a
                href="#"
                class="chat_item"
                data-product-id="${data.product_id}"
                data-room="${data.room_id}"
                data-user-a="${data.sender_name}"
                data-user-b=""
                data-product-img="${data.product_img}"
                style="text-decoration: none;"
            >
                <div class="chat">
                    <img
                        src="${data.product_img}"
                        style="width: 90px; height: 65px; object-fit: inherit; border-radius: 10px;"
                        alt=""
                    >
                    <div style="display: flex; flex-direction: column; justify-content: space-between; margin-left: 10px;">
                        <p
                            class="chat-username"
                            style="color: black; font-weight: bold; margin: 0;"
                        >
                            ${data.sender_username}
                        </p>
                        <p
                            id="chat-${data.room_id}-p"
                            class="chat-p"
                            style="color: #787878ff; margin: 0;"
                        >
                            ${data.last_message}
                        </p>
                    </div>
                </div>
            </a>
        `;

        sidebar.insertAdjacentHTML("afterbegin", newChatHTML);
        return;
    }


    const created = new Date(data.created);

    const hours = created
        .getHours()
        .toString()
        .padStart(2, "0");

    const minutes = created
        .getMinutes()
        .toString()
        .padStart(2, "0");

    const msgTime = `${hours}:${minutes}`;

    const day = created.toLocaleDateString();

    let dayBlock = document.getElementById(`day-${day}`);


    if (!dayBlock) {

        dayBlock = document.createElement("div");

        dayBlock.classList.add("day-block");

        dayBlock.id = `day-${day}`;


        const dayHeader = document.createElement("div");

        dayHeader.classList.add("day-header");

        dayHeader.textContent = day;


        dayBlock.appendChild(dayHeader);

        messageContainer.appendChild(dayBlock);
    }


    const messageEl = document.createElement("div");

    messageEl.classList.add("message");


    if (data.sender_name == currentUserId) {

        messageEl.classList.add("my-message");

    } else {

        messageEl.classList.add("other-message");

    }


    messageEl.innerHTML = `
        <div class="message-text">
            
        </div>

        <div class="message-time">
            ${msgTime}
        </div>
    `;
    messageEl.querySelector('.message-text').textContent = data.message;


    dayBlock.appendChild(messageEl);


    messageContainer.scrollTop =
        messageContainer.scrollHeight;
};


sendBtn.onclick = function () {

    const message = input.value.trim();

    if (!message) {
        return;
    }


    if (!room) {
        return;
    }


    ws.send(JSON.stringify({
        command: "send",
        room_id: room,
        message: message
    }));


    input.value = "";
};


input.addEventListener("keyup", function (e) {

    if (e.key === "Enter") {
        sendBtn.click();
    }

});


const back = document.getElementById("back-chat");

if (back) {

    back.onclick = function () {

        if (window.innerWidth <= 768) {

            document.getElementById("chat-window").style.display = "none";

            document.getElementById("chat-list").style.display = "block";
        }

    };

}
