#!/bin/bash
# Video-agnostic entry point: runs the whole extraction pipeline for every video in videos/ (or the names given).
# Usage: [VIDEO_DIR=testvideos] [BLIND=1] v1/scripts/extract_all.sh [video_name ...]   (names without extension; any of mp4/mkv/mov/webm)
# Each step writes a .done marker (v1/data/<V>/.done/<step>) only on success, so re-runs skip finished steps and a failed step stops the run.
# BLIND=1: do not create context.md (blind runs must not see it) and check_outputs runs with --blind.
set -eo pipefail
cd "$(dirname "$0")/../.."
S=v1/scripts; L=v1/logs; mkdir -p $L
export VIDEO_DIR=${VIDEO_DIR:-videos}
if [ $# -gt 0 ]; then NAMES="$*"; else
  NAMES=$(for f in $VIDEO_DIR/*.mp4 $VIDEO_DIR/*.mkv $VIDEO_DIR/*.mov $VIDEO_DIR/*.webm; do [ -f "$f" ] && basename "${f%.*}"; done | sort -u)
fi
[ -n "$NAMES" ] || { echo "ERROR: no videos found in $VIDEO_DIR (mp4/mkv/mov/webm)" >&2; exit 1; }
FIND_VIDEO() { for e in mp4 mkv mov webm; do [ -f "$VIDEO_DIR/$1.$e" ] && { echo "$VIDEO_DIR/$1.$e"; return; }; done; return 1; }
# step <name> <log> <command...>: run unless done; stdout+stderr to the log (warnings filtered for reading); abort on failure
step() {
  local n=$1 log=$2; shift 2
  [ -f v1/data/$V/.done/$n ] && return 0
  echo "[$V] $n ..."
  if "$@" > $L/$log.raw 2>&1; then grep -vi warn $L/$log.raw > $L/$log || true; rm -f $L/$log.raw; mkdir -p v1/data/$V/.done; touch v1/data/$V/.done/$n
  else echo "ERROR: step '$n' failed for $V; see $L/$log.raw" >&2; exit 1; fi
}
for V in $NAMES; do
  export VID=$V
  F=$(FIND_VIDEO $V) || { echo "ERROR: no $VIDEO_DIR/$V.{mp4,mkv,mov,webm}" >&2; exit 1; }
  ffprobe -v error -select_streams a -show_entries stream=codec_type -of csv=p=0 "$F" | grep -q audio || { echo "ERROR: $F has no audio stream; this toolkit analyses the music, so it cannot continue" >&2; exit 1; }
  mkdir -p v1/data/$V
  # outputs that predate .done markers: adopt them (marker only if the key output exists and is non-empty)
  if [ ! -d v1/data/$V/.done ]; then
    adopt() { [ -s "v1/data/$V/$2" ] && { mkdir -p v1/data/$V/.done; touch v1/data/$V/.done/$1; echo "(adopted existing $1 for $V)"; } || true; }
    adopt extract contact_sheets/sheet_01.jpg; adopt scenes scenes/shots.json; adopt audio audio_features/summary.json; adopt visual visual_features/per_second.json
    adopt stems stems/stem_rms_per_second.json; adopt music_views music_views/summary.json; adopt clap music_views/clap_tags.json; adopt sync sync/sync.json
    ls v1/data/$V/lyrics/*auto_transcribe.txt >/dev/null 2>&1 && adopt whisper_transcribe lyrics/$(basename $(ls v1/data/$V/lyrics/*auto_transcribe.txt | head -1))
    ls v1/data/$V/lyrics/*translate.txt >/dev/null 2>&1 && adopt whisper_translate lyrics/$(basename $(ls v1/data/$V/lyrics/*translate.txt | head -1))
  fi
  step extract ${V}_extract $S/01_extract.sh
  step scenes ${V}_scenes python3 $S/02_scenes.py
  step audio ${V}_audio python3 $S/04_audio_features.py
  step visual ${V}_visual python3 $S/05_visual_features.py
  step whisper_transcribe ${V}_whisper python3 $S/03_whisper.py medium "" mix auto transcribe
  step whisper_translate ${V}_whisper_en python3 $S/03_whisper.py medium "" mix auto translate
  step stems ${V}_stems $S/06_stem_one.sh
  step music_views ${V}_music_views python3 $S/07_audio_views.py
  step clap ${V}_clap python3 $S/08_clap_tags.py
  step sync ${V}_sync python3 $S/09_sync.py
  if [ -z "$BLIND" ] && [ ! -f v1/data/$V/context.md ]; then
    printf "# Context for %s\n\n<!-- TEMPLATE: not yet filled in -->\nPer-video facts discovered by agents (subject, artist, sources). Toolkit prompts read this file; keep subject-specific knowledge here, not in the toolkit.\n" "$V" > v1/data/$V/context.md
  fi
done
CHK=""; [ -n "$BLIND" ] && CHK="--blind"
python3 $S/check_outputs.py $CHK $NAMES
echo "extract_all done: $NAMES"
echo "Ready-to-paste workflow args (video_dir: $VIDEO_DIR; add blind/out as needed):"
python3 - $NAMES <<'PY'
import json, sys, os
vd = os.environ.get("VIDEO_DIR", "videos"); vs = []
for v in sys.argv[1:]:
    d = json.load(open(f"v1/data/{v}/audio_features/summary.json")).get("duration_s")
    vs.append({"vid": v, "dur": d})
print(json.dumps({"videos": vs, "video_dir": vd}))
PY
