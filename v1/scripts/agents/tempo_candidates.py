"""Tempo and metre candidates for one video (video-agnostic).
Usage: python tempo_candidates.py <video_id>
Reads v1/data/<vid>/stems/drums.mp3 and v1/data/<vid>/audio/song.wav.
Writes v1/data/<vid>/audio_features/tempo_candidates.json.
Per source (drum stem, full mix): global autocorrelation of the onset envelope (mean autocorrelation tempogram),
top tempo peaks (40-240 BPM) with strength relative to the strongest, and half/double-time relations.
Drum stem also: kick (40-120 Hz flux) inter-onset median, and a bar-phase estimate: which of 4 beats (at the
candidate grid nearest the kick IOI) carries most low-band onset energy. The bar phase is an assumption, not proof."""
import json, os, sys
import numpy as np, librosa

root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if len(sys.argv) != 2: sys.exit("usage: tempo_candidates.py <video_id>")
VID = sys.argv[1]; D = os.path.join(root, "v1/data", VID)
SR, HOP = 22050, 256
FPS = SR / HOP

def load(p): return librosa.load(p, sr=SR, mono=True)[0]

def candidates(y, n=5):
    oenv = librosa.onset.onset_strength(y=y, sr=SR, hop_length=HOP)
    tg = librosa.feature.tempogram(onset_envelope=oenv, sr=SR, hop_length=HOP, win_length=384)
    ac = tg.mean(axis=1)                       # global autocorrelation (mean over time)
    lags = np.arange(len(ac)); lags[0] = 1
    bpm = 60.0 * FPS / lags
    ok = (bpm >= 40) & (bpm <= 240); idx = np.where(ok)[0]
    ac_ok = ac[idx]; bp = bpm[idx]
    pk = [i for i in range(1, len(idx) - 1) if ac_ok[i] > ac_ok[i - 1] and ac_ok[i] >= ac_ok[i + 1]]
    pk.sort(key=lambda i: -ac_ok[i]); top = ac_ok[pk[0]]
    chosen = []
    for i in pk:
        if all(abs(bp[i] - c["bpm"]) / c["bpm"] > 0.06 for c in chosen):   # merge peaks within 6 per cent
            chosen.append({"bpm": round(float(bp[i]), 2), "lag_s": round(float(1 / (bp[i] / 60)), 4), "strength": round(float(ac_ok[i]), 4), "rel_strength": round(float(ac_ok[i] / top), 3)})
        if len(chosen) == n: break
    def val(b):   # autocorrelation at a BPM (max within +-3 per cent)
        m = (bp > b * 0.97) & (bp < b * 1.03)
        return float(ac_ok[m].max() / top) if m.any() else None
    for c in chosen:
        h, d = val(c["bpm"] / 2), val(c["bpm"] * 2)
        c["rel_strength_at_half_tempo"] = None if h is None else round(h, 3)
        c["rel_strength_at_double_tempo"] = None if d is None else round(d, 3)
        others = [o for o in chosen if o is not c]
        c["half_or_double_of_other_candidate"] = [o["bpm"] for o in others if abs(o["bpm"] * 2 / c["bpm"] - 1) < 0.06 or abs(o["bpm"] / 2 / c["bpm"] - 1) < 0.06]
    top2 = None
    if len(chosen) > 1:
        gap = 1 - chosen[1]["rel_strength"]
        top2 = {"top_bpm": chosen[0]["bpm"], "second_bpm": chosen[1]["bpm"], "second_rel_strength": chosen[1]["rel_strength"],
                "ambiguous_within_10pct": bool(gap <= 0.10),
                "second_is_half_or_double_of_top": bool(abs(chosen[1]["bpm"] * 2 / chosen[0]["bpm"] - 1) < 0.06 or abs(chosen[1]["bpm"] / 2 / chosen[0]["bpm"] - 1) < 0.06)}
    return chosen, top2

def kick_onsets(y):
    S = np.abs(librosa.stft(y, n_fft=2048, hop_length=128)); fr = librosa.fft_frequencies(sr=SR, n_fft=2048)
    k = S[(fr >= 40) & (fr <= 120)].sum(0); on = np.maximum(0, np.diff(k, prepend=k[0]))
    t = librosa.frames_to_time(np.arange(len(on)), sr=SR, hop_length=128); thr = np.percentile(on, 99)
    kt, kw = [], []
    for i in range(1, len(on) - 1):
        if on[i] >= on[i - 1] and on[i] > on[i + 1] and on[i] > thr:
            if kt and t[i] - kt[-1] < 0.2:
                if on[i] > kw[-1]: kt[-1], kw[-1] = t[i], on[i]
            else: kt.append(t[i]); kw.append(on[i])
    return np.array(kt), np.array(kw)

def bar_phase(kt, kw, period, nb=4, sigma=0.02):
    cand = np.arange(0, period, 0.002); sc = []
    for o in cand:
        r = ((kt - o + period / 2) % period) - period / 2; sc.append(float((kw * np.exp(-0.5 * (r / sigma) ** 2)).sum()))
    off = float(cand[int(np.argmax(sc))])
    bi = np.round((kt - off) / period).astype(int); ok = np.abs(kt - (off + bi * period)) < 0.04
    s = np.array([float(kw[ok & (bi % nb == j)].sum()) for j in range(nb)])
    order = np.argsort(-s)
    return {"period_s": round(period, 4), "beat_offset_s": round(off, 3), "n_kicks_on_grid": int(ok.sum()), "n_kicks": int(len(kt)),
            "low_band_weight_by_beat_index": [round(float(v), 2) for v in s], "strongest_beat_index_0based": int(order[0]),
            "strongest_over_second": round(float(s[order[0]] / s[order[1]]), 3) if s[order[1]] > 0 else None,
            "share_of_strongest": round(float(s[order[0]] / s.sum()), 3) if s.sum() > 0 else None,
            "note": "Beat index counted from the grid offset; the strongest beat is taken as the downbeat (assumption; bar lines could sit a whole beat away)."}

yd = load(f"{D}/stems/drums.mp3"); ym = load(f"{D}/audio/song.wav")
out = {"video": VID, "script": "v1/scripts/agents/tempo_candidates.py", "sr": SR, "hop": HOP,
       "method": "mean autocorrelation tempogram (win 384 frames, about 4.5 s) of onset strength, peaks 40-240 BPM merged within 6 per cent; rel_strength = autocorrelation relative to the strongest peak"}
for name, y in (("drum_stem", yd), ("full_mix", ym)):
    c, t2 = candidates(y); out[name] = {"candidates": c, "top_two": t2}
kt, kw = kick_onsets(yd); d = np.diff(kt); d = d[(d > 0.25) & (d < 1.5)]
med = float(np.median(d)) if len(d) else None
out["kick"] = {"n_onsets": int(len(kt)), "median_ioi_s": None if med is None else round(med, 4), "implied_bpm": None if med is None else round(60 / med, 2),
               "ioi_p25_p75_s": None if med is None else [round(float(np.percentile(d, 25)), 4), round(float(np.percentile(d, 75)), 4)]}
if med:
    cd = out["drum_stem"]["candidates"]
    near = min(cd, key=lambda c: abs(np.log(c["bpm"] / out["kick"]["implied_bpm"]))) if cd else None
    # grid period: refine around the kick IOI median (the candidate bin is coarse), so use the median IOI
    out["kick"]["nearest_drum_candidate_bpm"] = near["bpm"] if near else None
    out["bar_phase"] = bar_phase(kt, kw, med)
    out["bar_phase"]["grid_source"] = "median kick inter-onset interval"
    out["bar_phase"]["half_time_grid"] = bar_phase(kt, kw, med * 2)
    out["bar_phase"]["half_time_grid"]["grid_source"] = "twice the median kick IOI (kick on every second beat of the main grid)"
json.dump(out, open(f"{D}/audio_features/tempo_candidates.json", "w"), indent=1)
print(json.dumps({k: out[k] for k in ("drum_stem", "full_mix", "kick", "bar_phase") if k in out}, indent=1)[:6000])
