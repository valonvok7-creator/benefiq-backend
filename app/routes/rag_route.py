from fastapi import APIRouter
from pydantic import BaseModel
from app.services.rag_service import RAGService
from app.services.retriever import Retriever

router = APIRouter(tags=["RAG"])

class RAGRequest(BaseModel):
    question: str

# Initialisation du retriever
retriever = Retriever(
    "app/data/faiss.index",
    "app/data/metadata.json"
)

rag_service = RAGService(retriever)

@router.post("/rag")
def rag_endpoint(payload: RAGRequest):
    return rag_service.generate_answer(payload.question)

