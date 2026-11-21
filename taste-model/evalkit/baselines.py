"""Valid reference predictors (pool-independent, pass the independence gate). Signature: predict(train, cands, meta, cutoff) -> scores (higher = more
likely loved). No noise is added: tied scores stay tied (metrics average over tie-breaks). DIAGNOSTICS (use post-cutoff pool information, not valid
predictors) are computed inside the harness from raw pool data (run.score_diagnostics), not here."""
import re
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
_FIT = {}
def _gbm():
    from sklearn.ensemble import HistGradientBoostingClassifier
    return HistGradientBoostingClassifier(max_iter=150, learning_rate=0.05, max_leaf_nodes=8, min_samples_leaf=40, l2_regularization=1.0, early_stopping=False, random_state=0)

def _train_key(name, train, cutoff):
    return (name, str(cutoff), len(train), int(pd.util.hash_array(train.trackId.values).sum() % (1 << 60)), int(train.t.values.astype("int64").sum() % (1 << 60)))

def _fit_predict(name, train, cands, meta, cutoff, feats):
    """feats(rows, kind) -> DataFrame of features for training songs (kind='train', with `first`) or candidates (kind='cand').
    Training rows: train songs whose first play is before cutoff-90d (label horizon complete), labels from song_table(train), meta available."""
    from .data import song_table, HORIZON_DAYS
    key = _train_key(name, train, cutoff)
    if key not in _FIT:
        s = song_table(train).reset_index()
        s = s[(s["first"] < cutoff - pd.Timedelta(days=HORIZON_DAYS)) & s.trackId.isin(meta.index)].reset_index(drop=True)
        with _threads():
            X = feats(s, "train", train, s, cutoff); y = s.love.values
            mdl = _gbm().fit(X, y) if 0 < y.sum() < len(y) else None
        _FIT[key] = (mdl, float(y.mean()) if len(y) else 0.5, list(X.columns))
    mdl, prior, cols = _FIT[key]
    if mdl is None: return np.full(len(cands), prior)
    with _threads(): X = feats(cands, "cand", train, None, cutoff, meta)[cols]; return mdl.predict_proba(X)[:, 1]

def _mk(name, use_meta, use_artist):
    def feats(rows, kind, train, songs=None, cutoff=None, meta=None):
        meta = meta if meta is not None else feats.meta
        parts = []
        if use_meta is True: parts.append(_meta_feats(rows.trackId.values, rows.trackName.values, rows.artistIds.values, meta))
        elif use_meta == "dur": parts.append(_meta_feats(rows.trackId.values, rows.trackName.values, rows.artistIds.values, meta)[["dur"]])
        if use_artist:
            allsongs = songs if songs is not None else feats.songs
            tsec = _sec(rows["first"].values) if kind == "train" else np.full(len(rows), _sec(np.array([np.datetime64(cutoff)]))[0])
            mat = allsongs  # love labels of matured songs: see _Hist
            parts.append(_artist_feats(feats.hist, list(rows.artistIds.values), tsec, feats.prior).reset_index(drop=True))
        X = pd.concat([p.reset_index(drop=True) for p in parts], axis=1); X.index = range(len(X)); return X
    def predict(train, cands, meta, cutoff):
        from .data import song_table, HORIZON_DAYS
        if use_artist:
            key = _train_key("hist", train, cutoff)
            if key not in _FIT:
                st = song_table(train).reset_index(); mt = st[st["first"] < cutoff - pd.Timedelta(days=HORIZON_DAYS)]
                _FIT[key] = (_Hist(train, st), float(mt.love.mean()) if len(mt) else 0.25, st)
            feats.hist, feats.prior, feats.songs = _FIT[key]
        feats.meta = meta
        f2 = lambda rows, kind, tr, songs, c, m=None: feats(rows, kind, tr, songs, c, m if m is not None else meta)
        return _fit_predict(name, train, cands, meta, cutoff, f2)
    predict.__doc__ = f"GBM baseline {name}"
    return predict

duration = _mk("duration", "dur", False)
duration.__doc__ = "HistGradientBoosting on track duration (meta.durationMs) alone: learns the direction/shape of any duration effect from train songs."
meta_gbm = _mk("meta_gbm", True, False)
meta_gbm.__doc__ = ("HistGradientBoosting on metadata only (duration, explicit, popularity, preview present, #artists, title length, album==title, title keyword flags). "
                    "Training rows: train songs first played before cutoff-90d, labels from song_table(train).")
nonaudio_gbm = _mk("nonaudio_gbm", True, True)
nonaudio_gbm.__doc__ = ("meta_gbm features + point-in-time artist-history features (artist plays all-time and 180-day half-life, smoothed love rate of matured songs, "
                        "#earlier songs, days since last played, featured artist known, new-artist flag; training rows use streams before the song's own first play, candidates all train streams). "
                        "THE reference that any music/content claim must beat.")

DIAGNOSTIC = ("pool_artist_siblings", "pool_album_siblings", "exposure_session", "oracle_day1", "oracle_7d")   # harness-computed references, not predictors
BASELINES = dict(popularity=popularity, artist_plays=artist_plays, artist_recent=artist_recent, artist_love_rate=artist_love_rate,
                 duration=duration, meta_gbm=meta_gbm, nonaudio_gbm=nonaudio_gbm)
