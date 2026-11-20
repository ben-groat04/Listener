"""Data loading, song identity, fold construction and labels. All time logic lives here."""
import re, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[1]
STREAMS = ROOT.parent / "spotify-liked-songs/.cache/streams.jsonl"
TOP_TRACKS = ROOT.parent / "spotify-liked-songs/.cache/top_tracks.json"
SEALED_DIR = ROOT / ".sealed"

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
    return re.sub(r"\W+", " ", n).strip()


def _load_all() -> pd.DataFrame:
    d = pd.read_json(STREAMS, lines=True)
    d["t"] = pd.to_datetime(d.endTime).dt.tz_localize(None)
    d["artist"] = d.artistIds.map(lambda a: a[0] if len(a) else -1)
    d["song"] = d.trackName.map(song_key) + "|" + d.artist.astype(str)
    cols = ["t", "trackId", "albumId", "artistIds", "artist", "trackName", "song", "playedMs", "contextId"]
    return d[cols].sort_values("t", kind="stable").reset_index(drop=True)


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
        rows.append(dict(trackId=t["id"], durationMs=t.get("durationMs"), explicit=t.get("explicit"),
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
    rep = d.sort_values("t").drop_duplicates("song")[["song", "t", "trackId", "albumId", "artistIds", "artist", "trackName"]]
    s = rep.rename(columns={"t": "first"}).set_index("song").join(st)
    s["love"] = ((s.plays90 >= LOVE_PLAYS) & (s.days90 >= LOVE_DAYS)).astype(int)
    s["strong"] = ((s.plays90 >= STRONG_PLAYS) & (s.days90 >= STRONG_DAYS)).astype(int)
    return s


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
        yield c, f.reset_index()


def public_candidates(fold: pd.DataFrame) -> pd.DataFrame:
    """What a predictor is allowed to see about the pool (no labels, no first-listen time)."""
    return fold[["song", "trackId", "albumId", "artistIds", "artist", "trackName"]].copy()
