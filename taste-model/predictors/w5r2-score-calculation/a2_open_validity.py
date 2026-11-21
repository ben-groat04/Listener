"""Validity: (a) open-pool deltas parsed from the harness --fast default run text (decoys), (b) agreement of metrics with pooled sauc on model ranking and key-delta sign (from a1 raw)."""
import re, sys, itertools; sys.path.insert(0, "."); from lib import *
from scipy.stats import spearmanr
TXT = SCR + "/run_default_fast.txt"; L = open(TXT).read().split("\n")
def table(title):
    i = next(k for k, l in enumerate(L) if l.startswith("== [v5.1] TUNE " + title) and (title + " ") not in l[:len("== [v5.1] TUNE ") + len(title) + 1] or l.strip() == "== [v5.1] TUNE " + title)
    j = i + 1; out = []
    while j < len(L) and L[j].strip(): out.append(L[j]); j += 1
    return out
def parse80(title):
    t = table(title); hdr = t[0]; cols = re.findall(r"[A-Za-z_0-9]+", hdr.split("vs ->")[1]); res = {}
    for r in t[1:]:
        name = r.split()[0]; vals = re.findall(r"\(([-0-9.]+), ([-0-9.]+)\)", r)
        # self column is blank, so align by skipping the own-model position
        cc = [c for c in cols if c != name]
        if len(vals) == len(cols) - 1: res[name] = dict(zip(cc, [(float(a), float(b)) for a, b in vals]))
        elif len(vals) == len(cols): res[name] = dict(zip(cols, [(float(a), float(b)) for a, b in vals]))
    return res
print("== OPEN POOL (Spotify-CDN subset; decoys): delta 80% intervals, row minus column")
for title in ("open_dSAUC_80ci", "open_dSAUC_new_80ci", "open_dSAUC_known_80ci", "open_dP20_80ci"):
    R = parse80(title); print("--", title)
    for a, b in [("pair_z", "artist_recent"), ("ref_w4r1_listening", "artist_recent"), ("ref_w4r1_music", "artist_recent"), ("ref_audio_final", "artist_recent"), ("ref_w4r1_listening", "ref_w4r1_music"), ("ref_w4r1_listening", "ref_audio_final"), ("ref_w4r1_music", "ref_audio_final"), ("pair_z", "ref_w4r1_listening"), ("pair_z", "ref_w4r1_music")]:
        iv = R.get(a, {}).get(b); print(f"   {a:20s} - {b:20s}", iv, "" if iv is None else ("POS80" if iv[0] > 0 else "NEG80" if iv[1] < 0 else "undecided"))
# (b) ranking agreement
Z = np.load("results/a1_raw.npz"); IDX = {m: i for i, m in enumerate(MODELS)}
P = {k: Z[k + "__point"] for k in METRICS}
print("\n== Spearman of model ranking (13 models, point values, full TUNE) vs pooled sauc; and on the 7 top models")
TOP = ["artist_plays", "artist_recent", "duration", "ref_audio_final", "ref_w4r1_listening", "ref_w4r1_music", "pair_z"]
for k in METRICS:
    print(f"{k:22s} all13 {spearmanr(P['S1_sauc'], P[k])[0]:+.2f}   top7 {spearmanr(P['S1_sauc'][[IDX[m] for m in TOP]], P[k][[IDX[m] for m in TOP]])[0]:+.2f}")
print("\n== sign of key deltas per metric (z = delta / bootstrap SE)")
KEY = [("pair_z", "artist_recent"), ("ref_w4r1_listening", "artist_recent"), ("ref_w4r1_music", "artist_recent"), ("ref_audio_final", "artist_recent"), ("ref_w4r1_listening", "ref_w4r1_music"), ("ref_w4r1_listening", "ref_audio_final"), ("ref_w4r1_music", "ref_audio_final"), ("pair_z", "ref_w4r1_listening"), ("pair_z", "ref_w4r1_music")]
rows = []
for k in METRICS:
    B = Z[k + "__boot"]; r = {"metric": k}
    for a, b in KEY:
        dd = B[:, IDX[a]] - B[:, IDX[b]]; pt = P[k][IDX[a]] - P[k][IDX[b]]; r[a[:12] + "-" + b[:12]] = f"{pt:+.3f}({pt / dd.std(ddof=1):+.1f})"
    rows.append(r)
pd.set_option("display.width", 320); print(pd.DataFrame(rows).to_string())
