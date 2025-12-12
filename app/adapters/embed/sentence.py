
from sentence_transformers import SentenceTransformer
_model = None

def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")  # 384 dimensions
    return _model

def embed_text(text: str):
    return _get_model().encode(text).tolist()

def embed_many(texts):
    return _get_model().encode(texts)
