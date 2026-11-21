import sys; sys.path.insert(0, "."); from lib import *
from scipy.stats import spearmanr, kendalltau
Z = np.load("results/a1_raw.npz"); ks = list(METRICS)
IDX = {m: i for i, m in enumerate(MODELS)}
KEY = [("pair_z","artist_recent"),("ref_w4r1_listening","artist_recent"),("ref_w4r1_music","artist_recent"),("ref_audio_final","artist_recent"),
       ("ref_w4r1_listening","ref_w4r1_music"),("ref_w4r1_listening","ref_audio_final"),("ref_w4r1_music","ref_audio_final"),("pair_z","ref_w4r1_listening"),("pair_z","ref_w4r1_music")]
TOP = ["artist_plays","artist_recent","duration","ref_audio_final","ref_w4r1_listening","ref_w4r1_music","pair_z"]
allp = [(a, b) for a, b in itertools.combinations(MODELS, 2)] if False else None
import itertools
allp = list(itertools.combinations(MODELS, 2))
def dl(M, a, b): return M[..., IDX[a]] - M[..., IDX[b]]
rows = []
for k in ks:
    P = Z[k + "__point"]; B = Z[k + "__boot"]; H = Z[k + "__half"]
    r = dict(metric=k)
    # rank agreement between halves (all 13 models; top-7)
    for nm, sub in (("all13", MODELS), ("top7", TOP)):
        ii = [IDX[m] for m in sub]; rs = [spearmanr(H[s, 0, ii], H[s, 1, ii])[0] for s in range(len(H))]; r["halfrank_" + nm] = np.nanmean(rs)
    # delta agreement (all 78 pairs): correlation of half-deltas and sign agreement among top-7 pairs
    top_pairs = list(itertools.combinations(TOP, 2))
    cs = []; sg = []; sg_key = []
    for s in range(len(H)):
        da = np.array([dl(H[s, 0], a, b) for a, b in allp]); db = np.array([dl(H[s, 1], a, b) for a, b in allp]); cs.append(np.corrcoef(da, db)[0, 1])
        ta = np.array([dl(H[s, 0], a, b) for a, b in top_pairs]); tb = np.array([dl(H[s, 1], a, b) for a, b in top_pairs]); sg.append(np.mean(np.sign(ta) == np.sign(tb)))
        ka = np.array([dl(H[s, 0], a, b) for a, b in KEY]); kb = np.array([dl(H[s, 1], a, b) for a, b in KEY]); sg_key.append(np.mean(np.sign(ka) == np.sign(kb)))
    r["half_deltacorr_78pairs"] = np.mean(cs); r["half_signagree_top7pairs"] = np.mean(sg); r["half_signagree_keypairs"] = np.mean(sg_key)
    # bootstrap discriminability: |delta|/SE for the 21 top pairs; share of top pairs with 80% interval excluding 0 (and excluding +-0.005 scaled by metric SD of models)
    z = []; dec = []
    for a, b in top_pairs:
        dd = dl(B, a, b); se = dd.std(ddof=1); pt = dl(P, a, b); z.append(abs(pt) / se); dec.append((np.percentile(dd, 10) > 0) or (np.percentile(dd, 90) < 0))
    r["median_abs_z_top21"] = np.median(z); r["share_decided80_top21"] = np.mean(dec)
    zk = []; 
    for a, b in KEY: dd = dl(B, a, b); zk.append(dl(P, a, b) / dd.std(ddof=1))
    r["key_z"] = " ".join(f"{x:+.2f}" for x in zk)
    # spread of models (SD of metric over TOP) / mean SE
    se_m = B[:, [IDX[m] for m in TOP]].std(0, ddof=1); r["spread_over_se_top7"] = P[[IDX[m] for m in TOP]].std() / se_m.mean()
    rows.append(r)
out = pd.DataFrame(rows); out.to_csv("results/a1_summary.csv", index=False); pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
print(out.drop(columns="key_z").round(3).to_string()); print(out[["metric", "key_z"]].to_string())
