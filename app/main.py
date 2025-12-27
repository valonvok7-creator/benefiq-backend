from fastapi import FastAPI
from dotenv import load_dotenv

# Charge automatiquement le fichier .env au démarrage du backend
load_dotenv()

from app.routes.chat_route import router as chat_router
from app.routes.rag_route import router as rag_router

app = FastAPI(
    title="BenefiQ IA Backend",
    description="Backend FastAPI isolé pour le RAG et le chat",
    version="1.0.0"
)

# On isole toutes les routes sous /benefiq pour éviter les collisions avec Next.js
app.include_router(chat_router, prefix="/benefiq")
app.include_router(rag_router, prefix="/benefiq")

@app.get("/")
def root():
    return {"status": "BenefiQ backend running"}