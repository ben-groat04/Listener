"""Settle cut-vs-grid and ending-onset claims with one measurement re-run (video-agnostic despite the file name).
Usage: python sync_bar120_video2.py --vid video2 [--bpm 120] [--beats-per-bar 4] [--split 42] [--tol 0.1] [--perm 20000]
                                    [--end-window 301.8 304.5] [--expect-drums 302.34 302.59] [--expect-bass 302.34 302.60 302.85]
--bpm is mandatory-by-default 120 only for the claim being tested; for any other video pass its tempo explicitly (no default is assumed
for other videos: the script refuses --vid other than video2 unless --bpm is given on the command line).
Reads v1/data/<vid>/stems/{drums,bass}.mp3, audio/song.wav, scenes/shots.json. Writes v1/data/<vid>/sync/bar120_check.json.
Functions reused by copy (not imported, the originals are CLI scripts): kick band onset (09b_kick_grid.py), near()/offsets (09_sync.py)."""
import json, os, sys, argparse
import numpy as np, librosa

root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
ap = argparse.ArgumentParser()
ap.add_argument("--vid", required=True); ap.add_argument("--bpm", type=float); ap.add_argument("--beats-per-bar", type=int, default=4)
ap.add_argument("--split", type=float, default=42.0); ap.add_argument("--tol", type=float, default=0.1); ap.add_argument("--perm", type=int, default=20000)
ap.add_argument("--seed", type=int, default=20261117)
ap.add_argument("--end-window", type=float, nargs=2, default=[301.8, 304.5])
ap.add_argument("--expect-drums", type=float, nargs="*", default=[302.34, 302.59])
ap.add_argument("--expect-bass", type=float, nargs="*", default=[302.34, 302.60, 302.85])
ap.add_argument("--end-tol", type=float, default=0.03)
a = ap.parse_args(); VID = a.vid
if a.bpm is None:
    if VID != "video2": sys.exit("pass --bpm explicitly for any video other than video2 (e.g. video1: 78 or 156; not assumed)")
    a.bpm = 120.0
D = os.path.join(root, "v1/data", VID); P = 60.0 / a.bpm; NB = a.beats_per_bar; BAR = P * NB

# ---- (1) kick onsets from drum stem (same 40-120 Hz band-flux as 09b_kick_grid.py) ----
y, sr = librosa.load(f"{D}/stems/drums.mp3", sr=22050, mono=True); dur = len(y) / sr; hop = 128
S = np.abs(librosa.stft(y, n_fft=2048, hop_length=hop)); fr = librosa.fft_frequencies(sr=sr, n_fft=2048)
k = S[(fr >= 40) & (fr <= 120)].sum(0); on = np.maximum(0, np.diff(k, prepend=k[0])); t = librosa.frames_to_time(np.arange(len(on)), sr=sr, hop_length=hop)
thr = np.percentile(on, 99)
pk = [i for i in range(1, len(on) - 1) if on[i] >= on[i - 1] and on[i] > on[i + 1] and on[i] > thr]
kt, kw = [], []   # peak-pick with 0.2 s refractory, keep the stronger
for i in pk:
    if kt and t[i] - kt[-1] < 0.2:
        if on[i] > kw[-1]: kt[-1], kw[-1] = t[i], on[i]
    else: kt.append(t[i]); kw.append(on[i])
kt, kw = np.array(kt), np.array(kw)

def ioi_stats(x):
    d = np.diff(x); d = d[(d > 0.25) & (d < 1.5)]
    return {"n_onsets": int(len(x)), "median_ioi_s": round(float(np.median(d)), 4) if len(d) else None, "implied_bpm_from_median_ioi": round(60 / float(np.median(d)), 2) if len(d) else None}

def fit_phase(x, w, period, sigma=0.02):
    """Offset in [0, period) maximising summed strength-weighted Gaussian alignment of onsets x to the grid offset + n*period."""
    if len(x) < 5: return None
    cand = np.arange(0, period, 0.001); sc = []
    for o in cand:
        r = ((x - o + period / 2) % period) - period / 2; sc.append(float((w * np.exp(-0.5 * (r / sigma) ** 2)).sum()))
    sc = np.array(sc); o = float(cand[int(np.argmax(sc))]); r = ((x - o + period / 2) % period) - period / 2
    near = np.abs(r) < 0.04
    return {"offset_s": round(o, 4), "n_onsets": int(len(x)), "n_within_40ms": int(near.sum()), "median_resid_s": round(float(np.median(r[near])), 4) if near.any() else None, "resid_sd_s": round(float(np.std(r[near])), 4) if near.any() else None}

whole = fit_phase(kt, kw, P); m0 = kt < a.split
seg0 = fit_phase(kt[m0], kw[m0], P); seg1 = fit_phase(kt[~m0], kw[~m0], P)
off = whole["offset_s"]
# which beat of the bar is the downbeat: the beat index mod NB with the strongest summed kick weight (assumption, not verified by ear)
bi = np.round((kt - off) / P).astype(int); ok = np.abs(kt - (off + bi * P)) < 0.04
bsum = [float(kw[ok & (bi % NB == j)].sum()) for j in range(NB)]; dj = int(np.argmax(bsum))
bar_off = (off + dj * P) % BAR
beats = np.arange(off % P, dur + P, P); bars = np.arange(bar_off, dur + BAR, BAR)
# drift diagnostic: free period scan around the nominal
pscan = np.arange(P * 0.998, P * 1.002, P * 0.00002); best = max(pscan, key=lambda p: (lambda f: f["n_within_40ms"] if f else 0)(fit_phase(kt, kw, p)) * 1000 + 0)
grid = {"bpm": a.bpm, "beat_s": round(P, 5), "bar_s": round(BAR, 5), "beats_per_bar": NB, "beat_offset_s": whole["offset_s"], "bar_offset_s": round(float(bar_off), 4),
        "downbeat_beat_index_mod_bar": dj, "kick_weight_by_beat_in_bar": [round(v, 2) for v in bsum],
        "downbeat_note": "Bar phase = beat position with the largest summed kick onset strength; an assumption (bar lines could be offset by whole beats).",
        "kick_ioi": ioi_stats(kt), "kick_ioi_0_to_split": ioi_stats(kt[m0]), "kick_ioi_split_to_end": ioi_stats(kt[~m0]),
        "phase_fit_whole_track": whole, "phase_fit_0_to_%gs" % a.split: seg0, "phase_fit_%gs_to_end" % a.split: seg1,
        "phase_difference_segments_s": None if not (seg0 and seg1) else round(float((((seg1["offset_s"] - seg0["offset_s"]) + P / 2) % P) - P / 2), 4),
        "free_period_scan_best_period_s": round(float(best), 5), "free_period_scan_best_bpm": round(60 / float(best), 3),
        "first_kick_s": round(float(kt[0]), 3), "last_kick_s": round(float(kt[-1]), 3), "track_dur_s": round(dur, 2)}

# ---- (2) cut vs grid test with seeded permutation null ----
shots = json.load(open(f"{D}/scenes/shots.json")); cuts = np.array([s["start"] for s in shots[1:]], dtype=float)
def dist(c, g): return np.min(np.abs(c[:, None] - g[None, :]), axis=1)
rng = np.random.default_rng(a.seed)
def test(c, lo, hi, g, label):
    if len(c) == 0: return {"n_cuts": 0}
    obs = int((dist(c, g) <= a.tol).sum()); sims = np.array([int((dist(rng.uniform(lo, hi, len(c)), g) <= a.tol).sum()) for _ in range(a.perm)])
    spacing = float(np.median(np.diff(g)))
    return {"n_cuts": int(len(c)), "within_tol": obs, "frac": round(obs / len(c), 3), "null_expected_count": round(float(sims.mean()), 2), "null_expected_frac": round(float(sims.mean()) / len(c), 3),
            "analytic_expected_frac": round(min(1.0, 2 * a.tol / spacing), 3), "p_one_sided_perm": round((1 + int((sims >= obs).sum())) / (a.perm + 1), 4),
            "summary": f"{obs} of {len(c)} cuts within {a.tol} s of a {label} line; null expectation {sims.mean():.1f} (p={(1 + int((sims >= obs).sum())) / (a.perm + 1):.3f})"}
tests = {}
for name, (lo, hi) in {"whole_track": (0, dur), "0_to_%gs" % a.split: (0, a.split), "%gs_to_end" % a.split: (a.split, dur)}.items():
    c = cuts[(cuts >= lo) & (cuts < hi)]
    tests[name] = {"bars": test(c, lo, hi, bars, "bar"), "beats": test(c, lo, hi, beats, "beat")}

# ---- (3) onsets in the end window from 10 ms envelopes ----
w0, w1 = a.end_window
def env_onsets(path, label, band=None):
    z, s = librosa.load(path, sr=22050, mono=True)
    if band:
        import scipy.signal as sg; z = sg.sosfiltfilt(sg.butter(4, band, btype="band", fs=s, output="sos"), z)
    h = int(round(0.010 * s)); win = 2 * h; n = (len(z) - win) // h
    rms = np.array([np.sqrt(np.mean(z[i * h:i * h + win] ** 2)) for i in range(n)]); db = 20 * np.log10(rms + 1e-6); tt = (np.arange(n) * h + win / 2) / s
    r3 = np.array([db[min(i + 3, n - 1)] - db[i] for i in range(n)]); d1 = np.diff(db, append=db[-1])
    f6 = np.array([db[i] - db[min(i + 6, n - 1)] for i in range(n)])
    idx = np.where((tt >= w0) & (tt <= w1))[0]
    def pick(score, thr, ref, floor, refractory=0.1):
        out = []
        for i in idx:
            if score[i] > thr and score[i] >= score[max(0, i - 1)] and score[i] > score[min(n - 1, i + 1)] and db[min(i + 6, n - 1)] > floor:
                if ref == "rise":
                    pkv = float(np.max(db[i:i + 10])); ks = [k for k in range(i, min(i + 4, n - 1)) if db[k + 1] > pkv - 20] or list(range(i, min(i + 4, n - 1)))
                    j = ks[int(np.argmax([d1[k] for k in ks]))]
                else: j = i + int(np.argmin(d1[i:i + 7]))
                rec = {"t_s": round(float(tt[j]), 3), "change_db": round(float(score[i]), 1), "level_after_db": round(float(db[min(i + 6, n - 1)]), 1)}
                if out and rec["t_s"] - out[-1]["t_s"] < refractory:
                    if rec["change_db"] > out[-1]["change_db"]: out[-1] = rec
                else: out.append(rec)
        return out
    ons = pick(r3, 4.0, "rise", -60); offs = [{"t_s": o["t_s"], "fall_db_60ms": o["change_db"]} for o in pick(f6, 20.0, "fall", -200)]
    for o in ons: o["rise_db_30ms"] = o.pop("change_db")
    return {"source": os.path.relpath(path, root), "band_hz": band, "method": "10 ms hop, 20 ms RMS window, dB; onset = local max of 30 ms rise > 4 dB (time of steepest 10 ms rise among frames within 20 dB of the following peak, so noise-floor ramps do not count), 0.1 s refractory; offsets = local max of 60 ms fall > 20 dB (time of steepest 10 ms fall)", "onsets": ons, "offsets": offs}
ending = {"window_s": [w0, w1], "drums_stem": env_onsets(f"{D}/stems/drums.mp3", "drums"), "bass_stem": env_onsets(f"{D}/stems/bass.mp3", "bass"),
          "full_mix_song_wav": env_onsets(f"{D}/audio/song.wav", "mix"), "full_mix_song_wav_below_250hz": env_onsets(f"{D}/audio/song.wav", "mix_lo", [30, 250])}
def cmp(found, exp):
    ft = [o["t_s"] for o in found]; r = []
    for e in exp:
        j = min(ft, key=lambda x: abs(x - e)) if ft else None
        r.append({"expected_s": e, "nearest_found_s": j, "diff_s": None if j is None else round(j - e, 3), "match": j is not None and abs(j - e) <= a.end_tol})
    return {"expected_matches": r, "unexpected_extra_onsets_s": [x for x in ft if all(abs(x - e) > a.end_tol for e in exp)], "n_found": len(ft), "n_expected": len(exp)}
ending["drums_stem"]["vs_expected"] = cmp(ending["drums_stem"]["onsets"], a.expect_drums)
ending["bass_stem"]["vs_expected"] = cmp(ending["bass_stem"]["onsets"], a.expect_bass)
ending["full_mix_song_wav"]["vs_expected_union"] = cmp(ending["full_mix_song_wav"]["onsets"], sorted(set(a.expect_drums + a.expect_bass)))
ending["full_mix_song_wav_below_250hz"]["vs_expected_union"] = cmp(ending["full_mix_song_wav_below_250hz"]["onsets"], sorted(set(a.expect_drums + a.expect_bass)))
ending["tolerance_s"] = a.end_tol
for key in ("drums_stem", "bass_stem", "full_mix_song_wav", "full_mix_song_wav_below_250hz"):
    exp = a.expect_drums if key == "drums_stem" else a.expect_bass if key == "bass_stem" else sorted(set(a.expect_drums + a.expect_bass))
    ending[key]["expected_times_that_are_note_offsets_instead"] = [e for e in exp if any(abs(o["t_s"] - e) <= 0.08 for o in ending[key]["offsets"])]

# ---- (4) verdicts ----
def verdict(t):
    out = {}
    for u in ("bars", "beats"):
        r = t[u]
        if r.get("n_cuts", 0) < 10: out[u] = f"untested (only {r.get('n_cuts', 0)} cuts)"
        elif r["p_one_sided_perm"] < 0.05 and r["within_tol"] > r["null_expected_count"]: out[u] = "supported: " + r["summary"]
        else: out[u] = "not supported: " + r["summary"]
    return out
claims = {n: verdict(t) for n, t in tests.items()}
wt = tests["whole_track"]
overall = ("rhythm-locked supported" if any(v.startswith("supported") for v in claims["whole_track"].values()) else "rhythm-locked not supported")
ev = ending
def endv(src, key, srckey=None):
    c = src[key]; extra = ("; expected times that coincide with a note OFFSET (fall > 20 dB), not an onset: %s" % src["expected_times_that_are_note_offsets_instead"]) if src["expected_times_that_are_note_offsets_instead"] else ""
    return extra and (_endv(c) + extra) or _endv(c)
def _endv(c): return "onsets match expected (all within %.2f s), extras: %s" % (a.end_tol, c["unexpected_extra_onsets_s"]) if all(m["match"] for m in c["expected_matches"]) else "discrepancy: " + json.dumps([m for m in c["expected_matches"] if not m["match"]]) + "; extras: %s" % c["unexpected_extra_onsets_s"]
verdicts = {
  "cuts_rhythm_locked_whole_track": overall + " (alignment test at %.2f s tolerance; seeded permutation null; shot detector is the coarse one and under-detects cuts, LESSONS L8, so a null result is weak evidence of absence)" % a.tol,
  "cuts_rhythm_locked_by_segment": claims,
  "grid_basis": "grid fitted from drum-stem kicks over the whole track; kicks may be sparse or absent before the split, in which case the early-segment grid is an extrapolation (see phase_fit and n_onsets)",
  "ending_drums_onsets": endv(ev["drums_stem"], "vs_expected"),
  "ending_bass_onsets": endv(ev["bass_stem"], "vs_expected"),
  "ending_full_mix_onsets": endv(ev["full_mix_song_wav"], "vs_expected_union") + " (full mix; low-band-only version listed separately)",
}
res = {"video": VID, "script": "v1/scripts/agents/sync_bar120_video2.py", "args": {k: v for k, v in vars(a).items()}, "grid_used": grid,
       "cut_test": {"cut_source": f"v1/data/{VID}/scenes/shots.json (n_cuts=%d; detector under-detects, LESSONS L8)" % len(cuts), "tolerance_s": a.tol, "null": f"{a.perm} uniform-random cut sets of the same size in the segment, seed {a.seed}", "results": tests},
       "ending_onsets": ending, "verdict": verdicts}
os.makedirs(f"{D}/sync", exist_ok=True); json.dump(res, open(f"{D}/sync/bar120_check.json", "w"), indent=1)
print(json.dumps({"grid": {k: grid[k] for k in ("kick_ioi", "phase_fit_whole_track", "bar_offset_s", "downbeat_beat_index_mod_bar", "free_period_scan_best_bpm", "phase_difference_segments_s")}, "tests": {n: {u: t[u].get("summary") for u in t} for n, t in tests.items()},
  "ending": {k: [o["t_s"] for o in ending[k]["onsets"]] for k in ("drums_stem", "bass_stem", "full_mix_song_wav", "full_mix_song_wav_below_250hz")}, "verdict": verdicts}, indent=1))
