"""Per-clip MERT-v1-95M features from the shared preview-audio cache (each clip is processed independently of every other track, no fitted transform).
usage (from /home/user/Listener/taste-model, in the background):  python3 -W ignore predictors/w3r1-content-audio/build_mert.py [--limit N]
Output: .cache/shared/w3r1-mert-v1/shard_*.npz (keys: md5 [n], feat [n,4,12,768] fp16) + done.txt.  Resumable.
Per clip: 4 x 5 s windows evenly spread over the 30 s preview (audio z-scored per clip, 24 kHz mono), MERT-95M (dynamic int8 linear layers, 2 threads), output of each of the 12
transformer layers averaged over time within each window -> [window, layer, 768].  Whole-clip summary = mean over windows; time-local = windows kept separate.
Order of work: urls by the first dev fold in which they appear (so early folds complete first). ~1.8 s per clip."""
import sys, os, time, subprocess, glob, hashlib
import numpy as np, pandas as pd, torch
sys.path.insert(0, "/home/user/Listener/taste-model")
torch.set_num_threads(2)
from evalkit import data, run
OUT = data.ROOT / ".cache" / "shared" / "w3r1-mert-v1"; PRE = data.ROOT / ".cache" / "shared" / "previews"
SR = 24000; NW = 4; WL = 5.0

def ordered_urls():
    seen = {}
    for F in run.prepare_folds(data.DEV_CUTOFFS):
        for u in F["meta"].previewUrl.dropna(): seen.setdefault(u, len(seen))
    return list(seen)

def decode(path):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-t", "31", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, dtype=np.float32)

def windows(a):
    dur = len(a) / SR
    if dur < WL + 1: return None
    a = (a - a.mean()) / (a.std() + 1e-7)
    starts = np.linspace(0.5, max(0.5, dur - WL - 0.5), NW)
    return torch.tensor(np.stack([a[int(s * SR):int(s * SR) + int(WL * SR)] for s in starts]))

def main():
    from transformers import AutoModel
    OUT.mkdir(parents=True, exist_ok=True)
    lim = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
    man = pd.read_csv(PRE / "manifest.csv"); man = man[man.ok.astype(bool)].set_index("previewUrl")
    done = set()
    for f in glob.glob(str(OUT / "shard_*.npz")): done |= set(np.load(f)["md5"])
    todo = [(hashlib.md5(u.encode()).hexdigest(), man.loc[u, "ext"]) for u in ordered_urls() if u in man.index]
    todo = [t for t in todo if t[0] not in done][:lim]
    print(len(todo), "clips to do", flush=True)
    m = AutoModel.from_pretrained("m-a-p/MERT-v1-95M", trust_remote_code=True).eval()
    H = []
    for l in m.encoder.layers: l.register_forward_hook(lambda mod, i, o: H.append((o[0] if isinstance(o, tuple) else o).detach()))
    m = torch.ao.quantization.quantize_dynamic(m, {torch.nn.Linear}, dtype=torch.qint8)
    nshard = len(glob.glob(str(OUT / "shard_*.npz"))); t0 = time.time(); keys, feats = [], []
    def flush():
        nonlocal nshard, keys, feats
        if keys:
            np.savez(OUT / f"shard_{nshard:05d}.npz.tmp.npz", md5=np.array(keys), feat=np.stack(feats)); os.replace(OUT / f"shard_{nshard:05d}.npz.tmp.npz", OUT / f"shard_{nshard:05d}.npz")
            nshard += 1; keys, feats = [], []
    for i, (k, ext) in enumerate(todo):
        w = windows(decode(PRE / "audio" / f"{k}.{ext}"))
        if w is None: keys.append(k); feats.append(np.full((NW, 12, 768), np.nan, np.float16)); continue
        H.clear()
        with torch.inference_mode(): m(w)
        keys.append(k); feats.append(torch.stack(H).mean(2).permute(1, 0, 2).numpy().astype(np.float16))   # [12,NW,768] -> [NW,12,768]
        if len(keys) >= 100: flush(); print(i + 1, len(todo), int(time.time() - t0), "s", flush=True)
    flush(); print("done", flush=True)
if __name__ == "__main__": main()
