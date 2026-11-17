"""Shot/cut detection; saves shot list + a mid-shot keyframe per shot.
Two passes, merged (video-agnostic, no per-video constants):
 1. PySceneDetect ContentDetector (threshold 27.0): hard cuts.
 2. Dense pass over every frame (160x120 via ffmpeg): mean abs grey difference + colour-histogram distance, scored against the
    +-1 s local median/MAD, accepted as a cut only if it is a local peak, the structure correlation of the two neighbouring frames
    is low (<0.6: a new picture, not a tint swing or flicker) and the change is large (same rules as agents/dense_cuts.py 'likely_cut').
    This catches blurred whips, fades-through-blur and soft transitions the ContentDetector misses.
Cuts within MERGE_S of each other are merged (ContentDetector time kept). Output schema unchanged: list of
{shot,start,end,dur,keyframe}; each entry also gets 'src' ('content' or 'dense'). The previous shots.json is kept as shots_prev.json
(only if shots_prev.json does not exist yet, so the original ContentDetector list is never overwritten by a re-run).
Usage: VID=<video> python3 02_scenes.py   (VID mandatory)"""
import json, os, shutil, subprocess, sys
import numpy as np
from scenedetect import detect, ContentDetector
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from _common import require_vid, find_video
root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
VID = require_vid(); V = find_video(root, VID); D = os.path.join(root, f"v1/data/{VID}/scenes")
os.makedirs(os.path.join(D, "keyframes"), exist_ok=True)
SD_THR, DENSE_THR, DENSE_FLOOR, SCORR_MAX, MERGE_S = 27.0, 3.0, 0.25, 0.6, 0.2

# pass 1: ContentDetector
scenes = detect(V, ContentDetector(threshold=SD_THR))
cuts = [(s.get_seconds(), "content") for s, _ in scenes[1:]]

# pass 2: dense frame-difference
pr = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", V], capture_output=True, text=True)
fn, fd = pr.stdout.strip().split("/"); fps = float(fn) / float(fd)
W, H = 160, 120; fsz = W * H * 3
p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", V, "-vf", f"scale={W}:{H}", "-pix_fmt", "rgb24", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
def hist(f):
    q = (f // 64).reshape(-1, 3); h = np.bincount(q[:, 0] * 16 + q[:, 1] * 4 + q[:, 2], minlength=64).astype(float); return h / h.sum()
prev = ph = None; diffs = []; hd = []; grays = []
while True:
    b = p.stdout.read(fsz)
    if len(b) < fsz: break
    f = np.frombuffer(b, np.uint8).reshape(H, W, 3); h = hist(f); g = f.astype(float).mean(axis=2)
    diffs.append(float(np.abs(g - prev).mean()) if prev is not None else 0.0); hd.append(float(0.5 * np.abs(h - ph).sum()) if prev is not None else 0.0)
    grays.append(g.astype(np.float32)); prev, ph = g, h
p.wait()
comb = np.array(diffs) / 255.0 * 10 + np.array(hd) * 4; k = max(1, int(round(fps))); score = np.zeros(len(comb))
for j in range(len(comb)):
    nb = np.concatenate([comb[max(0, j - k):j], comb[j + 1:min(len(comb), j + k + 1)]])
    if len(nb): m = np.median(nb); score[j] = (comb[j] - m) / (np.median(np.abs(nb - m)) + 0.02)
def scorr(j):
    a, c = grays[j - 1], grays[j]; a = (a - a.mean()) / (a.std() + 1e-6); c = (c - c.mean()) / (c.std() + 1e-6); return float((a * c).mean())
dense = []
for j in range(1, len(comb)):
    lo, hi = max(1, j - 2), min(len(comb), j + 3)
    if score[j] >= DENSE_THR and comb[j] >= DENSE_FLOOR and score[j] == score[lo:hi].max() and scorr(j) < SCORR_MAX: dense.append((j / fps, "dense"))

# merge: keep ContentDetector cuts, add dense cuts not within MERGE_S of any kept cut
allc = sorted(cuts, key=lambda c: c[0]); kept = list(allc)
for t, s in dense:
    if all(abs(t - c[0]) > MERGE_S for c in kept): kept.append((t, s))
kept.sort(key=lambda c: c[0])
dur_total = scenes[-1][1].get_seconds() if scenes else len(comb) / fps
bounds = [(0.0, "content")] + kept + [(dur_total, "end")]

# keep the original list once
sj = os.path.join(D, "shots.json"); sp = os.path.join(D, "shots_prev.json")
if os.path.exists(sj) and not os.path.exists(sp): shutil.copy(sj, sp)

out = []
for i in range(len(bounds) - 1):
    st, src = bounds[i]; et = bounds[i + 1][0]; mid = (st + et) / 2; n = i + 1
    kf = f"keyframes/shot_{n:03d}_{mid:07.2f}s.jpg"
    if not os.path.exists(os.path.join(D, kf)):
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{mid:.2f}", "-i", V, "-frames:v", "1", "-q:v", "3", os.path.join(D, kf)], check=True)
    out.append({"shot": n, "start": round(st, 2), "end": round(et, 2), "dur": round(et - st, 2), "keyframe": kf, "src": src if i else "content"})
json.dump(out, open(sj, "w"), indent=1)
print(len(out), "shots (", len(cuts), "content +", len(kept) - len(cuts), "dense); median dur", sorted(o["dur"] for o in out)[len(out) // 2] if out else None)
