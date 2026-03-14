from database import DataBase
from typing import Optional
from llmclient import LLMCLIENT
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

api_key = os.getenv("OPENAI_API_KEY") 

db = DataBase()
app = FastAPI()
llm = LLMCLIENT(api_key)

app.mount("/static", StaticFiles(directory="static"), name = "static")

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"],
)

class RequestData(BaseModel):
    request: str
    chat_id: Optional[int] = None
class TitleRequest(BaseModel):
    title: str

def generate_title(message):
    words = message.split()
    title = " ".join(words[:5])
    return title

@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.get("/chats")
def get_chats():
    chats = db.load_all()
    chat = []
    for c in chats:
        chat.append({"id":c[0], "title":c[1]})
    return chat
@app.get("/chats/{chat_id}")
def get_chat(chat_id: int):
    messages = db.load(chat_id)
    message = []
    for r,c in messages:
        message.append({"role": r, "content":c})
    return message

@app.post("/title")
def receive_titles(data : TitleRequest):
    chat_id = db.get_id(data.title)
    return {"chat_id":chat_id}

@app.post("/request")
async def receive_messages(data : RequestData):
    chat_id = data.chat_id
    user_message = data.request

    if chat_id is None:
        title = generate_title(user_message)
        chat_id = db.get_id(title)
    db.storeUser(chat_id, user_message)

    history = db.load(chat_id)
    messages = []
    for role, content in history:
        messages.append({"role" :role, "content":content})

    print("end point hit")
    print(data.model_dump())
    print(f"user sent {user_message}")
    result = llm.generate(messages)

    db.storeAI(chat_id, result)
    print("AI RESULT:", result)

    return{
        "chat_id":chat_id,
        "user" : data.request,
        "assistant" : result
    }

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )


