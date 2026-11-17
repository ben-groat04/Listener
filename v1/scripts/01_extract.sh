#!/bin/bash
# Basic media extraction: audio, 1fps frames, contact sheets. VID is mandatory (video name without extension).
# Looks for $VIDEO_DIR (or videos/ then testvideos/) /<VID>.{mp4,mkv,mov,webm}. Outputs go to a temp dir and are moved into place only on success.
set -eo pipefail
cd "$(dirname "$0")/../.."
VID=${VID:?ERROR: VID is mandatory (e.g. VID=video1 $0)}
V=""
for d in ${VIDEO_DIR:-videos testvideos}; do for e in mp4 mkv mov webm; do [ -z "$V" ] && [ -f "$d/$VID.$e" ] && V="$d/$VID.$e"; done; done
[ -n "$V" ] || { echo "ERROR: no $VID.{mp4,mkv,mov,webm} in ${VIDEO_DIR:-videos or testvideos}" >&2; exit 1; }
ffprobe -v error -select_streams a -show_entries stream=codec_type -of csv=p=0 "$V" | grep -q audio || { echo "ERROR: $V has no audio stream; this toolkit needs audio" >&2; exit 1; }
D=v1/data/$VID; T=$D/.tmp_extract; rm -rf "$T"; mkdir -p $D/audio $T/frames $T/sheets
ffmpeg -loglevel error -y -i "$V" -vn -ac 2 -ar 44100 $T/song.wav
ffmpeg -loglevel error -y -i "$V" -vn -ac 1 -ar 16000 $T/song_16k_mono.wav
ffmpeg -loglevel error -y -i "$V" -vf fps=1 -q:v 3 $T/frames/f_%04d.jpg
# 5x4 grids of 1fps frames with timestamps burned in = 20s per sheet
ffmpeg -loglevel error -y -i "$V" -vf "fps=1,scale=300:240,drawtext=text='%{pts\:hms}':x=4:y=4:fontsize=18:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=5x4" -q:v 3 $T/sheets/sheet_%02d.jpg
[ -s $T/song.wav ] && [ -s $T/frames/f_0001.jpg ] && [ -s $T/sheets/sheet_01.jpg ] || { echo "ERROR: extraction produced empty output for $V" >&2; exit 1; }
rm -rf $D/frames_1fps $D/contact_sheets; mkdir -p $D/scenes
mv $T/song.wav $T/song_16k_mono.wav $D/audio/; mv $T/frames $D/frames_1fps; mv $T/sheets $D/contact_sheets; rmdir $T
echo extract done
