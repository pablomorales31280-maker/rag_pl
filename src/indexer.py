import faiss
import numpy as np

def build_faiss_index(vectors: np.ndarray) -> faiss.Index:
    """
    Cosine similarity:
    - normalise les embeddings
    - utilise IndexFlatIP (inner product)
    """
    dim = vectors.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(vectors)
    return index