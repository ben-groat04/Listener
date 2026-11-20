"""Data loading, song identity, fold construction and labels. All time logic lives here."""
import re, json, hashlib
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[1]
STREAMS = ROOT.parent / "spotify-liked-songs/.cache/streams.jsonl"
TOP_TRACKS = ROOT.parent / "spotify-liked-songs/.cache/top_tracks.json"
SEALED_DIR = ROOT / ".sealed"
DECOYS = ROOT / "evalkit" / "decoy_universe.csv.gz"  # build-time resource: builders must not read it
DECOY_RATIO = 5     # decoys per tried song in the open pool (~20x the loved songs at a ~25% love rate); label-independent
ID_SALT = "evalkit-v2"

HORIZON_DAYS = 90            # how long after first listen we watch a song to decide if it was loved
LOVE_PLAYS, LOVE_DAYS = 6, 3     # "love": >=6 plays on >=3 distinct days within the horizon
STRONG_PLAYS, STRONG_DAYS = 15, 5  # "strong": a clear favourite
# Dev folds: cutoffs quarterly; each tests songs FIRST heard in [cutoff, cutoff+3 months).
DEV_CUTOFFS = ["2023-01-01", "2023-04-01", "2023-07-01", "2023-10-01",
               "2024-01-01", "2024-04-01", "2024-07-01", "2024-10-01"]
DEV_END = pd.Timestamp("2025-04-01")  # builders/researchers may not look at any stream at/after this
SEALED_CUTOFFS = ["2025-04-01", "2025-07-01", "2025-10-01", "2026-01-01", "2026-04-01"]


def song_key(name: str) -> str:
    """Normalised title: merges re-releases/remasters/live/deluxe versions of the same song."""
    n = re.sub(r"\s*[\(\[][^)\]]*[\)\]]", "", name.lower())
    n = re.sub(r"\s+-\s+.*$", "", n)
    k = re.sub(r"\W+", " ", n).strip()
    return k or re.sub(r"\W+", " ", name.lower()).strip()   # a title that is entirely in brackets, e.g. '(JFK)', keeps its text


def _load_all() -> pd.DataFrame:
    """All streams, chronological, with a song identity that is robust to stats.fm quirks: the same trackId can appear
    under different artist ids or as 'unknown track name' (3% of plays), so song keys (title|primary artist) and trackIds
    are linked into connected components; every stream of a component gets the same song string (the earliest named key)."""
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    d = pd.read_json(STREAMS, lines=True)
    d["t"] = pd.to_datetime(d.endTime).dt.tz_localize(None)
    d["artist"] = d.artistIds.map(lambda a: a[0] if len(a) else -1)
    d = d.sort_values("t", kind="stable").drop_duplicates(["trackId", "t"]).reset_index(drop=True)  # exact re-imported duplicate plays
    unk = d.trackName.str.lower().str.strip().isin(["unknown track name", ""])
    key = np.where(unk, "unknown" + d.trackId.astype(str), d.trackName.map(song_key)) ; key = pd.Series(key) + "|" + d.artist.astype(str)
    kc, ku = pd.factorize(key); tc, tu = pd.factorize(d.trackId)
    n = len(ku) + len(tu)
    _, comp = connected_components(coo_matrix((np.ones(len(d)), (kc, tc + len(ku))), shape=(n, n)), directed=False)
    d["_comp"] = comp[kc]; d["_key"] = key.values
    named_first = d[~unk].drop_duplicates("_comp").set_index("_comp")["_key"]   # earliest named stream's key
    any_first = d.drop_duplicates("_comp").set_index("_comp")["_key"]
    canon = any_first.copy(); canon.loc[named_first.index] = named_first
    d["song"] = d._comp.map(canon); d["named"] = ~unk.values
    cols = ["t", "trackId", "albumId", "artistIds", "artist", "trackName", "song", "playedMs", "contextId", "named"]
    return d[cols]


def load_streams(until=None, _sealed=False) -> pd.DataFrame:
    """Streams strictly before `until` (default DEV_END). Going past DEV_END needs the sealed runner."""
    until = DEV_END if until is None else pd.Timestamp(until)
    if until > DEV_END and not _sealed:
        raise PermissionError(f"streams at/after {DEV_END.date()} are sealed")
    d = _load_all()
    return d[d.t < until].reset_index(drop=True)


def load_meta() -> pd.DataFrame:
    """Static track metadata indexed by trackId. Lifetime play counts/rank are deliberately dropped.
    Caveat: spotifyPopularity is measured in 2026 (mild look-ahead; popularity is a public prior)."""
    rows = []
    for r in json.load(open(TOP_TRACKS)):
        t = r["track"]
        rows.append(dict(trackId=t["id"], name=t.get("name"), durationMs=t.get("durationMs"), explicit=t.get("explicit"),
                         popularity=t.get("spotifyPopularity"),
                         spotifyId=(t.get("externalIds", {}).get("spotify") or [None])[0],
                         previewUrl=t.get("spotifyPreview") or t.get("appleMusicPreview"),
                         albumName=(t["albums"][0]["name"] if t.get("albums") else None),
                         artistNames=[a["name"] for a in t.get("artists", [])]))
    return pd.DataFrame(rows).drop_duplicates("trackId").set_index("trackId")


def song_table(all_streams: pd.DataFrame) -> pd.DataFrame:
    """Per-song first listen, representative track, and love statistics over the horizon."""
    d = all_streams
    first = d.groupby("song").t.transform("min")
    d = d.assign(first=first)
    inh = d[d.t < d["first"] + pd.Timedelta(days=HORIZON_DAYS)]
    st = inh.groupby("song").agg(plays90=("t", "size"), days90=("t", lambda s: s.dt.normalize().nunique()))
    rc = ["song", "t", "trackId", "albumId", "artistIds", "artist", "trackName"]
    d = d.sort_values("t", kind="stable")
    rep = d.drop_duplicates("song")[rc].set_index("song")
    if "named" in d:   # representative = earliest NAMED stream ('unknown track name' streams carry no usable identity/meta); `first` stays the earliest stream
        nm = d[d.named].drop_duplicates("song")[rc].set_index("song")
        rep = pd.concat([rep[~rep.index.isin(nm.index)], nm])
        rep["t"] = d.groupby("song").t.min().reindex(rep.index)
    s = rep.rename(columns={"t": "first"}).join(st)
    s["love"] = ((s.plays90 >= LOVE_PLAYS) & (s.days90 >= LOVE_DAYS)).astype(int)
    s["strong"] = ((s.plays90 >= STRONG_PLAYS) & (s.days90 >= STRONG_DAYS)).astype(int)
    # neighbouring label definitions for the sensitivity check (never the primary target)
    s["love_4_2"] = ((s.plays90 >= 4) & (s.days90 >= 2)).astype(int)
    s["love_10_4"] = ((s.plays90 >= 10) & (s.days90 >= 4)).astype(int)
    return s


_MOK = []
def _meta_ok():
    if not _MOK:
        m = load_meta(); _MOK.append(set(m.index[m.name.notna() & m.popularity.notna()]))
    return _MOK[0]

def make_folds(cutoffs, all_streams=None):
    """Yield (cutoff, candidates_with_labels). Candidates = songs never heard before cutoff whose
    first listen is in [cutoff, cutoff+3 months). The label columns must never be shown to predictors."""
    d = _load_all() if all_streams is None else all_streams
    s = song_table(d)
    for c in cutoffs:
        c = pd.Timestamp(c)
        end = c + pd.DateOffset(months=3)
        f = s[(s["first"] >= c) & (s["first"] < end)].copy()
        f["cutoff"] = c
        seen = set(d.loc[d.t < c, "artist"])
        f["new_artist"] = ~f.artist.isin(seen)
        # songs with no usable identity (never named in any stream, or no metadata record) cannot be scored from anything and
        # would otherwise be recognisable as 'user-played' (decoys always have full metadata): not candidates. Label-independent.
        f = f.reset_index()
        ok = f.trackId.isin(_meta_ok()) & ~f.song.str.startswith("unknown")
        yield c, f[ok].reset_index(drop=True)


# ---------------------------------------------------------------- anonymisation (what predictors see)
_hc = {}
def h(x) -> int:
    """Opaque stable token for an id: usable for equality joins, carries no order/time information."""
    k = x if isinstance(x, (int, np.integer, str)) else str(x)
    v = _hc.get(k)
    if v is None: v = _hc[k] = int(hashlib.sha1(f"{ID_SALT}|{k}".encode()).hexdigest()[:13], 16)
    return v

def _anon_title(t: pd.Series) -> pd.Series:
    """'unknown<rawTrackId>' song keys carry a raw id: hash it like every other id."""
    return t.map(lambda x: "unknown%d" % h(int(x[7:])) if x.startswith("unknown") and x[7:].isdigit() else x)

def anon_streams(d: pd.DataFrame) -> pd.DataFrame:
    """Hash trackId/albumId/artistIds/artist, and the artist part of the song key. Row order stays chronological (it is the stream log)."""
    o = d.copy()
    o["trackId"] = o.trackId.map(h); o["albumId"] = o.albumId.map(h)
    o["artistIds"] = o.artistIds.map(lambda a: [h(x) for x in a]); o["artist"] = o.artist.map(h)
    o["song"] = _anon_title(d.song.str.rsplit("|", n=1).str[0]) + "|" + o.artist.astype(str)
    return o

def anon_song(song: pd.Series) -> pd.Series:
    return _anon_title(song.str.rsplit("|", n=1).str[0]) + "|" + song.str.rsplit("|", n=1).str[1].map(lambda a: str(h(int(a))))

# ---------------------------------------------------------------- open-universe (decoy) pool
def _decoys():
    u = pd.read_csv(DECOYS)
    u["artistIds"] = u.artistIds.map(lambda x: [int(i) for i in str(x).split(";")])
    u["artistNames"] = u.artistNames.map(lambda x: str(x).split(";"))
    u["artist"] = u.artistIds.map(lambda a: a[0]); u["release"] = pd.to_datetime(u.release)
    u["song"] = u.trackName.map(song_key) + "|" + u.artist.astype(str)
    return u

def make_open_folds(cutoffs, all_streams=None):
    """Yield (cutoff, pool). pool = the tried songs of make_folds (is_decoy=0) plus DECOY_RATIO x as many decoys
    (is_decoy=1): real songs by the user's artists / related artists that the user NEVER played (checked against the whole
    history incl. sealed era) and that were already released by the end of the fold window. Decoys get love=0 and are
    labelled 'not tried' (not 'would hate'). Sampling is seeded by the cutoff and independent of any label."""
    d = _load_all() if all_streams is None else all_streams
    u = _decoys(); played_songs = set(d.song); played_tracks = set(d.trackId); mm = load_meta_all()
    u = u[~u.song.isin(played_songs) & ~u.trackId.isin(played_tracks)].drop_duplicates("song")
    for c, f in make_folds(cutoffs, d):
        end = c + pd.DateOffset(months=3)
        seen = set(d.loc[d.t < c, "artist"])
        elig = u[u.release < end].copy(); elig["new_artist"] = ~elig.artist.isin(seen)
        # Covariate-matched decoys. v2.0 audit: a tried-vs-decoy classifier on metadata shape (missing fields, preview/spotifyId presence,
        # title==album, duration, explicit, #artists, popularity) reached AUC 0.73, so the open pool could be 'solved' without music or
        # history. Decoys are now drawn with probability proportional to the odds p/(1-p) of a logistic model (fit per fold on tried vs all
        # eligible decoys, metadata/public features only, NEVER labels), which re-weights the decoy universe to the tried songs' joint
        # distribution of these features and of the new-artist flag; popularity deciles + new-artist are additionally matched exactly.
        fm = mm.reindex(f.trackId); em = mm.reindex(elig.trackId)
        def feats(m, names, na):
            nm = names.str.lower().str.strip().values
            X = pd.DataFrame(dict(pv=m.previewUrl.notna().values, sid=m.spotifyId.notna().values,
                                  ae=(m.albumName.fillna("").str.lower().str.strip().values == nm), ex=m.explicit.fillna(False).astype(bool).values,
                                  dur=(m.durationMs.fillna(240000).values - 240000) / 60000.0, nart=m.artistNames.map(lambda a: len(a) if isinstance(a, list) else 1).values,
                                  ln=np.log1p(names.str.len().values), na=na.values.astype(float)))
            pop = m.popularity.fillna(0).values / 100.0
            for a_, b_ in (("pv", "sid"), ("pv", "ae"), ("sid", "ae"), ("pv", "ex"), ("sid", "ex"), ("ae", "ex"), ("pv", "dur"), ("sid", "dur"), ("ae", "dur"), ("pv", "ln"), ("sid", "ln"), ("ae", "ln"), ("pv", "nart"), ("sid", "nart"), ("na", "pv"), ("na", "sid"), ("na", "ae")):
                X[a_ + "_" + b_] = X[a_].astype(float) * X[b_].astype(float)
            for a_ in ("pv", "sid", "ae", "ex"): X[a_ + "_pop"] = X[a_].astype(float) * pop
            X["dur2"] = X.dur ** 2; X["ln2"] = X.ln ** 2; X["na_pop"] = X.na * (m.popularity.fillna(0).values / 100.0)
            return X.astype(float).values
        f = f.assign(_pb=(fm.popularity.fillna(0).values // 10).clip(0, 9)); elig["_pb"] = (em.popularity.fillna(0).values // 10).clip(0, 9)
        Xf, Xe = feats(fm, f.trackName, f.new_artist), feats(em, elig.trackName, elig.new_artist)
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import OneHotEncoder
        oh = OneHotEncoder(handle_unknown="ignore").fit(np.r_[f._pb.values, elig._pb.values].reshape(-1, 1))
        Z = lambda X, pb: np.c_[X, oh.transform(pb.values.reshape(-1, 1)).toarray()]
        clf = LogisticRegression(C=5.0, max_iter=2000, class_weight="balanced").fit(np.r_[Z(Xf, f._pb), Z(Xe, elig._pb)], np.r_[np.ones(len(f)), np.zeros(len(elig))])
        pr = np.clip(clf.predict_proba(Z(Xe, elig._pb))[:, 1], 1e-4, 1 - 1e-4); w = pr / (1 - pr); w = np.minimum(w, np.quantile(w, .995))
        rng = np.random.default_rng(int(c.strftime("%Y%m%d")))
        n_dec = min(len(elig), DECOY_RATIO * len(f)); key = np.log(rng.random(len(elig))) / w   # Efraimidis-Spirakis weighted sampling w/o replacement
        parts = [elig.iloc[np.argsort(-key)[:n_dec]]]
        dec = pd.concat(parts).copy()
        dec = dec.assign(first=pd.NaT, love=0, strong=0, plays90=0, days90=0, love_4_2=0, love_10_4=0, cutoff=c, is_decoy=1)
        tried = f.assign(is_decoy=0)
        cols = ["song", "trackId", "albumId", "artistIds", "artist", "trackName", "first", "cutoff", "new_artist", "is_decoy",
                "love", "strong", "plays90", "days90", "love_4_2", "love_10_4"]
        yield c, pd.concat([tried[cols], dec[cols]], ignore_index=True)

def load_meta_all() -> pd.DataFrame:
    """Meta for every track the harness can show (user's tracks + decoys), indexed by RAW trackId (internal)."""
    m = load_meta(); u = _decoys().drop_duplicates("trackId").set_index("trackId")
    u = u.assign(name=u.trackName)[["name", "durationMs", "explicit", "popularity", "spotifyId", "previewUrl", "albumName", "artistNames"]]
    return pd.concat([m, u[~u.index.isin(m.index)]])

def public_view(pool: pd.DataFrame, meta_all: pd.DataFrame, train_raw: pd.DataFrame, seed=0):
    """What a predictor may see about the pool: shuffled rows, opaque ids, no labels/flags/timing.
    Returns (cands, meta, order); order[i] = row of `pool` that public row i came from.
    meta covers only tracks in the train history or in the pool, so its index says nothing about other future tracks."""
    order = np.random.default_rng(seed).permutation(len(pool))
    p = pool.iloc[order]
    cands = pd.DataFrame(dict(song=anon_song(p.song).values, trackId=p.trackId.map(h).values, albumId=p.albumId.map(h).values,
                              artistIds=[[h(x) for x in a] for a in p.artistIds], artist=p.artist.map(h).values,
                              trackName=p.trackName.values))
    raw = pd.Index(train_raw.trackId.unique()).union(pd.Index(p.trackId.values))
    m = meta_all.reindex(raw)
    # meta.name of a pool track is overwritten with the candidate's title: v2.0 meta.name equalled the title for every decoy but differed
    # (version suffix / missing) for ~7% of tried songs, which identified them as user-played.
    m.loc[p.trackId.values, "name"] = p.trackName.values
    m.index = [h(x) for x in raw]; m.index.name = "trackId"
    return cands, m, order
