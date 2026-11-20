"""Regenerates the three shared audio caches used by predict.py (all keyed by previewUrl, dev folds only):
   python3 build_features.py urls  WORKDIR                 # list of preview URLs in the dev folds' meta -> WORKDIR/urls.json
   python3 build_features.py dl    WORKDIR                 # 30 s previews -> WORKDIR/audio/<md5>.npy  (32 kHz mono int16; needs ffmpeg, network)
   python3 build_features.py hand  WORKDIR                 # -> .cache/shared/hand-audio-feat-v1/{feat,seg}.pkl   (librosa, ~0.1 s/clip)
   python3 build_features.py lclap WORKDIR SHARD NSHARDS   # laion/larger_clap_music, middle 10 s -> WORKDIR/lc_mid_<SHARD>of<NSHARDS>.pkl (~0.5 s/clip/thread)
   python3 build_features.py merge WORKDIR NSHARDS         # -> .cache/shared/larger-clap-music-mid-v1/emb.pkl
The CLAP (htsat-unfused) cache clap-preview-emb/emb.pkl comes from ../B-audio/build_dl.py + build_embed.py (unprojected pooler_output of the middle 10 s)."""
import sys, os, json, hashlib, pickle, time
import numpy as np
SH = "/home/user/Listener/taste-model/.cache/shared/"
key = lambda u: hashlib.md5(u.encode()).hexdigest()
def atomic(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True); tmp = path + ".tmp"; pickle.dump(obj, open(tmp, "wb")); os.replace(tmp, path)
stage, W = sys.argv[1], sys.argv[2]; os.makedirs(W + "/audio", exist_ok=True)
if stage == "urls":
    sys.path.insert(0, "/home/user/Listener/taste-model")
    from evalkit import run, data
    u = set()
    for F in run.prepare_folds(data.DEV_CUTOFFS): u |= set(x for x in F["meta"].previewUrl.dropna() if isinstance(x, str))
    json.dump(sorted(u), open(W + "/urls.json", "w")); print(len(u))
elif stage == "dl":
    import subprocess, requests
    from concurrent.futures import ThreadPoolExecutor
    urls = json.load(open(W + "/urls.json"))
    def work(u):
        out = f"{W}/audio/{key(u)}.npy"
        if os.path.exists(out) or os.path.exists(out + ".bad"): return
        try:
            r = requests.get(u, timeout=30); r.raise_for_status()
            p = subprocess.run(["ffmpeg", "-v", "quiet", "-i", "pipe:0", "-t", "30", "-ac", "1", "-ar", "32000", "-f", "s16le", "pipe:1"], input=r.content, capture_output=True, timeout=60)
            a = np.frombuffer(p.stdout, dtype=np.int16)
            if len(a) < 32000 * 5: raise Exception("short")
            np.save(out, a)
        except Exception as e: open(out + ".bad", "w").write(str(e)[:100])
    with ThreadPoolExecutor(6) as ex: list(ex.map(work, urls))
elif stage == "hand":
    import librosa
    urls = json.load(open(W + "/urls.json")); H, G = {}, {}
    for u in urls:
        f = f"{W}/audio/{key(u)}.npy"
        if not os.path.exists(f): H[u] = G[u] = None; continue
        a = np.load(f).astype(np.float32) / 32768; a = a[::2]; sr = 16000
        S = np.abs(librosa.stft(a, n_fft=1024, hop_length=512))
        lm = librosa.power_to_db(librosa.feature.melspectrogram(S=S ** 2, sr=sr, n_mels=64))
        mf = librosa.feature.mfcc(S=lm, n_mfcc=20); ch = librosa.feature.chroma_stft(S=S ** 2, sr=sr)
        cen = librosa.feature.spectral_centroid(S=S, sr=sr)[0]; con = librosa.feature.spectral_contrast(S=S, sr=sr)
        rms = librosa.feature.rms(S=S, frame_length=1024)[0]; on = librosa.onset.onset_strength(S=lm, sr=sr)
        tempo = librosa.feature.tempo(onset_envelope=on, sr=sr, hop_length=512)[0]
        ac = librosa.autocorrelate(on, max_size=200); ac = ac / (ac[0] + 1e-9)
        T = lm.shape[1]; seg = np.array_split(np.arange(T), 6); ds = np.log(rms + 1e-4)
        segf = np.array([[rms[s].mean(), cen[s].mean(), on[s].mean()] for s in seg])
        H[u] = np.concatenate([mf.mean(1), mf.std(1), ch.mean(1), con.mean(1), lm.mean(1)[::4],
            [np.log(tempo), cen.mean(), cen.std(), ds.mean(), ds.std(), np.percentile(ds, 95) - np.percentile(ds, 5), on.mean(), on.std(), (rms < 0.01).mean()],
            ac[[10, 20, 40, 80, 160]], np.log(segf[:, 0] + 1e-4).std(keepdims=True), segf[:, 1].std(keepdims=True), segf[:, 2].std(keepdims=True),
            [np.log(segf[:, 0].max() / (segf[:, 0].min() + 1e-4) + 1e-4)]]).astype(np.float32)
        G[u] = np.array([np.concatenate([mf[:, s].mean(1), ch[:, s].mean(1), [ds[s].mean(), cen[s].mean(), on[s].mean()]]) for s in seg], dtype=np.float32)
    atomic(H, SH + "hand-audio-feat-v1/feat.pkl"); atomic(G, SH + "hand-audio-feat-v1/seg.pkl")
elif stage == "lclap":
    import torch, librosa
    from transformers import ClapModel, ClapProcessor
    torch.set_num_threads(1); sh, nsh = int(sys.argv[3]), int(sys.argv[4])
    m = ClapModel.from_pretrained("laion/larger_clap_music").eval(); p = ClapProcessor.from_pretrained("laion/larger_clap_music")
    urls = json.load(open(W + "/urls.json")); out = {}; fn = f"{W}/lc_mid_{sh}of{nsh}.pkl"
    for i, u in enumerate(urls):
        if i % nsh != sh: continue
        f = f"{W}/audio/{key(u)}.npy"
        if not os.path.exists(f): out[u] = None; continue
        a = np.load(f).astype(np.float32) / 32768; s = len(a) // 2; a = a[max(0, s - 160000):s + 160000]
        a = librosa.resample(a, orig_sr=32000, target_sr=48000)
        x = p(audio=[a], sampling_rate=48000, return_tensors="pt")
        with torch.no_grad(): out[u] = m.audio_model(**x).pooler_output[0].numpy().astype(np.float32)
    atomic(out, fn)
elif stage == "merge":
    out = {}
    for i in range(int(sys.argv[3])): out.update(pickle.load(open(f"{W}/lc_mid_{i}of{sys.argv[3]}.pkl", "rb")))
    atomic(out, SH + "larger-clap-music-mid-v1/emb.pkl"); print(len(out))
