"""Catalogue clients (public catalogue info only; no user listening data). Stdlib only.
    from catalogue import catalogue as C      (run with cwd=/home/user/Listener/taste-model, python3 -I needs sys.path insert)
Every call is throttled per host (MIN_GAP seconds), retried on 429/5xx/403 with back-off, returns parsed JSON or None.
Hosts (all verified reachable 2026-11-22): api.deezer.com, itunes.apple.com, open.spotify.com (embed), p.scdn.co,
musicbrainz.org, api.listenbrainz.org, labs.api.listenbrainz.org, acousticbrainz.org, lrclib.net, api.discogs.com.
"""
import json, time, re, threading, urllib.request, urllib.parse, urllib.error, unicodedata
UA = "taste-research-catalogue/0.1 (research groundwork)"
MIN_GAP = {"api.deezer.com": 0.25, "itunes.apple.com": 3.5, "open.spotify.com": 1.0, "musicbrainz.org": 1.1,
           "api.listenbrainz.org": 0.5, "labs.api.listenbrainz.org": 0.5, "acousticbrainz.org": 0.5, "lrclib.net": 0.5, "api.discogs.com": 2.5}
_last, _lock = {}, threading.Lock()

def _throttle(host):
    with _lock:
        w = _last.get(host, 0) + MIN_GAP.get(host, 1.0) - time.time()
        if w > 0: time.sleep(w)
        _last[host] = time.time()

def http(url, raw=False, tries=4, timeout=30):
    host = urllib.parse.urlparse(url).netloc
    for k in range(tries):
        _throttle(host)
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=timeout) as r:
                b = r.read()
            return b if raw else json.loads(b)
        except urllib.error.HTTPError as e:
            if e.code == 404: return None
            time.sleep(4 * (k + 1) * (3 if e.code in (403, 429) else 1))
        except Exception:
            time.sleep(2 * (k + 1))
    return None

def q(**kw): return urllib.parse.urlencode(kw)

# ---- Deezer (no key; ~50 req/5 s documented; 30 rapid calls ok) ----
def dz_search(artist, title, limit=5):
    r = http("https://api.deezer.com/search?" + q(q=f'artist:"{artist}" track:"{title}"', limit=limit))
    if r and r.get("data"): return r["data"]
    r = http("https://api.deezer.com/search?" + q(q=f"{artist} {title}", limit=limit))   # loose fallback
    return (r or {}).get("data", [])
def dz_track(i): return http(f"https://api.deezer.com/track/{i}")            # adds release_date, bpm(mostly 0), gain, contributors
def dz_isrc(isrc): return http(f"https://api.deezer.com/track/isrc:{isrc}")
def dz_artist_top(i, limit=50): return (http(f"https://api.deezer.com/artist/{i}/top?limit={limit}") or {}).get("data", [])
def dz_artist_related(i): return (http(f"https://api.deezer.com/artist/{i}/related?limit=50") or {}).get("data", [])
def dz_artist_albums(i, limit=100): return (http(f"https://api.deezer.com/artist/{i}/albums?limit={limit}") or {}).get("data", [])
def dz_album_tracks(i): return (http(f"https://api.deezer.com/album/{i}/tracks?limit=200") or {}).get("data", [])
def dz_album(i): return http(f"https://api.deezer.com/album/{i}")            # genres, label, release_date
def dz_genres(): return (http("https://api.deezer.com/genre") or {}).get("data", [])
def dz_genre_artists(g): return (http(f"https://api.deezer.com/genre/{g}/artists") or {}).get("data", [])
def dz_chart(genre=0, what="tracks", limit=100): return (http(f"https://api.deezer.com/chart/{genre}/{what}?limit={limit}") or {}).get("data", [])
def dz_playlist_tracks(i): return (http(f"https://api.deezer.com/playlist/{i}/tracks?limit=500") or {}).get("data", [])

# ---- iTunes (no key; 403 after ~20 req/min; previews 30 s AAC; lookup by id is not rate-limited the same way in practice) ----
def it_search(term, entity="song", limit=10, country="us"):
    r = http("https://itunes.apple.com/search?" + q(term=term, entity=entity, limit=limit, country=country)); return (r or {}).get("results", [])
def it_lookup(**kw):
    r = http("https://itunes.apple.com/lookup?" + q(**kw)); return (r or {}).get("results", [])   # id=, upc=, isbn=, amgArtistId=, entity=song&limit=
def it_topsongs(country="us", limit=100, genre=None):
    g = f"/genre={genre}" if genre else ""
    r = http(f"https://itunes.apple.com/{country}/rss/topsongs/limit={limit}{g}/json"); return ((r or {}).get("feed") or {}).get("entry", [])

# ---- Spotify: only the public embed page (no token). Gives name, artists, preview URL for ANY spotify track id ----
def sp_embed(track_id):
    h = http(f"https://open.spotify.com/embed/track/{track_id}", raw=True)
    if not h: return None
    m = re.search(rb'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', h, re.S)
    if not m: return None
    try: e = json.loads(m.group(1))["props"]["pageProps"]["state"]["data"]["entity"]
    except Exception: return None
    ap = e.get("audioPreview") or {}
    return dict(id=track_id, name=e.get("name") or e.get("title"), artists=[a.get("name") for a in e.get("artists", [])], duration_ms=e.get("duration"),
                is_explicit=e.get("isExplicit"), release_date=(e.get("releaseDate") or {}).get("isoString"), preview_url=ap.get("url"))
def sp_oembed(track_id): return http("https://open.spotify.com/oembed?url=" + urllib.parse.quote(f"https://open.spotify.com/track/{track_id}"))

# ---- MusicBrainz (no key; 1 req/s; 503 when busy -> retried) ----
def mb_recording_search(artist, title, limit=5):
    r = http("https://musicbrainz.org/ws/2/recording/?" + q(query=f'recording:"{title}" AND artist:"{artist}"', fmt="json", limit=limit)); return (r or {}).get("recordings", [])
def mb_isrc(isrc): return (http(f"https://musicbrainz.org/ws/2/isrc/{isrc}?fmt=json&inc=artist-credits") or {}).get("recordings", [])
def mb_recording(mbid): return http(f"https://musicbrainz.org/ws/2/recording/{mbid}?fmt=json&inc=artist-credits+isrcs+tags+genres+releases")
def mb_artist(mbid): return http(f"https://musicbrainz.org/ws/2/artist/{mbid}?fmt=json&inc=tags+genres")

# ---- ListenBrainz (public, sitewide / per-artist popularity & similarity only; never user-specific endpoints) ----
def lb_top_recordings_for_artist(artist_mbid): return http(f"https://api.listenbrainz.org/1/popularity/top-recordings-for-artist/{artist_mbid}")
def lb_recording_popularity(mbids): return http("https://api.listenbrainz.org/1/popularity/recording?" + q(recording_mbid=",".join(mbids))) if False else None  # POST-only; not used
def lb_similar_artists(artist_mbid, algo="session_based_days_9000_session_300_contribution_5_threshold_15_limit_50_skip_30"):
    return http("https://labs.api.listenbrainz.org/similar-artists/json?" + q(artist_mbids=artist_mbid, algorithm=algo))
def lb_sitewide_artists(count=100, rng="all_time"): return ((http(f"https://api.listenbrainz.org/1/stats/sitewide/artists?count={count}&range={rng}") or {}).get("payload") or {}).get("artists", [])

# ---- AcousticBrainz (frozen 2022 dump of essentia low/high-level features, keyed by MusicBrainz recording MBID) ----
def ab_low(mbid): return http(f"https://acousticbrainz.org/api/v1/{mbid}/low-level")
def ab_high(mbid): return http(f"https://acousticbrainz.org/api/v1/{mbid}/high-level")

# ---- LRCLIB lyrics (plain + synced) ----
def lrc_get(artist, title, album=None, dur=None):
    kw = dict(artist_name=artist, track_name=title); 
    if album: kw["album_name"] = album
    if dur: kw["duration"] = int(dur)
    return http("https://lrclib.net/api/get?" + q(**kw))
def lrc_search(artist, title): return http("https://lrclib.net/api/search?" + q(track_name=title, artist_name=artist)) or []

# ---- Discogs (unauthenticated search worked; 25 req/min unauth) ----
def dc_search(**kw): return http("https://api.discogs.com/database/search?" + q(**kw))
def dc_artist(i): return http(f"https://api.discogs.com/artists/{i}")

def download(url, path):
    b = http(url, raw=True, timeout=60)
    if b and len(b) > 1000: open(path, "wb").write(b); return len(b)
    return 0

def norm(x):
    x = unicodedata.normalize("NFKD", str(x)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", x).strip()
