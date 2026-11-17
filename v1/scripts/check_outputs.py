"""Verify the extraction pipeline produced every expected, non-empty, plausible output for each video. Exit 1 if anything is wrong.
Usage: check_outputs.py [--blind] [video ...]   (default: every folder in v1/data)
--blind: context.md is not required (blind runs must not have one). Otherwise a context.md that is still the unfilled template
(contains '<!-- TEMPLATE' or the original template sentence, or is under 400 bytes) counts as missing/empty."""
import json, os, sys, glob
root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
args = sys.argv[1:]; blind = "--blind" in args; args = [a for a in args if a != "--blind"]
EXPECT = ["audio/song.wav", "contact_sheets/sheet_01.jpg", "frames_1fps/f_0001.jpg", "scenes/shots.json", "audio_features/summary.json",
          "audio_features/beat_times.json", "visual_features/per_second.json", "visual_features/cut_beat_alignment.json",
          "stems_raw/htdemucs/song/vocals.wav", "stems_raw/htdemucs/song/drums.wav", "stems_raw/htdemucs/song/bass.wav", "stems_raw/htdemucs/song/other.wav",
          "stems/stem_rms_per_second.json", "music_views/summary.json", "music_views/chords.json", "music_views/clap_tags.json", "sync/sync.json"]
if not blind: EXPECT.append("context.md")
TEMPLATE_MARKS = ("<!-- TEMPLATE", "Per-video facts discovered by agents (subject, artist, sources)")
vids = args or sorted(os.path.basename(p) for p in glob.glob(f"{root}/v1/data/*") if os.path.isdir(p))
bad = 0
for v in vids:
    D = f"{root}/v1/data/{v}"; miss = [e for e in EXPECT if not os.path.exists(f"{D}/{e}") or os.path.getsize(f"{D}/{e}") == 0]
    if not glob.glob(f"{D}/lyrics/*.txt") or not [p for p in glob.glob(f"{D}/lyrics/*.txt") if not p.endswith("_doubtful.txt")]: miss.append("lyrics/*.txt")
    if not glob.glob(f"{D}/music_views/window_*.png"): miss.append("music_views/window_*.png")
    try:
        dur = json.load(open(f"{D}/audio_features/summary.json"))["duration_s"]
        nf = len(glob.glob(f"{D}/frames_1fps/f_*.jpg"))
        if abs(nf - dur) > 2: miss.append(f"frames_1fps count {nf} != duration {dur:.1f} s (tolerance 2)")
        nw = len(glob.glob(f"{D}/music_views/window_*.png"))
        if nw and abs(nw - -(-dur // 20)) > 1: miss.append(f"music_views windows {nw} != ceil(duration/20)={int(-(-dur // 20))}")
    except Exception as e:
        miss.append(f"duration check impossible ({e.__class__.__name__}: {e})")
    cm = f"{D}/context.md"
    if not blind and os.path.exists(cm) and os.path.getsize(cm) > 0:
        t = open(cm).read()
        if any(m in t for m in TEMPLATE_MARKS) or len(t.encode()) < 400: miss.append("context.md is still the empty template")
    print(f"{v}: {'OK' if not miss else 'MISSING/BAD ' + '; '.join(miss)}"); bad += bool(miss)
sys.exit(1 if bad else 0)
