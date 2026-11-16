"""Per-second visual descriptors: brightness, saturation, warmth, dominant colours, motion energy, face count; cut-vs-beat alignment; charts."""
import json, os, glob
import numpy as np, cv2, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
VID = os.environ.get("VID", "video2")
V = os.path.join(root, f"{os.environ.get('VIDEO_DIR', 'videos')}/{VID}.mp4"); D = os.path.join(root, f"v1/data/{VID}/visual_features"); os.makedirs(D, exist_ok=True)
cap = cv2.VideoCapture(V); fps = cap.get(cv2.CAP_PROP_FPS)
face = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
per = {}; prev = None; i = 0
while True:
    ok, f = cap.read()
    if not ok: break
    sec = int(i / fps); g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY); hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    d = per.setdefault(sec, {"bright": [], "sat": [], "warm": [], "motion": [], "faces": [], "px": []})
    d["bright"].append(g.mean()); d["sat"].append(hsv[..., 1].mean())
    b, gg, r = [f[..., k].mean() for k in range(3)]; d["warm"].append(r - b)
    if prev is not None: d["motion"].append(cv2.absdiff(g, prev).mean())
    if i % int(fps) == 0:
        d["faces"].append(len(face.detectMultiScale(g, 1.2, 5, minSize=(30, 30))))
        d["px"].append(cv2.resize(f, (60, 48)).reshape(-1, 3))
    prev = g; i += 1
rows = []
for s in sorted(per):
    d = per[s]; px = np.vstack(d["px"]).astype(np.float32) if d["px"] else None; dom = []
    if px is not None:
        _, lab, cen = cv2.kmeans(px, 4, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0), 2, cv2.KMEANS_PP_CENTERS)
        cnt = np.bincount(lab.ravel(), minlength=4); order = cnt.argsort()[::-1]
        dom = ["#%02x%02x%02x" % tuple(int(c) for c in cen[k][::-1]) for k in order]
    rows.append({"t": s, "brightness": round(float(np.mean(d["bright"])), 1), "saturation": round(float(np.mean(d["sat"])), 1),
                 "warmth_r_minus_b": round(float(np.mean(d["warm"])), 1), "motion": round(float(np.mean(d["motion"])) if d["motion"] else 0, 2),
                 "faces": int(max(d["faces"])) if d["faces"] else 0, "dominant_colours": dom})
json.dump(rows, open(f"{D}/per_second.json", "w"), indent=0)
# cut/beat alignment
shots = json.load(open(os.path.join(root, f"v1/data/{VID}/scenes/shots.json"))); beats = np.array(json.load(open(os.path.join(root, f"v1/data/{VID}/audio_features/beat_times.json"))))
cuts = np.array([s["start"] for s in shots[1:]]); off = np.array([np.min(np.abs(beats - c)) for c in cuts])
ibi = float(np.median(np.diff(beats)))
rand = np.array([np.min(np.abs(beats - c)) for c in np.random.default_rng(0).uniform(beats[0], beats[-1], 5000)])
align = {"n_cuts": int(len(cuts)), "median_beat_interval_s": round(ibi, 3), "median_cut_to_beat_offset_s": round(float(np.median(off)), 3),
         "frac_cuts_within_80ms_of_beat": round(float((off < .08).mean()), 3), "chance_frac_within_80ms": round(float((rand < .08).mean()), 3),
         "cuts_per_10s": [int(((cuts >= a) & (cuts < a + 10)).sum()) for a in range(0, 310, 10)]}
json.dump(align, open(f"{D}/cut_beat_alignment.json", "w"), indent=1)
t = [r["t"] for r in rows]
fig, ax = plt.subplots(5, 1, figsize=(16, 12), sharex=True)
for a, k in zip(ax, ["brightness", "saturation", "warmth_r_minus_b", "motion", "faces"]): a.plot(t, [r[k] for r in rows]); a.set_ylabel(k)
for a in ax:
    for c in cuts: a.axvline(c, color="grey", lw=.3)
ax[-1].set_xticks(np.arange(0, 310, 10)); plt.tight_layout(); plt.savefig(f"{D}/overview.png", dpi=80)
# colour barcode of the film (one stripe per second)
bar = np.zeros((120, len(rows), 3), np.uint8)
for j, r in enumerate(rows):
    if r["dominant_colours"]: h = r["dominant_colours"][0].lstrip("#"); bar[:, j] = [int(h[k:k+2], 16) for k in (0, 2, 4)]
plt.figure(figsize=(16, 2)); plt.imshow(bar, aspect="auto"); plt.xticks(np.arange(0, len(rows), 10)); plt.yticks([]); plt.tight_layout(); plt.savefig(f"{D}/colour_barcode.png", dpi=80)
print(json.dumps(align))
