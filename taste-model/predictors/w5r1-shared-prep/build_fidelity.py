"""Artefact C: fidelity check of cached per-clip audio features on a seeded sample. Offline only. Run: HF_HUB_OFFLINE=1 python3 -W ignore -I predictors/w5r1-shared-prep/build_fidelity.py [--n 200] [--out DIR]
Output: fidelity_sample.npz (md5, fp32 [n,4,12,768], int8_12win [n,12,12,768]) fp16; decode/windows identical to predictors/w3r1-content-audio/build_mert.py."""
import os, sys, time, subprocess, numpy as np, pandas as pd, torch
os.environ["HF_HUB_OFFLINE"] = "1"; torch.set_num_threads(2)
S = "/home/user/Listener/taste-model/.cache/shared/previews/"; SR = 24000
n = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 200
out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "/home/user/Listener/taste-model/.cache/shared-w5r1/fidelity_sample.npz"
man = pd.read_csv(S + "manifest.csv"); man = man[man.ok.astype(bool)].sort_values("md5").reset_index(drop=True)
idx = np.random.default_rng(0).choice(len(man), 200, replace=False)[:n]; sm = man.iloc[idx]
def decode(p): return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-t", "31", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, dtype=np.float32)
def windows(a, nw, wl):
    dur = len(a) / SR
    if dur < wl + 1: return None
    a = (a - a.mean()) / (a.std() + 1e-7); st = np.linspace(0.5, max(0.5, dur - wl - 0.5), nw)
    return torch.tensor(np.stack([a[int(s * SR):int(s * SR) + int(wl * SR)] for s in st]))
from transformers import AutoModel
def load(q):
    m = AutoModel.from_pretrained("m-a-p/MERT-v1-95M", trust_remote_code=True).eval(); H = []
    for l in m.encoder.layers: l.register_forward_hook(lambda mod, i, o: H.append((o[0] if isinstance(o, tuple) else o).detach()))
    if q: m = torch.ao.quantization.quantize_dynamic(m, {torch.nn.Linear}, dtype=torch.qint8)
    return m, H
def run(m, H, w):
    H.clear()
    with torch.inference_mode(): m(w)
    return torch.stack(H).mean(2).permute(1, 0, 2).numpy().astype(np.float16)
mf, Hf = load(False); mq, Hq = load(True)
keys, F, Q = [], [], []; t0 = time.time()
for i, r in enumerate(sm.itertuples()):
    a = decode(f"{S}audio/{r.md5}.{r.ext}"); w4 = windows(a, 4, 5.0); w12 = windows(a, 12, 2.5)
    keys.append(r.md5)
    if w4 is None: F.append(np.full((4, 12, 768), np.nan, np.float16)); Q.append(np.full((12, 12, 768), np.nan, np.float16))
    else: F.append(run(mf, Hf, w4)); Q.append(run(mq, Hq, w12))
    if i % 10 == 9 or i < 5: print(i + 1, int(time.time() - t0), "s", flush=True)
np.savez(out + ".tmp.npz", md5=np.array(keys), fp32_4win=np.stack(F), int8_12win=np.stack(Q)); os.replace(out + ".tmp.npz", out); print("done", int(time.time() - t0))
