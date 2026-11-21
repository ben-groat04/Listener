"""Valid reference predictors (pool-independent, pass the independence gate). Signature: predict(train, cands, meta, cutoff) -> scores (higher = more
likely loved). No noise is added: tied scores stay tied (metrics average over tie-breaks). DIAGNOSTICS (use post-cutoff pool information, not valid
predictors) are computed inside the harness from raw pool data (run.score_diagnostics), not here."""
import re, os, hashlib
from pathlib import Path
import numpy as np, pandas as pd

HL = 180.0          # days, recency half-life
K_SMOOTH = 2.0      # smoothing pseudo-count of the artist love rate
_T0 = np.datetime64("2015-01-01")

def _threads():
    from threadpoolctl import threadpool_limits
    return threadpool_limits(2)

# ---------------------------------------------------------------- simple baselines
def popularity(train, cands, meta, cutoff):
    """Spotify popularity (public prior, no personal data)."""
    return meta.popularity.reindex(cands.trackId).fillna(0).values.astype(float)

def _artist_table(train, cutoff, half_life=None):
    d = train[["t", "artistIds"]].explode("artistIds").dropna()   # one row per (stream, artist) incl. featured artists
    w = np.ones(len(d)) if half_life is None else 0.5 ** ((cutoff - d.t).dt.days.values / half_life)
    return pd.Series(w, index=d.artistIds.values).groupby(level=0).sum()

def _artist_score(train, cands, cutoff, half_life):
    tab = _artist_table(train, cutoff, half_life)
    return np.array([max([tab.get(a, 0.0) for a in ids], default=0.0) for ids in cands.artistIds])

def artist_plays(train, cands, meta, cutoff):
    """Total historic plays of the track's artist."""
    return np.log1p(_artist_score(train, cands, cutoff, None))

def artist_recent(train, cands, meta, cutoff):
    """Recency-weighted artist plays (half-life 180 d) -- crude taste-drift handling."""
    return np.log1p(_artist_score(train, cands, cutoff, 180))

def artist_love_rate(train, cands, meta, cutoff):
    """Smoothed share of the artist's previously discovered songs that became loved (same label definition, labels only from songs whose horizon ended before cutoff)."""
    from .data import song_table, HORIZON_DAYS
    s = song_table(train)  # train has no data past cutoff, so late songs get truncated horizons: keep only mature ones
    s = s[s["first"] < cutoff - pd.Timedelta(days=HORIZON_DAYS)]
    ex = s[["artistIds", "love"]].explode("artistIds").dropna()
    g = ex.groupby("artistIds").love.agg(["sum", "count"]); prior = s.love.mean(); k = 2.0
    rate = (g["sum"] + k * prior) / (g["count"] + k)
    sc = np.array([max([rate.get(a, prior) for a in ids], default=prior) for ids in cands.artistIds])
    return sc + 1e-3 * np.log1p(_artist_score(train, cands, cutoff, None))   # deterministic secondary key (artist plays), not noise

# ---------------------------------------------------------------- point-in-time features
def _sec(t): return ((np.asarray(t, dtype="datetime64[ns]") - _T0.astype("datetime64[ns]")) // np.timedelta64(1, "s")).astype(np.int64)

class _Hist:
    """Per-artist event tables of a train stream log, queried 'as of' arbitrary times (strictly before), so a training song's features use only
    streams before its own first play."""
    def __init__(self, train, songs):
        ev = train[["t", "artistIds"]].explode("artistIds").dropna()
        self.codes = pd.Index(pd.unique(np.r_[ev.artistIds.values, songs.artistIds.explode().dropna().values]))
        c = self.codes.get_indexer(ev.artistIds.values).astype(np.int64); sec = _sec(ev.t.values)
        k = (c << 32) | sec; o = np.argsort(k, kind="stable"); self.k, self.sec = k[o], sec[o]
        self.cs = np.r_[0.0, np.cumsum(2.0 ** (self.sec / 86400.0 / HL))]
        # song-level table: one row per (song, artist): first-play time and love label
        ex = songs[["first", "love", "artistIds"]].explode("artistIds").dropna()
        c2 = self.codes.get_indexer(ex.artistIds.values).astype(np.int64); s2 = _sec(ex["first"].values)
        k2 = (c2 << 32) | s2; o2 = np.argsort(k2, kind="stable"); self.k2 = k2[o2]; self.cl = np.r_[0.0, np.cumsum(ex.love.values[o2].astype(float))]
    def query(self, artist_lists, tsec, mature_sec):
        """Features of rows (artist list, time): plays all-time, plays with half-life, matured love (sum, n), earlier songs, last-played time, known-featured flag, new-artist flag."""
        n = len(artist_lists); ln = np.array([len(a) for a in artist_lists]); qi = np.repeat(np.arange(n), ln)
        pos = np.concatenate([np.arange(l) for l in ln]) if n else np.zeros(0, int)
        c = self.codes.get_indexer(np.concatenate([np.asarray(a, dtype=object) for a in artist_lists]) if n else []).astype(np.int64)
        t = tsec[qi]; base = c << 32
        lo = np.searchsorted(self.k, base); hi = np.searchsorted(self.k, base | t)
        cnt = hi - lo; wsum = (self.cs[hi] - self.cs[lo]) * 2.0 ** (-t / 86400.0 / HL)
        last = np.where(cnt > 0, self.sec[np.maximum(hi - 1, 0)], -1)
        lo2 = np.searchsorted(self.k2, base); hi2 = np.searchsorted(self.k2, base | t); hm = np.searchsorted(self.k2, base | mature_sec[qi])
        nm = hm - lo2; lm = self.cl[hm] - self.cl[lo2]; nearlier = hi2 - lo2
        bad = c < 0; cnt[bad] = 0; wsum[bad] = 0; nm[bad] = 0; lm[bad] = 0; nearlier[bad] = 0; last[bad] = -1
        return dict(qi=qi, pos=pos, cnt=cnt, wsum=wsum, nm=nm, lm=lm, nearlier=nearlier, last=last, t=t, n=n)

def _agg(q, f):
    out = np.full(q["n"], -np.inf); np.maximum.at(out, q["qi"], f); return out

def _artist_feats(h, artist_lists, tsec, prior):
    q = h.query(artist_lists, tsec, tsec - 90 * 86400)
    rate = (q["lm"] + K_SMOOTH * prior) / (q["nm"] + K_SMOOTH)
    ds = np.where(q["last"] >= 0, (q["t"] - q["last"]) / 86400.0, np.nan)
    dmin = np.full(q["n"], np.inf); np.minimum.at(dmin, q["qi"], np.where(np.isnan(ds), np.inf, ds)); dmin[np.isinf(dmin)] = np.nan
    feat_known = np.zeros(q["n"]); np.maximum.at(feat_known, q["qi"], ((q["pos"] > 0) & (q["cnt"] > 0)).astype(float))
    first_cnt = np.zeros(q["n"]); np.maximum.at(first_cnt, q["qi"], np.where(q["pos"] == 0, q["cnt"], 0))
    return pd.DataFrame(dict(ap_all=_agg(q, q["cnt"]), ap_hl=_agg(q, q["wsum"]), love_rate=_agg(q, rate), n_songs=_agg(q, q["nearlier"]),
                             days_since=dmin, feat_known=feat_known, new_artist=(first_cnt == 0).astype(float)))

KW = ["live", "remix", "acoustic", "remaster(?:ed)?", "version", "edit", "(?:feat|ft|featuring)", "intro", "interlude", "skit", "instrumental", "demo", "mix"]
_KW = [re.compile(r"\b" + k + r"\b") for k in KW]
META_COLS = ["dur", "explicit", "popularity", "preview", "nart", "title_len", "album_eq_title"] + ["kw_" + k.split("(")[0].strip("?:") for k in KW]

def _meta_feats(trackId, title, artistIds, meta):
    m = meta.reindex(trackId); tl = pd.Series(title).fillna("").str.lower().str.strip().values
    X = pd.DataFrame(dict(dur=m.durationMs.values.astype(float), explicit=m.explicit.astype(float).values, popularity=m.popularity.values.astype(float),
                          preview=m.previewUrl.notna().astype(float).values, nart=[len(a) for a in artistIds], title_len=[len(x) for x in tl],
                          album_eq_title=(m.albumName.fillna("").str.lower().str.strip().values == tl).astype(float)))
    for k, rx in zip(META_COLS[7:], _KW): X[k] = [float(bool(rx.search(x))) for x in tl]
    return X

# ---------------------------------------------------------------- GBM baselines (fit once per cutoff/train, cached)
GBM_KW = dict(max_iter=150, learning_rate=0.05, max_leaf_nodes=8, min_samples_leaf=40, l2_regularization=1.0, early_stopping=False, random_state=0)
# Artist-history features are confounded with calendar time in the training rows (counts grow with the history length while the love rate of newly discovered
# songs falls from ~65% to ~20%), and an unconstrained GBM learned the REVERSED direction (TUNE sauc 0.46, below chance). So: familiarity features are monotone
# (more familiar artist => not less likely loved) and training songs are weighted by recency (half-life 180 d, as artist_recent).
MONO = dict(ap_all=1, ap_hl=1, love_rate=1, n_songs=1, days_since=-1, feat_known=1, new_artist=-1)
WEIGHT_HL = 180.0   # days: exponential recency weight of training songs (half-life), None = uniform
_FIT = {}

def _train_key(name, train, cutoff):
    """Fit-cache key: cutoff, null seed (EVALKIT_NULL_SEED), and hashes of the train identities (trackId, song, artist) and timestamps, so a cached fit can never be reused
    for a different seed or a relabelled / shuffled train. With EVALKIT_NO_FIT_CACHE set the cache is bypassed altogether."""
    def hid(a):   # position-weighted hash of the values (a plain sum of row hashes would be blind to a permutation of the rows)
        v = pd.util.hash_array(np.asarray(a).astype(str).astype(object)); return int((v * (np.arange(len(v), dtype=np.uint64) * 2 + 1)).sum() % (1 << 60))
    return (name, str(cutoff), os.environ.get("EVALKIT_NULL_SEED", ""), len(train), hid(train.trackId.values), hid(train.song.values), hid(train.artist.values), int(train.t.values.astype("int64").sum() % (1 << 60)))

def _features(use_meta, rows, tsec, meta, hist=None, prior=None):
    parts = []
    if use_meta == "dur": parts.append(_meta_feats(rows.trackId.values, rows.trackName.values, rows.artistIds.values, meta)[["dur"]])
    elif use_meta: parts.append(_meta_feats(rows.trackId.values, rows.trackName.values, rows.artistIds.values, meta))
    if hist is not None: parts.append(_artist_feats(hist, list(rows.artistIds.values), tsec, prior))
    return pd.concat([p.reset_index(drop=True) for p in parts], axis=1)

def _make(name, use_meta, use_artist):
    def predict(train, cands, meta, cutoff):
        """Training rows: train songs first played before cutoff-90d (label horizon complete) with meta available, labels from song_table(train)."""
        from sklearn.ensemble import HistGradientBoostingClassifier
        from threadpoolctl import threadpool_limits
        from .data import song_table, HORIZON_DAYS
        key = _train_key(name, train, cutoff); csec = int(_sec(np.array([np.datetime64(cutoff)]))[0])
        _nofit = bool(os.environ.get("EVALKIT_NO_FIT_CACHE")); fit = {} if _nofit else _FIT
        if key not in fit:
            st = song_table(train).reset_index(); mt = st[st["first"] < cutoff - pd.Timedelta(days=HORIZON_DAYS)]
            hist, prior = (_Hist(train, st), float(mt.love.mean()) if len(mt) else .25) if use_artist else (None, None)
            rows = mt[mt.trackId.isin(meta.index)].reset_index(drop=True); y = rows.love.values
            X = _features(use_meta, rows, _sec(rows["first"].values), meta, hist, prior); mdl = None
            if 0 < y.sum() < len(y):
                w = None if WEIGHT_HL is None else 0.5 ** ((cutoff - rows["first"]).dt.days.values / WEIGHT_HL)
                with threadpool_limits(2):
                    mdl = HistGradientBoostingClassifier(monotonic_cst=[MONO.get(c, 0) for c in X.columns], **GBM_KW).fit(X, y, sample_weight=w)
            fit[key] = (mdl, float(y.mean()) if len(y) else .5, list(X.columns), hist, prior)
        mdl, base, cols, hist, prior = fit[key]
        if mdl is None: return np.full(len(cands), base)
        X = _features(use_meta, cands, np.full(len(cands), csec), meta, hist, prior)[cols]
        with threadpool_limits(2): return mdl.predict_proba(X)[:, 1]
    return predict

duration = _make("duration", "dur", False)
duration.__doc__ = "HistGradientBoosting on track duration (meta.durationMs) alone: learns the direction/shape of any duration effect from train songs."
meta_gbm = _make("meta_gbm", True, False)
meta_gbm.__doc__ = ("HistGradientBoosting on metadata only (duration, explicit, popularity, preview present, #artists, title length, album==title, title keyword flags). "
                    "Training rows: train songs first played before cutoff-90d, labels from song_table(train).")
nonaudio_gbm = _make("nonaudio_gbm", True, True)
nonaudio_gbm.__doc__ = ("meta_gbm features + point-in-time artist-history features (artist plays all-time and 180-day half-life, smoothed love rate of matured songs, "
                        "#earlier songs, days since last played, featured artist known, new-artist flag; training rows use streams before the song's own first play, candidates all train streams). "
                        "THE reference that any music/content claim must beat.")

# ---------------------------------------------------------------- open-pool shortcut references (v4): preview presence / source carry no taste information
_MAN = {}
def _manifest_source():
    """md5(previewUrl) -> source (spotify / itunes_meta / itunes_fallback) from the shared preview manifest (harness-side reference only)."""
    if not _MAN:
        f = Path(__file__).resolve().parents[1] / ".cache" / "shared" / "previews" / "manifest.csv"
        m = pd.read_csv(f, usecols=["md5", "source"]) if f.exists() else pd.DataFrame(columns=["md5", "source"])
        _MAN.update(dict(zip(m.md5, m.source)))
    return _MAN

def has_preview(train, cands, meta, cutoff):
    """Shortcut reference: 1 if the candidate has a previewUrl (Spotify, Apple or iTunes fallback)."""
    return meta.previewUrl.reindex(cands.trackId).notna().values.astype(float)

def preview_source_itunes(train, cands, meta, cutoff):
    """Shortcut reference: 1 if the candidate's preview is iTunes-sourced (manifest source itunes_meta / itunes_fallback), 0 if Spotify-sourced or absent."""
    man = _manifest_source(); u = meta.previewUrl.reindex(cands.trackId).values
    return np.array([float(str(man.get(hashlib.md5(x.encode()).hexdigest(), "")).startswith("itunes")) if isinstance(x, str) else 0.0 for x in u])

SHORTCUTS = dict(has_preview=has_preview, preview_source_itunes=preview_source_itunes)   # scored next to the baselines, exempt from the null control / independence / constant-score warning
REFERENCES = ("nonaudio_gbm", "artist_recent", "duration", "meta_gbm", "ref_audio_final", "ref_w4r1_listening", "ref_w4r1_music")   # the references of the VERDICT (best_ref is the one with the highest TUNE point sauc); v4.1 adds the two Workflow 4 round-1 finals
DIAGNOSTIC = ("pool_artist_siblings", "pool_album_siblings", "exposure_before", "exposure_after", "exposure_session", "replays_first_session", "oracle_day1", "oracle_7d")   # harness-computed references, not predictors
BASELINES = dict(popularity=popularity, artist_plays=artist_plays, artist_recent=artist_recent, artist_love_rate=artist_love_rate,
                 duration=duration, meta_gbm=meta_gbm, nonaudio_gbm=nonaudio_gbm)
