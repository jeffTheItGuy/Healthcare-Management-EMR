import os
import numpy as np
from functools import lru_cache
from sentence_transformers import SentenceTransformer

_model = None

def _load_model():
    global _model
    if _model is None:
        model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        device = os.getenv("EMBEDDING_DEVICE", "cpu")
        _model = SentenceTransformer(model_name, device=device)
    return _model

@lru_cache(maxsize=1024)
def get_embedding(text: str) -> np.ndarray:
    """Generate a 384-dim embedding using a local CPU model."""
    model = _load_model()
    return model.encode(text, normalize_embeddings=True)