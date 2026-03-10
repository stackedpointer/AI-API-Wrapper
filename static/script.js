console.log("JS LOADED");


let chatId = null;
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
}catch(error){
    console.error(error)
}}