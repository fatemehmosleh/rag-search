
import os
from dataclasses import dataclass

@dataclass
class Settings:
    MODEL_NAME: str = os.getenv("OLLAMA_MODEL", "mistral")
    FAISS_INDEX_PATH: str = os.getenv("FAISS_INDEX_PATH", "data/index/faiss.index")
    META_PATH: str = os.getenv("META_PATH", "data/index/meta.jsonl")
    CLEAN_DIR: str = os.getenv("CLEAN_DIR", "data/clean")
    RAW_DIR: str = os.getenv("RAW_DIR", "data/raw")
    WHOOSH_DIR: str = os.getenv("WHOOSH_DIR", "data/index/whoosh")  # optional lexical
