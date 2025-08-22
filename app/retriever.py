import os
import json
from typing import List, Dict, Any, Tuple, Optional
from pathlib import Path
import hashlib

try:
    import faiss  # type: ignore
except Exception:
    faiss = None

try:
    from sentence_transformers import SentenceTransformer  # type: ignore
except Exception:
    SentenceTransformer = None  # type: ignore

from .data import load_employees
from .search import make_profile_text, retrieve as lexical_retrieve

STORE_PATH = Path(__file__).resolve().parent.parent / "store"
EMB_FILE = STORE_PATH / "employees_embeddings.npy"
IDX_FILE = STORE_PATH / "faiss.index"
META_FILE = STORE_PATH / "employees_meta.json"
MODEL_NAME = os.getenv("HR_EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

def _hash_profiles(profiles: List[Dict[str, Any]]) -> str:
    m = hashlib.sha256()
    for p in profiles:
        m.update(json.dumps(p, sort_keys=True).encode("utf-8"))
    return m.hexdigest()

class SemanticRetriever:
    def __init__(self, profiles: Optional[List[Dict[str, Any]]] = None):
        self.mode = "semantic"
        self.model = None
        self.index = None
        self.embeddings = None
        self.meta: List[Dict[str, Any]] = []
        self._profiles = profiles or load_employees()
        self.profile_hash = _hash_profiles(self._profiles)
        self.available = False
        self._init()

    def _init(self) -> None:
        if SentenceTransformer is None or faiss is None:
            self.available = False
            return
        try:
            STORE_PATH.mkdir(parents=True, exist_ok=True)
            if META_FILE.exists():
                meta = json.loads(META_FILE.read_text(encoding="utf-8"))
                if meta.get("profile_hash") == self.profile_hash and IDX_FILE.exists():
                    import numpy as np
                    self.embeddings = np.load(str(EMB_FILE))
                    self.index = faiss.read_index(str(IDX_FILE))
                    self.meta = meta["profiles"]
                    self.model = SentenceTransformer(MODEL_NAME)
                    self.available = True
                    return
            self.model = SentenceTransformer(MODEL_NAME)
            texts = [make_profile_text(p) for p in self._profiles]
            import numpy as np
            self.embeddings = self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
            dim = self.embeddings.shape[1]
            self.index = faiss.IndexFlatIP(dim)
            self.index.add(self.embeddings.astype("float32"))
            faiss.write_index(self.index, str(IDX_FILE))
            np.save(str(EMB_FILE), self.embeddings)
            self.meta = self._profiles
            META_FILE.write_text(json.dumps({"profile_hash": self.profile_hash, "profiles": self.meta}, indent=2), encoding="utf-8")
            self.available = True
        except Exception:
            self.available = False

    def search(self, query: str, top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        if not self.available or self.model is None or self.index is None:
            pairs = lexical_retrieve(query, self._profiles, top_k=top_k)
            return [(emp, 0.5 + min(max(score, 0.0), 1.0) * 0.5) for emp, score in pairs]
        import numpy as np
        q = self.model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
        D, I = self.index.search(q.astype("float32"), top_k * 2)
        results: List[Tuple[Dict[str, Any], float]] = []
        for idx, score in zip(I[0], D[0]):
            if idx == -1:
                continue
            emp = self.meta[idx]
            if score > 0.15:
                results.append((emp, float(score)))
        return results[:top_k]