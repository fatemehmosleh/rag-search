
import faiss
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "data" / "index" / "faiss.index"

idx = faiss.read_index(str(INDEX_PATH))
print("✅ Vectors in index:", idx.ntotal)
print("✅ Embedding dimension:", idx.d)
