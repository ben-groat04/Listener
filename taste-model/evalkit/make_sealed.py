"""Regenerate the sealed holdout labels deterministically:  python -m evalkit.make_sealed
Writes .sealed/labels.csv (git-ignored, do not read) and checks it against the committed sealed_manifest.json."""
import sys, json, hashlib
import pandas as pd
from . import data

MANIFEST = data.ROOT / "evalkit" / "sealed_manifest.json"

def build():
    folds = [f.assign(fold=str(c.date())) for c, f in data.make_folds(data.SEALED_CUTOFFS)]
    df = pd.concat(folds)[["fold", "song", "trackId", "love", "strong", "plays90", "days90", "new_artist"]]
    return df.sort_values(["fold", "song"]).reset_index(drop=True)

def main(write_manifest=False):
    df = build(); data.SEALED_DIR.mkdir(exist_ok=True)
    csv = df.to_csv(index=False); (data.SEALED_DIR / "labels.csv").write_text(csv)
    info = dict(sha256=hashlib.sha256(csv.encode()).hexdigest(), n_songs=len(df), per_fold=df.groupby("fold").size().to_dict())
    # open-universe pool: hash of the decoy universe file plus the exact decoy ids drawn per sealed fold
    dec = []
    for c, pool in data.make_open_folds(data.SEALED_CUTOFFS):
        dec += [f"{c.date()}:{t}" for t in sorted(pool[pool.is_decoy == 1].trackId)]
    info["decoy_universe_sha256"] = hashlib.sha256(data.DECOYS.read_bytes()).hexdigest()
    info["decoys_drawn_sha256"] = hashlib.sha256("\n".join(dec).encode()).hexdigest(); info["n_decoys"] = len(dec)
    if write_manifest: MANIFEST.write_text(json.dumps(info, indent=1))
    m = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else None
    ok = (m is not None and all(m.get(k) == info[k] for k in ("sha256", "decoys_drawn_sha256"))) if m else None
    print(info["n_songs"], "sealed songs; matches manifest:", ok); return ok

if __name__ == "__main__": main("--write-manifest" in sys.argv)
