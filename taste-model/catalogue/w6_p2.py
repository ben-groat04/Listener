"""P2: Deezer second-excerpt audio for tried-pool tracks of TUNE and LATE folds (non-HOLDOUT: the harness 'main' pools already exclude HOLDOUT-artist pool rows; asserted below with data.is_holdout on
the raw artist of the pool rows) that have a matched Deezer preview. Pipeline (resumable): download Deezer 30 s mp3 -> alignment vs the dev clip -> MERT (catalogue.w6_mert, same extractor as the dev cache).
Outputs in .cache/shared-w6r1/: previews_deezer/, previews_manifest.csv, mert_deezer/shard_*.npz (md5 [n] of the Deezer FILE bytes, feat [n,4,12,768] fp16), align.csv.
    python3 -W ignore -m catalogue.w6_p2 [--wait-for-records]      (loops until the records stage has finished and everything is processed)"""
import sys, os, time, glob, hashlib, json, subprocess
import numpy as np, pandas as pd
sys.path.insert(0, "/home/user/Listener/taste-model")
from evalkit import data, run
from catalogue import w6_fetch as F
D = data.ROOT / ".cache" / "shared-w6r1"; PRE = data.ROOT / ".cache" / "shared" / "previews"
HOP = 2048; SRC = 22050
def scope():
    M = pd.read_csv(D / "universe_membership.csv"); ids = set(M[(M.group == "tried")].trackId)   # tried tracks of all 14 folds (TUNE + LATE)
    # HOLDOUT check on raw artist of the main-part pool rows (public-meta artist route is not available for raw ids): none may be holdout
    for Fd in run.prepare_folds(data.DEV_CUTOFFS):
        assert not data.is_holdout(Fd["pool"].artist.values).any()
    return ids
def chroma(path):
    import librosa
    a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-t", "31", "-ac", "1", "-ar", str(SRC), "-f", "f32le", "-"], capture_output=True).stdout, dtype=np.float32)
    c = librosa.feature.chroma_stft(y=a, sr=SRC, hop_length=HOP).T; c = c - c.mean(1, keepdims=True); return c / (np.linalg.norm(c, axis=1, keepdims=True) + 1e-9)
def align(dev_path, dz_path, min_overlap_s=5):
    A, B = chroma(dev_path), chroma(dz_path); S = A @ B.T; n, m = S.shape; fr = HOP / SRC; mo = int(min_overlap_s / fr)
    best = (-9, 0); allm = []
    for k in range(-(m - mo), n - mo + 1):                 # dev frame i <-> deezer frame i-k
        d = np.diagonal(S, offset=-k); 
        if len(d) < mo: continue
        v = float(d.mean()); allm.append(v)
        if v > best[0]: best = (v, k)
    return dict(align_offset_s=best[1] * fr, align_score=best[0], align_margin=best[0] - float(np.median(allm)))
def main():
    T = F.Cache(str(D / "p1_user" / "dz_tracks.jsonl")); ids = scope(); U = pd.read_csv(D / "universe_tracks.csv").set_index("trackId")
    man = pd.read_csv(PRE / "manifest.csv"); man = man[man.ok.astype(bool)].set_index("md5")
    from catalogue.w6_mert import Extractor
    ex = Extractor(); os.makedirs(D / "mert_deezer", exist_ok=True)
    done = set(); [done.update(np.load(f)["md5"]) for f in glob.glob(str(D / "mert_deezer/shard_*.npz"))]
    ap = D / "align.csv"; arows = pd.read_csv(ap) if ap.exists() else pd.DataFrame()
    nshard = len(glob.glob(str(D / "mert_deezer/shard_*.npz"))); keys, feats = [], []
    def flush():
        nonlocal nshard, keys, feats
        if keys:
            np.savez(D / f"mert_deezer/tmp.npz", md5=np.array(keys), feat=np.stack(feats)); os.replace(D / "mert_deezer/tmp.npz", D / f"mert_deezer/shard_{nshard:05d}.npz"); nshard += 1; keys, feats = [], []
    idle = 0; ndone = 0
    while True:
        T.d = F.Cache(str(D / "p1_user" / "dz_tracks.jsonl")).d      # reload
        pairs = [(int(t), v["dz_id"]) for t, v in T.d.items() if int(t) in ids and v.get("status") == "match" and v.get("dz_has_preview")]
        if "--no-download" not in sys.argv: F.run_previews(str(D), [p for p in pairs], threads=1)
        pm = pd.read_csv(D / "previews_manifest.csv") if (D / "previews_manifest.csv").exists() else pd.DataFrame(columns=["md5", "trackId", "ok"])
        pm = pm[pm.ok.astype(bool)]; todo = [r for r in pm.to_dict("records") if r["md5"] not in done]; 
        for r in todo:
            p = D / "previews_deezer" / f"{r['md5']}.mp3"; u = U.loc[r["trackId"]]; dev = u.md5 if isinstance(u.md5, str) else ""
            a = dict(trackId=r["trackId"], md5=r["md5"], dev_md5=dev, align_offset_s=np.nan, align_score=np.nan, align_margin=np.nan)
            if dev and dev in man.index:
                try: a.update(align(PRE / "audio" / f"{dev}.{man.loc[dev, 'ext']}", p))
                except Exception as e: a["err"] = str(e)[:80]
            arows = pd.concat([arows, pd.DataFrame([a])]); keys.append(r["md5"]); feats.append(ex(p)); done.add(r["md5"]); ndone += 1
            if len(keys) >= 50: flush(); arows.to_csv(ap, index=False); print("mert", ndone, int(time.time()), flush=True)
        flush(); arows.drop_duplicates("md5").to_csv(ap, index=False)
        fin = os.path.exists(D / "p1_user" / "records.csv")
        if not todo:
            idle += 1
            if fin and idle >= 2: break
            time.sleep(30)
        else: idle = 0
    print("p2 done", len(done), flush=True)
if __name__ == "__main__": main()
