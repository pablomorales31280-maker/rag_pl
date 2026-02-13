import json
import argparse

import faiss

from src.config import SETTINGS
from src.embedder import Embedder
from src.rag_answer import Generator

def load_jsonl(path: str) -> list[dict]:
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            rows.append(json.loads(line))
    return rows

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", "--question", dest="question", required=True)
    parser.add_argument("--k", type=int, default=SETTINGS.top_k)
    args = parser.parse_args()

    question = args.question
    top_k = args.k

    # Charger index FAISS + metadatas + chunks
    index = faiss.read_index(SETTINGS.faiss_index_path)
    metadatas = load_jsonl(SETTINGS.metadatas_path)
    chunks = [row["text"] for row in load_jsonl(SETTINGS.chunks_path)]

    # Embedding de la question
    embedder = Embedder(SETTINGS.embedding_model_name)
    q_vec = embedder.encode([question])

    # Recherche top-k
    scores, ids = index.search(q_vec, top_k)
    ids = ids[0].tolist()
    scores = scores[0].tolist()

    retrieved = []
    print("\n=== PASSAGES RETROUVÉS (top-k) ===\n")
    for rank, (idx, score) in enumerate(zip(ids, scores), start=1):
        md = metadatas[idx]
        text = chunks[idx]

        source = md["source_url"] or md["source_file"]

        print(f"[{rank}] score={score:.4f} | title={md['title']}")
        print(f"    source={source}")
        if md.get("category"):
            print(f"    category={md['category']}")
        print("    excerpt=" + (text[:280].replace("\n", " ") + ("..." if len(text) > 280 else "")))
        print()

        retrieved.append(text)

    # Génération
    gen = Generator(SETTINGS.generator_model_name, SETTINGS.max_new_tokens)
    answer = gen.answer(question, retrieved)

    # Afficher réponse + sources
    print("\n=== RÉPONSE (basée sur le contexte) ===\n")
    print(answer)

    print("\n=== SOURCES UTILISÉES ===\n")
    seen = set()
    for idx in ids:
        md = metadatas[idx]
        source = md["source_url"] or md["source_file"]
        if source not in seen:
            print("-", source)
            seen.add(source)

if __name__ == "__main__":
    main()
