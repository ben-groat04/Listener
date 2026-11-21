"""W4 shared prep P3, stage 2: build .cache/shared/w4-lyrics/feats.pkl and emb.pkl from w4-lyrics/lyrics.jsonl with the Workflow 3 code (features.py feats/text_chunks) and model
(paraphrase-multilingual-MiniLM-L12-v2, max_seq_length 128, mean of normalised chunk embeddings). Records already embedded in the W3 emb.pkl are copied unchanged; only new records are encoded. 1 torch thread."""
import json, pickle, sys, importlib.util, numpy as np
from pathlib import Path
ROOT = Path("/home/user/Listener/taste-model"); W3 = ROOT / "predictors/w3r1-song-content-beyond-audio"; D = ROOT / ".cache/shared/w4-lyrics"; OLD = ROOT / ".cache/shared/w3r1-song-content-beyond-audio-lyrics"
sys.path.insert(0, str(W3)); from features import feats, text_chunks
recs = {}
for l in open(D / "lyrics.jsonl"):
    r = json.loads(l); recs[r["id"]] = r
F = {i: feats(r) for i, r in recs.items()}; pickle.dump(F, open(D / "feats.pkl", "wb")); print("feats", len(F), "with lyrics", sum(v is not None for v in F.values()), flush=True)
E = dict(pickle.load(open(OLD / "emb.pkl", "rb"))); E = {i: v for i, v in E.items() if i in recs}; n_old = len(E)
import torch; torch.set_num_threads(1)
from sentence_transformers import SentenceTransformer
m = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"); m.max_seq_length = 128
todo = [(i, text_chunks(r)) for i, r in recs.items() if i not in E]; print("copied", n_old, "to encode", len(todo), flush=True)
for k in range(0, len(todo), 200):
    b = todo[k:k + 200]; flat = [c for _, ch in b for c in ch]
    V = m.encode(flat, batch_size=64, normalize_embeddings=True, show_progress_bar=False) if flat else np.zeros((0, 384)); j = 0
    for i, ch in b:
        E[i] = V[j:j + len(ch)].mean(0).astype(np.float16) if ch else None; j += len(ch)
    print("emb", len(E), flush=True)
tmp = D / "emb.pkl.tmp"; pickle.dump(E, open(tmp, "wb")); tmp.replace(D / "emb.pkl"); print("done", len(E))
