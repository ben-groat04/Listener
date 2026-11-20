"""Simple reference predictors. Signature: predict(train, cands, meta, cutoff) -> scores (higher = more likely loved)."""
import numpy as np, pandas as pd

def _tie(n, seed=0): return np.random.default_rng(seed).random(n) * 1e-9

def random_(train, cands, meta, cutoff):
    """Chance level. Keyed on the (opaque) track id so the score of a candidate does not depend on the pool."""
    return (cands.trackId.values % 1000003) / 1000003.0

def popularity(train, cands, meta, cutoff):
    """Spotify popularity (public prior, no personal data)."""
    return meta.popularity.reindex(cands.trackId).fillna(0).values + _tie(len(cands))

def _artist_table(train, cutoff, half_life=None):
    # one row per (stream, artist) incl. featured artists
    d = train[["t", "artistIds"]].explode("artistIds").dropna()
    w = np.ones(len(d)) if half_life is None else 0.5 ** ((cutoff - d.t).dt.days.values / half_life)
    return pd.Series(w, index=d.artistIds.values).groupby(level=0).sum()

def _artist_score(train, cands, cutoff, half_life):
    tab = _artist_table(train, cutoff, half_life)
    return np.array([max([tab.get(a, 0.0) for a in ids], default=0.0) for ids in cands.artistIds])

def artist_plays(train, cands, meta, cutoff):
    """Total historic plays of the track's artist."""
    return np.log1p(_artist_score(train, cands, cutoff, None)) + _tie(len(cands))

def artist_recent(train, cands, meta, cutoff):
    """Recency-weighted artist plays (half-life 180 d) -- crude taste-drift handling."""
    return np.log1p(_artist_score(train, cands, cutoff, 180)) + _tie(len(cands))

def artist_love_rate(train, cands, meta, cutoff):
    """Smoothed share of the artist's previously discovered songs that became loved (same label definition, labels only from songs whose horizon ended before cutoff)."""
    from .data import song_table, HORIZON_DAYS
    s = song_table(train)  # train has no data past cutoff, so late songs get truncated horizons: keep only mature ones
    s = s[s["first"] < cutoff - pd.Timedelta(days=HORIZON_DAYS)]
    ex = s[["artistIds", "love"]].explode("artistIds").dropna()
    g = ex.groupby("artistIds").love.agg(["sum", "count"]); prior = s.love.mean(); k = 2.0
    rate = (g["sum"] + k * prior) / (g["count"] + k)
    sc = np.array([max([rate.get(a, prior) for a in ids], default=prior) for ids in cands.artistIds])
    return sc + 1e-3 * np.log1p(_artist_score(train, cands, cutoff, None)) + _tie(len(cands))

def pool_artist_siblings(train, cands, meta, cutoff):
    """DIAGNOSTIC, not a valid predictor: number of OTHER candidates in the pool by the same primary artist.
    Pool composition is shaped by the user's future behaviour (binge artists), so this scores above chance with no music or
    history at all. Any method must beat it (paired CI)."""
    n = cands.groupby("artist").artist.transform("size").values - 1
    return n + _tie(len(cands))

def pool_album_siblings(train, cands, meta, cutoff):
    """DIAGNOSTIC, not a valid predictor: number of OTHER candidates on the same album."""
    return cands.groupby("albumId").albumId.transform("size").values - 1 + _tie(len(cands))

DIAGNOSTIC = {"pool_artist_siblings", "pool_album_siblings"}  # use the pool; exempt from the independence check
BASELINES = dict(random=random_, popularity=popularity, artist_plays=artist_plays,
                 artist_recent=artist_recent, artist_love_rate=artist_love_rate,
                 pool_artist_siblings=pool_artist_siblings, pool_album_siblings=pool_album_siblings)
