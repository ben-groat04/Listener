"""W4 shared prep P1: Essentia pretrained-model outputs per preview clip -> .cache/shared/w4-essentia/shard_*.npz (resumable; a finished shard is never rewritten).
Per clip, independent of other clips, no fitted cross-track transform.
Usage: python3 build_essentia.py [--workers 3] [--shard 100] [--limit N --out DIR]   (models: .cache/shared/w4-essentia/models/, fetched by fetch_models.sh)"""
import os, sys, json, time, subprocess, argparse
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("TF_NUM_INTRAOP_THREADS", "1"); os.environ.setdefault("TF_NUM_INTEROP_THREADS", "1")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
import numpy as np, pandas as pd
from pathlib import Path
ROOT = Path("/home/user/Listener/taste-model"); SH = ROOT / ".cache/shared"; PREV = SH / "previews"
OUT = SH / "w4-essentia"; MD = OUT / "models"
HEADS = ["genre_discogs400", "mtg_jamendo_moodtheme", "mtg_jamendo_instrument", "mtg_jamendo_genre", "danceability", "voice_instrumental",
         "mood_aggressive", "mood_happy", "mood_party", "mood_relaxed", "mood_sad", "mood_acoustic", "mood_electronic", "tonal_atonal",
         "approachability_regression", "engagement_regression"]
SR = 16000; HOP = 256
EFF_PATCH, EFF_HOP = 128, 62      # frames; 2.048 s patches every 0.992 s
MN_PATCH, MN_HOP = 187, 93        # musicnn: 187 frames (~3.0 s) every 93 frames (~1.49 s)

def head_info(name):
    j = json.load(open(MD / f"{name}-discogs-effnet-1.json")); s = j["schema"]
    inp = s["inputs"][0]["name"]; out = [o for o in s["outputs"] if o.get("output_purpose") == "predictions"][0]
    return inp, out["name"], j["classes"]

def labels():
    L = {"heads": [], "av_heads": ["emomusic_valence", "emomusic_arousal", "deam_valence", "deam_arousal"]}
    for h in HEADS:
        _, _, cl = head_info(h); L["heads"].append(dict(name=h, model=f"{h}-discogs-effnet-1", classes=cl))
    return L

def decode(path, sr=SR):
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True)
    return np.frombuffer(p.stdout, np.float32)

class Models:
    def __init__(self):
        import essentia.standard as es; self.es = es
        self.eff = es.TensorflowPredictEffnetDiscogs(graphFilename=str(MD / "discogs-effnet-bs64-1.pb"), output="PartitionedCall:1", patchHopSize=EFF_HOP) if False else es.TensorflowPredictEffnetDiscogs(graphFilename=str(MD / "discogs-effnet-bs64-1.pb"), output="PartitionedCall:1")
        self.heads = []
        for h in HEADS:
            i, o, cl = head_info(h); self.heads.append((h, es.TensorflowPredict2D(graphFilename=str(MD / f"{h}-discogs-effnet-1.pb"), input=i, output=o), len(cl)))
        self.mn = es.TensorflowPredictMusiCNN(graphFilename=str(MD / "msd-musicnn-1.pb"), output="model/dense/BiasAdd")
        self.av = [es.TensorflowPredict2D(graphFilename=str(MD / f"{n}-msd-musicnn-2.pb"), input="model/Placeholder", output="model/Identity") for n in ("emomusic", "deam")]
    def run(self, x):
        E = self.eff(x)                                   # [P,1280]
        A = np.concatenate([np.asarray(h(E)).reshape(len(E), -1) for _, h, _ in self.heads], 1)   # [P, 605+]
        t = (np.arange(len(E)) * EFF_HOP + EFF_PATCH / 2) * HOP / SR
        M = self.mn(x)                                    # [Q,200]
        AV = np.concatenate([np.asarray(a(M)).reshape(len(M), -1) for a in self.av], 1)   # [Q,4]
        tq = (np.arange(len(M)) * MN_HOP + MN_PATCH / 2) * HOP / SR
        return E, A, t, AV, tq

def build_shard(models, rows, path):
    md5s, off, offq = [], [0], [0]; A_, T_, AV_, TQ_, E_ = [], [], [], [], []; am, ax, em, es_, vm, vx, failed = [], [], [], [], [], [], []
    for m, f in rows:
        x = decode(f); ok = len(x) >= SR * 3
        if ok:
            try: E, A, t, AV, tq = models.run(x); ok = len(E) > 0 and len(AV) > 0
            except Exception as e: ok = False
        if not ok: failed.append(m); continue
        md5s.append(m); A_.append(A.astype(np.float16)); T_.append(t.astype(np.float32)); AV_.append(AV.astype(np.float16)); TQ_.append(tq.astype(np.float32)); E_.append(E.astype(np.float16))
        off.append(off[-1] + len(A)); offq.append(offq[-1] + len(AV))
        am.append(A.mean(0)); ax.append(A.max(0)); em.append(E.mean(0)); es_.append(E.std(0)); vm.append(AV.mean(0)); vx.append(AV.max(0))
    f16 = lambda l: np.asarray(l, np.float32).astype(np.float16)
    tmp = str(path) + ".tmp.npz"
    np.savez(tmp, md5=np.array(md5s, dtype="<U32"), patch_off=np.array(off, np.int64), patch_t=np.concatenate(T_), patch_act=np.concatenate(A_), patch_emb=np.concatenate(E_),
             av_off=np.array(offq, np.int64), av_t=np.concatenate(TQ_), av_act=np.concatenate(AV_),
             act_mean=f16(am), act_max=f16(ax), emb_mean=f16(em), emb_std=f16(es_), av_mean=f16(vm), av_max=f16(vx), failed=np.array(failed, dtype="<U32"))
    os.replace(tmp, path)
    return len(md5s), len(failed)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--workers", type=int, default=3); ap.add_argument("--shard", type=int, default=100); ap.add_argument("--limit", type=int); ap.add_argument("--out"); ap.add_argument("--worker-id", type=int)
    a = ap.parse_args()
    out = Path(a.out) if a.out else OUT; out.mkdir(parents=True, exist_ok=True)
    man = pd.read_csv(PREV / "manifest.csv"); man = man[man.ok.astype(str) == "True"].sort_values("md5")
    rows = [(r.md5, PREV / "audio" / f"{r.md5}.{r.ext}") for r in man.itertuples()]
    if a.limit: rows = rows[:a.limit]
    shards = [rows[i:i + a.shard] for i in range(0, len(rows), a.shard)]
    if a.worker_id is None:
        json.dump(labels(), open(out / "labels.json", "w"), indent=1)
        procs = [subprocess.Popen([sys.executable, "-W", "ignore", __file__, "--workers", str(a.workers), "--shard", str(a.shard), "--worker-id", str(w)] + (["--limit", str(a.limit)] if a.limit else []) + (["--out", a.out] if a.out else [])) for w in range(a.workers)]
        sys.exit(max(p.wait() for p in procs))
    models = Models(); t0 = time.time()
    for k, sh in enumerate(shards):
        if k % a.workers != a.worker_id: continue
        p = out / f"shard_{k:04d}.npz"
        if p.exists(): continue
        t = time.time(); n, nf = build_shard(models, sh, p); print(f"[w{a.worker_id}] shard {k}/{len(shards)} ok={n} failed={nf} {time.time()-t:.1f}s", flush=True)
