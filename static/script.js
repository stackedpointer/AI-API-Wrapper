console.log("JS LOADED");


let chatId = null;

async function loadSidebar(){
    const res = await fetch("http://127.0.0.1:8000/chats");
    const chats = await res.json();
    const list = document.getElementById("chat-list");
    list.innerHTML = "";
    chats.forEach(chat => {
        const div = document.createElement("div");
        div.className = "chat-item";
        div.textContent = chat.title;
        div.onclick = (event) => openChat(chat.id, event);
        list.appendChild(div)
    });
}
async function openChat(id, event) {
    chatId = id;
    document.querySelectorAll(".chat-item").forEach(el => el.classList.remove("active"));
    event.target.classList.add("active");

    const res = await fetch(`http://127.0.0.1:8000/chats/${id}`);
    const messages = await res.json();
    const container = document.getElementById("chat-container");
    container.innerHTML = "";
    messages.forEach(m => {
        container.innerHTML += `<p class = "${m.role === "user" ? "user-message":"ai-message"}">${m.content}</p>`;
    });
};
window.onload = loadSidebar;


async function sendData() {

    console.log("BUTTOON CLICKED")
    const input = document.getElementById("userinput").value;
    document.getElementById("userinput").value = ""

    document.getElementById("chat-container").innerHTML += '<p class = "user-message" >' + input + '</p>';


    const chatContainer = document.getElementById("chat-container");

    if (!chatContainer) {
        console.error("chat-container element not found!");
        return;
    }

    try{const response = await fetch("http://127.0.0.1:8000/request", {
        method: "POST", 
        headers: {
        "Content-Type":"application/json"
        },
        body: JSON.stringify({request : input,chat_id:chatId
        })
    });
    const data = await response.json();
    console.log(data)

    chatId = data.chat_id;

    document.getElementById("chat-container").innerHTML += '<p class = "ai-message" >' + data.assistant + '</p>';

    await loadSidebar();
}catch(error){
    console.error(error)
}}