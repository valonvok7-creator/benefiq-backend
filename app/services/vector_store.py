import faiss
import json
import numpy as np

class VectorStore:
    def __init__(self, index_path: str, metadata_path: str):
        self.index = faiss.read_index(index_path)

        with open(metadata_path, "r") as f:
            self.metadata = json.load(f)

    def search(self, embedding, k=5):
        embedding = np.array([embedding]).astype("float32")
        distances, indices = self.index.search(embedding, k)

        results = []
        for idx in indices[0]:
            if idx == -1:
                continue
            results.append(self.metadata[idx])
        return results

