from fastapi import APIRouter
from pydantic import BaseModel
from app.services.rag import answer_with_rag

router = APIRouter()

class ChatQuery(BaseModel):
    message: str

@router.post("/chat")
def chat_endpoint(payload: ChatQuery):
    answer, sources = answer_with_rag(payload.message)
    return {
        "message": payload.message,
        "answer": answer,
        "sources": sources
    }

