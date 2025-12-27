import os
import json
import tiktoken

# Tokenizer compatible OpenAI
tokenizer = tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text))


def chunk_text(text: str, max_tokens: int = 300):
    """
    Découpe un texte en chunks de max_tokens,
    en respectant les paragraphes et la logique.
    """
    paragraphs = text.split("\n")
    chunks = []
    current = ""

    for p in paragraphs:
        if not p.strip():
            continue

        if count_tokens(current + p) < max_tokens:
            current += p + "\n"
        else:
            chunks.append(current.strip())
            current = p + "\n"

    if current.strip():
        chunks.append(current.strip())

    return chunks


def process_folder(input_folder: str, output_file: str):
    """
    Transforme tous les fichiers .txt du dossier en chunks premium.
    """
    all_chunks = []
    file_id = 0

    for filename in os.listdir(input_folder):
        if not filename.endswith(".txt"):
            continue

        path = os.path.join(input_folder, filename)

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = chunk_text(text)

        for c in chunks:
            all_chunks.append({
                "id": f"{filename}__chunk_{file_id}",
                "text": c
            })
            file_id += 1

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)

    print(f"Chunking terminé : {len(all_chunks)} chunks générés.")

if __name__ == "__main__":
    process_folder("corpus", "metadata.json")

