"""Download freely licensed test videos from Wikimedia Commons and re-encode to small 480p mp4 in testvideos/.
Usage: fetch_commons.py selection.json   (list of {title,url,license,...}); writes testvideos/<slug>.mp4 + testvideos/SOURCES.md"""
import json, os, re, subprocess, sys, urllib.request
root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")); out = os.path.join(root, "testvideos"); os.makedirs(out, exist_ok=True)
sel = json.load(open(sys.argv[1])); tmp = os.path.join(out, ".tmp"); os.makedirs(tmp, exist_ok=True)
src = open(os.path.join(out, "SOURCES.md"), "a")
for s in sel:
    slug = re.sub(r"[^a-z0-9]+", "_", s["title"].replace("File:", "").rsplit(".", 1)[0].lower()).strip("_")[:40]
    dst = os.path.join(out, slug + ".mp4")
    if os.path.exists(dst): continue
    raw = os.path.join(tmp, slug + "." + s["url"].rsplit(".", 1)[1])
    req = urllib.request.Request(s["url"], headers={"User-Agent": "video-analysis-research/0.1"})
    with urllib.request.urlopen(req) as r, open(raw, "wb") as f: f.write(r.read())
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", raw, "-vf", "scale=-2:480", "-c:v", "libx264", "-crf", "28", "-preset", "veryfast", "-c:a", "aac", "-b:a", "128k", dst], check=True)
    os.remove(raw)
    src.write(f"- `{slug}.mp4`: {s['title']} · licence: {s['license']} · source: {s['url']}\n"); print("ok", slug)
