import os
import json

import faiss

from src.config import SETTINGS
from src.chunking import chunk_text
from src.embedder import Embedder
from src.indexer import build_faiss_index

def main():
    os.makedirs("index", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    # Charger les documents nettoyés
    documents = []
    with open(SETTINGS.documents_path, "r", encoding="utf-8") as f:
        for line in f:
            documents.append(json.loads(line))

    # Chunking + préparation métadonnées
    chunks = []
    metadatas = []

    for doc_id, doc in enumerate(documents):
        parts = chunk_text(
            doc["main_text"],
            chunk_size=SETTINGS.chunk_size_chars,
            overlap=SETTINGS.chunk_overlap_chars,
        )

        for i, part in enumerate(parts):
            chunks.append(part)
            metadatas.append({
                "doc_id": doc_id,
                "chunk_id": i,
                "title": doc["title"],
                "source_url": doc.get("source_url"),
                "source_file": doc["source_file"],
                "category": doc.get("category"),
            })

    # Sauver chunks
    with open(SETTINGS.chunks_path, "w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps({"text": c}, ensure_ascii=False) + "\n")

    # Embeddings
    embedder = Embedder(SETTINGS.embedding_model_name)
    vectors = embedder.encode(chunks)

    # FAISS
    index = build_faiss_index(vectors)
    faiss.write_index(index, SETTINGS.faiss_index_path)

    # Sauver métadonnées alignées sur l’ordre FAISS
    with open(SETTINGS.metadatas_path, "w", encoding="utf-8") as f:
        for md in metadatas:
            f.write(json.dumps(md, ensure_ascii=False) + "\n")

    print(f"OK -> {SETTINGS.faiss_index_path} (+ {len(chunks)} chunks)")

if __name__ == "__main__":
    main()
