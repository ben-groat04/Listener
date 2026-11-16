#!/bin/bash
# Sequential CPU jobs (4 cores): video1 extraction, then Dutch transcriptions for both.
cd "$(dirname "$0")/../.."
S=v1/scripts; L=v1/logs
VID=video1 $S/01_extract.sh > $L/v1_extract.log 2>&1
VID=video1 python3 $S/02_scenes.py 2>&1 | grep -v -i warn > $L/v1_scenes.log
VID=video1 python3 $S/04_audio_features.py 2>&1 | grep -v -i warn > $L/v1_audio.log
VID=video1 python3 $S/05_visual_features.py 2>&1 | grep -v -i warn > $L/v1_visual.log
VID=video2 python3 $S/05_visual_features.py 2>&1 | grep -v -i warn > $L/v2_visual.log
for V in video2 video1; do
  VID=$V python3 $S/03_whisper.py medium "" mix nl transcribe 2>&1 | grep -v -i warn > $L/${V}_whisper_nl.log
  VID=$V python3 $S/03_whisper.py medium "" mix nl translate 2>&1 | grep -v -i warn > $L/${V}_whisper_en.log
done
echo CHAIN DONE > $L/chain.done
