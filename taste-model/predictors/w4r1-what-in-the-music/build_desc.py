"""Cheap librosa descriptors per preview clip (no HPSS): for 6 segments of 5 s and the whole clip: loudness (dB rms mean/std), spectral centroid / rolloff / flatness / bandwidth, onset strength mean, zero-crossing rate;
clip-level: dB-std, dynamic range (p95-p10 dB), log2(tempo/120) via librosa.feature.tempo. 16 kHz decode; chroma/key/HPSS dropped for cost.  Output .cache/w4r1-what-in-the-music/desc/shard_<w>.npz (resumable per worker).
Usage (from /home/user/Listener/taste-model): python3 -W ignore predictors/w4r1-what-in-the-music/build_desc.py WORKER NWORKERS [LIMIT]"""
import sys, os, subprocess, glob, numpy as np, pandas as pd, librosa, time
ROOT = "/home/user/Listener/taste-model/"; OUT = ROOT + ".cache/w4r1-what-in-the-music/desc/"; os.makedirs(OUT, exist_ok=True)
SR = 16000; HOP = 512
NAMES = None
def feats(path):
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True)
    y = np.frombuffer(p.stdout, np.float32)
    if len(y) < SR * 5: return None
    rms = librosa.feature.rms(y=y, hop_length=HOP)[0]; db = 20 * np.log10(rms + 1e-6)
    S = np.abs(librosa.stft(y, n_fft=1024, hop_length=HOP)); cen = librosa.feature.spectral_centroid(S=S, sr=SR)[0]; rol = librosa.feature.spectral_rolloff(S=S, sr=SR)[0]
    flat = librosa.feature.spectral_flatness(S=S)[0]; bw = librosa.feature.spectral_bandwidth(S=S, sr=SR)[0]; zc = librosa.feature.zero_crossing_rate(y, hop_length=HOP)[0]
    on = librosa.onset.onset_strength(S=librosa.amplitude_to_db(S[:, :]), sr=SR, hop_length=HOP)
    n = min(len(db), len(cen), len(on), len(zc)); fr = np.arange(n) * HOP / SR
    per = np.stack([db[:n], cen[:n], rol[:n], flat[:n], bw[:n], on[:n], zc[:n]], 1)   # [n, 7]
    seg = []
    for s in range(6):
        m = (fr >= 5 * s) & (fr < 5 * s + 5); seg.append(np.r_[per[m].mean(0), db[:n][m].std()] if m.any() else np.full(8, np.nan))
    clip = np.r_[per.mean(0), db[:n].std(), np.percentile(db[:n], 95) - np.percentile(db[:n], 10)]
    tempo = float(librosa.feature.tempo(onset_envelope=on, sr=SR, hop_length=HOP)[0])
    glob_ = np.r_[clip, np.log2(max(tempo, 30) / 120.0)]
    return np.stack(seg).astype(np.float32), glob_.astype(np.float32)
if __name__ == "__main__":
    w, nw = int(sys.argv[1]), int(sys.argv[2]); lim = int(sys.argv[3]) if len(sys.argv) > 3 else None
    man = pd.read_csv(ROOT + ".cache/shared/previews/manifest.csv"); man = man[man.ok == True].sort_values("md5").reset_index(drop=True)
    man = man.iloc[w::nw]; man = man.iloc[:lim] if lim else man
    f = OUT + f"shard_{w}of{nw}.npz"; done = {}
    if os.path.exists(f):
        z = np.load(f); done = {k: (a, b) for k, a, b in zip(z["md5"], z["seg"], z["glob"])}
    t0 = time.time(); new = 0
    for i, r in enumerate(man.itertuples()):
        if r.md5 in done: continue
        o = feats(ROOT + f".cache/shared/previews/audio/{r.md5}.{r.ext}")
        if o is not None: done[r.md5] = o; new += 1
        if new and new % 400 == 0 and i:
            np.savez(f, md5=np.array(list(done)), seg=np.stack([v[0] for v in done.values()]), glob=np.stack([v[1] for v in done.values()])); print(w, i, len(man), time.time() - t0, flush=True)
    np.savez(f, md5=np.array(list(done)), seg=np.stack([v[0] for v in done.values()]), glob=np.stack([v[1] for v in done.values()])); print("done", w, len(done), time.time() - t0)
