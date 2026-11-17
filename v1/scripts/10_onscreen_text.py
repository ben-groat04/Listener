"""Find frames with on-screen print; save full-size crops and text/index.json.
Usage: VID=<name> python3 10_onscreen_text.py [--step 1.0] [--max-crops 200]   (or: python3 10_onscreen_text.py <name>)
Candidate regions come from an edge-density heuristic (morphological text-line blobs); each is OCRed with the tesseract
CLI if installed (else tagged 'unread'). Tags: legible (mean word conf >= 70 and >= 3 letters), partial (some text, low conf), unread.
Output: v1/data/<VID>/text/crop_*.png and index.json [{t, bbox[x,y,w,h], frame_size, ocr, conf, legibility, crop}]."""
import json, os, shutil, subprocess, sys, argparse, tempfile
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from _common import find_video
root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("vid", nargs="?"); ap.add_argument("--step", type=float, default=1.0, help="seconds between sampled frames")
ap.add_argument("--max-crops", type=int, default=200)
a = ap.parse_args()
VID = os.environ.get("VID") or a.vid
if not VID: sys.exit("ERROR: VID is mandatory. Run as: VID=<video name without extension> python3 " + os.path.basename(sys.argv[0]))
V = find_video(root, VID); D = os.path.join(root, f"v1/data/{VID}/text"); os.makedirs(D, exist_ok=True)
TESS = shutil.which("tesseract")

def candidates(f):
    g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY); h, w = g.shape
    grad = cv2.morphologyEx(g, cv2.MORPH_GRADIENT, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    _, bw = cv2.threshold(grad, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    bw = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (max(9, w // 60), 3)))
    cs, _ = cv2.findContours(bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE); out = []
    for c in cs:
        x, y, bw_, bh = cv2.boundingRect(c)
        if bw_ < w * 0.04 or bh < 8 or bh > h * 0.25 or bw_ / bh < 1.8: continue
        dens = float((cv2.Canny(g[y:y + bh, x:x + bw_], 80, 200) > 0).mean())
        if dens < 0.06: continue
        p = 4; x0, y0 = max(x - p, 0), max(y - p, 0); out.append((x0, y0, min(bw_ + 2 * p, w - x0), min(bh + 2 * p, h - y0), dens))
    return out

def ocr(img):
    if not TESS: return "", 0.0
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "c.png"); cv2.imwrite(p, cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC))
        r = subprocess.run([TESS, p, "-", "--psm", "6", "tsv"], capture_output=True, text=True)
    words, confs = [], []
    for ln in r.stdout.splitlines()[1:]:
        c = ln.split("\t")
        if len(c) >= 12 and c[11].strip() and float(c[10]) >= 0: words.append(c[11].strip()); confs.append(float(c[10]))
    return " ".join(words), (float(np.mean(confs)) if confs else 0.0)

def tag(txt, conf):
    letters = sum(ch.isalpha() for ch in txt)
    if letters >= 3 and conf >= 70: return "legible"
    if letters >= 2 and conf >= 30: return "partial"
    return "unread"

cap = cv2.VideoCapture(V); fps = cap.get(cv2.CAP_PROP_FPS) or 25.0; n = cap.get(cv2.CAP_PROP_FRAME_COUNT); dur = n / fps
idx, k, t = [], 0, 0.0
while t < dur: idx.append(t); t += a.step
rows = []
for t in idx:
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000); ok, f = cap.read()
    if not ok: continue
    for (x, y, w, h, dens) in candidates(f):
        if len(rows) >= a.max_crops: break
        crop = f[y:y + h, x:x + w]; txt, conf = ocr(crop); lg = tag(txt, conf) if TESS else "unread"
        name = f"crop_t{t:07.2f}_{x}_{y}.png"; cv2.imwrite(os.path.join(D, name), crop)
        rows.append({"t": round(t, 2), "bbox": [x, y, w, h], "frame_size": [f.shape[1], f.shape[0]], "edge_density": round(dens, 3),
                     "ocr": txt, "conf": round(conf, 1), "legibility": lg, "crop": name})
json.dump({"video": VID, "ocr_engine": "tesseract" if TESS else "none (edge heuristic only)", "step_s": a.step, "crops": rows},
          open(os.path.join(D, "index.json"), "w"), indent=1, ensure_ascii=False)
print(f"{VID}: {len(rows)} crops -> {D}/index.json (engine={'tesseract' if TESS else 'none'}); legible={sum(r['legibility']=='legible' for r in rows)}")
