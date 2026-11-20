#!/usr/bin/env python3
"""Export your Spotify liked songs to CSV, with listening info.

Usage:
  python3 spotify_export.py auth-url <CLIENT_ID>   # step 1: prints a login link
  python3 spotify_export.py auth-code <URL|CODE>   # step 2: paste the page you were sent to
  python3 spotify_export.py export                 # step 3: writes liked_songs.csv

Optional: put the JSON files from Spotify's "Extended streaming history"
download into ./streaming_history/ and re-run `export` to add real play counts.

Auth uses PKCE, so no client secret is needed. Tokens live in ./.auth/ (git-ignored).
Times are UTC unless you pass --tz, e.g. `export --tz Europe/London`.
"""
import base64
import collections
import csv
import glob
import hashlib
import json
import os
import secrets
import sys
import time
import urllib.parse
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
AUTH_DIR = os.path.join(HERE, ".auth")
STATE_FILE = os.path.join(AUTH_DIR, "pkce.json")
TOKEN_FILE = os.path.join(AUTH_DIR, "token.json")
HISTORY_DIR = os.path.join(HERE, "streaming_history")
OUT_CSV = os.path.join(HERE, "liked_songs.csv")

REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPES = "user-library-read user-top-read user-read-recently-played"
API = "https://api.spotify.com/v1"
TOKEN_URL = "https://accounts.spotify.com/api/token"


# ---------------------------------------------------------------- auth
def _save(path, data):
    os.makedirs(AUTH_DIR, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f)
    os.chmod(path, 0o600)


def _load(path):
    with open(path) as f:
        return json.load(f)


def auth_url(client_id):
    verifier = secrets.token_urlsafe(64)[:128]
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    state = secrets.token_urlsafe(16)
    _save(STATE_FILE, {"client_id": client_id, "verifier": verifier, "state": state})
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "code_challenge_method": "S256",
        "code_challenge": challenge,
        "scope": SCOPES,
        "state": state,
    }
    print("https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(params))


def auth_code(arg):
    st = _load(STATE_FILE)
    code = arg
    if arg.startswith("http"):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(arg).query)
        if "error" in q:
            sys.exit(f"Spotify returned an error: {q['error'][0]}")
        if q.get("state", [None])[0] != st["state"]:
            sys.exit("State mismatch - run auth-url again and use the newest link.")
        code = q["code"][0]
    r = requests.post(TOKEN_URL, data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": st["client_id"],
        "code_verifier": st["verifier"],
    }, timeout=30)
    if r.status_code != 200:
        sys.exit(f"Token exchange failed ({r.status_code}): {r.text}")
    tok = r.json()
    tok["client_id"] = st["client_id"]
    tok["expires_at"] = time.time() + tok["expires_in"] - 60
    _save(TOKEN_FILE, tok)
    os.remove(STATE_FILE)
    print("Signed in. Now run: python3 spotify_export.py export")


def access_token():
    tok = _load(TOKEN_FILE)
    if time.time() < tok["expires_at"]:
        return tok["access_token"]
    r = requests.post(TOKEN_URL, data={
        "grant_type": "refresh_token",
        "refresh_token": tok["refresh_token"],
        "client_id": tok["client_id"],
    }, timeout=30)
    if r.status_code != 200:
        sys.exit(f"Token refresh failed ({r.status_code}): {r.text}\nRun auth-url again.")
    new = r.json()
    tok["access_token"] = new["access_token"]
    tok["refresh_token"] = new.get("refresh_token", tok["refresh_token"])
    tok["expires_at"] = time.time() + new["expires_in"] - 60
    _save(TOKEN_FILE, tok)
    return tok["access_token"]


# ---------------------------------------------------------------- API
def get(path, params=None, quiet=False):
    url = path if path.startswith("http") else API + path
    for _ in range(6):
        r = requests.get(url, params=params, timeout=30,
                         headers={"Authorization": f"Bearer {access_token()}"})
        if r.status_code == 429:
            time.sleep(int(r.headers.get("Retry-After", "2")) + 1)
            continue
        if r.status_code >= 500:
            time.sleep(2)
            continue
        if r.status_code != 200:
            if not quiet:
                print(f"  ! {path} -> {r.status_code}: {r.text[:200]}", file=sys.stderr)
            return None
        return r.json()
    return None


def paged(path, limit=50):
    data = get(path, {"limit": limit})
    while data:
        yield from data.get("items", [])
        data = get(data["next"]) if data.get("next") else None


# ---------------------------------------------------------------- helpers
def to_local(iso, tz):
    if not iso:
        return ""
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return dt.astimezone(tz).strftime("%Y-%m-%d %H:%M")


def mmss(ms):
    if not ms:
        return ""
    s = round(ms / 1000)
    return f"{s // 60}:{s % 60:02d}"


def load_history(tz):
    """Aggregate Extended Streaming History files by track id."""
    files = sorted(glob.glob(os.path.join(HISTORY_DIR, "**", "*.json"), recursive=True))
    if not files:
        return None
    stats = collections.defaultdict(lambda: {
        "plays": 0, "skips": 0, "ms": 0, "first": None, "last": None,
        "hours": collections.Counter(), "days": collections.Counter()})
    for fp in files:
        try:
            with open(fp, encoding="utf-8") as f:
                rows = json.load(f)
        except Exception:
            continue
        if not isinstance(rows, list):
            continue
        for e in rows:
            uri = e.get("spotify_track_uri") or ""
            if not uri.startswith("spotify:track:") or "ts" not in e:
                continue
            tid = uri.split(":")[-1]
            ms = e.get("ms_played") or 0
            dt = datetime.fromisoformat(e["ts"].replace("Z", "+00:00")).astimezone(tz)
            s = stats[tid]
            s["ms"] += ms
            if ms >= 30000:  # Spotify's own threshold for counting a stream
                s["plays"] += 1
                s["hours"][dt.hour] += 1
                s["days"][dt.strftime("%A")] += 1
                s["first"] = dt if s["first"] is None or dt < s["first"] else s["first"]
                s["last"] = dt if s["last"] is None or dt > s["last"] else s["last"]
            if e.get("skipped"):
                s["skips"] += 1
    print(f"  Read streaming history from {len(files)} file(s), {len(stats)} tracks.")
    return stats


# ---------------------------------------------------------------- export
def export(tz):
    print("Fetching liked songs...")
    liked = list(paged("/me/tracks"))
    print(f"  {len(liked)} liked songs")

    print("Fetching top tracks...")
    ranks = {}
    for term, label in [("short_term", "4w"), ("medium_term", "6m"), ("long_term", "1y")]:
        r = {}
        for offset in (0, 49):
            d = get("/me/top/tracks", {"time_range": term, "limit": 50, "offset": offset})
            for i, t in enumerate((d or {}).get("items", [])):
                r.setdefault(t["id"], offset + i + 1)
        ranks[label] = r

    print("Fetching recently played (Spotify only keeps the last 50)...")
    recent_count, recent_last = collections.Counter(), {}
    for it in (get("/me/player/recently-played", {"limit": 50}) or {}).get("items", []):
        tid = (it.get("track") or {}).get("id")
        if tid:
            recent_count[tid] += 1
            recent_last[tid] = max(recent_last.get(tid, ""), it["played_at"])

    print("Fetching artist genres...")
    artist_ids = sorted({a["id"] for it in liked for a in (it["track"] or {}).get("artists", []) if a.get("id")})
    genres = {}
    for i in range(0, len(artist_ids), 50):
        d = get("/artists", {"ids": ",".join(artist_ids[i:i + 50])}, quiet=True)
        if d is None:
            print("  (artist details not available for this app - skipping genres)")
            break
        for a in d.get("artists", []):
            if a:
                genres[a["id"]] = a.get("genres", [])

    hist = load_history(tz)

    cols = ["liked_at", "track", "artists", "album", "album_release_date", "duration",
            "explicit", "popularity", "genres",
            "top_rank_last_4_weeks", "top_rank_last_6_months", "top_rank_last_year",
            "plays_in_last_50", "last_played_recent"]
    if hist is not None:
        cols += ["play_count", "skips", "minutes_listened", "first_played", "last_played",
                 "favourite_hour", "favourite_weekday"]
    cols += ["spotify_url", "track_id"]

    rows = []
    for it in liked:
        t = it.get("track") or {}
        tid = t.get("id")
        if not tid:
            continue
        g = []
        for a in t.get("artists", []):
            for x in genres.get(a.get("id"), []):
                if x not in g:
                    g.append(x)
        row = {
            "liked_at": to_local(it.get("added_at"), tz),
            "track": t.get("name", ""),
            "artists": ", ".join(a.get("name", "") for a in t.get("artists", [])),
            "album": (t.get("album") or {}).get("name", ""),
            "album_release_date": (t.get("album") or {}).get("release_date", ""),
            "duration": mmss(t.get("duration_ms")),
            "explicit": "yes" if t.get("explicit") else "no",
            "popularity": t.get("popularity", ""),
            "genres": ", ".join(g),
            "top_rank_last_4_weeks": ranks["4w"].get(tid, ""),
            "top_rank_last_6_months": ranks["6m"].get(tid, ""),
            "top_rank_last_year": ranks["1y"].get(tid, ""),
            "plays_in_last_50": recent_count.get(tid, "") or "",
            "last_played_recent": to_local(recent_last.get(tid), tz),
            "spotify_url": (t.get("external_urls") or {}).get("spotify", ""),
            "track_id": tid,
        }
        if hist is not None:
            s = hist.get(tid)
            if s:
                row.update({
                    "play_count": s["plays"],
                    "skips": s["skips"],
                    "minutes_listened": round(s["ms"] / 60000, 1),
                    "first_played": s["first"].strftime("%Y-%m-%d %H:%M") if s["first"] else "",
                    "last_played": s["last"].strftime("%Y-%m-%d %H:%M") if s["last"] else "",
                    "favourite_hour": f"{s['hours'].most_common(1)[0][0]:02d}:00" if s["hours"] else "",
                    "favourite_weekday": s["days"].most_common(1)[0][0] if s["days"] else "",
                })
            else:
                row.update({"play_count": 0, "skips": 0, "minutes_listened": 0})
        rows.append(row)

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {len(rows)} songs to {OUT_CSV}")


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    if a[0] == "auth-url" and len(a) == 2:
        auth_url(a[1].strip())
    elif a[0] == "auth-code" and len(a) == 2:
        auth_code(a[1].strip())
    elif a[0] == "export":
        tz = ZoneInfo(a[a.index("--tz") + 1]) if "--tz" in a else timezone.utc
        export(tz)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
