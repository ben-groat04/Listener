#!/bin/bash
# Video-agnostic source separation for one video (VID=<name>): demucs htdemucs -> stems_raw/ (git-ignored),
# per-second stem loudness + plot + small mp3 stems in stems/, then a whisper pass on the isolated vocals.
cd "$(dirname "$0")/../.."
V=${VID:?set VID}; D=v1/data/$V
[ -f $D/stems_raw/htdemucs/song/vocals.wav ] || python3 -m demucs -n htdemucs -j 4 -o $D/stems_raw $D/audio/song.wav
python3 - "$V" <<'PY'
import json, os, sys, numpy as np, librosa, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
V = sys.argv[1]; d = f"v1/data/{V}/stems_raw/htdemucs/song"; o = f"v1/data/{V}/stems"; os.makedirs(o, exist_ok=True); out = {}
for st in ("vocals", "drums", "bass", "other"):
    y, sr = librosa.load(f"{d}/{st}.wav", sr=11025, mono=True)
    out[st] = [round(float(x), 4) for x in librosa.feature.rms(y=y, frame_length=sr, hop_length=sr)[0]]
    os.system(f"ffmpeg -loglevel error -y -i {d}/{st}.wav -b:a 96k {o}/{st}.mp3")
json.dump(out, open(f"{o}/stem_rms_per_second.json", "w"))
plt.figure(figsize=(16, 5))
for st, v in out.items(): plt.plot(v, label=st)
plt.legend(); plt.xticks(range(0, len(out["vocals"]), 10)); plt.grid(alpha=.3); plt.title(f"{V} stem loudness per second"); plt.tight_layout(); plt.savefig(f"{o}/stems.png", dpi=80)
PY
ls $D/lyrics/*vocals* >/dev/null 2>&1 || VID=$V python3 v1/scripts/03_whisper.py medium $D/stems_raw/htdemucs/song/vocals.wav vocals auto transcribe 2>&1 | grep -vi warn | tail -1
