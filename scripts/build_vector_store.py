import json
import faiss
import numpy as np
from tqdm import tqdm

CHUNKS_FILE = "../chunks.jsonl"
INDEX_FILE = "faiss.index"
META_FILE = "../metadata.jsonl"

# ---------------------------------------------------------
# 1. Embedding model (placeholder — plug your Groq client)
# ---------------------------------------------------------

def embed(text: str) -> np.ndarray:
    # TODO: replace with your Groq embedding call
    # Must return a 1D numpy array
    import hashlib
    h = hashlib.sha256(text.encode()).digest()
    return np.frombuffer(h, dtype=np.uint8).astype("float32")

# ---------------------------------------------------------
# 2. Build vector store
# ---------------------------------------------------------

def main():
    vectors = []
    metadata = []

    with open("../chunks.jsonl", "r", encoding="utf-8") as f:
        for line in tqdm(f, desc="Embedding chunks"):
            record = json.loads(line)
            vec = embed(record["text"])
            vectors.append(vec)
            metadata.append(record)

    vectors = np.vstack(vectors).astype("float32")

    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)

    faiss.write_index(index, INDEX_FILE)

    with open(META_FILE, "w", encoding="utf-8") as f:
        for m in metadata:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")

    print(f"Vector store built:")
    print(f"- {INDEX_FILE}")
    print(f"- {META_FILE}")
    print(f"- {vectors.shape[0]} vectors")

if __name__ == "__main__":
    main()

