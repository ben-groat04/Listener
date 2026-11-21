"""Frame-study library: metrics on a score dump (evalkit v5.0 dump) with shared artist-cluster bootstrap. Uses evalkit.metrics.Block / group_auc."""
import sys, numpy as np, pandas as pd
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from evalkit import metrics as M
SCR = Path("/tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf5/builder-r1-eval-frame-folds")
OUT = Path(__file__).resolve().parent / "results"
BASE = ["popularity", "artist_plays", "artist_recent", "artist_love_rate", "duration", "meta_gbm", "nonaudio_gbm"]
REFS = ["ref_audio_final", "ref_w4r1_listening", "ref_w4r1_music"]
STACK = ["w5r1_stack3", "w5r1_stack2_content"]
MODELS = BASE + REFS + STACK
REFROWS = ["nonaudio_gbm", "artist_recent", "duration", "meta_gbm"] + REFS     # harness best_ref candidates (7 reference rows)
FIXED_BEST = "ref_w4r1_listening"

def dump(name="dump_all.pkl"): return pd.read_pickle(SCR / name)

def qlabel(month): return (month.str[:4] + "Q" + ((month.str[5:7].astype(int) - 1) // 3 + 1).astype(str)).values
def hlabel(month): return (month.str[:4] + "H" + ((month.str[5:7].astype(int) - 1) // 6 + 1).astype(str)).values

def frame(d, fold_set, group="fold", label="love", exp=None):
    g = d[d.fold_set == fold_set].reset_index(drop=True)
    fold = {"fold": g.fold.astype(str).values, "quarter": qlabel(g.month), "half": hlabel(g.month), "year": g.month.str[:4].values, "all": np.zeros(len(g), int).astype(str)}[group]
    lab = g[label] if isinstance(label, str) else label(g)
    return g.assign(fold=fold, is_decoy=0, exp_before=(g.exposure_before if exp is None else exp(g)).astype(float), _lab=np.asarray(lab).astype(int))

def block(g, nboot=300, seed=0, edges=None):
    B = M.Block(g, "_lab", nboot, seed)
    if edges is not None:   # alternative exposure-bucket edges for wx: bucket = number of edges <= e  (edges ascending, e.g. (1,3,9))
        e = g.exp_before.values; b = np.searchsorted(np.asarray(edges), e, side="right")
        B.wx = pd.factorize(pd.Series(B.fold_key if hasattr(B, "fold_key") else g.fold.astype(str).values) + "|" + pd.Series(b).astype(str).values)[0]
    return B

def evaluate(g, models, nboot=300, seed=0, edges=None, which=("sauc", "macro", "wa", "wx"), new=True):
    """-> {model: {metric: (point, boot array)}}; metric 'new' = sauc on rows with new_artist (own fold pairing)."""
    B = block(g, nboot, seed, edges); nm = g.new_artist.values.astype(bool); Bn = B.sub(nm) if new else None; res = {}
    for m in models:
        s = g["score__" + m].values; st = B.stats(s, True, which); r = {k: (float(st[k][0]), st[k + "_b"]) for k in which}
        if new: sn = Bn.stats(s, True, ("sauc",)); r["new"] = (float(sn["sauc"][0]), sn["sauc_b"])
        res[m] = r
    return res

def best_ref(res, metric="sauc", pool=REFROWS): return max(pool, key=lambda m: res[m][metric][0])

def delta(res, a, b, metric="sauc"):
    pa, ba = res[a][metric]; pb, bb = res[b][metric]; x = ba - bb; f = x[np.isfinite(x)]
    return dict(d=pa - pb, lo80=float(np.percentile(f, 10)), hi80=float(np.percentile(f, 90)), P=float(np.mean(f > 0)), lo95=float(np.percentile(f, 2.5)))

def hw80(res, m, metric="sauc"):
    b = res[m][metric][1]; b = b[np.isfinite(b)]; return float((np.percentile(b, 90) - np.percentile(b, 10)) / 2)

def kendall(x, y):
    from scipy.stats import kendalltau
    return float(kendalltau(x, y)[0])

def groupstats(g, s, W=None, groupcol="fold"):
    """per-group (num, den) with W (B,n) or point (W=None)."""
    y = g._lab.values.astype(int); gr = g[groupcol].values
    W = np.ones((1, len(y))) if W is None else W
    gval, num, den = M.group_auc(y, np.asarray(s, float), gr, W); return gval, num, den

def boot_W(g, nboot=300, seed=0):
    cl, _ = pd.factorize(g.artist.values); n = cl.max() + 1; rng = np.random.default_rng(seed)
    C = rng.multinomial(n, np.full(n, 1.0 / n), size=nboot).astype(float); return C[:, cl]
