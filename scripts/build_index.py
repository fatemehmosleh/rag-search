
# scripts/build_index.py
import os, json, numpy as np
from app.adapters.vector.faiss_store import FaissStore
from app.adapters.embed.sentence import embed_many

CLEAN_DIR = "data/clean"
INDEX_PATH = "data/index/faiss.index"
META_PATH = "data/index/meta.jsonl"

def load_texts():
    texts, payloads = [], []
    if not os.path.isdir(CLEAN_DIR):
        print(f"Directory not found: {CLEAN_DIR}")
        return texts, payloads
    for name in os.listdir(CLEAN_DIR):
        if not name.endswith(".jsonl"): continue
        path = os.path.join(CLEAN_DIR, name)
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                item = json.loads(line)
                if "text" in item and item["text"].strip():
                    texts.append(item["text"])
                    payloads.append(item)
    return texts, payloads

def main():
    os.makedirs("data/index", exist_ok=True)
    texts, payloads = load_texts()
    if not texts:
        print("No chunks found in data/clean. Run your ingest scripts first.")
        return
    print(f"Embedding {len(texts)} chunks...")
    vecs = embed_many(texts)
    print(f"Writing FAISS index to: {INDEX_PATH}")
    store = FaissStore(index_path=INDEX_PATH, meta_path=META_PATH)
    store.add(np.array(vecs), payloads)
    print(f"✅ Indexed {len(texts)} chunks")
    print(f"   • Index: {INDEX_PATH}")
    print(f"   • Meta:  {META_PATH}")

if __name__ == "__main__":
    main()
