"""Equivalence check: re-extract N existing dev preview clips with catalogue.w6_mert and compare to the cached rows (.cache/shared/w3r1-mert-v1). Writes DIR/equivalence_check.json.
    python3 -W ignore -m catalogue.w6_equiv [N=20]"""
import sys, glob, json, numpy as np, pandas as pd
sys.path.insert(0, "/home/user/Listener/taste-model")
from catalogue.w6_mert import Extractor
from evalkit import data
R = data.ROOT / ".cache"; D = R / "shared-w6r1"
n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
cache = {}
for f in sorted(glob.glob(str(R / "shared/w3r1-mert-v1/shard_*.npz")))[:3]:
    z = np.load(f); cache.update(zip(z["md5"], z["feat"]))
man = pd.read_csv(R / "shared/previews/manifest.csv"); man = man[man.ok.astype(bool) & man.md5.isin(cache)]
sm = man.sample(n, random_state=0); ex = Extractor(); mx, rel, exact = 0, 0, 0
for _, r in sm.iterrows():
    a = ex(R / f"shared/previews/audio/{r.md5}.{r.ext}").astype(np.float32); b = cache[r.md5].astype(np.float32)
    assert np.isfinite(a).all() and a.shape == b.shape == (4, 12, 768)
    d = np.abs(a - b).max(); mx = max(mx, float(d)); rel = max(rel, float(np.linalg.norm(a - b) / np.linalg.norm(b))); exact += int(d == 0)
res = dict(n=n, max_abs_diff=mx, max_rel_l2=rel, n_bitwise_equal=exact, tolerance="max rel L2 <= 1e-2 per clip (fp16 storage, int8 dynamic quantisation)", passed=bool(rel <= 1e-2))
D.mkdir(parents=True, exist_ok=True); json.dump(res, open(D / "equivalence_check.json", "w"), indent=1); print(res)
