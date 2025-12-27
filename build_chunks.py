import os
import hashlib
import json

CORPUS_DIR = "corpus_afa"
OUTPUT_FILE = "chunks.json"

def sha256(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def chunk_text(text, chunk_size=800, overlap=200):
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk_text = " ".join(chunk_words)
        chunks.append(chunk_text)
        start += chunk_size - overlap

    return chunks

def main():
    all_chunks = []

    for filename in os.listdir(CORPUS_DIR):
        if not filename.endswith(".txt"):
            continue

        path = os.path.join(CORPUS_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = chunk_text(text)

        for i, c in enumerate(chunks):
            all_chunks.append({
                "file": filename,
                "chunk_id": i,
                "text": c,
                "source_hash": sha256(c)
            })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print(f"Chunks générés : {len(all_chunks)}")
    print(f"Fichier écrit : {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

