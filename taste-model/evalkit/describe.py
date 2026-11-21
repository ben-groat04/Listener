"""Label descriptives (v4):  python3 -m evalkit.describe      TUNE slice, non-HOLDOUT tried songs only. Facts only; no recommendation.
Tables: love rate and n by exposure_before bucket x exposure_after bucket (harness diagnostics: number of OTHER new songs first played earlier / later in the same listening session of the
candidate's first play; sessions come from 30-minute gaps, the count includes songs heard after the candidate); the same split by replays_first_session (1 vs 2 or more); AUC of
exposure_before restricted to songs with replays_first_session == 1; love rate by contextId present vs absent at the song's first play."""
import numpy as np, pandas as pd
from . import data, metrics, run

BUCKETS = ["0", "1-2", "3-8", "9+"]

def _wilson(k, n, z=1.96):
    if n == 0: return (np.nan, np.nan)
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d; return (round(c - h, 2), round(c + h, 2))

def rate_table(df, rows, cols, rname, cname):
    out = {}
    for r in rows:
        out[r] = {}
        for c in cols:
            m = df[(df[rname] == r) & (df[cname] == c)]; n = len(m); out[r][c] = f"{m.love.mean():.2f} (n={n})" if n else "- (n=0)"
    return pd.DataFrame(out).T.rename_axis(f"{rname} \\ {cname}")

def main():
    P = run.prepare_folds(data.TUNE_CUTOFFS, "main")
    d = data.load_streams(); fs = d.sort_values("t", kind="stable").drop_duplicates("song").set_index("song")
    df = pd.concat([F["pool"].assign(fold=str(F["c"].date())) for F in P]); df = df[df.is_decoy == 0].reset_index(drop=True)
    df["xb"] = pd.Series(metrics.exp_bucket(df.exp_before.values)).map(lambda v: BUCKETS[int(v)]).values
    df["xa"] = pd.Series(metrics.exp_bucket(df.exp_after.values)).map(lambda v: BUCKETS[int(v)]).values
    df["replays"] = np.where(df.replays_s1 == 1, "1", "2+")
    cid = fs.contextId.reindex(df.song).values; df["ctx"] = np.where(pd.isna(cid), "absent", "present")
    print(f"TUNE non-HOLDOUT tried songs: {len(df)} songs, {int(df.love.sum())} loved (love rate {df.love.mean():.3f}), folds {data.TUNE_CUTOFFS[0]} .. {data.TUNE_CUTOFFS[-1]}")
    print("\n== love rate (n) by exposure_before (rows) x exposure_after (columns), all songs"); print(rate_table(df, BUCKETS, BUCKETS, "xb", "xa").to_string())
    for rp in ("1", "2+"):
        print(f"\n== the same, replays_first_session == {rp}"); print(rate_table(df[df.replays == rp], BUCKETS, BUCKETS, "xb", "xa").to_string())
    print("\n== love rate (n) by replays_first_session x exposure_after (marginal over exposure_before)"); print(rate_table(df, ["1", "2+"], BUCKETS, "replays", "xa").to_string())
    print("\n== love rate (n) by replays_first_session x exposure_before"); print(rate_table(df, ["1", "2+"], BUCKETS, "replays", "xb").to_string())
    s1 = df[df.replays == "1"].reset_index(drop=True)
    B = metrics.Block(s1, "love", 300, 0)
    for nm, v in (("exposure_before (higher = more new songs earlier in the session)", s1.exp_before.values.astype(float)), ("minus exposure_before", -s1.exp_before.values.astype(float))):
        st = B.stats(v, True, ("sauc",)); lo, hi = np.nanpercentile(st["sauc_b"], [2.5, 97.5]); print(f"\nAUC (fold-stratified, artist-cluster bootstrap 95% CI) of {nm} on songs with replays_first_session == 1: n={len(s1)}, loved={int(s1.love.sum())}: {st['sauc'][0]:.3f} [{lo:.3f}, {hi:.3f}]")
    print("   (all songs, same score:", round(float(metrics.Block(df, "love", 2, 0).stats(df.exp_before.values.astype(float), False, ("sauc",))["sauc"][0]), 3), ")")
    print("\n== love rate by contextId at the song's first play")
    t = df.groupby("ctx").love.agg(["size", "sum", "mean"]).rename(columns={"size": "n", "sum": "loved", "mean": "love_rate"}); t["wilson95"] = [_wilson(k, n) for k, n in zip(t["loved"], t["n"])]; print(t.round(3).to_string())
    print("\n== love rate by contextId present/absent x exposure_before"); print(rate_table(df, ["present", "absent"], BUCKETS, "ctx", "xb").to_string())

if __name__ == "__main__": main()
