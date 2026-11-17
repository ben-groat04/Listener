"""Music-picture relationship (video-agnostic): cut alignment to beats/bars/section boundaries, cut rate vs loudness,
visual motion vs musical onset strength, brightness vs spectral brightness (with lag search), per auto-section.
Usage: VID=<video> python 09_sync.py [--grid grid.json] [--bar-s 2.0] [--out sync] [--perm 5000]   (or --vid <video>)
VID is mandatory (no default). --grid: beat-grid override, a JSON list of beat times in s, or {"beats_s": [...], "downbeat_index": i}
(default: audio_features/beat_times.json). --bar-s: bar length in s; bars = every round(bar_s / beat period)-th grid beat starting at
downbeat_index (default: every 4th beat from the first). --out: output stem (default 'sync' -> sync.json/sync.png; use another to keep sync.json).
Output: v1/data/<VID>/sync/<out>.json + <out>.png"""
import json, os, sys, argparse
import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
ap = argparse.ArgumentParser(); ap.add_argument("--vid"); ap.add_argument("--grid"); ap.add_argument("--bar-s", type=float); ap.add_argument("--out", default="sync"); ap.add_argument("--perm", type=int, default=5000)
args = ap.parse_args(); VID = args.vid or os.environ.get("VID")
if not VID: sys.exit("09_sync.py: VID is mandatory (set env VID=<video> or pass --vid); there is no default video.")
GRID = args.grid or os.environ.get("GRID_JSON"); OUT = args.out; D = os.path.join(root, f"v1/data/{VID}"); O = os.path.join(D, "sync"); os.makedirs(O, exist_ok=True)
af = json.load(open(f"{D}/audio_features/summary.json")); _g = json.load(open(GRID or f"{D}/audio_features/beat_times.json")); dbi = 0
if isinstance(_g, dict): dbi = int(_g.get("downbeat_index", 0)); _g = _g["beats_s"]
beats = np.array(_g, dtype=float)
vf = json.load(open(f"{D}/visual_features/per_second.json")); shots = json.load(open(f"{D}/scenes/shots.json"))
cuts = np.array([s["start"] for s in shots[1:]]); n = min(len(af["per_second"]), len(vf))
rms = np.array([r["rms"] for r in af["per_second"][:n]]); bright_a = np.array([r["brightness_hz"] for r in af["per_second"][:n]]); onset = np.array([r["onset"] for r in af["per_second"][:n]])
motion = np.array([r["motion"] for r in vf[:n]]); bright_v = np.array([r["brightness"] for r in vf[:n]]); warm = np.array([r["warmth_r_minus_b"] for r in vf[:n]])
cutrate = np.array([((cuts >= s) & (cuts < s + 1)).sum() for s in range(n)]).astype(float)
def sm(x, w=5): return np.convolve(x, np.ones(w) / w, mode="same")
def corr_lag(a, b, maxlag=4):
    a, b = sm(a), sm(b); best = (0, 0.0)
    for L in range(-maxlag, maxlag + 1):
        x, y = (a[L:], b[:len(b) - L]) if L >= 0 else (a[:L], b[-L:])
        if len(x) > 10 and x.std() > 0 and y.std() > 0:
            c = float(np.corrcoef(x, y)[0, 1])
            if abs(c) > abs(best[1]): best = (L, c)
    return {"lag_s_picture_after_music": best[0], "r": round(best[1], 3), "r_lag0": round(float(np.corrcoef(sm(a), sm(b))[0, 1]), 3) if a.std() and b.std() else None}
nb = max(1, int(round(args.bar_s / float(np.median(np.diff(beats)))))) if args.bar_s else 4
bars = beats[dbi % nb::nb]
def near(c, ts): return float(np.min(np.abs(ts - c))) if len(ts) else 99
off_b = np.array([near(c, beats) for c in cuts]); off_bar = np.array([near(c, bars) for c in cuts])
secs = af["sections_auto"]; sec_b = np.array([s["start"] for s in secs[1:]])
rng = np.random.default_rng(0); rnd = rng.uniform(beats[0], beats[-1], 5000)
res = {"n_cuts": int(len(cuts)), "median_beat_interval_s": round(float(np.median(np.diff(beats))), 3),
 "cuts_within_80ms_of_beat": round(float((off_b < .08).mean()), 3), "chance_beat": round(float((np.array([near(c, beats) for c in rnd]) < .08).mean()), 3),
 "cuts_within_150ms_of_bar_start(4-beat guess)": round(float((off_bar < .15).mean()), 3), "chance_bar": round(float((np.array([near(c, bars) for c in rnd]) < .15).mean()), 3),
 "section_boundaries_with_cut_within_0.5s": [{"t": float(b), "nearest_cut_s": round(near(b, cuts), 2)} for b in sec_b],
 "cut_rate_vs_loudness": corr_lag(rms, cutrate), "motion_vs_onset": corr_lag(onset, motion), "motion_vs_loudness": corr_lag(rms, motion),
 "picture_brightness_vs_sound_brightness": corr_lag(bright_a, bright_v), "picture_warmth_vs_loudness": corr_lag(rms, warm),
 "per_section": []}
for i, s in enumerate(secs):
    a, b = int(s["start"]), int(min(s["end"], n))
    if b - a < 2: continue
    c = cuts[(cuts >= s["start"]) & (cuts < s["end"])]
    res["per_section"].append({"start": s["start"], "end": s["end"], "label": s["label"], "mean_loudness": round(float(rms[a:b].mean()), 4), "cuts_per_10s": round(len(c) / (s["end"] - s["start"]) * 10, 2),
        "mean_motion": round(float(motion[a:b].mean()), 2), "mean_brightness": round(float(bright_v[a:b].mean()), 1), "mean_warmth": round(float(warm[a:b].mean()), 1),
        "cuts_on_beat_frac": round(float((np.array([near(x, beats) for x in c]) < .08).mean()), 2) if len(c) else None})
# beat-phase clustering (Rayleigh): are cuts locked to a consistent point in the beat even if the tracker's phase is offset?
def phase_stats(ts, grid):
    ph = []
    for c in ts:
        i = np.searchsorted(grid, c) - 1
        if 0 <= i < len(grid) - 1: ph.append((c - grid[i]) / (grid[i + 1] - grid[i]))
    ph = np.array(ph)
    if len(ph) < 5: return None
    z = np.exp(2j * np.pi * ph).mean(); R = abs(z); p_ray = float(np.exp(-len(ph) * R ** 2))
    return {"n": int(len(ph)), "mean_phase_0to1": round(float((np.angle(z) / (2 * np.pi)) % 1), 3), "resultant_R": round(float(R), 3), "rayleigh_p": round(p_ray, 4)}
res["cut_phase_in_beat"] = phase_stats(cuts, beats); res["cut_phase_in_half_beat"] = phase_stats(cuts, np.sort(np.concatenate([beats, (beats[:-1] + beats[1:]) / 2])))
res["cut_phase_in_bar"] = phase_stats(cuts, bars)
# significance of cut-rate vs loudness: shuffle cut rate in time (circular shift and block shuffle) and compare |r| at best lag (same statistic as observed)
def best_abs_r(a, b, maxlag=4):
    a, b = sm(a), sm(b); m = 0.0
    for L in range(-maxlag, maxlag + 1):
        x, y = (a[L:], b[:len(b) - L]) if L >= 0 else (a[:L], b[-L:])
        if len(x) > 10 and x.std() > 0 and y.std() > 0: m = max(m, abs(float(np.corrcoef(x, y)[0, 1])))
    return m
obs = best_abs_r(rms, cutrate); prng = np.random.default_rng(1); NP = args.perm; B = 10
shift = [best_abs_r(rms, np.roll(cutrate, int(prng.integers(10, max(11, n - 10))))) for _ in range(NP)]
blocks = [cutrate[i:i + B] for i in range(0, n, B)]
blk = [best_abs_r(rms, np.concatenate([blocks[j] for j in prng.permutation(len(blocks))])[:n]) for _ in range(NP)]
res["cut_rate_vs_loudness_permutation"] = {"statistic": "max |r| over lags -4..4 s after 5 s smoothing", "observed_abs_r": round(obs, 3), "n_perm": NP,
  "circular_shift_p": round((1 + sum(v >= obs for v in shift)) / (NP + 1), 4), "block_shuffle_10s_p": round((1 + sum(v >= obs for v in blk)) / (NP + 1), 4),
  "note": "p = share of shuffled series with |r| at least as large; circular shift keeps the cut-rate autocorrelation, block shuffle keeps it within 10 s blocks only. Smoothed series are strongly autocorrelated, so naive r p-values are not valid."}
res["grid"] = {"source": GRID or "audio_features/beat_times.json", "n_beats": int(len(beats)), "first_beat_s": round(float(beats[0]), 3), "last_beat_s": round(float(beats[-1]), 3), "beats_per_bar": nb, "bar_s": round(float(np.median(np.diff(bars))), 3) if len(bars) > 1 else None}
c42 = cuts[cuts < 42]; res["first_42s"] = {"n_cuts": int(len(c42)), "cut_phase_in_beat": phase_stats(c42, beats), "cut_phase_in_bar": phase_stats(c42, bars),
  "cuts_within_80ms_of_beat": round(float((np.array([near(c, beats) for c in c42]) < .08).mean()), 3) if len(c42) else None}
res["notes"] = "Correlations use 5 s smoothing; lag>0 means the picture change follows the music by that many seconds. cut_phase: Rayleigh p<0.05 means cuts cluster at a consistent beat phase (cutting to the rhythm even if the tracker phase is offset). Bars assume 4/4 from beat 1 (unverified)."
json.dump(res, open(f"{O}/{OUT}.json", "w"), indent=1)
t = np.arange(n); fig, ax = plt.subplots(4, 1, figsize=(16, 10), sharex=True)
ax[0].plot(t, rms / rms.max(), label="music loudness"); ax[0].plot(t, sm(cutrate) / max(sm(cutrate).max(), 1e-9), label="cut rate (smoothed)"); ax[0].legend()
ax[1].plot(t, onset / onset.max(), label="musical onsets"); ax[1].plot(t, motion / motion.max(), label="picture motion"); ax[1].legend()
ax[2].plot(t, bright_a / bright_a.max(), label="sound brightness"); ax[2].plot(t, bright_v / bright_v.max(), label="picture brightness"); ax[2].legend()
ax[3].plot(t, warm, label="picture warmth (R-B)"); ax[3].legend()
for a_ in ax:
    for s in secs: a_.axvline(s["start"], color="r", ls="--", lw=.7)
    for c in cuts: a_.axvline(c, color="grey", lw=.2)
ax[3].set_xticks(np.arange(0, n, 10)); plt.suptitle(f"{VID}: music vs picture"); plt.tight_layout(); plt.savefig(f"{O}/{OUT}.png", dpi=70)
print(json.dumps({k: res[k] for k in ("cuts_within_80ms_of_beat", "chance_beat", "cut_phase_in_beat", "cut_phase_in_bar", "cut_rate_vs_loudness", "cut_rate_vs_loudness_permutation", "motion_vs_onset", "picture_brightness_vs_sound_brightness")}))
