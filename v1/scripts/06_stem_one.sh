#!/bin/bash
# Video-agnostic source separation for one video (VID=<name>): demucs htdemucs -> stems_raw/ (git-ignored),
# per-second stem loudness + plot + small mp3 stems in stems/, then a whisper pass on the isolated vocals.
set -eo pipefail
cd "$(dirname "$0")/../.."
V=${VID:?ERROR: VID is mandatory (e.g. VID=video1 $0)}; D=v1/data/$V
# Existing stems count as complete only if all four exist and each lasts within 1 s of the source.
STEMS_OK() {
  python3 - "$D" <<'PY'
import sys, soundfile as sf
d = sys.argv[1]
try:
    src = sf.info(f"{d}/audio/song.wav").duration
    ok = all(abs(sf.info(f"{d}/stems_raw/htdemucs/song/{s}.wav").duration - src) <= 1.0 for s in ("vocals", "drums", "bass", "other"))
except Exception:
    ok = False
sys.exit(0 if ok else 1)
PY
}
if ! STEMS_OK; then
  # demucs writes to a temp directory; only a successful run is renamed into place (an interrupted run leaves no half stems)
  TMP=$D/stems_raw.tmp.$$; rm -rf $TMP; trap 'rm -rf $TMP' EXIT
  python3 -m demucs -n htdemucs -j 4 -o $TMP $D/audio/song.wav
  rm -rf $D/stems_raw; mv $TMP $D/stems_raw
  STEMS_OK || { echo "ERROR: demucs output incomplete or wrong length for $V" >&2; exit 1; }
fi
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
