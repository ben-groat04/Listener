#!/bin/bash
# Video-agnostic entry point: runs the whole extraction pipeline for every videos/*.mp4 (or the names given).
# Usage: [VIDEO_DIR=testvideos] v1/scripts/extract_all.sh [video_name ...]   (names without .mp4; default folder videos/)
cd "$(dirname "$0")/../.."
S=v1/scripts; L=v1/logs; mkdir -p $L
export VIDEO_DIR=${VIDEO_DIR:-videos}
NAMES=${@:-$(ls $VIDEO_DIR/*.mp4 | xargs -n1 basename | sed 's/\.mp4$//')}
for V in $NAMES; do
  export VID=$V
  [ -d v1/data/$V/contact_sheets ] || $S/01_extract.sh > $L/${V}_extract.log 2>&1
  [ -f v1/data/$V/scenes/shots.json ] || python3 $S/02_scenes.py 2>&1 | grep -vi warn > $L/${V}_scenes.log
  [ -f v1/data/$V/audio_features/summary.json ] || python3 $S/04_audio_features.py 2>&1 | grep -vi warn > $L/${V}_audio.log
  [ -f v1/data/$V/visual_features/per_second.json ] || python3 $S/05_visual_features.py 2>&1 | grep -vi warn > $L/${V}_visual.log
  ls v1/data/$V/lyrics/*auto_transcribe.txt >/dev/null 2>&1 || python3 $S/03_whisper.py medium "" mix auto transcribe 2>&1 | grep -vi warn > $L/${V}_whisper.log
  ls v1/data/$V/lyrics/*translate.txt >/dev/null 2>&1 || python3 $S/03_whisper.py medium "" mix auto translate 2>&1 | grep -vi warn > $L/${V}_whisper_en.log
  [ -f v1/data/$V/context.md ] || printf "# Context for %s\n\nPer-video facts discovered by agents (subject, artist, sources). Toolkit prompts read this file; keep subject-specific knowledge here, not in the toolkit.\n" "$V" > v1/data/$V/context.md
done
echo "extract_all done: $NAMES"
