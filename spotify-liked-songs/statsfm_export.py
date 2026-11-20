#!/usr/bin/env python3
"""Export full stats.fm listening history into a per-song CSV (listening_stats.csv)."""
import argparse, csv, json, statistics, sys, time
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

BASE = "https://api.stats.fm/api/v1/users/gtwz5m9b4rqppdd60zmin4j8h"
HERE = Path(__file__).resolve().parent
CACHE = HERE / ".cache"
STREAMS_F = CACHE / "streams.jsonl"
TOP_F = CACHE / "top_tracks.json"
CSV_F = HERE / "listening_stats.csv"
TZ = ZoneInfo("Europe/London")
WINDOW_DAYS = 730
CUTOFF = datetime.now(timezone.utc) - timedelta(days=WINDOW_DAYS)
PL_F = CACHE / "playlist_names.json"
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
anomalies = []


def get(session, url, params):
    delay = 2
    for attempt in range(8):
        try:
            r = session.get(url, params=params, timeout=60)
        except requests.RequestException as e:
            print(f"  request error {e}; retry", file=sys.stderr)
            time.sleep(delay); delay = min(delay * 2, 60); continue
        if r.status_code == 429 or r.status_code >= 500:
            wait = float(r.headers.get("Retry-After", delay)) if str(r.headers.get("Retry-After", "")).replace(".", "").isdigit() else delay
            print(f"  HTTP {r.status_code}; sleeping {wait}s", file=sys.stderr)
            time.sleep(wait); delay = min(delay * 2, 60); continue
        r.raise_for_status()
        time.sleep(0.2)
        return r.json()
    raise RuntimeError(f"giving up on {url} {params}")


def parse_ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def fetch_top(session):
    items, off = [], 0
    while True:
        d = get(session, f"{BASE}/top/tracks", {"range": "lifetime", "limit": 500, "offset": off})
        page = d.get("items", [])
        if not page:
            break
        items += page
        off += 500
        print(f"top tracks: {len(items)}")
    return items


def stream_key(s):
    return s.get("id") or (s["endTime"], s.get("trackId"), s.get("playedMs"))


def fetch_streams(session):
    seen, out = set(), []
    before = int(time.time() * 1000) + 60_000
    pages = 0
    while True:
        d = get(session, f"{BASE}/streams", {"limit": 1000, "before": before})
        page = d.get("items", [])
        if not page:
            break
        pages += 1
        new = 0
        for s in page:
            k = stream_key(s)
            if k not in seen:
                seen.add(k); out.append(s); new += 1
        oldest = min(int(parse_ts(s["endTime"]).timestamp() * 1000) for s in page)
        nb = oldest + 1  # inclusive overlap so ties across the page boundary aren't lost
        if new == 0 or nb >= before:
            nb = before - 1 if nb >= before else nb
            if new == 0:
                nb = min(nb, oldest)
                if nb >= before:
                    nb = before - 1
        if new == 0:
            anomalies.append(f"page {pages}: no new streams at before={before}; stepped back")
        before = nb
        if oldest < CUTOFF.timestamp() * 1000:
            break
        print(f"streams page {pages}: +{new} (total {len(out)}), oldest {page[-1]['endTime']}")
    return out


def load(refresh):
    CACHE.mkdir(exist_ok=True)
    session = requests.Session()
    session.headers["User-Agent"] = "statsfm-export/1.0"
    if refresh or not TOP_F.exists():
        TOP_F.write_text(json.dumps(fetch_top(session)))
    if refresh or not STREAMS_F.exists():
        streams = fetch_streams(session)
        with STREAMS_F.open("w") as f:
            for s in streams:
                f.write(json.dumps(s) + "\n")
    top = json.loads(TOP_F.read_text())
    streams = [json.loads(l) for l in STREAMS_F.read_text().splitlines() if l.strip()]
    streams = [x for x in streams if parse_ts(x["endTime"]) >= CUTOFF]
    return top, streams


def fmt_dur(ms):
    s = round(ms / 1000)
    return f"{s // 60}:{s % 60:02d}"


def mode(counter, fmt):
    if not counter:
        return ""
    best = max(counter.values())
    return fmt(min(k for k, v in counter.items() if v == best))


def ctx_of(s):
    c = (s.get("contextId") or "").split("?")[0]
    if c.startswith("spotify:playlist:"):
        return "playlist", c.split(":")[-1]
    if c.startswith("spotify:album:"):
        return "album", c.split(":")[-1]
    return "other", ""


def resolve_playlists(ids):
    try:
        names = json.loads(PL_F.read_text())
    except Exception:
        names = {}
    session = requests.Session()
    for i in sorted(ids):
        if i in names:
            continue
        try:
            r = session.get("https://open.spotify.com/oembed", params={"url": f"https://open.spotify.com/playlist/{i}"}, timeout=30)
            names[i] = r.json()["title"] if r.status_code == 200 else i
            if r.status_code != 200:
                anomalies.append(f"oembed {r.status_code} for playlist {i}")
        except Exception as e:
            names[i] = i
            anomalies.append(f"oembed failed for playlist {i}: {e}")
        time.sleep(0.2)
    PL_F.write_text(json.dumps(names, ensure_ascii=False))
    return names


def build(top, streams, plnames):
    meta = {it["track"]["id"]: it["track"] for it in top}
    by_track = defaultdict(list)
    names = {}
    for s in streams:
        kind, cid = ctx_of(s)
        by_track[s["trackId"]].append((parse_ts(s["endTime"]).astimezone(TZ), s.get("playedMs") or 0, cid if kind == "playlist" else ""))
        names.setdefault(s["trackId"], s.get("trackName", ""))
    rows = []
    for tid, plays in by_track.items():
        t = meta.get(tid) or {}
        dts = [p[0] for p in plays]
        spot = (t.get("externalIds") or {}).get("spotify") or []
        plc = Counter(p[2] for p in plays if p[2])
        top_pl = min(plc.items(), key=lambda kv: (-kv[1], kv[0]))[0] if plc else ""
        rows.append({
            "track": t.get("name") or names.get(tid, ""),
            "artists": ", ".join(a["name"] for a in t.get("artists", [])),
            "album": (t.get("albums") or [{}])[0].get("name", ""),
            "play_count": len(plays),
            "minutes_listened": round(sum(p[1] for p in plays) / 60000, 1),
            "first_played": min(dts).strftime("%Y-%m-%d %H:%M"),
            "last_played": max(dts).strftime("%Y-%m-%d %H:%M"),
            "favourite_hour": mode(Counter(d.hour for d in dts), lambda h: f"{h:02d}:00"),
            "favourite_weekday": mode(Counter(d.weekday() for d in dts), lambda w: WEEKDAYS[w]),
            "top_playlist": plnames.get(top_pl, top_pl),
            "spotify_url": f"https://open.spotify.com/track/{spot[0]}" if spot else "",
        })
    rows.sort(key=lambda r: (-r["play_count"], r["track"]))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true", help="re-download from API")
    args = ap.parse_args()
    top, streams = load(args.refresh)
    pl_ids = {ctx_of(s)[1] for s in streams if ctx_of(s)[0] == "playlist"}
    plnames = resolve_playlists(pl_ids)
    rows = build(top, streams, plnames)
    with CSV_F.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    print(f"window since {CUTOFF:%Y-%m-%d}; tracks: {len(rows)}; total plays: {sum(r['play_count'] for r in rows)}")
    for r in rows[:5]:
        print(f"  {r['track']} - {r['artists']}: {r['play_count']}")
    print(f"tracks without spotify url: {sum(1 for r in rows if not r['spotify_url'])}; without metadata: {sum(1 for r in rows if not r['artists'])}")
    print(f"playlists: {len(pl_ids)}, unresolved names: {sum(1 for i in pl_ids if plnames.get(i, i) == i)}")
    for a in anomalies:
        print("anomaly:", a)
    print(f"wrote {CSV_F} ({CSV_F.stat().st_size} B)")


if __name__ == "__main__":
    main()
