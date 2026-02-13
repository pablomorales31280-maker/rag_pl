from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    # Dossiers
    raw_zip_path: str = "data/raw/help.pennylane.com.zip"
    documents_path: str = "data/processed/documents.jsonl"
    chunks_path: str = "data/processed/chunks.jsonl"

    faiss_index_path: str = "index/faiss.index"
    metadatas_path: str = "index/metadatas.jsonl"

    # Chunking
    chunk_size_chars: int = 1200
    chunk_overlap_chars: int = 200

    # Retrieval
    top_k: int = 5

    # Embeddings (SentenceTransformers)
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Génération (Transformers)
    generator_model_name: str = "google/flan-t5-base"
    max_new_tokens: int = 200

SETTINGS = Settings()