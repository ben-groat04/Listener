"""Extra point-in-time features (representation R1) on top of evalkit's nonaudio_gbm features.
All features of a row (a training song at its own first-play time tf, or a candidate at the cutoff) use only train streams strictly before tf;
song-level engagement of earlier songs is used only for songs whose 90-day horizon ended before tf.
Audio (optional): per-track CLAP embedding of the shared preview (independent per track); features are similarities to earlier songs / recent listening.
"""
import hashlib, os
import numpy as np, pandas as pd

H90 = np.timedelta64(90, "D")
EMB_FILE = "/home/user/Listener/taste-model/.cache/shared/w3r1-clap/emb.npz"
_E = {}

def emb_table():
    if "d" not in _E:
        try:
            z = np.load(EMB_FILE, allow_pickle=True); k = z["k"]; v = z["v"].astype(np.float32)
            v = v / np.maximum(np.linalg.norm(v, axis=1, keepdims=True), 1e-6); v[np.abs(z["v"]).sum(1) == 0] = np.nan
            _E["d"] = dict(zip(k, v))
        except Exception: _E["d"] = {}
    return _E["d"]

def track_emb(trackIds, meta):
    """(n,768) embeddings of tracks via meta.previewUrl (NaN row where no preview / no embedding)."""
    d = emb_table(); out = np.full((len(trackIds), 768), np.nan, np.float32)
    if not d: return out
    pu = meta.previewUrl.reindex(trackIds).values
    for i, u in enumerate(pu):
        if isinstance(u, str):
            v = d.get(hashlib.md5(u.encode()).hexdigest())
            if v is not None: out[i] = v
    return out


class Stream:
    """index of the train streams by primary artist and by album, time sorted."""
    def __init__(self, train, st):
        t = train.t.values.astype("datetime64[ns]")
        self.t = t
        self.art_idx = {a: np.flatnonzero(train.artist.values == a) for a in pd.unique(train.artist.values)}
        self.alb_idx = {a: np.flatnonzero(train.albumId.values == a) for a in pd.unique(train.albumId.values)}
        self.song = train.song.values; self.trk = train.trackId.values
        # song level (one row per song): rep primary artist, first time, plays90 etc.
        self.st = st
        s = st.sort_values("first")
        self.s_art = {a: g for a, g in s.groupby("artist")}
        self.gf = s["first"].values; self.gcum = np.r_[0.0, np.cumsum(np.log1p(s.plays90.values))]   # prior of the artist mean: mean over songs matured before tf
        self.tot_t = np.sort(t)

def _row_feats(S, artist, album, tf, ids_other=()):
    """feature dict for a primary artist `artist`, album `album` at time tf (np.datetime64)."""
    f = {}
    ia = S.art_idx.get(artist)
    if ia is None: ia = np.zeros(0, int)
    ta = S.t[ia]; nb = np.searchsorted(ta, tf)
    n30 = nb - np.searchsorted(ta, tf - np.timedelta64(30, "D")); n90 = nb - np.searchsorted(ta, tf - H90)
    n7 = nb - np.searchsorted(ta, tf - np.timedelta64(7, "D"))
    tot90 = np.searchsorted(S.tot_t, tf) - np.searchsorted(S.tot_t, tf - H90)
    f["a_n7"] = n7; f["a_n30"] = n30; f["a_n90"] = n90; f["a_share90"] = n90 / max(tot90, 1)
    if nb:
        sl = ta[np.searchsorted(ta, tf - H90):nb]
        f["a_days90"] = len(np.unique(sl.astype("datetime64[D]"))) if len(sl) else 0
        f["a_first_age"] = float((tf - ta[0]) / np.timedelta64(1, "D"))
        # fraction of the artist's plays that are in the last 90 d (current vs old interest)
        f["a_recent_frac"] = n90 / nb
    else:
        f["a_days90"] = 0; f["a_first_age"] = np.nan; f["a_recent_frac"] = np.nan
    # earlier songs of the artist: engagement (matured only), relative meta
    g = S.s_art.get(artist)
    km_g = np.searchsorted(S.gf, tf - H90); prior_lp = S.gcum[km_g] / km_g if km_g >= 10 else 2.0
    nm = 0; lpm = prior_lp; mx = np.nan; fl = np.nan
    if g is not None:
        fs = g["first"].values; k = np.searchsorted(fs, tf)              # earlier songs (first play before tf)
        km = np.searchsorted(fs, tf - H90)                                # matured songs
        if km > 0:
            lp = np.log1p(g.plays90.values[:km]); w = 0.5 ** (((tf - fs[:km]) / np.timedelta64(1, "D")).astype(float) / 365.0)
            nm = km; lpm = float((lp * w).sum() + 2 * prior_lp) / (w.sum() + 2); mx = float(lp.max()); fl = float(g.love.values[:km].mean())
        if k > 0:
            f["_dur_mean"] = np.nanmean(g.dur.values[:k]) if np.isfinite(g.dur.values[:k]).any() else np.nan
            f["_pop_mean"] = np.nanmean(g["popu"].values[:k]) if np.isfinite(g["popu"].values[:k]).any() else np.nan
    f["a_lp_mean"] = lpm; f["a_lp_max"] = mx; f["a_love_frac"] = fl
    ib = S.alb_idx.get(album)
    if ib is not None:
        tb = S.t[ib]; nbb = np.searchsorted(tb, tf)
        f["al_n"] = nbb; f["al_n90"] = nbb - np.searchsorted(tb, tf - H90)
        f["al_songs"] = len(np.unique(S.song[ib[:nbb]])) if nbb else 0
    else:
        f["al_n"] = 0; f["al_n90"] = 0; f["al_songs"] = 0
    return f


def extra_features(S, art, alb, tfs, dur, pop):
    """art, alb: primary artist / album ids per row; tfs: datetime64 per row; dur,pop: candidate meta."""
    rows = [_row_feats(S, a, b, t) for a, b, t in zip(art, alb, tfs)]
    X = pd.DataFrame(rows)
    X["dur_rel"] = dur - X.pop("_dur_mean") if "_dur_mean" in X else np.nan
    X["pop_rel"] = pop - X.pop("_pop_mean") if "_pop_mean" in X else np.nan
    for c in ("dur_rel", "pop_rel"):
        if c not in X: X[c] = np.nan
    return X


def audio_features(S, E_rows, tfs, E_song, song_first, song_grade, song_love, E_trk, trk_codes_stream, trk_t, E_cent_cache=None):
    """Similarity of each row's embedding (E_rows, normalised, NaN if missing) to
       pos_top3 / neg_top3: mean of 3 largest cosine similarities to loved / dismissed songs that matured before tf (within the last 450 days),
       cent60 / cent365: cosine similarity to the play-weighted centroid of everything played in the last 60 / 365 days (track embeddings, plays of tracks w/o preview ignored)."""
    n = len(E_rows); out = np.full((n, 4), np.nan)
    ok_song = np.isfinite(E_song[:, 0])
    ok_trk = np.isfinite(E_trk[:, 0]) if len(E_trk) else np.zeros(0, bool)
    for i in range(n):
        e = E_rows[i]
        if not np.isfinite(e[0]): continue
        tf = tfs[i]
        m = ok_song & (song_first < tf - H90) & (song_first >= tf - np.timedelta64(450, "D"))
        if m.any():
            sims = E_song[m] @ e; lv = song_love[m].astype(bool); dis = song_grade[m] <= 1
            if lv.sum() >= 3: out[i, 0] = np.sort(sims[lv])[-3:].mean()
            if dis.sum() >= 3: out[i, 1] = np.sort(sims[dis])[-3:].mean()
        for j, d in enumerate((60, 365)):
            lo = np.searchsorted(trk_t, tf - np.timedelta64(d, "D")); hi = np.searchsorted(trk_t, tf)
            c = trk_codes_stream[lo:hi]; c = c[ok_trk[c]] if len(c) else c
            if len(c) >= 5:
                w = np.bincount(c, minlength=len(E_trk)); nz = np.flatnonzero(w)
                cen = (w[nz, None] * E_trk[nz]).sum(0); out[i, 2 + j] = float(e @ cen / max(np.linalg.norm(cen), 1e-6))
    return pd.DataFrame(out, columns=["au_pos3", "au_neg3", "au_cent60", "au_cent365"])
