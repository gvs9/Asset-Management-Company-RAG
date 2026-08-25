from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from src.query_router import analyze_intent
from src.rag_pipeline import generate_answer

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for Vercel deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")

class ChatRequest(BaseModel):
    prompt: str

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    is_factual, refusal_response = analyze_intent(req.prompt)
    
    if not is_factual:
        return {"response": refusal_response, "is_factual": False}
    
    answer = generate_answer(req.prompt)
    return {"response": answer, "is_factual": True}
