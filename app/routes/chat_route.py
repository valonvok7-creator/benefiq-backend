from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from groq import Groq

router = APIRouter()
client = Groq()

# Le modèle accepte message ET question
class ChatRequest(BaseModel):
    message: Optional[str] = None
    question: Optional[str] = None

    @property
    def text(self) -> str:
        # On unifie les deux champs
        return self.message or self.question or ""

@router.post("/chat")
def chat_endpoint(payload: ChatRequest):
    user_input = payload.text

    # Sécurité : aucun champ envoyé
    if not user_input:
        return {"answer": "Je n'ai reçu ni 'message' ni 'question'."}

    # Appel Groq
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": user_input}]
    )

    return {"answer": completion.choices[0].message.content}

