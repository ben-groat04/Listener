"""Builds CACHE/feats.pkl (id -> lyric stats dict) and CACHE/emb.pkl (id -> 384d multilingual MiniLM mean-of-chunks embedding). Resumable per stage."""
import json, pickle, sys, numpy as np
from common import *
from features import feats, text_chunks
recs = {}
for l in open(CACHE / "lyrics.jsonl"):
    r = json.loads(l); recs[r["id"]] = r
F = {i: feats(r) for i, r in recs.items()}
pickle.dump(F, open(CACHE / "feats.pkl", "wb"))
print("feats", len(F), "with lyrics", sum(v is not None for v in F.values()))
if "--emb" in sys.argv:
    import torch; torch.set_num_threads(2)
    from sentence_transformers import SentenceTransformer
    m = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"); m.max_seq_length = 128
    p = CACHE / "emb.pkl"; E = pickle.load(open(p, "rb")) if p.exists() else {}
    todo = [(i, text_chunks(r)) for i, r in recs.items() if i not in E]
    for k in range(0, len(todo), 200):
        b = todo[k:k + 200]; flat = [c for _, ch in b for c in ch]
        V = m.encode(flat, batch_size=64, normalize_embeddings=True, show_progress_bar=False) if flat else np.zeros((0, 384)); j = 0
        for i, ch in b:
            E[i] = V[j:j + len(ch)].mean(0).astype(np.float16) if ch else None; j += len(ch)
        pickle.dump(E, open(p, "wb")); print("emb", len(E), flush=True)
