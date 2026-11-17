"""Verify the extraction pipeline produced every expected, non-empty output for each video. Exit 1 if anything is missing.
Usage: check_outputs.py [video ...]   (default: every folder in v1/data)"""
import json, os, sys, glob
root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
EXPECT = ["audio/song.wav", "contact_sheets/sheet_01.jpg", "frames_1fps/f_0001.jpg", "scenes/shots.json", "audio_features/summary.json",
          "audio_features/beat_times.json", "visual_features/per_second.json", "visual_features/cut_beat_alignment.json",
          "stems/stem_rms_per_second.json", "music_views/summary.json", "music_views/chords.json", "music_views/clap_tags.json", "context.md"]
vids = sys.argv[1:] or sorted(os.path.basename(p) for p in glob.glob(f"{root}/v1/data/*") if os.path.isdir(p))
bad = 0
for v in vids:
    D = f"{root}/v1/data/{v}"; miss = [e for e in EXPECT if not os.path.exists(f"{D}/{e}") or os.path.getsize(f"{D}/{e}") == 0]
    lyr = glob.glob(f"{D}/lyrics/*.txt")
    if not lyr: miss.append("lyrics/*.txt")
    print(f"{v}: {'OK' if not miss else 'MISSING ' + ', '.join(miss)}"); bad += bool(miss)
sys.exit(1 if bad else 0)
