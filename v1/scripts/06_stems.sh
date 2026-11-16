#!/bin/bash
# Source separation (vocals/drums/bass/other) with demucs htdemucs, then stem loudness curves.
cd "$(dirname "$0")/../.."
for V in video2 video1; do
  python3 -m demucs -n htdemucs -j 4 -o v1/data/$V/stems_raw v1/data/$V/audio/song.wav
done
python3 - <<'PY'
import json, glob, os, numpy as np, librosa
for V in ("video1", "video2"):
    d = glob.glob(f"v1/data/{V}/stems_raw/htdemucs/song")[0]; out = {}
    for st in ("vocals", "drums", "bass", "other"):
        y, sr = librosa.load(f"{d}/{st}.wav", sr=11025, mono=True)
        r = librosa.feature.rms(y=y, hop_length=sr)[0]; out[st] = [round(float(x), 4) for x in r]
    os.makedirs(f"v1/data/{V}/stems", exist_ok=True); json.dump(out, open(f"v1/data/{V}/stems/stem_rms_per_second.json", "w"))
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    plt.figure(figsize=(16, 5))
    for st, v in out.items(): plt.plot(v, label=st)
    plt.legend(); plt.xticks(range(0, len(out["vocals"]), 10)); plt.grid(alpha=.3); plt.title(f"{V} stem loudness per second"); plt.tight_layout(); plt.savefig(f"v1/data/{V}/stems/stems.png", dpi=80)
    for st in ("vocals", "drums", "bass", "other"):  # small mp3s that can be committed
        os.system(f"ffmpeg -loglevel error -y -i {d}/{st}.wav -b:a 96k v1/data/{V}/stems/{st}.mp3")
print("stems done")
PY
VID=video2 python3 v1/scripts/03_whisper.py medium v1/data/video2/stems_raw/htdemucs/song/vocals.wav vocals auto transcribe
echo STEMS DONE > v1/logs/stems.done
