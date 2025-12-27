class RerankerService:
    def __init__(self):
        # Pas de modèle HuggingFace (offline)
        pass

    def rerank(self, query: str, docs: list, top_k: int = 4):
        # Si pas de docs → rien à reranker
        if not docs:
            return []

        # Reranking simple : on garde l’ordre FAISS
        return docs[:top_k]

