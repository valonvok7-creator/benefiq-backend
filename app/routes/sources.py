from fastapi import APIRouter
from pydantic import BaseModel
from app.services.rag import answer_with_rag

router = APIRouter()

class Query(BaseModel):
    question: str

@router.post("/sources")
def sources_endpoint(payload: Query):
    _, sources = answer_with_rag(payload.question)
    return {"sources": sources}

