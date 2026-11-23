import sys, os, glob, time, importlib.util
sys.path.insert(0, "/home/user/Listener/taste-model")
import numpy as np, pandas as pd, torch
from pathlib import Path
from transformers import AutoModel
R = Path("/home/user/Listener/taste-model"); O = R / ".cache/suggest"
part, nparts = int(sys.argv[1]), int(sys.argv[2])
sp = importlib.util.spec_from_file_location("bm", str(R / "predictors/w3r1-content-audio/build_mert.py")); bm = importlib.util.module_from_spec(sp); sp.loader.exec_module(bm)
torch.set_num_threads(2); NW = bm.NW
df = pd.read_csv(O / "candidates.csv"); df = df[df.audio_ok].reset_index(drop=True)
df = df.iloc[part::nparts]
d = O / "mert" / f"p{part}"; d.mkdir(parents=True, exist_ok=True)
have = set()
for f in glob.glob(str(O / "mert/p*/shard_*.npz")): have |= set(map(str, np.load(f)["md5"]))
todo = [k for k in df.key if k not in have]; print("todo", len(todo), flush=True)
m = AutoModel.from_pretrained("m-a-p/MERT-v1-95M", trust_remote_code=True).eval(); H = []
for l in m.encoder.layers: l.register_forward_hook(lambda mod, i, o: H.append((o[0] if isinstance(o, tuple) else o).detach()))
m = torch.ao.quantization.quantize_dynamic(m, {torch.nn.Linear}, dtype=torch.qint8)
nsh = len(glob.glob(str(d / "shard_*.npz"))); keys, feats = [], []; t0 = time.time()
def flush():
    global nsh, keys, feats
    if keys:
        tmp = d / f"shard_{nsh:05d}.npz.tmp.npz"; np.savez(tmp, md5=np.array(keys), feat=np.stack(feats)); os.replace(tmp, d / f"shard_{nsh:05d}.npz"); nsh += 1; keys, feats = [], []
for i, k in enumerate(todo):
    w = bm.windows(bm.decode(O / "audio" / f"{k}.mp3"))
    if w is None: keys.append(k); feats.append(np.full((NW, 12, 768), np.nan, np.float16))
    else:
        H.clear()
        with torch.inference_mode(): m(w)
        keys.append(k); feats.append(torch.stack(H).mean(2).permute(1, 0, 2).numpy().astype(np.float16))
    if len(keys) >= 50: flush(); print(f"mert {i+1}/{len(todo)} {int(time.time()-t0)} s", flush=True)
flush(); print("DONE", flush=True)
