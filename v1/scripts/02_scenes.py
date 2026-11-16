"""Shot/cut detection with PySceneDetect; saves shot list + a mid-shot keyframe per shot."""
import json, os, subprocess, sys
from scenedetect import detect, ContentDetector
root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
VID = os.environ.get("VID", "video2")
V = os.path.join(root, f"{os.environ.get('VIDEO_DIR', 'videos')}/{VID}.mp4"); D = os.path.join(root, f"v1/data/{VID}/scenes")
os.makedirs(os.path.join(D, "keyframes"), exist_ok=True)
scenes = detect(V, ContentDetector(threshold=27.0))
out = []
for i, (s, e) in enumerate(scenes, 1):
    st, et = s.get_seconds(), e.get_seconds(); mid = (st + et) / 2
    kf = f"keyframes/shot_{i:03d}_{mid:07.2f}s.jpg"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{mid:.2f}", "-i", V, "-frames:v", "1", "-q:v", "3", os.path.join(D, kf)], check=True)
    out.append({"shot": i, "start": round(st, 2), "end": round(et, 2), "dur": round(et - st, 2), "keyframe": kf})
json.dump(out, open(os.path.join(D, "shots.json"), "w"), indent=1)
print(len(out), "shots; median dur", sorted(o["dur"] for o in out)[len(out)//2] if out else None)
