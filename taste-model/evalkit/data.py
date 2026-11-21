"""Data loading, song identity, fold construction and labels. All time logic lives here."""
import re, json, hashlib
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[1]
STREAMS = ROOT.parent / "spotify-liked-songs/.cache/streams.jsonl"
TOP_TRACKS = ROOT.parent / "spotify-liked-songs/.cache/top_tracks.json"
SEALED_DIR = ROOT / ".sealed"
DECOYS = ROOT / ".cache" / "decoy_universe.csv.gz"  # build-time resource: builders must not read it
DECOY_RATIO = 5     # decoys per tried song in the open pool (~20x the loved songs at a ~25% love rate); label-independent
ID_SALT = "evalkit-v2"   # unchanged in v3: opaque ids stay stable so per-track feature caches stay valid
SESSION_GAP_MIN = 30

HORIZON_DAYS = 90            # how long after first listen we watch a song to decide if it was loved
LOVE_PLAYS, LOVE_DAYS = 6, 3     # "love": >=6 plays on >=3 distinct days within the horizon
STRONG_PLAYS, STRONG_DAYS = 15, 5  # "strong": a clear favourite
# Dev folds: cutoffs quarterly; each tests songs FIRST heard in [cutoff, cutoff+3 months).
DEV_CUTOFFS = [str(c.date()) for c in pd.date_range("2021-07-01", "2024-10-01", freq="QS")]   # 14 quarterly folds
TUNE_CUTOFFS = DEV_CUTOFFS[:10]   # 2021-07 .. 2023-10: used for all iteration
LATE_CUTOFFS = DEV_CUTOFFS[10:]   # 2024-01 .. 2024-10: held-out dev slice; every `run --late` is logged (.cache/late_runs.log)
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
    # share90: plays90 / ALL the user's plays in the same song's own 90-day window [first, first+90d): normalises for listening volume over time
    tt = np.sort(d.t.values); f0 = s["first"].values.astype("datetime64[ns]")
    tot = np.searchsorted(tt, f0 + np.timedelta64(HORIZON_DAYS, "D")) - np.searchsorted(tt, f0)
    s["share90"] = s.plays90.values / np.maximum(tot, 1)
    return s


def _sessions(d: pd.DataFrame) -> np.ndarray:
    """Listening-session id per stream (d chronological): a new session starts after a gap of more than SESSION_GAP_MIN minutes."""
    return (d.t.diff() > pd.Timedelta(minutes=SESSION_GAP_MIN)).cumsum().values

def song_diag(d: pd.DataFrame) -> pd.DataFrame:
    """HARNESS-ONLY diagnostics per song (use post-cutoff information; never shown to predictors):
    sess = session id of the first play, week = ISO year*100+week of the first play, nnew_sess = number of distinct songs whose first play is in
    that same session (= exp_before + exp_after + 1), exp_before / exp_after = number of distinct songs whose first play is in the same session
    EARLIER / LATER than this song's first play, replays_s1 = plays of the song inside its first session, day1 = plays on the first-listen calendar
    day, d7 = plays in the first 7 days. NOTE: exp_after and replays_s1 can be consequences of liking the song (a liked song is replayed and
    followed by other new songs); exp_before cannot."""
    dd = d.assign(sess=_sessions(d)); f = dd.drop_duplicates("song")   # chronological => earliest stream of each song
    fs = f.set_index("song")
    out = pd.DataFrame(dict(sess=fs.sess, week=(fs.t.dt.isocalendar().year.astype(int) * 100 + fs.t.dt.isocalendar().week.astype(int)).values), index=fs.index)
    out["nnew_sess"] = out.sess.map(f.groupby("sess").song.nunique())
    out["exp_before"] = f.groupby("sess").cumcount().values.astype(int)   # f is chronological: position of the song among the new songs of its session
    out["exp_after"] = (out.nnew_sess.values - 1 - out.exp_before.values).astype(int)
    t0 = dd.song.map(fs.t)
    out["replays_s1"] = (dd.sess == dd.song.map(fs.sess)).groupby(dd.song).sum()
    out["day1"] = (dd.t.dt.normalize() == t0.dt.normalize()).groupby(dd.song).sum()
    out["d7"] = (dd.t < t0 + pd.Timedelta(days=7)).groupby(dd.song).sum()
    return out


_MOK = []
def _meta_ok():
    if not _MOK:
        m = load_meta(); _MOK.append(set(m.index[m.name.notna() & m.popularity.notna()]))
    return _MOK[0]

def make_folds(cutoffs, all_streams=None):
    """Yield (cutoff, candidates_with_labels). Candidates = songs never heard before cutoff whose
    first listen is in [cutoff, cutoff+3 months). The label columns must never be shown to predictors."""
    d = _load_all() if all_streams is None else all_streams
    s = song_table(d).join(song_diag(d))
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
RAW = ROOT / ".cache" / "decoy_raw"                 # per-artist stats.fm fetch cache (tracks/albums/related), shared with make_decoys
ALBUM_REL = ROOT / ".cache" / "album_release.json"  # albumId -> release date (ms) or null, for the tried songs' albums
FALLBACK = ROOT / ".cache" / "itunes_fallback.csv"
FALLBACK_DONE = ROOT / ".cache" / "itunes_fallback.complete"   # marker written by fetch_itunes when ALL targets are resolved; the fill is only active then (a partial fill would make preview presence mean different things for tried songs and decoys)  # iTunes Search preview lookup (built by evalkit/fetch_itunes.py)
N_SEED, N_REL_SEEDS, N_REL = 300, 150, 6            # per fold: top-300 pre-cutoff artists + up to 6 related artists of each of the top 150
PRESAMPLE = 8                                       # stage 1 draws PRESAMPLE x |tried| decoys (limits the iTunes lookups); stage 2 draws DECOY_RATIO x |tried| from them
API = "https://api.stats.fm/api/v1"

def related_artists(a):
    f = RAW / f"rel_{a}.json"
    return json.loads(f.read_text()) if f.exists() else None

def fold_seed_artists(d, c):
    """Seed artists of a fold from PRE-CUTOFF information only: the 300 artists with most plays in streams before c, plus up to 6 stats.fm
    related artists of each of the 150 most-played. Returns (seeds, related). Raises if a related list is not in the fetch cache (run make_decoys)."""
    cnt = d.loc[d.t < c, "artistIds"].explode().dropna().value_counts()
    seeds = [int(x) for x in cnt.index[:N_SEED]]; rel = []
    for a in seeds[:N_REL_SEEDS]:
        it = related_artists(a)
        if it is None: raise RuntimeError(f"related list of artist {a} (fold {c.date()}) not cached: run `python3 -m evalkit.make_decoys`")
        rel += [int(x["id"]) for x in it[:N_REL]]
    return seeds, list(dict.fromkeys(rel))

def _decoys():
    u = pd.read_csv(DECOYS)
    u["artistIds"] = u.artistIds.map(lambda x: [int(i) for i in str(x).split(";")])
    u["artistNames"] = u.artistNames.map(lambda x: str(x).split(";"))
    u["src"] = u.source_artists.map(lambda x: frozenset(int(i) for i in str(x).split(";")))
    u["artist"] = u.artistIds.map(lambda a: a[0]); u["release"] = pd.to_datetime(u.release)
    u["song"] = u.trackName.map(song_key) + "|" + u.artist.astype(str)
    return u

def _valid_ms(x): return x is not None and 0 < x < 4.1e12   # drop junk dates

def album_release(ids, fetch=True):
    """albumId -> release timestamp (NaT if unknown), cached in .cache/album_release.json; missing ids are fetched from api.stats.fm."""
    import urllib.request, time
    from concurrent.futures import ThreadPoolExecutor
    cache = json.loads(ALBUM_REL.read_text()) if ALBUM_REL.exists() else {}
    miss = [str(i) for i in dict.fromkeys(ids) if str(i) not in cache]
    if miss and fetch:
        def get(i):
            for k in range(4):
                try:
                    r = json.load(urllib.request.urlopen(urllib.request.Request(f"{API}/albums/{i}", headers={"User-Agent": "taste-eval-research/0.1"}), timeout=40))
                    return i, (r.get("item") or {}).get("releaseDate")
                except Exception as e:
                    if "404" in str(e): return i, None
                    time.sleep(1.5 * (k + 1))
            return i, "ERR"
        with ThreadPoolExecutor(4) as ex:
            for i, v in ex.map(get, miss):
                if v != "ERR": cache[i] = v if _valid_ms(v) else None
        ALBUM_REL.parent.mkdir(parents=True, exist_ok=True); ALBUM_REL.write_text(json.dumps(cache))
    return pd.Series([pd.to_datetime(cache.get(str(i)), unit="ms") if _valid_ms(cache.get(str(i))) else pd.NaT for i in ids], index=list(ids))

_TA = []
def _track_albums():
    """trackId -> album ids listed for the track in the metadata export (internal; ids are NOT exposed to predictors)."""
    if not _TA: _TA.append({r["track"]["id"]: [a["id"] for a in r["track"].get("albums", [])] for r in json.load(open(TOP_TRACKS))})
    return _TA[0]

def tried_release(f):
    """Release date of each tried song = earliest known release date over the albums listed for its track (and the stream's album). NaT = unknown."""
    ta = _track_albums(); al = [list(dict.fromkeys(ta.get(t, []) + [a])) for t, a in zip(f.trackId, f.albumId)]
    rel = album_release(sorted({x for l in al for x in l}))
    return pd.Series([min([rel[x] for x in l if pd.notna(rel[x])], default=pd.NaT) for l in al], index=f.index)

def release_bucket(release, c):
    """Release age relative to the cutoff: 0 <3 months (incl. released after the cutoff), 1 3-12 months, 2 1-3 years, 3 >3 years, 4 unknown."""
    age = (c - release).dt.days
    return np.select([age.isna(), age < 91, age < 365, age < 1096], [4, 0, 1, 2], 3).astype(int)

def _match_features(m, names, na, rb):
    nm = names.str.lower().str.strip().values
    X = pd.DataFrame(dict(pv=m.previewUrl.notna().values, sid=m.spotifyId.notna().values,
                          ae=(m.albumName.fillna("").str.lower().str.strip().values == nm), ex=m.explicit.fillna(False).astype(bool).values,
                          dur=(m.durationMs.fillna(240000).values - 240000) / 60000.0, nart=m.artistNames.map(lambda a: len(a) if isinstance(a, list) else 1).values,
                          ln=np.log1p(names.str.len().values), na=na.values.astype(float)))
    pop = m.popularity.fillna(0).values / 100.0
    for a_, b_ in (("pv", "sid"), ("pv", "ae"), ("sid", "ae"), ("pv", "ex"), ("sid", "ex"), ("ae", "ex"), ("pv", "dur"), ("sid", "dur"), ("ae", "dur"), ("pv", "ln"), ("sid", "ln"), ("ae", "ln"), ("pv", "nart"), ("sid", "nart"), ("na", "pv"), ("na", "sid"), ("na", "ae")):
        X[a_ + "_" + b_] = X[a_].astype(float) * X[b_].astype(float)
    for a_ in ("pv", "sid", "ae", "ex"): X[a_ + "_pop"] = X[a_].astype(float) * pop
    X["dur2"] = X.dur ** 2; X["ln2"] = X.ln ** 2; X["na_pop"] = X.na * pop
    for k in range(5):   # release-age bucket (relative to the cutoff), alone and crossed with new-artist / preview presence
        X[f"rb{k}"] = (rb == k).astype(float); X[f"rb{k}_na"] = X[f"rb{k}"] * X.na; X[f"rb{k}_pv"] = X[f"rb{k}"] * X.pv.astype(float)
    return X.astype(float).values

def _draw(f, elig, mm, n, seed):
    """Covariate-matched weighted sampling of n decoys from `elig` (rows of the universe). v2.0 audit: a tried-vs-decoy classifier on metadata shape
    reached AUC 0.73. Decoys are drawn with probability proportional to the odds p/(1-p) of a logistic model (fit per fold on tried vs all eligible
    decoys, metadata/public features + release-age bucket only, NEVER labels), which re-weights the universe to the tried songs' joint distribution of
    these features and of the new-artist flag; popularity deciles are additionally one-hot matched."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import OneHotEncoder
    fm = mm.reindex(f.trackId); em = mm.reindex(elig.trackId)
    pb_f = (fm.popularity.fillna(0).values // 10).clip(0, 9); pb_e = (em.popularity.fillna(0).values // 10).clip(0, 9)
    Xf = _match_features(fm, f.trackName, f.new_artist, f.rb.values); Xe = _match_features(em, elig.trackName, elig.new_artist, elig.rb.values)
    oh = OneHotEncoder(handle_unknown="ignore").fit(np.r_[pb_f, pb_e].reshape(-1, 1))
    Z = lambda X, pb: np.c_[X, oh.transform(pb.reshape(-1, 1)).toarray()]
    clf = LogisticRegression(C=5.0, max_iter=3000, class_weight="balanced").fit(np.r_[Z(Xf, pb_f), Z(Xe, pb_e)], np.r_[np.ones(len(f)), np.zeros(len(elig))])
    pr = np.clip(clf.predict_proba(Z(Xe, pb_e))[:, 1], 1e-4, 1 - 1e-4); w = pr / (1 - pr); w = np.minimum(w, np.quantile(w, .995))
    rng = np.random.default_rng(seed)
    key = np.log(rng.random(len(elig))) / w   # Efraimidis-Spirakis weighted sampling w/o replacement
    return elig.iloc[np.argsort(-key)[:min(n, len(elig))]]

def _open_parts(cutoffs, d):
    """Yield (cutoff, tried folds frame f, stage-1 decoy pre-sample, elig size). Everything here is label-independent; seeds use only pre-cutoff streams.
    Exclusion: any song/track the user EVER played (full history incl. later years; the harness may look, builders may not) is removed from the universe.
    Release age of tried songs comes from stats.fm album dates (tracks with no date: bucket 4 'unknown'; decoys always have a date)."""
    u = _decoys(); played_songs = set(d.song); played_tracks = set(d.trackId)
    u = u[~u.song.isin(played_songs) & ~u.trackId.isin(played_tracks)].drop_duplicates("song")
    resolved = set(fallback_table().trackId); active = FALLBACK_DONE.exists()
    mraw = load_meta_all(fill=False)   # stage 1 does not depend on the (slow, rate-limited) iTunes preview lookups
    for c, f in make_folds(cutoffs, d):
        end = c + pd.DateOffset(months=3)
        seeds, rel = fold_seed_artists(d, c); S = set(seeds) | set(rel)
        seen = set(d.loc[d.t < c, "artist"])
        elig = u[(u.release < end) & u.src.map(lambda s: not s.isdisjoint(S))].copy(); elig["new_artist"] = ~elig.artist.isin(seen)
        if active: elig = elig[elig.previewUrl.notna() | elig.trackId.isin(resolved)]   # iTunes lookups are rate limited: a decoy without preview is eligible only if it was looked up
        elig["rb"] = release_bucket(elig.release, c); f = f.assign(rb=release_bucket(tried_release(f), c))
        pre = _draw(f, elig, mraw, PRESAMPLE * len(f), int(c.strftime("%Y%m%d")))
        yield c, f, pre

def decoy_presample(cutoffs):
    """Raw trackIds of the stage-1 decoy pre-sample (for the iTunes lookups). Internal build-time helper."""
    return {str(c.date()): list(pre.trackId) for c, f, pre in _open_parts(cutoffs, _load_all())}

POOL_COLS = ["song", "trackId", "albumId", "artistIds", "artist", "trackName", "first", "cutoff", "new_artist", "is_decoy", "love", "strong", "plays90", "days90",
             "love_4_2", "love_10_4", "share90", "sess", "week", "nnew_sess", "exp_before", "exp_after", "replays_s1", "day1", "d7", "rb"]

def make_open_folds(cutoffs, all_streams=None):
    """Yield (cutoff, pool). pool = the tried songs of make_folds (is_decoy=0) plus DECOY_RATIO x as many decoys (is_decoy=1): real songs by the fold's
    seed artists (see fold_seed_artists) that the user NEVER played (checked against the whole history incl. sealed era) and that were already released
    by the end of the fold window. Decoys get love=0 and are labelled 'not tried' (not 'would hate'). Two-stage covariate-matched draw (see _draw);
    sampling is seeded by the cutoff and independent of any label. Pool also carries HARNESS-ONLY diagnostics columns (sess, week, nnew_sess, exp_before, exp_after, replays_s1, day1, d7)
    that public_view never exposes."""
    d = _load_all() if all_streams is None else all_streams
    mm = load_meta_all()
    for c, f, pre in _open_parts(cutoffs, d):
        dec = _draw(f, pre, mm, DECOY_RATIO * len(f), int(c.strftime("%Y%m%d")) + 1)
        dec = dec.assign(first=pd.NaT, love=0, strong=0, plays90=0, days90=0, love_4_2=0, love_10_4=0, share90=np.nan, sess=np.nan, week=np.nan,
                         nnew_sess=np.nan, exp_before=np.nan, exp_after=np.nan, replays_s1=0, day1=0, d7=0, cutoff=c, is_decoy=1)
        tried = f.assign(is_decoy=0)
        yield c, pd.concat([tried[POOL_COLS], dec[POOL_COLS]], ignore_index=True)

_FBC = []
def fallback_table():
    """iTunes fallback lookup results (empty frame if the cache has not been built)."""
    if not _FBC: _FBC.append(pd.read_csv(FALLBACK) if FALLBACK.exists() else pd.DataFrame(columns=["trackId", "status", "previewUrl"]))
    return _FBC[0]

def load_meta_all(fill=True) -> pd.DataFrame:
    """Meta for every track the harness can show (user's tracks + decoys), indexed by RAW trackId (internal). With fill=True, tracks (user's and decoys alike)
    that have no previewUrl get the iTunes-Search fallback preview (accepted only for matching normalised title + primary artist and |duration diff| <= 5 s)."""
    m = load_meta(); u = _decoys().drop_duplicates("trackId").set_index("trackId")
    u = u.assign(name=u.trackName)[["name", "durationMs", "explicit", "popularity", "spotifyId", "previewUrl", "albumName", "artistNames"]]
    out = pd.concat([m, u[~u.index.isin(m.index)]])
    if fill and FALLBACK_DONE.exists():
        fb = fallback_table(); fb = fb[fb.status == "match"].drop_duplicates("trackId").set_index("trackId").previewUrl
        need = out.previewUrl.isna() & out.index.isin(fb.index)
        out.loc[need, "previewUrl"] = fb.reindex(out.index[need]).values
    return out

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
