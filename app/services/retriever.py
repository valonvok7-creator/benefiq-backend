import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer


class Retriever:
    def __init__(self, index_path: str, metadata_path: str):
        self.index = faiss.read_index(index_path)

        with open(metadata_path, "r") as f:
            self.metadata = json.load(f)

        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        self.embedding_dim = self.index.d
        self.max_distance = 1.2

    def embed(self, text: str) -> np.ndarray:
        emb = self.model.encode(text, normalize_embeddings=True)
        return emb.astype("float32")

    def retrieve(self, query: str, base_k: int = 5):
        q_emb = self.embed(query)
        q_emb = np.expand_dims(q_emb, axis=0)

        distances, indices = self.index.search(q_emb, base_k)

        distances = distances[0]
        indices = indices[0]

        results = []

        for dist, idx in zip(distances, indices):

            if dist > self.max_distance:
                continue

            # SUPPORT METADATA LIST
            item = None
            if isinstance(self.metadata, list):
                if 0 <= idx < len(self.metadata):
                    item = self.metadata[idx]
            else:
                item = self.metadata.get(str(idx))

            if item:
                results.append({
                    "distance": float(dist),
                    "id": item.get("id"),
                    "preview": item.get("preview")
                })

        if len(results) >= 3:
            return results[:3]
        elif len(results) == 2:
            return results[:2]
        elif len(results) == 1:
            return results[:1]
        else:
            return []
