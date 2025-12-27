from sentence_transformers import SentenceTransformer
import os, json, numpy as np

CORPUS_DIR = "corpus"
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def load_corpus():
    docs = []
    for filename in os.listdir(CORPUS_DIR):
        if filename.endswith(".txt"):
            with open(os.path.join(CORPUS_DIR, filename), "r", encoding="utf-8") as f:
                docs.append({"id": filename, "text": f.read().strip()})
    return docs

def main():
    docs = load_corpus()
    texts = [d["text"] for d in docs]

    embeddings = model.encode(texts, convert_to_numpy=True)

    np.save("embeddings.npy", embeddings)

    with open("metadata.json", "w", encoding="utf-8") as f:
        json.dump(docs, f, indent=2, ensure_ascii=False)

    print("Embeddings générés avec succès.")

if __name__ == "__main__":
    main()


