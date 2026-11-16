"""Music descriptors via librosa: tempo/beats, key estimate, loudness & brightness curves, structural segmentation, charts."""
import json, os
import numpy as np, librosa, librosa.display, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
VID = os.environ.get("VID", "video2")
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
           "key_whole_song_top3": key(chroma), "keys_per_30s": keys_windowed, "sections_auto": sections,
           "loudness_rms_mean": float(rms.mean()), "loudest_moment_s": float(t[rms.argmax()]), "quietest_moment_s_after_5s": float(t[t>5][rms[t>5].argmin()]),
           "tempo_local_percentiles": {p: float(np.percentile(tg, p)) for p in (10, 50, 90)},
           "per_second": [{"t": s, "rms": round(float(rms[(t>=s)&(t<s+1)].mean()),4), "brightness_hz": round(float(cent[(t>=s)&(t<s+1)].mean())), "onset": round(float(onset[(t>=s)&(t<s+1)].mean()),3)} for s in range(int(dur))]}
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
