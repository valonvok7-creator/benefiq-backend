import json
import os

INDEX_FILE = "index.json"
CHUNKS_FILE = "../chunks.jsonl"
METADATA_FILE = "../metadata.jsonl"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

def chunk_text(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start += size - overlap
    return chunks

def main():
    # Charger l'index
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        index = json.load(f)

    all_chunks = []
    metadata = []

    for file_info in index:
        path = file_info["path"]

        if not os.path.exists(path):
            print(f"❌ Missing file: {path}")
            continue

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        chunks = chunk_text(content)

        for i, chunk in enumerate(chunks):
            all_chunks.append(json.dumps({"text": chunk}, ensure_ascii=False))
            metadata.append(json.dumps({
                "file": path,
                "chunk_id": i
            }, ensure_ascii=False))

    # Écrire les chunks
    with open(CHUNKS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(all_chunks))

    # Écrire les métadonnées
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(metadata))

    print("Chunks generated in chunks.jsonl")

if __name__ == "__main__":
    main()


