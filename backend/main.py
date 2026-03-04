from database import DataBase
from llmclient import LLMCLIENT
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

api_key = os.getenv("OPENAI_API_KEY") 

db = DataBase()
app = FastAPI()
llm = LLMCLIENT(api_key)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"],
)

class RequestData(BaseModel):
    request: str

@app.get("/")
def home():
    return {"message" : "server running"}


@app.post("/request")
async def recieve_messages(data : RequestData):
    print("end point hit")
    print(f"user sent {data.request}")
    result = llm.generate(data.request)

    return{
        "user" : data.request, "assistant" : result
    }


