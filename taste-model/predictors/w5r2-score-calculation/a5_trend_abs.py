"""Per-fold composition and absolute-AUC trend of single models (global artist bootstrap), to see which side of the delta trend moves."""
import sys; sys.path.insert(0, "."); import lib; from lib import *
if len(sys.argv) > 1: lib.DUMP = sys.argv[1]
d = load("tune"); folds = sorted(d.fold.unique()); NB = 300
comp = d.groupby("fold").agg(n=("love", "size"), loved=("love", "sum"), love_rate=("love", "mean"), new_artist=("new_artist", "mean"), med_plays90=("plays90", "median")).round(3)
hist = {}
print(comp.to_string())
cols = ["artist_recent", "artist_plays", "ref_audio_final", "ref_w4r1_listening", "ref_w4r1_music", "pair_z", "pairz_trunc12", "pool_artist_siblings", "duration"]
rng = np.random.default_rng(11); cut = pd.to_datetime(d.groupby("fold").cutoff.first().reindex(folds)).values; x = cut.astype("datetime64[D]").astype(float) / 365.25
def fa(dd):
    A = np.full((len(folds), len(cols)), np.nan)
    for i, f in enumerate(folds):
        m = dd.fold.values == f; y = dd.love.values[m]; n1 = y.sum(); n0 = len(y) - n1
        if n1 < 5 or n0 < 5: continue
        for j, c in enumerate(cols): r = rankdata(dd["score__" + c].values[m]); A[i, j] = (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
    return A
A0 = fa(d); Bs = np.array([fa(d.iloc[artist_resample(d, rng)].reset_index(drop=True)) for _ in range(NB)])
ok = np.isfinite(A0).all(1)
def trend(A, w): xb = (w * x[ok]).sum() / w.sum(); return (w * (x[ok] - xb) * A[ok]).sum() / (w * (x[ok] - xb) ** 2).sum()
print("eligible folds", ok.sum(), "of", len(folds))
print(pd.DataFrame(A0, index=[str(c)[:7] for c in cut], columns=cols).round(3).to_string())
for j, c in enumerate(cols):
    se = np.nanstd(Bs[:, ok, j], 0, ddof=1); w = 1 / se ** 2; t0 = trend(A0[:, j], w); tb = [trend(np.where(np.isfinite(Bs[i, :, j]), Bs[i, :, j], A0[:, j]), w) for i in range(NB)]  # a fold with <5 of a class in a resample keeps its point value
    print(f"{c:22s} abs-AUC trend/yr (IV weighted) {t0:+.3f}  80% [{np.percentile(tb,10):+.3f},{np.percentile(tb,90):+.3f}]")
