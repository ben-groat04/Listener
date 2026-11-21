"""Writes .cache/shared/MANIFEST.txt: every file/dir under .cache/shared (bulk shards and preview audio listed by count/size only; all other files with sha256)."""
import os, hashlib, glob, numpy as np
from pathlib import Path
SH = Path("/home/user/Listener/taste-model/.cache/shared")
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
L = ["# MANIFEST of .cache/shared (written by predictors/w4-shared-prep/make_manifest.py; MANIFEST.txt itself and FROZEN are not listed)", "path | kind | size_bytes | detail | sha256"]
bulk_dirs = {"previews/audio"}
for root, dirs, files in sorted(os.walk(SH)):
    rel = str(Path(root).relative_to(SH)); dirs.sort()
    if rel in bulk_dirs:
        sz = sum((Path(root) / f).stat().st_size for f in files); L.append(f"{rel}/ | dir (bulk) | {sz} | {len(files)} audio files | not hashed"); dirs[:] = []; continue
    shards = [f for f in files if f.startswith("shard_") and f.endswith(".npz")]
    if shards:
        sz = sum((Path(root) / f).stat().st_size for f in shards); L.append(f"{rel}/shard_*.npz | npz shards (bulk) | {sz} | {len(shards)} files | not hashed")
    for f in sorted(files):
        if f in shards or f in ("MANIFEST.txt", "FROZEN"): continue
        p = Path(root) / f; r = str(p.relative_to(SH)); det = ""
        if f.endswith(".jsonl"): det = f"{sum(1 for _ in open(p))} lines"
        elif f.endswith(".csv"): det = f"{sum(1 for _ in open(p)) - 1} rows"
        elif f == "emb.npz": det = f"{len(np.load(p)['k'])} rows"
        L.append(f"{r} | {p.suffix[1:] or 'file'} | {p.stat().st_size} | {det} | {sha(p)}")
(SH / "MANIFEST.txt").write_text("\n".join(L) + "\n"); print(len(L))
