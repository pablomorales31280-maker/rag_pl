# Mini RAG (Retrieval-Augmented Generation) sur un corpus HTML (Help Center)

Ce projet met en place un mini pipeline RAG à partir d’un ZIP contenant des pages HTML exportées (format help center Intercom / Next.js).

Objectifs :
1) Parser et nettoyer les fichiers HTML du ZIP pour extraire uniquement le contenu utile.
2) Découper le texte en chunks.
3) Créer des embeddings, indexer avec FAISS.
4) Permettre de poser une question en CLI : récupérer les passages pertinents (top-k), générer une réponse basée sur le contexte, afficher les sources.

---

## Pré-requis

- Python 3.10+ recommandé
- Accès Internet au premier lancement (téléchargement des modèles HuggingFace)

---


## Installation

Créer un environnement virtuel et installer les dépendances : (avec conda pour ma part)
conda create -n rag_pl python=3.11
cd "path"
pip install -r requirements.txt

---


## Utilisation

Le ZIP est déjà dans data/raw
Parsing / nettoyage HTML : 

python -m scripts.build_corpus

Chunking + indexation

python -m scripts.build_index

Question / Réponse :

python -m scripts.ask --q "My question" --k 5