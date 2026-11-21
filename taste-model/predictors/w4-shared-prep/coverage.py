"""Coverage tables (FEATURES.md format) for the W4 shared caches. Usage: python3 coverage.py  -> prints markdown. Groups per fold: train / tried / decoy (main + holdout parts), summed over folds; TUNE = first 10 cutoffs, LATE = last 4."""
import sys, json, pickle, hashlib, glob, numpy as np, pandas as pd
from pathlib import Path
ROOT = Path("/home/user/Listener/taste-model"); SH = ROOT / ".cache/shared"; sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(Path(__file__).parent))
from universe import universe
def groups():
    U, G = universe(True); by = {}
    for g in G:
        d = by.setdefault(g["c"], dict(train=[], tried=[], decoy=[]))
        for k in d: d[k] += list(g[k])
    return U, by
def md5(u): return hashlib.md5(u.encode()).hexdigest() if isinstance(u, str) else None
def table(by, cols):
    from evalkit import data
    cuts = sorted(by); sl = dict(TUNE=cuts[:10], LATE=cuts[10:], ALL=cuts); out = ["| slice | group | tracks (summed over folds) | " + " | ".join(cols) + " |", "|---|---|---|" + "---|" * len(cols)]
    for s, cs in sl.items():
        for g in ("train", "tried", "decoy"):
            ids = [t for c in cs for t in by[c][g]]
            out.append(f"| {s} | {g} | {len(ids)} | " + " | ".join(f"{np.mean([cols[c](t) for t in ids]):.3f}" for c in cols) + " |")
    return "\n".join(out)
if __name__ == "__main__":
    U, by = groups(); from evalkit import data
    meta = data.load_meta_all(); url = meta.previewUrl.to_dict()
    man = pd.read_csv(SH / "previews/manifest.csv"); ok = set(man.md5[man.ok.astype(str) == "True"])
    cuts = sorted(by); print("cutoffs", cuts)
    cols = {}
    cols["has_url"] = lambda t: isinstance(url.get(t), str)
    cols["preview_ok"] = lambda t: md5(url.get(t)) in ok
    for name, d in (("essentia", "w4-essentia"), ("descriptors", "w4-descriptors")):
        keys, failed = set(), set()
        for f in glob.glob(str(SH / d / "shard_*.npz")):
            z = np.load(f); keys |= set(z["md5"]); failed |= set(z["failed"])
        if keys or failed: cols[name] = (lambda keys: lambda t: md5(url.get(t)) in keys)(keys); print(d, "clips", len(keys), "failed", len(failed))
    print("### Audio-derived caches\n" + table(by, cols))
    recs = {}
    for l in open(SH / "w4-lyrics/lyrics.jsonl"):
        r = json.loads(l); recs[r["id"]] = r
    E = pickle.load(open(SH / "w4-lyrics/emb.pkl", "rb")) if (SH / "w4-lyrics/emb.pkl").exists() else {}
    lc = {"lyr_record": lambda t: t in recs, "lyr_found": lambda t: bool(recs.get(t, {}).get("found")), "lyr_emb": lambda t: E.get(t) is not None}
    print("### Lyrics (w4-lyrics)\n" + table(by, lc))
