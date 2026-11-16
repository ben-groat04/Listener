#!/bin/bash
# Basic media extraction: audio, 1fps frames, contact sheets, scene cuts.
set -e
cd "$(dirname "$0")/../.."
VID=${VID:-video2}; V=videos/$VID.mp4; D=v1/data/$VID
mkdir -p $D/audio $D/frames_1fps $D/contact_sheets $D/scenes
ffmpeg -loglevel error -y -i $V -vn -ac 2 -ar 44100 $D/audio/song.wav
ffmpeg -loglevel error -y -i $V -vn -ac 1 -ar 16000 $D/audio/song_16k_mono.wav
ffmpeg -loglevel error -y -i $V -vf fps=1 -q:v 3 $D/frames_1fps/f_%04d.jpg
# 5x4 grids of 1fps frames with timestamps burned in = 20s per sheet
ffmpeg -loglevel error -y -i $V -vf "fps=1,scale=300:240,drawtext=text='%{pts\:hms}':x=4:y=4:fontsize=18:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=5x4" -q:v 3 $D/contact_sheets/sheet_%02d.jpg
echo extract done
