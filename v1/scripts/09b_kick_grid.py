"""Build a beat-grid override for 09_sync.py from the drums-stem kick (40-120 Hz onsets), video-agnostic.
Usage: VID=<video> python 09b_kick_grid.py --period 0.49995 --anchor 88.6 [--bar-beats 4] [--name grid_120bpm]
--period: beat period in s (from your own kick fit); --anchor: approximate time of a known downbeat (s); the exact anchor is the median
offset of kick onsets snapped to the period grid (+-80 ms) after the anchor, with the period held fixed. Grid runs from <=0 to the end of the stem.
Writes v1/data/<VID>/sync/<name>.json {beats_s, downbeat_index, period_s, anchor_s, bar_s, ...}"""
import json, os, sys, argparse
import numpy as np, librosa
ap = argparse.ArgumentParser(); ap.add_argument("--vid"); ap.add_argument("--period", type=float, required=True); ap.add_argument("--anchor", type=float, required=True)
ap.add_argument("--bar-beats", type=int, default=4); ap.add_argument("--name", default="grid"); a = ap.parse_args()
VID = a.vid or os.environ.get("VID")
if not VID: sys.exit("VID is mandatory")
root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
D = os.path.join(root, f"v1/data/{VID}"); os.makedirs(f"{D}/sync", exist_ok=True)
y, sr = librosa.load(f"{D}/stems/drums.mp3", sr=22050, mono=True); dur = len(y) / sr; hop = 128
S = np.abs(librosa.stft(y, n_fft=2048, hop_length=hop)); f = librosa.fft_frequencies(sr=sr, n_fft=2048)
k = S[(f >= 40) & (f <= 120)].sum(0); on = np.maximum(0, np.diff(k, prepend=k[0])); t = librosa.frames_to_time(np.arange(len(on)), sr=sr, hop_length=hop)
thr = np.percentile(on, 99); P = a.period; offs = []
for n in range(0, int((dur - a.anchor) / P)):
    g = a.anchor + n * P; m = (t > g - .08) & (t < g + .08)
    if m.any():
        i = int(np.argmax(on * m))
        if on[i] > thr: offs.append(t[i] - n * P)
anchor = float(np.median(offs)); sd = float(np.std(offs))
n0 = int(np.floor(anchor / P)); first = anchor - n0 * P
beats = np.arange(first, dur, P); di = int(round((anchor - first) / P))
out = {"source": f"drums-stem kick fit ({VID}); period fixed by caller, anchor = median snapped kick offset", "period_s": P, "bpm": round(60 / P, 3), "anchor_downbeat_s": round(anchor, 4),
       "n_kicks_used": len(offs), "kick_offset_sd_s": round(sd, 4), "bar_beats": a.bar_beats, "bar_s": round(P * a.bar_beats, 4), "downbeat_index": di, "beats_s": [round(float(b), 4) for b in beats]}
json.dump(out, open(f"{D}/sync/{a.name}.json", "w")); print({k: v for k, v in out.items() if k != "beats_s"}, len(beats), beats[:3])
