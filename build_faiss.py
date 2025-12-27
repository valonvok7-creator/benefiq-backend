import numpy as np
import faiss

def main():
    embeddings = np.load("embeddings.npy").astype("float32")

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)

    index.add(embeddings)

    faiss.write_index(index, "faiss.index")

    print("Index FAISS généré avec succès.")

if __name__ == "__main__":
    main()


