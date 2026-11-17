#!/bin/bash
# Video-agnostic entry point: runs the whole extraction pipeline for every video in videos/ (or the names given).
# Usage: [VIDEO_DIR=<folder>] [BLIND=1] v1/scripts/extract_all.sh [video_name ...]   (bare names or file paths; searched in videos/ then testvideos/ unless VIDEO_DIR is set)
# Each step writes a .done marker (v1/data/<V>/.done/<step>) only on success, so re-runs skip finished steps and a failed step stops the run.
# BLIND=1: do not create context.md (blind runs must not see it) and check_outputs runs with --blind.
set -eo pipefail
cd "$(dirname "$0")/../.."
S=v1/scripts; L=v1/logs; mkdir -p $L
# Refuse to run twice at once (lock file holds the PID; stale locks from dead PIDs are replaced)
LOCK=$L/extract_all.lock
if [ -f "$LOCK" ] && kill -0 "$(cat "$LOCK" 2>/dev/null)" 2>/dev/null; then echo "ERROR: another extract_all.sh is running (PID $(cat "$LOCK"), lock $LOCK)" >&2; exit 1; fi
echo $$ > "$LOCK"; trap 'rm -f "$LOCK"' EXIT
# Where to look: $VIDEO_DIR if set, otherwise videos/ then testvideos/ (child scripts use the same rule). Do not export a default.
DIRS=${VIDEO_DIR:-"videos testvideos"}
if [ $# -gt 0 ]; then NAMES=""; for a in "$@"; do b=$(basename "$a"); case "$b" in *.mp4|*.mkv|*.mov|*.webm) b="${b%.*}";; esac; NAMES="$NAMES $b"; done  # bare names, or file paths
else
  NAMES=$(for d in $DIRS; do for f in $d/*.mp4 $d/*.mkv $d/*.mov $d/*.webm; do [ -f "$f" ] && basename "${f%.*}"; done; done | sort -u)
fi
[ -n "$NAMES" ] || { echo "ERROR: no videos found in $DIRS (mp4/mkv/mov/webm)" >&2; exit 1; }
FIND_VIDEO() { for d in $DIRS; do for e in mp4 mkv mov webm; do [ -f "$d/$1.$e" ] && { echo "$d/$1.$e"; return; }; done; done; return 1; }
# Preflight: free space on the repo filesystem (MIN_FREE_MB overrides the 2048 MB floor; the need is the larger of the floor and 10x the biggest video's size)
FREE_MB=$(df -Pm . | awk 'NR==2{print $4}')
NEED_MB=${MIN_FREE_MB:-2048}
for V in $NAMES; do  # need the larger of the floor and 10x the biggest video (frames, WAVs, stems)
  F0=$(FIND_VIDEO $V) || continue; SZ=$(( $(stat -c %s "$F0") / 1048576 * 10 )); [ "$SZ" -gt "$NEED_MB" ] && NEED_MB=$SZ
done
if [ "${FREE_MB:-0}" -lt "$NEED_MB" ]; then
  echo "ERROR: only ${FREE_MB} MB free on the repo filesystem; need about ${NEED_MB} MB. Free space first, e.g.: python3 -m pip cache purge ; rm -rf ~/.cache/huggingface/hub/<unused model> ; (stems_raw/ and frames_1fps/ are regenerable). Then re-run." >&2
  exit 1
fi
# Preflight: drawtext (contact-sheet timestamps) needs ffmpeg built with freetype and at least one fontconfig font
ffmpeg -hide_banner -filters 2>/dev/null | grep -q drawtext || { echo "ERROR: this ffmpeg has no drawtext filter (needs libfreetype). Install a full ffmpeg build." >&2; exit 1; }
{ command -v fc-list >/dev/null && [ -n "$(fc-list 2>/dev/null | head -1)" ]; } || { echo "ERROR: no fontconfig fonts found (fc-list empty or missing); drawtext will fail. Install one, e.g. apt-get install -y fontconfig fonts-dejavu-core" >&2; exit 1; }
# step <name> <log> <command...>: run unless done; stdout+stderr to the log (warnings filtered for reading); abort on failure
step() {
  local n=$1 log=$2; shift 2
  [ -f v1/data/$V/.done/$n ] && return 0
  echo "[$V] $n ..."
  if "$@" > $L/$log.raw 2>&1; then grep -vi warn $L/$log.raw > $L/$log || true; rm -f $L/$log.raw; mkdir -p v1/data/$V/.done; touch v1/data/$V/.done/$n
  else echo "ERROR: step '$n' failed for $V; last 20 lines of $L/$log.raw (the filtered log is not written on failure):" >&2; tail -n 20 $L/$log.raw >&2; exit 1; fi
}
for V in $NAMES; do
  export VID=$V
  F=$(FIND_VIDEO $V) || { echo "ERROR: no $V.{mp4,mkv,mov,webm} in $DIRS (set VIDEO_DIR=<folder> if elsewhere)" >&2; exit 1; }
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
# Whole-run marker, written only after every step and the output check succeeded
for V in $NAMES; do mkdir -p v1/data/$V/.done; touch v1/data/$V/.done/extract_all; done
echo "extract_all done: $NAMES"
echo "Ready-to-paste workflow args (add blind/out as needed; one line per video folder):"
python3 - "$DIRS" $NAMES <<'PY'
import json, sys, os
dirs = sys.argv[1].split(); groups = {}
for v in sys.argv[2:]:
    d = json.load(open(f"v1/data/{v}/audio_features/summary.json")).get("duration_s")
    vd = next((x for x in dirs if any(os.path.isfile(f"{x}/{v}.{e}") for e in ("mp4", "mkv", "mov", "webm"))), dirs[0])
    groups.setdefault(vd, []).append({"vid": v, "dur": d})
for vd, vs in groups.items():
    print(json.dumps({"videos": vs, "video_dir": vd}))
PY
