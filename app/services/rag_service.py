from app.services.retriever import Retriever
from app.services.llm_service import LLMService


class RAGService:
    def __init__(self, retriever: Retriever):
        self.retriever = retriever
        self.llm = LLMService()

    def generate_answer(self, query: str):
        """
        Pipeline RAG complet :
        1. Retrieve FAISS
        2. Pas de reranker (offline)
        3. Construction du prompt
        4. Appel LLM
        """

        # 1) Récupération des documents via FAISS
        docs = self.retriever.retrieve(query, base_k=8)

        # 2) Pas de reranker (offline)
        # docs = self.reranker.rerank(query, docs, top_k=4)

        # 3) Construction du contexte
        if docs:
            context = "\n\n".join([f"- {doc['preview']}" for doc in docs])
        else:
            context = "Aucune source pertinente trouvée dans le corpus."

        # 4) Prompt final pour le LLM
        prompt = f"""
Tu es un expert en assurance suisse. Utilise UNIQUEMENT le contexte suivant pour répondre.

Contexte :
{context}

Question :
{query}

Réponse :
"""

        # 5) Appel au LLM
        answer = self.llm.generate(prompt)

        # 6) Retour structuré
        return {
            "answer": answer,
            "sources": docs
        }