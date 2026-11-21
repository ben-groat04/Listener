"""How much does lo80 of a paired sauc delta move with the bootstrap seed / resample count? (justifies the |lo80|<0.005 undecided band)"""
import sys; sys.path.insert(0, "."); sys.path.insert(0, "/home/user/Listener/taste-model")
from lib import *; import evalkit.metrics as M
d = pd.read_pickle(DUMP)
for a, b in [("pair_z", "ref_w4r1_listening"), ("ref_w4r1_listening", "artist_recent"), ("pair_z", "artist_recent"), ("ref_w4r1_music", "ref_audio_final")]:
    for nb in (300, 1000):
        r = [M.dump_sauc_delta(d, "tune", a, b, "fold", "love", nb, s) for s in range(8)]
        lo = np.array([x["lo80"] for x in r]); hi = np.array([x["hi80"] for x in r])
        print(f"{a} - {b} nboot={nb}: d={r[0]['d']:+.4f} lo80 mean {lo.mean():+.4f} sd over 8 seeds {lo.std(ddof=1):.4f} range [{lo.min():+.4f},{lo.max():+.4f}]; hi80 sd {hi.std(ddof=1):.4f}", flush=True)
