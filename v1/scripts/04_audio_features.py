"""Music descriptors via librosa: tempo/beats, key estimate, loudness & brightness curves, structural segmentation, charts."""
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
