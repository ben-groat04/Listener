"""Music descriptors via librosa: tempo/beats, key estimate, loudness & brightness curves, structural segmentation, charts.

Usage: VID=<folder under v1/data/> python3 v1/scripts/04_audio_features.py   (VID is mandatory)

Outputs in v1/data/<VID>/audio_features/: summary.json, beat_times.json, overview.png, spectrogram.png, form.json.
All added blocks below are measurements (tag "OBS"); reading mode or form musically stays out of this script.
  summary['tempo_candidates']  drums-stem autocorrelation candidates + 3:4 / 2:1 warnings vs the whole-mix tempo.
  summary['downbeat_estimate'] older drum-onset phase guess on the whole-mix beat grid.
  summary['tempo_resolved']    (D4, needs stems/drums.mp3, else {"skipped": ...}) kick grid (40-120 Hz onset autocorrelation + least-squares
                               fit: bpm, period, grid fit quality), level_vs_whole_mix (same level / double / half / 4:3 / 3:4, half_double_ambiguous
                               with notes, reused tempo_candidates warnings), backbeat_test (snare/clap 1-5 kHz energy on beats 2,4 vs 1,3),
                               downbeat_guess (time, grid position, confidence capped at moderate, assumes 4/4).
  summary['mode_reading']      (D6) pitch-class histogram of mean chroma; template score for ionian, dorian, phrygian, lydian, mixolydian,
                               aeolian, locrian at the Krumhansl-Schmuckler reference tonic and best over tonics; third/sixth/seventh/second/fourth
                               evidence; key_ambiguous (KS flag, unchanged), mode_ambiguous and combined ambiguous.
  form.json                    (D7) stem-activity novelty curve and peaks (which stems rise/fall), stem first-active times, beat-lag recurrence
                               and loop-length estimate; sections_auto is kept only as a secondary, labelled field.
"""
import json, os, sys
import numpy as np, librosa, librosa.display, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
VID = os.environ.get("VID")
if not VID: sys.exit("ERROR: environment variable VID is not set. Usage: VID=<video folder name under v1/data/> python3 04_audio_features.py")
if not os.path.exists(os.path.join(root, f"v1/data/{VID}/audio/song.wav")): sys.exit(f"ERROR: v1/data/{VID}/audio/song.wav not found (VID={VID!r}); run the audio extraction first.")
A = os.path.join(root, f"v1/data/{VID}/audio/song.wav"); D = os.path.join(root, f"v1/data/{VID}/audio_features"); os.makedirs(D, exist_ok=True)
y, sr = librosa.load(A, sr=22050, mono=True); dur = len(y) / sr
tempo, beats = librosa.beat.beat_track(y=y, sr=sr); bt = librosa.frames_to_time(beats, sr=sr)
hop = 512
rms = librosa.feature.rms(y=y, hop_length=hop)[0]; t = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop)
cent = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=hop)[0]
onset = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop)
chroma = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=hop)
# Krumhansl-Schmuckler key estimate (whole song + per 30s window)
maj = np.array([6.35,2.23,3.48,2.33,4.38,4.09,2.52,5.19,2.39,3.66,2.29,2.88]); mnr = np.array([6.33,2.68,3.52,5.38,2.60,3.53,2.54,4.75,3.98,2.69,3.34,3.17])
names = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
def key(c):
    v = c.mean(axis=1); best = []
    for i in range(12):
        best.append((np.corrcoef(np.roll(maj, i), v)[0,1], names[i]+" major")); best.append((np.corrcoef(np.roll(mnr, i), v)[0,1], names[i]+" minor"))
    best.sort(reverse=True); return [(n, round(float(s),3)) for s, n in best[:3]]
win = int(30 * sr / hop); keys_windowed = [{"start_s": round(i*hop/sr,1), "top": key(chroma[:, i:i+win])} for i in range(0, chroma.shape[1], win)]
# structural segmentation: agglomerative on stacked chroma+mfcc, k=10
mfcc = librosa.feature.mfcc(y=y, sr=sr, hop_length=hop, n_mfcc=13)
feat = librosa.util.sync(np.vstack([librosa.util.normalize(chroma), librosa.util.normalize(mfcc)]), beats)
bounds = librosa.segment.agglomerative(feat, 10); bound_t = [float(bt[min(b, len(bt)-1)]) if b > 0 else 0.0 for b in bounds]
# label recurring sections by clustering segment mean features
segs = list(zip(bounds, list(bounds[1:]) + [feat.shape[1]]))
means = np.array([feat[:, a:max(b, a+1)].mean(axis=1) for a, b in segs])
from scipy.cluster.hierarchy import linkage, fcluster
labels = fcluster(linkage(means, "ward"), t=5, criterion="maxclust") if len(means) > 1 else [1]
sections = [{"start": round(bound_t[i],2), "end": round(bound_t[i+1] if i+1 < len(bound_t) else dur,2), "label": chr(64+int(l)),
             "mean_rms": round(float(rms[(t>=bound_t[i]) & (t<(bound_t[i+1] if i+1<len(bound_t) else dur))].mean()),4)} for i, l in enumerate(labels)]
# local tempo drift
tg = librosa.feature.tempo(onset_envelope=onset, sr=sr, hop_length=hop, aggregate=None)
summary = {"duration_s": round(dur,2), "tempo_bpm": float(np.atleast_1d(tempo)[0]), "n_beats": int(len(bt)),
           "key_whole_song_top3": key(chroma), "key_ambiguous": None, "keys_per_30s": keys_windowed, "sections_auto": sections,
           "loudness_rms_mean": float(rms.mean()), "loudest_moment_s": float(t[rms.argmax()]), "quietest_moment_s_after_5s": float(t[t>5][rms[t>5].argmin()]),
           "tempo_local_percentiles": {p: float(np.percentile(tg, p)) for p in (10, 50, 90)},
           "per_second": [{"t": s, "rms": round(float(rms[(t>=s)&(t<s+1)].mean()),4), "brightness_hz": round(float(cent[(t>=s)&(t<s+1)].mean())), "onset": round(float(onset[(t>=s)&(t<s+1)].mean()),3)} for s in range(int(dur))]}
# tempo candidates from the drums stem (extra block; skipped when no drums stem). Warns when the whole-mix tempo is a 3:4 or 2:1 multiple of the drum tempo.
drums_path = os.path.join(root, f"v1/data/{VID}/stems/drums.mp3")
if os.path.exists(drums_path):
    try:
        yd, _ = librosa.load(drums_path, sr=sr, mono=True); od = librosa.onset.onset_strength(y=yd, sr=sr, hop_length=hop); od = od - od.mean()
        ac = np.correlate(od, od, "full")[len(od) - 1:]; ac = ac / ac[0]; fps = sr / hop
        lo, hi = int(fps * 60 / 240), int(fps * 60 / 60); seg = ac[lo:hi + 1]
        pk = [i for i in range(1, len(seg) - 1) if seg[i] > seg[i - 1] and seg[i] >= seg[i + 1] and seg[i] > 0.05]
        pk = sorted(pk, key=lambda i: -seg[i])[:6]
        cands = []
        for i in pk:
            lag = i + lo; lag_r = float(lag + (0.5 * (ac[lag - 1] - ac[lag + 1]) / (ac[lag - 1] - 2 * ac[lag] + ac[lag + 1]) if 0 < lag < len(ac) - 1 and (ac[lag - 1] - 2 * ac[lag] + ac[lag + 1]) != 0 else 0))
            cands.append({"bpm": round(60 * fps / lag_r, 2), "lag_s": round(lag_r / fps, 4), "autocorr": round(float(seg[i]), 3)})
        mix_bpm = float(np.atleast_1d(tempo)[0]); top = cands[0]["bpm"] if cands else None; warns = []
        if cands:
            for c in cands: c["ratio_to_mix_tempo"] = round(c["bpm"] / mix_bpm, 3)
            for c in cands:
                r = mix_bpm / c["bpm"]
                for name, tgt in (("3:4", 4 / 3), ("3:4", 3 / 4), ("2:1", 2.0), ("2:1", 0.5)):
                    if abs(r - tgt) / tgt < 0.04: warns.append(f"whole-mix tempo {mix_bpm:.1f} BPM vs drums-stem candidate {c['bpm']} BPM (autocorr {c['autocorr']}): ratio {r:.3f} is about {name}; the beat grid may be on a different metrical level or feel than the drums.")
        summary["tempo_candidates"] = {"source": "autocorrelation of drums-stem onset strength, 60-240 BPM, top peaks by height", "whole_mix_tempo_bpm": mix_bpm, "drum_candidates": cands, "warnings": warns}
    except Exception as e: summary["tempo_candidates"] = {"error": repr(e)}
_k3 = summary["key_whole_song_top3"]
summary["key_ambiguous"] = bool(len(_k3) > 1 and abs(_k3[0][1] - _k3[1][1]) < 0.05)
summary["key_ambiguity_note"] = (f"top two key scores ({_k3[0][0]} {_k3[0][1]}, {_k3[1][0]} {_k3[1][1]}) are within 0.05: treat the key as ambiguous, not as a fact." if summary["key_ambiguous"] else "top key leads the runner-up by 0.05 or more (Krumhansl-Schmuckler on the whole mix; still an estimate).")
# downbeat estimate from the drums stem: beat-synchronous onset strength folded by a 4-beat cycle (assumes 4/4; a guess, not a fact)
if os.path.exists(drums_path) and len(bt) >= 16:
    try:
        bf = librosa.time_to_frames(bt, sr=sr, hop_length=hop); bf = bf[bf < len(od)]
        bs = od[bf]; phase = [float(bs[k::4].mean()) for k in range(4)]; k0 = int(np.argmax(phase)); srt = sorted(phase, reverse=True)
        summary["downbeat_estimate"] = {"assumes": "4 beats per bar", "beat_index_mod4_of_downbeat": k0, "first_downbeat_s": round(float(bt[k0]), 3), "phase_drum_onset_means": [round(x, 3) for x in phase], "confidence": "low" if srt[0] < 1.15 * srt[1] else "moderate", "note": "strongest drum-onset beat position in a 4-beat cycle over the whole song; unreliable if the metre is not 4/4 or the beat grid is on the wrong level."}
    except Exception as e: summary["downbeat_estimate"] = {"error": repr(e)}
# ---- D4: tempo_resolved (OBS). Kick grid + backbeat test from the drums stem; skipped cleanly when there is no drums stem. ----
from scipy.signal import butter, sosfiltfilt, find_peaks
fps = sr / hop
def _band_env(sig, lo_hz, hi_hz):
    return librosa.onset.onset_strength(y=sosfiltfilt(butter(4, [lo_hz, hi_hz], "bandpass", fs=sr, output="sos"), sig), sr=sr, hop_length=hop)
def _local_max(env, times_s, half=2):
    ix = np.round(np.asarray(times_s) * fps).astype(int); out = np.zeros(len(ix))
    for j, i in enumerate(ix):
        a, b = max(i - half, 0), min(i + half + 1, len(env)); out[j] = env[a:b].max() if b > a else 0.0
    return out
def tempo_resolved():
    ydr, _ = librosa.load(drums_path, sr=sr, mono=True)
    ko2 = _band_env(ydr, 40, 120); so2 = _band_env(ydr, 1000, 5000)
    x = ko2 - ko2.mean(); ac2 = np.correlate(x, x, "full")[len(x) - 1:]; ac2 = ac2 / ac2[0]
    lo_l, hi_l = int(fps * 60 / 220), int(fps * 60 / 55); seg2 = ac2[lo_l:hi_l + 1]
    pk2 = [i for i in range(1, len(seg2) - 1) if seg2[i] > seg2[i - 1] and seg2[i] >= seg2[i + 1]]
    if not pk2: return {"tag": "OBS", "error": "no autocorrelation peak in the kick-band onset envelope"}
    i0 = max(pk2, key=lambda i: seg2[i]); lag = i0 + lo_l
    den = ac2[lag - 1] - 2 * ac2[lag] + ac2[lag + 1]; lag_r = float(lag + (0.5 * (ac2[lag - 1] - ac2[lag + 1]) / den if den != 0 else 0))
    p = lag_r / fps; kick_bpm0 = 60 / p
    def ac_at(l):
        l = int(round(l))
        return float(ac2[l]) if 0 < l < len(ac2) else None
    # grid phase: maximise kick-envelope sum over grid points, then least-squares refine on kick onsets near the grid
    best = None
    for ph in np.arange(0, p, 0.004):
        pts = np.arange(ph, dur, p); sc = ko2[np.clip(np.round(pts * fps).astype(int), 0, len(ko2) - 1)].mean()
        if best is None or sc > best[0]: best = (sc, ph)
    t0 = best[1]
    kt2 = librosa.frames_to_time(librosa.onset.onset_detect(onset_envelope=ko2, sr=sr, hop_length=hop, units="frames"), sr=sr, hop_length=hop)
    for _ in range(3):
        n = np.round((kt2 - t0) / p); res = kt2 - (t0 + n * p); m = np.abs(res) < 0.05
        if m.sum() >= 8: p, t0 = (lambda c: (float(c[0]), float(c[1])))(np.polyfit(n[m], kt2[m], 1))
    n = np.round((kt2 - t0) / p); res = kt2 - (t0 + n * p); on = np.abs(res) < 0.05
    grid_pts = np.arange(t0 + p * np.ceil(-t0 / p), dur, p); kstr = _local_max(ko2, grid_pts)
    kick_at_grid_frac = float((kstr > 0.5 * np.median(ko2[ko2 > 0])).mean()) if len(grid_pts) else 0.0
    kick_bpm = 60 / p; mix_bpm = float(np.atleast_1d(tempo)[0]); r = mix_bpm / kick_bpm
    rel = None
    for nm, tgt in (("same_level", 1.0), ("mix_is_double_of_kick_grid", 2.0), ("mix_is_half_of_kick_grid", 0.5), ("mix_is_4:3_of_kick_grid", 4 / 3), ("mix_is_3:4_of_kick_grid", 3 / 4)):
        if abs(r - tgt) / tgt < 0.04: rel = nm; break
    rel = rel or "unrelated_or_unclear"
    a_half, a_dbl = ac_at(lag_r / 2), ac_at(lag_r * 2); top_h = float(ac2[lag])
    amb = []
    if a_half is not None and a_half >= 0.8 * top_h: amb.append(f"kick-envelope autocorrelation at half the lag (double tempo, {2*kick_bpm:.1f} BPM) is {a_half:.2f} vs {top_h:.2f} at the chosen lag")
    if a_dbl is not None and a_dbl >= 0.8 * top_h: amb.append(f"autocorrelation at double the lag (half tempo, {kick_bpm/2:.1f} BPM) is {a_dbl:.2f} vs {top_h:.2f} at the chosen lag")
    if not (70 <= kick_bpm <= 160): amb.append(f"kick-grid {kick_bpm:.1f} BPM lies outside 70-160 BPM, where half/double readings are common")
    # beat-level grid for the backbeat test: the kick-grid level (or a 2x / 0.5x subdivision of it) closest to the whole-mix tempo
    level = "kick grid as is"; pts = grid_pts; pb = p
    if rel == "mix_is_double_of_kick_grid": pb = p / 2; pts = np.arange(t0 + pb * np.ceil(-t0 / pb), dur, pb); level = "kick grid halved in period to match the mix tempo"
    elif rel == "mix_is_half_of_kick_grid":
        pb = p * 2; level = "kick grid doubled in period to match the mix tempo (phase chosen by stronger kick)"
        cand = [np.arange(t0 + s * p + 0.0, dur, pb) for s in (0, 1)]; cand = [c[c >= 0] for c in cand]
        pts = max(cand, key=lambda c: _local_max(ko2, c).mean())
    S = _local_max(so2, pts); K = _local_max(ko2, pts)
    fr_rms = librosa.feature.rms(y=ydr, hop_length=hop)[0]; act_v = _local_max(fr_rms, pts, 2); act = act_v > 0.25 * np.median(act_v[act_v > 0]) if (act_v > 0).any() else act_v > 0
    idx = np.arange(len(pts)) % 4
    if act.sum() < 16: return {"tag": "OBS", "error": "fewer than 16 active drum beats on the grid", "kick_grid_bpm": round(kick_bpm, 2)}
    Ps = np.array([S[act & (idx == k)].mean() if (act & (idx == k)).any() else 0.0 for k in range(4)]); Pk = np.array([K[act & (idx == k)].mean() if (act & (idx == k)).any() else 0.0 for k in range(4)])
    eps = 1e-9
    def bb(o): return float((Ps[(o + 1) % 4] + Ps[(o + 3) % 4]) / (Ps[o] + Ps[(o + 2) % 4] + eps))
    par = max((0, 1), key=bb); R = bb(par)  # beats 2&4 are positions par+1, par+3; downbeat is par or par+2
    o = max((par, (par + 2) % 4), key=lambda q: Pk[q]); other = (o + 2) % 4
    kick_13 = float((Pk[o] + Pk[other]) / (Pk[(o + 1) % 4] + Pk[(o + 3) % 4] + eps)); kick_sep = float(Pk[o] / (Pk[other] + eps))
    first_i = int(np.where(act & (idx == o))[0][0]); first_db = float(pts[first_i])
    verdict = "backbeat_present" if R >= 1.5 else "weak_backbeat" if R >= 1.2 else "no_clear_backbeat"
    conf = "moderate" if (R >= 1.5 and kick_sep >= 1.1 and rel == "same_level" and kick_at_grid_frac >= 0.5) else "low"
    return {"tag": "OBS", "source": "drums stem; kick = 40-120 Hz onset strength, snare/clap = 1-5 kHz onset strength (hi-hats not excluded)",
        "kick_grid": {"bpm": round(kick_bpm, 2), "period_s": round(p, 4), "first_grid_s": round(float(t0 + p * np.ceil(-t0 / p)), 3), "autocorr_at_period": round(top_h, 3), "autocorr_at_half_lag": None if a_half is None else round(a_half, 3), "autocorr_at_double_lag": None if a_dbl is None else round(a_dbl, 3),
            "kick_onsets_n": int(len(kt2)), "kick_onsets_within_50ms_of_grid_frac": round(float(on.mean()), 3) if len(on) else None, "grid_points_with_kick_frac": round(kick_at_grid_frac, 3), "residual_std_ms": round(float(res[on].std() * 1000), 1) if on.sum() > 2 else None},
        "level_vs_whole_mix": {"whole_mix_tempo_bpm": round(mix_bpm, 2), "ratio_mix_to_kick_grid": round(r, 3), "relation": rel, "same_level": rel == "same_level",
            "half_double_ambiguous": bool(amb), "half_double_notes": amb, "tempo_candidates_warnings": list(summary.get("tempo_candidates", {}).get("warnings", []))},
        "backbeat_test": {"beat_grid_used": level, "beat_grid_bpm": round(60 / pb, 2), "active_beats_n": int(act.sum()), "assumes": "4 beats per bar",
            "snare_mean_by_beat_position": [round(float(v), 3) for v in Ps], "kick_mean_by_beat_position": [round(float(v), 3) for v in Pk],
            "backbeat_ratio_beats_2_4_over_1_3": round(R, 3), "verdict": verdict, "kick_beats_1_3_over_2_4": round(kick_13, 3)},
        "downbeat_guess": {"first_downbeat_s": round(first_db, 3), "grid_position_mod4": int(o), "snare_parity_decides": "beats 2 and 4 are the positions with the larger snare/clap energy; which of the two beat-1 candidates is the downbeat is picked by the kick (kick_1_vs_3 ratio below), a weak cue", "kick_beat1_over_beat3": round(kick_sep, 3), "confidence": conf,
            "note": "assumes 4/4; confidence is capped at moderate and is low unless the backbeat ratio is at least 1.5, the kick separates beat 1 from 3 by 10%, and the kick grid is the same level as the whole-mix tempo."}}
if os.path.exists(drums_path):
    try: summary["tempo_resolved"] = tempo_resolved()
    except Exception as e: summary["tempo_resolved"] = {"tag": "OBS", "error": repr(e)}
else: summary["tempo_resolved"] = {"tag": "OBS", "skipped": "no drums stem (v1/data/<VID>/stems/drums.mp3) for this video"}
# ---- D6: mode_reading (OBS). Pitch-class histogram, mode template scores, third/seventh evidence. No interpretation here. ----
def mode_reading():
    h = chroma.mean(axis=1); h = h / h.sum()
    MODES = {"ionian": [0, 2, 4, 5, 7, 9, 11], "dorian": [0, 2, 3, 5, 7, 9, 10], "phrygian": [0, 1, 3, 5, 7, 8, 10], "lydian": [0, 2, 4, 6, 7, 9, 11], "mixolydian": [0, 2, 4, 5, 7, 9, 10], "aeolian": [0, 2, 3, 5, 7, 8, 10], "locrian": [0, 1, 3, 5, 6, 8, 10]}
    def score(tonic, iv):
        w = np.zeros(12)
        for d in iv: w[(tonic + d) % 12] = 1.0
        w[tonic] = 2.0; w[(tonic + iv[4]) % 12] = 1.5
        return float(np.corrcoef(w, h)[0, 1])
    allp = sorted(((score(tn, iv), names[tn], m) for tn in range(12) for m, iv in MODES.items()), reverse=True)
    ks = summary["key_whole_song_top3"][0]; ref_name, ref_q = ks[0].split(" "); ref = names.index(ref_name)
    at_ref = {m: round(score(ref, iv), 3) for m, iv in MODES.items()}; rk = sorted(at_ref.items(), key=lambda kv: -kv[1])
    best_by_mode = {}
    for m, iv in MODES.items():
        sc = max((score(tn, iv), names[tn]) for tn in range(12)); best_by_mode[m] = {"tonic": sc[1], "score": round(sc[0], 3)}
    def deg(lo, hi, lab_lo, lab_hi):
        a, b = float(h[(ref + lo) % 12]), float(h[(ref + hi) % 12]); return {f"{lab_lo}_semitones_{lo}": round(a, 4), f"{lab_hi}_semitones_{hi}": round(b, 4), f"share_of_{lab_hi}": round(b / (a + b), 3) if a + b > 0 else None}
    third = deg(3, 4, "minor3", "major3"); seventh = deg(10, 11, "minor7", "major7")
    third_major = third["share_of_major3"] is not None and third["share_of_major3"] > 0.5
    margin = rk[0][1] - rk[1][1]; mode_amb = bool(margin < 0.05); key_amb = bool(summary["key_ambiguous"])
    return {"tag": "OBS", "method": "mean chroma_cqt of the whole mix as a pitch-class histogram; each mode scored by Pearson correlation with a template (scale degrees 1, tonic 2, fifth degree 1.5). Relative modes share a pitch set, so they differ only through the tonic weighting.",
        "pitch_class_histogram": {names[i]: round(float(h[i]), 4) for i in range(12)}, "pitch_classes_by_weight": [names[i] for i in np.argsort(-h)],
        "reference_tonic": ref_name, "reference_tonic_source": f"Krumhansl-Schmuckler top key '{ks[0]}' (score {ks[1]})",
        "mode_scores_at_reference_tonic": at_ref, "top_mode_at_reference_tonic": rk[0][0], "top_two_margin": round(margin, 3),
        "mode_best_over_all_tonics": best_by_mode, "top5_tonic_mode_pairs": [{"tonic": a, "mode": b, "score": round(s, 3)} for s, a, b in allp[:5]],
        "overall_best_agrees_with_reference_tonic": allp[0][1] == ref_name,
        "evidence": {"third_above_reference_tonic": third, "seventh_above_reference_tonic": seventh, "sixth_above_reference_tonic": deg(8, 9, "minor6", "major6"), "second_above_reference_tonic": deg(1, 2, "minor2", "major2"), "fourth_above_reference_tonic": deg(5, 6, "perfect4", "tritone")},
        "third_agrees_with_ks_quality": bool(third_major == (ref_q == "major")),
        "key_ambiguous": key_amb, "mode_ambiguous": mode_amb, "ambiguous": bool(key_amb or mode_amb),
        "ambiguity_note": "key_ambiguous is the Krumhansl-Schmuckler flag (top two keys within 0.05); mode_ambiguous means the top two mode scores at the reference tonic are within 0.05; ambiguous is true if either is. Treat the reading as a measurement of the pitch content, not as a verdict on mode."}
try: summary["mode_reading"] = mode_reading()
except Exception as e: summary["mode_reading"] = {"tag": "OBS", "error": repr(e)}
# ---- D7: form.json (OBS). Stem-activity novelty + beat-lag recurrence; auto sections kept as a secondary, labelled field. ----
def form_analysis():
    stems = {}
    for sn in ("bass", "drums", "other", "vocals"):
        pth = os.path.join(root, f"v1/data/{VID}/stems/{sn}.mp3")
        if os.path.exists(pth):
            ys, _ = librosa.load(pth, sr=sr, mono=True); stems[sn] = librosa.feature.rms(y=ys, hop_length=hop)[0]
    nf = len(rms)
    if stems:
        src = "stems: " + ", ".join(stems); fr_db = np.array([20 * np.log10(np.pad(v, (0, max(nf - len(v), 0)))[:nf] + 1e-5) for v in stems.values()]); fnames = list(stems)
    else:
        src = "whole mix (no stems): loudness, brightness, onset strength"; fr_db = np.array([20 * np.log10(rms + 1e-5), cent[:nf], onset[:nf]]); fnames = ["mix_loudness", "mix_brightness", "mix_onset"]
    def z(a): return (a - a.mean(axis=1, keepdims=True)) / (a.std(axis=1, keepdims=True) + 1e-6)
    fz = z(fr_db); ns = int(dur)
    sec = np.array([fz[:, (t >= s) & (t < s + 1)].mean(axis=1) for s in range(ns)]).T  # features x seconds
    # stem activity (stems only)
    act_info = {}
    if stems:
        for k, sn in enumerate(fnames):
            v = np.array([10 ** (fr_db[k][(t >= s) & (t < s + 1)].mean() / 20) for s in range(ns)]); thr = 0.1 * np.percentile(v, 95); a = v >= thr
            run = next((s for s in range(ns - 3) if a[s:s + 4].all()), None)
            act_info[sn] = {"active_fraction": round(float(a.mean()), 3), "first_sustained_active_s": run, "active_threshold": "per-second RMS at least 10% of the stem's 95th percentile"}
    # novelty: checkerboard kernel on a Euclidean-similarity matrix of per-second features
    w = 8; X = sec.T; D2 = ((X[:, None, :] - X[None, :, :]) ** 2).sum(-1); Sm = np.exp(-D2 / (2 * np.median(D2[D2 > 0]) + 1e-9))
    g = np.exp(-0.5 * (np.arange(-w, w) + 0.5) ** 2 / (w / 2) ** 2); kern = np.outer(g, g) * np.outer(np.sign(np.arange(-w, w) + 0.5), np.sign(np.arange(-w, w) + 0.5))
    P = np.pad(Sm, w, mode="edge"); nov = np.array([(P[i:i + 2 * w, i:i + 2 * w] * kern).sum() for i in range(ns)]); nov = np.clip(nov, 0, None); nov = nov / (nov.max() + 1e-9)
    pk, pr = find_peaks(nov, height=float(nov.mean() + 0.75 * nov.std()), distance=8); peaks = []
    for i in pk:
        a0, b0, c0 = max(i - 8, 0), i, min(i + 8, ns)
        if b0 - a0 < 2 or c0 - b0 < 2: continue
        dl = sec[:, b0:c0].mean(axis=1) - sec[:, a0:b0].mean(axis=1)
        peaks.append({"t_s": int(i), "novelty": round(float(nov[i]), 3), "stems_up": [fnames[k] for k in range(len(fnames)) if dl[k] > 0.5], "stems_down": [fnames[k] for k in range(len(fnames)) if dl[k] < -0.5], "delta_z": {fnames[k]: round(float(dl[k]), 2) for k in range(len(fnames))}})
    # recurrence: beat-synchronous (stem activity z + chroma), mean similarity at each beat lag
    rec = {"note": "too few beats for a recurrence estimate"}
    if len(bt) >= 48:
        bfr = librosa.time_to_frames(bt, sr=sr, hop_length=hop); bfr = bfr[bfr < nf]; edges = list(bfr) + [nf]
        B = np.array([np.concatenate([fz[:, a:max(b, a + 1)].mean(axis=1), librosa.util.normalize(chroma[:, a:max(b, a + 1)].mean(axis=1))]) for a, b in zip(edges[:-1], edges[1:])])
        B = (B - B.mean(0)) / (B.std(0) + 1e-6); B = B / (np.linalg.norm(B, axis=1, keepdims=True) + 1e-9); nb = len(B); maxL = min(128, nb - 16)
        rr = np.array([float((B[:-L] * B[L:]).sum(1).mean()) for L in range(1, maxL + 1)]); Ls = np.arange(1, maxL + 1)
        pkl, _ = find_peaks(rr); pkl = [i for i in pkl if Ls[i] >= 2]; top = sorted(pkl, key=lambda i: -rr[i])[:6]
        step = float(np.median(np.diff(bt)))
        cand = [{"lag_beats": int(Ls[i]), "lag_bars_if_4_4": round(float(Ls[i] / 4), 2), "lag_s": round(float(Ls[i] * step), 2), "similarity": round(float(rr[i]), 3)} for i in top]
        small = None
        if top:
            mx = rr[top[0]]; small = next((c for c in sorted(cand, key=lambda c: c["lag_beats"]) if c["similarity"] >= 0.9 * mx), None)
        rec = {"method": "beat-synchronous features (stem-activity z-scores + chroma), mean cosine similarity of beat i and i+L over all i", "beat_step_s": round(step, 3), "beats_used": nb, "assumes": "4 beats per bar for the bar conversion; beat grid is the whole-mix beat tracker (see summary.tempo_resolved for its level vs the kick grid)",
            "similarity_by_lag_beats": {str(int(L)): round(float(v), 3) for L, v in zip(Ls, rr) if L <= 64}, "peak_lags": cand, "loop_length_estimate": small,
            "loop_length_rule": "smallest peak lag whose similarity is at least 90% of the highest peak (multiples of a loop also peak, so the strongest peak is often a multiple)"}
    return {"tag": "OBS", "video": VID, "feature_source": src, "stem_activity": act_info,
        "novelty": {"method": "checkerboard kernel (half-width 8 s) on a Euclidean-similarity matrix of per-second stem-activity z-scores; peaks above mean+0.75 sd, at least 8 s apart", "per_second": [round(float(v), 3) for v in nov], "peaks": peaks,
            "peak_note": "stems_up/stems_down: stems whose mean level changes by more than 0.5 sd between the 8 s before and the 8 s after the peak"},
        "recurrence": rec,
        "sections_auto_secondary": {"label": "SECONDARY: automatic segmentation (agglomerative, k=10, on beat-synced chroma+MFCC), not stem-based; labels A-E are clusters, not musical section names", "sections": sections}}
try: json.dump(form_analysis(), open(f"{D}/form.json", "w"), indent=1)
except Exception as e: json.dump({"tag": "OBS", "error": repr(e)}, open(f"{D}/form.json", "w"), indent=1)
# production-era features
try:
    yf, _ = librosa.load(A, sr=None, mono=False); ym = np.atleast_2d(yf); pk_amp = float(np.abs(ym).max()); peak_db = 20 * np.log10(max(pk_amp, 1e-9))
    rms_all = float(np.sqrt(np.mean(ym ** 2))); crest = 20 * np.log10(max(pk_amp, 1e-9) / max(rms_all, 1e-9))
    spread = None; kick_n = 0
    kick_src = None
    if os.path.exists(drums_path):
        kick_src = yd
    else: kick_src = y
    from scipy.signal import butter, sosfiltfilt
    lowf = sosfiltfilt(butter(4, [40, 120], "bandpass", fs=sr, output="sos"), kick_src)
    ko = librosa.onset.onset_strength(y=lowf, sr=sr, hop_length=hop); kf = librosa.onset.onset_detect(onset_envelope=ko, sr=sr, hop_length=hop, units="frames")
    kt = librosa.frames_to_time(kf, sr=sr, hop_length=hop); kick_n = int(len(kt))
    if len(bt) > 4 and kick_n > 4:
        step = float(np.median(np.diff(bt))); off = [min(((k - b) / step + 0.5) % 1 - 0.5 for b in [bt[np.abs(bt - k).argmin()]]) for k in kt]
        spread = float(np.std(off) * step * 1000)
    Sp = np.abs(librosa.stft(y, hop_length=hop)) ** 2; fr = librosa.fft_frequencies(sr=sr); tot = float(Sp.sum()) + 1e-12
    band = float(Sp[(fr >= 300) & (fr <= 3400)].sum()) / tot; low = float(Sp[fr < 300].sum()) / tot; high = float(Sp[fr > 3400].sum()) / tot
    # loop regularity: similarity of consecutive bars (4 beats) in chroma+onset terms; high = machine-like repetition
    reg = None
    if len(bt) >= 16:
        bars = [chroma[:, bf2:bf3].mean(axis=1) for bf2, bf3 in zip(librosa.time_to_frames(bt[::4], sr=sr, hop_length=hop)[:-1], librosa.time_to_frames(bt[::4], sr=sr, hop_length=hop)[1:]) if bf3 > bf2]
        if len(bars) > 4: reg = float(np.mean([np.corrcoef(bars[i], bars[i + 1])[0, 1] for i in range(len(bars) - 1)]))
    hints = []
    if peak_db > -1: hints.append(f"peak {peak_db:.1f} dBFS is near full scale")
    hints.append(f"crest factor {crest:.1f} dB ({'heavily compressed/limited, modern loudness-war style' if crest < 9 else 'moderate dynamics' if crest < 14 else 'wide dynamics, older or unlimited mastering'})")
    if spread is not None: hints.append(f"kick-onset spread {spread:.0f} ms around the beat grid ({'tight, quantised or sequenced' if spread < 25 else 'loose, human-played or live feel'}; the grid itself is estimated, so treat as indicative)")
    hints.append(f"{band*100:.0f}% of energy in 300-3400 Hz vs {(low+high)*100:.0f}% outside ({'narrow, telephone/radio-like band' if band > 0.6 else 'full-range mix'})")
    if reg is not None: hints.append(f"bar-to-bar chroma similarity {reg:.2f} ({'loop-like, repetitive' if reg > 0.9 else 'varied'})")
    summary["production_era"] = {"peak_dbfs": round(peak_db, 2), "rms_dbfs": round(20 * np.log10(max(rms_all, 1e-9)), 2), "crest_factor_db": round(crest, 2),
        "kick_onset_spread_ms": None if spread is None else round(spread, 1), "kick_onsets_n": kick_n, "kick_source": "drums stem" if os.path.exists(drums_path) else "whole mix (40-120 Hz band)",
        "energy_ratio_300_3400hz_to_full": round(band, 3), "energy_below_300hz": round(low, 3), "energy_above_3400hz": round(high, 3), "loop_regularity_bar_chroma_corr": None if reg is None else round(reg, 3),
        "hint": "Indicative only, not a dating of the recording: " + "; ".join(hints) + "."}
except Exception as e: summary["production_era"] = {"error": repr(e)}
json.dump(summary, open(f"{D}/summary.json", "w"), indent=1)
json.dump([round(float(b),3) for b in bt], open(f"{D}/beat_times.json", "w"))
fig, ax = plt.subplots(4, 1, figsize=(16, 11), sharex=True)
ax[0].plot(t, rms); ax[0].set_ylabel("loudness (RMS)")
ax[1].plot(t, cent, lw=.5); ax[1].set_ylabel("brightness (centroid Hz)")
librosa.display.specshow(chroma, sr=sr, hop_length=hop, x_axis="time", y_axis="chroma", ax=ax[2]); ax[2].set_ylabel("chroma")
ax[3].plot(t[:len(tg)], tg, lw=.5); ax[3].set_ylabel("local tempo")
for a in ax:
    for s in sections: a.axvline(s["start"], color="r", ls="--", lw=.8)
for s in sections: ax[0].text(s["start"]+1, rms.max()*.9, s["label"], color="r")
ax[3].set_xticks(np.arange(0, dur, 10)); plt.tight_layout(); plt.savefig(f"{D}/overview.png", dpi=80)
S = librosa.amplitude_to_db(np.abs(librosa.stft(y, hop_length=hop)), ref=np.max)
plt.figure(figsize=(16, 5)); librosa.display.specshow(S, sr=sr, hop_length=hop, x_axis="time", y_axis="log"); plt.xticks(np.arange(0, dur, 10)); plt.tight_layout(); plt.savefig(f"{D}/spectrogram.png", dpi=80)
print(json.dumps({k: summary[k] for k in ("tempo_bpm","key_whole_song_top3","loudest_moment_s","tempo_local_percentiles")}), "\n", [(s["start"], s["label"]) for s in sections])
