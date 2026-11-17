"""Pull one full-resolution frame at a time from the mp4 itself (not from sampled frames).
Usage: python3 v1/scripts/frame_at.py <video path or bare name> <t_seconds> [--out DIR]
Writes <video>_t<seconds>.png and .json (requested time, actual PTS from ffprobe, delta)."""
import argparse, json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from _common import find_video
root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video"); ap.add_argument("t", type=float); ap.add_argument("--out", default=".")
    a = ap.parse_args()
    v = a.video if os.path.exists(a.video) else find_video(root, os.path.splitext(os.path.basename(a.video))[0])
    name = os.path.splitext(os.path.basename(v))[0]; os.makedirs(a.out, exist_ok=True)
    tag = ("%g" % a.t); png = os.path.join(a.out, f"{name}_t{tag}.png")
    # -ss after -i: frame-accurate decode (slower than input seeking, but exact)
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", v, "-ss", str(a.t), "-frames:v", "1", png], capture_output=True, text=True)
    if r.returncode or not os.path.exists(png): sys.exit("ERROR: ffmpeg produced no frame (time beyond end?): " + r.stderr.strip()[-300:])
    # real PTS of the first frame at/after the requested time
    p = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-read_intervals", f"{max(a.t - 1, 0)}%{a.t + 1}",
                        "-show_entries", "frame=pts_time,best_effort_timestamp_time", "-of", "json", v], capture_output=True, text=True)
    pts = None
    try:
        fr = [float(f.get("pts_time") or f["best_effort_timestamp_time"]) for f in json.loads(p.stdout)["frames"]]
        fr = [x for x in fr if x >= a.t - 1e-6]; pts = min(fr) if fr else None
    except Exception: pass
    info = {"video": v, "requested_t": a.t, "actual_pts": pts, "delta_s": None if pts is None else round(pts - a.t, 4), "png": png}
    json.dump(info, open(png[:-4] + ".json", "w"), indent=1); print(json.dumps(info))
main()
