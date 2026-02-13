# Mini RAG – Pennylane Help Center (HTML Intercom/Next.js)

## Objectif
- Parser des pages HTML exportées (Intercom/Next.js) et extraire: title, main_text, source_url (canonical).
- Chunker le texte, indexer avec embeddings + FAISS.
- Permettre de poser une question en CLI: retrieval top-k + génération + sources.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt