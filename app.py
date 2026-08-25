from fastapi import FastAPI, Request
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
class ChatRequest(BaseModel):
    prompt: str

@app.get("/")
async def root():
    return {"message": "Navi AI Backend is running. The chat API is at /chat"}

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    is_factual, refusal_response = analyze_intent(req.prompt)
    
    if not is_factual:
        return {"response": refusal_response, "is_factual": False}
    
    answer = generate_answer(req.prompt)
    return {"response": answer, "is_factual": True}
