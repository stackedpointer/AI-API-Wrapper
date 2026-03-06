console.log("JS LOADED");


let chatId = null;
async function sendData() {
    console.log("BUTTOON CLICKED")
    const input = document.getElementById("userinput").value;

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

    document.getElementById("usermessage").innerHTML += "<p>" + data.user + "</p>";;
    document.getElementById("aimessage").innerHTML += "<p>" + data.assistant + "</p>";
}catch(error){
    console.error(error)
}}