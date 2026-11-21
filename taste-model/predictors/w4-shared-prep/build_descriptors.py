"""W4 shared prep P2: hand-crafted time-resolved descriptors (librosa) per preview clip -> .cache/shared/w4-descriptors/shard_*.npz. Resumable; per clip, no cross-track transform.
Usage: python3 build_descriptors.py [--workers 1] [--shard 100] [--limit N --out DIR] [--no-hpss]"""
import os, sys, json, time, subprocess, argparse
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("NUMBA_NUM_THREADS", "1")
import numpy as np, pandas as pd, librosa
from pathlib import Path
ROOT = Path("/home/user/Listener/taste-model"); SH = ROOT / ".cache/shared"; PREV = SH / "previews"; OUT = SH / "w4-descriptors"
SR = 22050; HOP = 512; AGG = 11  # 11 native hops = 11*512/22050 = 0.2554 s ; AGG2 below gives ~0.5 s
STEP = 22      # native hops per output frame: 22*512/22050 = 0.511 s
SERIES = ["rms_db", "centroid", "bandwidth", "rolloff85", "flatness"] + [f"contrast{i}" for i in range(7)] + ["zcr", "onset_strength"] + [f"chroma{i}" for i in range(12)] + [f"mfcc{i}" for i in range(20)] + ["harmonic_share"]
CLIP = ["tempo", "beat_strength_mean", "beat_strength_std", "beat_strength_max", "key_index", "mode_major", "key_corr", "loudness_range_db", "dynamic_contrast_db", "onset_rate_hz", "rms_slope_db_per_s"]
KP_MAJ = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]); KP_MIN = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])

def decode(path):
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True)
    return np.frombuffer(p.stdout, np.float32)
def agg(M):   # [d, T] -> [n, d] mean over STEP hops
    n = M.shape[1] // STEP
    return M[:, :n * STEP].reshape(M.shape[0], n, STEP).mean(2).T
def clip(y, hpss=True):
    S = np.abs(librosa.stft(y, n_fft=2048, hop_length=HOP)); T = S.shape[1]
    rms = librosa.feature.rms(S=S, frame_length=2048, hop_length=HOP)[0]; rdb = librosa.amplitude_to_db(rms, ref=1.0, top_db=None)
    cen = librosa.feature.spectral_centroid(S=S, sr=SR)[0]; bw = librosa.feature.spectral_bandwidth(S=S, sr=SR)[0]; ro = librosa.feature.spectral_rolloff(S=S, sr=SR, roll_percent=0.85)[0]
    fl = librosa.feature.spectral_flatness(S=S)[0]; co = librosa.feature.spectral_contrast(S=S, sr=SR)
    zc = librosa.feature.zero_crossing_rate(y, frame_length=2048, hop_length=HOP)[0][:T]
    mel = librosa.feature.melspectrogram(S=S ** 2, sr=SR); on = librosa.onset.onset_strength(S=librosa.power_to_db(mel), sr=SR, hop_length=HOP)
    ch = librosa.feature.chroma_stft(S=S ** 2, sr=SR); mf = librosa.feature.mfcc(S=librosa.power_to_db(mel), n_mfcc=20)
    if hpss:
        H, P = librosa.decompose.hpss(S); hs = (H.sum(0) / (H.sum(0) + P.sum(0) + 1e-9))
    else: hs = np.full(T, np.nan)
    F = np.vstack([rdb[None], cen[None], bw[None], ro[None], fl[None], co, zc[None], on[None], ch, mf, hs[None]])[:, :T]
    tempo, beats = librosa.beat.beat_track(onset_envelope=on, sr=SR, hop_length=HOP); tempo = float(np.atleast_1d(tempo)[0])
    bs = on[beats[beats < len(on)]] if len(beats) else np.array([0.0])
    cm = ch.mean(1); kc = [np.corrcoef(np.roll(KP_MAJ, k), cm)[0, 1] for k in range(12)] + [np.corrcoef(np.roll(KP_MIN, k), cm)[0, 1] for k in range(12)]; kb = int(np.argmax(kc))
    tt = np.arange(len(rdb)) * HOP / SR
    pk = librosa.onset.onset_detect(onset_envelope=on, sr=SR, hop_length=HOP)
    cv = [tempo, bs.mean(), bs.std(), bs.max(), kb % 12, float(kb < 12), kc[kb], np.percentile(rdb, 95) - np.percentile(rdb, 10), rdb.max() - np.median(rdb), len(pk) / (T * HOP / SR), np.polyfit(tt, rdb, 1)[0]]
    return agg(F), np.array(cv)
def build_shard(rows, path, hpss):
    md5s, off, SER, CV, failed = [], [0], [], [], []
    for m, f in rows:
        y = decode(f)
        try:
            if len(y) < SR * 3: raise ValueError
            s, c = clip(y, hpss)
        except Exception: failed.append(m); continue
        md5s.append(m); SER.append(s.astype(np.float16)); CV.append(c); off.append(off[-1] + len(s))
    tmp = str(path) + ".tmp.npz"
    np.savez(tmp, md5=np.array(md5s, dtype="<U32"), off=np.array(off, np.int64), series=np.concatenate(SER), clip=np.asarray(CV, np.float32), failed=np.array(failed, dtype="<U32"))
    os.replace(tmp, path); return len(md5s), len(failed)
if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--workers", type=int, default=1); ap.add_argument("--shard", type=int, default=100); ap.add_argument("--limit", type=int); ap.add_argument("--out"); ap.add_argument("--worker-id", type=int); ap.add_argument("--no-hpss", action="store_true")
    a = ap.parse_args(); out = Path(a.out) if a.out else OUT; out.mkdir(parents=True, exist_ok=True)
    man = pd.read_csv(PREV / "manifest.csv"); man = man[man.ok.astype(str) == "True"].sort_values("md5")
    rows = [(r.md5, PREV / "audio" / f"{r.md5}.{r.ext}") for r in man.itertuples()]
    if a.limit: rows = rows[:a.limit]
    shards = [rows[i:i + a.shard] for i in range(0, len(rows), a.shard)]
    if a.worker_id is None:
        json.dump(dict(series=SERIES, clip=CLIP, sr=SR, hop=HOP, step_hops=STEP, frame_s=STEP * HOP / SR, hpss=not a.no_hpss), open(out / "names.json", "w"), indent=1)
        procs = [subprocess.Popen([sys.executable, "-W", "ignore", __file__, "--workers", str(a.workers), "--shard", str(a.shard), "--worker-id", str(w)] + (["--limit", str(a.limit)] if a.limit else []) + (["--out", a.out] if a.out else []) + (["--no-hpss"] if a.no_hpss else [])) for w in range(a.workers)]
        sys.exit(max(p.wait() for p in procs))
    for k, sh in enumerate(shards):
        if k % a.workers != a.worker_id: continue
        p = out / f"shard_{k:04d}.npz"
        if p.exists(): continue
        t = time.time(); n, nf = build_shard(sh, p, not a.no_hpss); print(f"[w{a.worker_id}] shard {k}/{len(shards)} ok={n} failed={nf} {time.time()-t:.1f}s", flush=True)
