import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


def build_faiss(metadata_path: str, index_path: str):
    print(">>> Script FAISS lancé")

    # Charger les chunks
    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    print(f">>> {len(metadata)} chunks chargés depuis {metadata_path}")

    # Embeddings cohérents avec ton retriever
    embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    texts = [item["text"] for item in metadata]
    embeddings = embedder.encode(texts, convert_to_numpy=True).astype("float32")

    print(f">>> Embeddings shape: {embeddings.shape}")

    # Création de l'index FAISS
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    # Sauvegarde
    faiss.write_index(index, index_path)

    print(f">>> FAISS reconstruit avec {len(texts)} embeddings.")
    print(f">>> Index sauvegardé dans {index_path}")


if __name__ == "__main__":
    build_faiss("metadata.json", "faiss.index")

