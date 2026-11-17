"""Shared helpers for numbered scripts: mandatory VID and video-file lookup (any extension)."""
import os, sys
EXTS = (".mp4", ".mkv", ".mov", ".webm")
def require_vid():
    v = os.environ.get("VID")
    if not v:
        sys.exit("ERROR: VID is mandatory (no default). Run as: VID=<video name without extension> python3 " + os.path.basename(sys.argv[0]))
    return v
def find_video(root, vid):
    """Return the path of <VIDEO_DIR or videos|testvideos>/<vid>.<ext> for any supported extension, or exit with a clear error."""
    dirs = [os.environ["VIDEO_DIR"]] if os.environ.get("VIDEO_DIR") else ["videos", "testvideos"]
    for d in dirs:
        for e in EXTS:
            p = os.path.join(root, d, vid + e)
            if os.path.exists(p): return p
    sys.exit(f"ERROR: no video file named {vid} with extension {'/'.join(EXTS)} in {', '.join(dirs)} (set VIDEO_DIR=<folder> if it lives elsewhere)")
