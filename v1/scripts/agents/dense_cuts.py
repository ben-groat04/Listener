"""Dense cut finder: every frame at full rate, mean abs frame difference + colour-histogram distance.
Lower threshold than PySceneDetect, so it also catches soft, blurred and whip cuts.
Usage: python3 v1/scripts/agents/dense_cuts.py <video name> [--thr 3.0]
Writes v1/data/<video>/scenes/dense_cuts.json (every candidate with scores and whether shots.json has a cut within 0.2 s).
Score = z-like ratio of the frame's combined change to the local (+-1 s) median change; a candidate is a local peak above --thr
and above an absolute floor. Tiers: strong = histogram distance >=0.12 (new picture content); medium = big pixel change with some histogram change; weak = rest (often motion within a shot, flicker). Spot checks: 55.12 (skaters moving within a shot) was a false positive at medium/weak level. struct_corr (grey-level correlation of consecutive frames, mean and contrast removed) separates real cuts (<0.6) from tint swings and flicker (~0.9+); likely_cut uses it. Caveat: flicker/burn artefacts in old film can give false candidates; check with frame_at.py."""
import argparse, json, os, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from _common import find_video
root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
ap = argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("--thr", type=float, default=3.0)
a = ap.parse_args()
v = find_video(root, a.video)
W, H = 160, 120
pr = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", v], capture_output=True, text=True)
n, d = pr.stdout.strip().split("/"); fps = float(n) / float(d)
p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", v, "-vf", f"scale={W}:{H}", "-pix_fmt", "rgb24", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
fs = W * H * 3; prev = None; ph = None; diffs = []; hd = []; i = 0; grays = []
def hist(f):
    q = (f // 64).reshape(-1, 3)  # 4 levels per channel -> 64 bins
    idx = q[:, 0] * 16 + q[:, 1] * 4 + q[:, 2]
    h = np.bincount(idx, minlength=64).astype(float); return h / h.sum()
while True:
    b = p.stdout.read(fs)
    if len(b) < fs: break
    f = np.frombuffer(b, np.uint8).reshape(H, W, 3)
    h = hist(f); g = f.astype(float).mean(axis=2)
    if prev is not None:
        diffs.append(np.abs(g - prev).mean()); hd.append(0.5 * np.abs(h - ph).sum())
    else: diffs.append(0.0); hd.append(0.0)
    grays.append(g.astype(np.float32)); prev, ph = g, h; i += 1
diffs = np.array(diffs); hd = np.array(hd)
comb = diffs / 255.0 * 10 + hd * 4   # both roughly 0-few
k = int(fps)
score = np.zeros(len(comb))
for j in range(len(comb)):
    lo, hi = max(0, j - k), min(len(comb), j + k + 1)
    nb = np.concatenate([comb[lo:j], comb[j + 1:hi]])
    med = np.median(nb); mad = np.median(np.abs(nb - med)) + 0.02
    score[j] = (comb[j] - med) / mad
def scorr(j):
    # structure correlation between frame j-1 and j after removing mean and contrast: ~1 = same picture (tint or flicker change), low = new picture
    a, c = grays[j - 1], grays[j]
    a = (a - a.mean()) / (a.std() + 1e-6); c = (c - c.mean()) / (c.std() + 1e-6)
    return float((a * c).mean())
shots = json.load(open(os.path.join(root, f"v1/data/{a.video}/scenes/shots.json")))
sb = [s["start"] for s in shots[1:]]
cuts = []
for j in range(1, len(comb)):
    lo, hi = max(1, j - 2), min(len(comb), j + 3)
    if score[j] >= a.thr and comb[j] >= 0.25 and score[j] == score[lo:hi].max():
        t = j / fps; hist_ = float(hd[j])
        near = min(sb, key=lambda x: abs(x - t)) if sb else None
        cuts.append({"t": round(t, 2), "frame": j, "score": round(float(score[j]), 1), "diff": round(float(diffs[j]), 2),
                     "hist": round(float(hd[j]), 3), "struct_corr": round(scorr(j), 2), "likely_cut": bool(scorr(j) < 0.6), "tier": ("strong" if hist_ >= 0.12 else "medium" if (diffs[j] >= 30 and hist_ >= 0.05) else "weak"),
                     "in_shots_json": bool(near is not None and abs(near - t) <= 0.2),
                     "nearest_shots_json": near})
out = {"video": a.video, "fps": fps, "frames": i, "threshold": a.thr, "n_cuts": len(cuts),
       "n_missed_strong_or_medium": sum(1 for c in cuts if not c["in_shots_json"] and c["tier"] != "weak"),
       "n_missed_by_shots_json": sum(1 for c in cuts if not c["in_shots_json"]),
       "n_likely_cuts": sum(1 for c in cuts if c["likely_cut"]), "n_likely_cuts_missed_by_shots_json": sum(1 for c in cuts if c["likely_cut"] and not c["in_shots_json"]), "cuts": cuts}
od = os.path.join(root, f"v1/data/{a.video}/scenes"); json.dump(out, open(os.path.join(od, "dense_cuts.json"), "w"), indent=1)
print(out["n_likely_cuts"], "likely cuts (struct_corr<0.6),", out["n_likely_cuts_missed_by_shots_json"], "missed by shots.json;", out["n_cuts"], "candidates;", out["n_missed_by_shots_json"], "not in shots.json (", out["n_missed_strong_or_medium"], "strong/medium ); shots.json boundaries:", len(sb))
