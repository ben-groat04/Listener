"""Regenerable per-track audio cache: CLAP (laion/clap-htsat-unfused) audio embedding of the middle 10 s of every shared preview (keyed by md5 of previewUrl).
Each embedding depends only on its own file (no fitted transform). Output: /home/user/Listener/taste-model/.cache/shared/w3r1-clap/emb.npz (md5 -> 768-d float16).
usage: python3 build_clap.py [limit]   (resumable, 1 thread)"""
import sys, os, subprocess, time
import numpy as np, pandas as pd, torch
torch.set_num_threads(1)
ROOT = "/home/user/Listener/taste-model/.cache/shared"
OUT = ROOT + "/w3r1-clap"; os.makedirs(OUT, exist_ok=True)
man = pd.read_csv(ROOT + "/previews/manifest.csv"); man = man[man.ok == True]
def load():
    f = OUT + "/emb.npz"
    if os.path.exists(f):
        z = np.load(f, allow_pickle=True); return dict(zip(z["k"], z["v"]))
    return {}
def save(d):
    ks = np.array(list(d)); vs = np.stack([d[k] for k in ks]).astype(np.float16)
    np.savez(OUT + "/tmp.npz", k=ks, v=vs); os.replace(OUT + "/tmp.npz", OUT + "/emb.npz")
def decode(path):
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "48000", "-f", "f32le", "-"], capture_output=True)
    return np.frombuffer(p.stdout, dtype=np.float32)
if __name__ == "__main__":
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else None
    from transformers import ClapModel, ClapProcessor
    m = ClapModel.from_pretrained("laion/clap-htsat-unfused").eval(); pr = ClapProcessor.from_pretrained("laion/clap-htsat-unfused")
    d = load(); todo = [r for r in man.itertuples() if r.md5 not in d]
    if lim: todo = todo[:lim]
    t0 = time.time(); n = 0
    for r in todo:
        a = decode(f"{ROOT}/previews/audio/{r.md5}.{r.ext}")
        if len(a) < 48000: d[r.md5] = np.zeros(768, np.float16); continue
        s = len(a) // 2; a = a[max(0, s - 240000): s + 240000]
        x = pr(audio=[a], sampling_rate=48000, return_tensors="pt")
        with torch.no_grad(): e = m.audio_model(**x).pooler_output[0].numpy()
        d[r.md5] = e.astype(np.float16); n += 1
        if n % 250 == 0: save(d); print(n, len(todo), round(time.time() - t0), flush=True)
    save(d); print("done", n, round(time.time() - t0))
