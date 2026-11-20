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
BY_ID_F = CACHE / "by_spotify_id.json"
TZ = ZoneInfo("Europe/London")
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
    return top, streams


def fmt_dur(ms):
    s = round(ms / 1000)
    return f"{s // 60}:{s % 60:02d}"


def mode(counter, fmt):
    if not counter:
        return ""
    best = max(counter.values())
    return fmt(min(k for k, v in counter.items() if v == best))


def build(top, streams):
    now = datetime.now(TZ)
    d30, d365 = now - timedelta(days=30), now - timedelta(days=365)
    meta = {}
    for it in top:
        t = it["track"]
        meta[t["id"]] = (it, t)
    by_track = defaultdict(list)
    names = {}
    for s in streams:
        by_track[s["trackId"]].append((parse_ts(s["endTime"]).astimezone(TZ), s.get("playedMs") or 0))
        names.setdefault(s["trackId"], s.get("trackName", ""))
    years = sorted({dt.year for v in by_track.values() for dt, _ in v})
    rows = []
    for tid in set(by_track) | set(meta):
        it, t = meta.get(tid, (None, None))
        plays = by_track.get(tid, [])
        dur = (t or {}).get("durationMs") or 0
        spot = ((t or {}).get("externalIds") or {}).get("spotify") or []
        row = {
            "track": t["name"] if t else names.get(tid, ""),
            "artists": ", ".join(a["name"] for a in (t or {}).get("artists", [])),
            "album": ((t or {}).get("albums") or [{}])[0].get("name", ""),
            "duration": fmt_dur(dur) if dur else "",
            "explicit": ("yes" if t.get("explicit") else "no") if t else "",
            "spotify_popularity": (t or {}).get("spotifyPopularity", "") if t else "",
            "play_count": len(plays),
            "lifetime_rank": it["position"] if it else "",
        }
        if plays:
            tot = sum(p for _, p in plays)
            row["minutes_listened"] = round(tot / 60000, 1)
            row["avg_listen_pct"] = round(tot / len(plays) / dur * 100) if dur else ""
            dts = [d for d, _ in plays]
            row["first_played"] = min(dts).strftime("%Y-%m-%d %H:%M")
            row["last_played"] = max(dts).strftime("%Y-%m-%d %H:%M")
            row["plays_last_30_days"] = sum(d >= d30 for d in dts)
            row["plays_last_12_months"] = sum(d >= d365 for d in dts)
            yc = Counter(d.year for d in dts)
            for y in years:
                row[f"plays_{y}"] = yc.get(y, 0)
            row["favourite_hour"] = mode(Counter(d.hour for d in dts), lambda h: f"{h:02d}:00")
            row["favourite_weekday"] = mode(Counter(d.weekday() for d in dts), lambda w: WEEKDAYS[w])
            tod = Counter()
            for d in dts:
                h = d.hour
                tod["M" if 5 <= h < 12 else "A" if 12 <= h < 17 else "E" if 17 <= h < 22 else "N"] += 1
            row["time_of_day_mix"] = " ".join(f"{k}{round(tod[k] / len(dts) * 100)}%" for k in "MAEN")
            mc = Counter(d.strftime("%Y-%m") for d in dts)
            pm = max(mc.values())
            row["peak_month"] = min(k for k, v in mc.items() if v == pm)
            row["peak_month_plays"] = pm
        else:
            for k in ["minutes_listened", "avg_listen_pct", "first_played", "last_played", "plays_last_30_days",
                      "plays_last_12_months", *[f"plays_{y}" for y in years], "favourite_hour",
                      "favourite_weekday", "time_of_day_mix", "peak_month", "peak_month_plays"]:
                row[k] = ""
        row["spotify_url"] = f"https://open.spotify.com/track/{spot[0]}" if spot else ""
        row["spotify_track_id"] = spot[0] if spot else ""
        row["statsfm_track_id"] = tid
        rows.append(row)
    rows.sort(key=lambda r: (-r["play_count"], r["lifetime_rank"] if r["lifetime_rank"] != "" else 10**9))
    return rows, years


def build_stats_rows(refresh=False):
    """Reusable: returns dict spotify_track_id -> row dict (also written to .cache/by_spotify_id.json)."""
    top, streams = load(refresh)
    rows, _ = build(top, streams)
    return {r["spotify_track_id"]: r for r in rows if r["spotify_track_id"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true", help="re-download from API")
    args = ap.parse_args()
    top, streams = load(args.refresh)
    rows, years = build(top, streams)
    cols = ["track", "artists", "album", "duration", "explicit", "spotify_popularity", "play_count",
            "lifetime_rank", "minutes_listened", "avg_listen_pct", "first_played", "last_played",
            "plays_last_30_days", "plays_last_12_months", *[f"plays_{y}" for y in years],
            "favourite_hour", "favourite_weekday", "time_of_day_mix", "peak_month", "peak_month_plays",
            "spotify_url", "spotify_track_id", "statsfm_track_id"]
    with CSV_F.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader(); w.writerows(rows)
    BY_ID_F.write_text(json.dumps({r["spotify_track_id"]: r for r in rows if r["spotify_track_id"]}, ensure_ascii=False))

    total = sum(r["play_count"] for r in rows)
    print(f"\nrows: {len(rows)}  total plays: {total} (expected ~147256)  raw streams: {len(streams)}")
    print(f"top track: {rows[0]['track']} by {rows[0]['artists']} - {rows[0]['play_count']} (expected Synthesis Moment / Laplage ~1258)")
    nospot = [r for r in rows if not r["spotify_track_id"]]
    noplay = [r for r in rows if r["play_count"] == 0]
    print(f"tracks without spotify id: {len(nospot)}; tracks with 0 streams (top-only): {len(noplay)}")
    ids = {s["trackId"] for s in streams}
    print(f"stream-only tracks (no metadata): {sum(1 for r in rows if not r['artists'])}")
    print("lifetime streams per top list vs dump:", sum(i['streams'] for i in top), "vs", len(streams))
    for a in anomalies:
        print("anomaly:", a)
    print(f"wrote {CSV_F} ({CSV_F.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
