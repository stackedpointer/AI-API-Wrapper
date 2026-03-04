console.log("JS LOADED");

async function sendData() {
    const input = document.getElementById("userinput").value;

    const response = await fetch("http://127.0.0.1:8000/request", {
        method: "POST", 
        headers: {
        "Content-Type":"application/json"
        },
        body: JSON.stringify({request : input})
    });
    const data = await response.json();
    document.getElementById("usermessage").innerText = data.user;
    document.getElementById("aimessage").innerText = data.assistant;
}