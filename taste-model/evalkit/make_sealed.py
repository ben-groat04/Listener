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
    if write_manifest: MANIFEST.write_text(json.dumps(info, indent=1))
    ok = json.loads(MANIFEST.read_text())["sha256"] == info["sha256"] if MANIFEST.exists() else None
    print(info["n_songs"], "sealed songs; matches manifest:", ok); return ok

if __name__ == "__main__": main("--write-manifest" in sys.argv)
