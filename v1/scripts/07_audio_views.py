"""Music 'listening views' for agents (video-agnostic). Per 20 s window: a stacked image of the mix + stem mel-spectrograms,
chroma with estimated chords, onset/drum activity and vocal pitch contour. Plus whole-song chord timeline, melody notes,
loudness (LUFS-ish), stereo width and a section-level summary. Uses demucs stems if present, otherwise the mix only."""
import json, os, glob
import numpy as np, librosa, librosa.display, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from _common import require_vid, find_video
root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
VID = require_vid(); D = os.path.join(root, f"v1/data/{VID}"); O = os.path.join(D, "music_views"); os.makedirs(O, exist_ok=True)
SR = 22050; HOP = 512
mix, _ = librosa.load(f"{D}/audio/song.wav", sr=SR, mono=True)
st_dir = glob.glob(f"{D}/stems_raw/htdemucs/song")
stems = {k: librosa.load(f"{st_dir[0]}/{k}.wav", sr=SR, mono=True)[0] for k in ("vocals", "drums", "bass", "other")} if st_dir else {}
dur = len(mix) / SR
# --- chords: beat-synchronous chroma vs 24 triad templates (+ 'N' for no chord) ---
NAMES = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
harm = stems.get("other", mix) + stems.get("bass", 0 * mix) if stems else librosa.effects.harmonic(mix)
chroma = librosa.feature.chroma_cqt(y=harm, sr=SR, hop_length=HOP)
tpl, lab = [], []
for i in range(12):
    for q, iv in (("", (0, 4, 7)), ("m", (0, 3, 7))):
        v = np.zeros(12); v[[(i + k) % 12 for k in iv]] = 1; tpl.append(v / np.linalg.norm(v)); lab.append(NAMES[i] + q)
tpl = np.array(tpl)
_, beats = librosa.beat.beat_track(y=mix, sr=SR, hop_length=HOP); bt = librosa.frames_to_time(beats, sr=SR, hop_length=HOP)
cs = librosa.util.sync(chroma, beats, aggregate=np.median); cn = cs / (np.linalg.norm(cs, axis=0, keepdims=True) + 1e-9)
sc = tpl @ cn; best = sc.argmax(0); conf = sc.max(0)
edges = np.concatenate([[0], bt, [dur]])
chords = []
for j, b in enumerate(best):
    name = lab[b] if conf[j] > 0.6 else "N"
    if chords and chords[-1]["chord"] == name: chords[-1]["end"] = round(float(edges[j + 1]), 2)
    else: chords.append({"start": round(float(edges[j]), 2), "end": round(float(edges[j + 1]), 2), "chord": name})
chords = [c for c in chords if c["end"] - c["start"] >= 0.4]
json.dump(chords, open(f"{O}/chords.json", "w"))
from collections import Counter
cc = Counter(); [cc.update({c["chord"]: c["end"] - c["start"]}) for c in chords]
# --- melody of the vocal (or lead) stem via pYIN ---
lead = stems.get("vocals", mix)
f0, vflag, _ = librosa.pyin(librosa.resample(lead, orig_sr=SR, target_sr=11025), fmin=70, fmax=1000, sr=11025, hop_length=256)
ft = librosa.times_like(f0, sr=11025, hop_length=256)
notes = []
for t, f, v in zip(ft, f0, vflag):
    if v and not np.isnan(f):
        n = librosa.hz_to_note(f)
        if notes and notes[-1]["note"] == n and t - notes[-1]["end"] < 0.05: notes[-1]["end"] = round(float(t), 2)
        else: notes.append({"start": round(float(t), 2), "end": round(float(t), 2), "note": n})
notes = [n for n in notes if n["end"] - n["start"] >= 0.12]
json.dump(notes, open(f"{O}/lead_notes.json", "w"))
# --- loudness, stereo width per second ---
st, _ = librosa.load(f"{D}/audio/song.wav", sr=SR, mono=False)
L, Rr = st[0], st[1]; per = []
for s in range(int(dur)):
    a, b = s * SR, (s + 1) * SR; l, r = L[a:b], Rr[a:b]; m = (l + r) / 2; sd = (l - r) / 2
    rms = np.sqrt(np.mean(m ** 2)) + 1e-12
    per.append({"t": s, "dbfs": round(float(20 * np.log10(rms)), 1), "width": round(float(np.sqrt(np.mean(sd ** 2)) / rms), 3),
                **({k: round(float(20 * np.log10(np.sqrt(np.mean(v[a:b] ** 2)) + 1e-9)), 1) for k, v in stems.items()} if stems else {})})
json.dump(per, open(f"{O}/per_second_levels.json", "w"))
# --- per-window images ---
def mel(ax, y, title):
    S = librosa.power_to_db(librosa.feature.melspectrogram(y=y, sr=SR, hop_length=HOP, n_mels=96), ref=np.max)
    librosa.display.specshow(S, sr=SR, hop_length=HOP, x_axis="time", y_axis="mel", ax=ax, vmin=-80, vmax=0); ax.set_ylabel(title); ax.set_xlabel("")
for w0 in range(0, int(np.ceil(dur)), 20):
    a, b = int(w0 * SR), int(min(dur, w0 + 20) * SR)
    rows = [("mix", mix)] + list(stems.items())
    fig, ax = plt.subplots(len(rows) + 2, 1, figsize=(14, 2.0 * (len(rows) + 2)))
    for i, (k, y) in enumerate(rows): mel(ax[i], y[a:b], k)
    c = chroma[:, a // HOP: b // HOP]; librosa.display.specshow(c, sr=SR, hop_length=HOP, x_axis="time", y_axis="chroma", ax=ax[-2]); ax[-2].set_ylabel("chroma")
    for ch in chords:
        if ch["end"] > w0 and ch["start"] < w0 + 20: ax[-2].text(max(ch["start"], w0) - w0, 11.3, ch["chord"], fontsize=8, color="w", va="top")
    ax[-1].set_xlim(0, 20); ax[-1].set_ylabel("lead pitch")
    for n in notes:
        if w0 <= n["start"] < w0 + 20: ax[-1].plot([n["start"] - w0, n["end"] - w0], [librosa.note_to_midi(n["note"])] * 2, lw=3)
    for x in ax: x.set_xlim(0, 20)
    ax[0].set_title(f"{VID} music view {w0//60}:{w0%60:02d}-{(w0+20)//60}:{(w0+20)%60:02d} (x axis = seconds into window)")
    plt.tight_layout(); plt.savefig(f"{O}/window_{w0:04d}s.png", dpi=60); plt.close()
summary = {"has_stems": bool(stems), "chord_time_share_top10": [(k, round(v, 1)) for k, v in cc.most_common(10)], "n_chord_changes": len(chords),
           "lead_note_range": [min((n["note"] for n in notes), key=librosa.note_to_midi), max((n["note"] for n in notes), key=librosa.note_to_midi)] if notes else None,
           "files": "chords.json, lead_notes.json, per_second_levels.json, window_XXXXs.png (one per 20 s)"}
json.dump(summary, open(f"{O}/summary.json", "w"), indent=1); print(json.dumps(summary))
