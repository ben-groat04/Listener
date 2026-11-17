"""Verify the extraction pipeline produced every expected, non-empty, plausible output for each video. Exit 1 if anything is wrong.
Usage: check_outputs.py [--blind] [video ...]   (default: every folder in v1/data)
       check_outputs.py --tags EARLIER_STAGE.md LATER_STAGE.md   (tag-lowering report; exit 1 if any lowered without a stated reason)
Warnings (do not change the exit code): missing .done marker in the video folder; emotive nouns (heartbeat, bell, breath ...) in
v1/analysis*/<video>/**/*.md with no digit or 'metaphor'/'figurative'/'literal' label within 100 characters.
--blind: context.md is not required (blind runs must not have one). Otherwise a context.md that is still the unfilled template
(contains '<!-- TEMPLATE' or the original template sentence, or is under 400 bytes) counts as missing/empty."""
import json, os, sys, glob, re
root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# ---- confidence-tag extraction (--tags) ----
TAG_RE = re.compile(r"\b(OBSERVED|HEARD[ -]?(?:HIGH|MED(?:IUM)?|LOW)|HEARD(?![ -]?DATA)|INFERRED|SPECULATED)\b(?:[ :/-]*(high|med(?:ium)?|low)\b)?", re.I)
RANK = {"OBSERVED": 4, "HEARD-HIGH": 4, "HEARD-MED": 3, "INFERRED": 2, "HEARD-LOW": 1, "SPECULATED": 0}
REASON_RE = re.compile(r"\b(because|reason|lowered|downgrad\w*|demoted|softened|revised|re-?check\w*|re-?listen\w*|corrected|on closer|no longer|cannot be verified|not verified)\b", re.I)
STOP = set("the a an and or of to in on at is was are were it its this that with for as by from be has had have not no but".split())
def norm_tag(m):
    t = re.sub(r"[ -]+", "-", m.group(1).upper()); lvl = (m.group(2) or "").upper()[:3]
    if t == "HEARD": t = "HEARD-" + (lvl if lvl else "MED")  # bare HEARD: treated as medium (unstated level)
    return "HEARD-MED" if t.startswith("HEARD-MED") else t
def tagged_claims(path):
    out = []
    for i, line in enumerate(open(path, errors="replace").read().splitlines()):
        ms = list(TAG_RE.finditer(line))
        if not ms: continue
        tags = [norm_tag(m) for m in ms]
        body = TAG_RE.sub(" ", line).lower()
        words = {w for w in re.findall(r"[a-z0-9][a-z0-9.:']+", body) if w not in STOP and len(w) > 2}
        out.append((i + 1, min(tags, key=lambda t: RANK[t]), words, line.strip()))
    return out
def tags_mode(a, b):
    ca, cb = tagged_claims(a), tagged_claims(b); lb = open(b, errors="replace").read().splitlines(); n = 0
    print(f"tags: {len(ca)} tagged lines in {os.path.basename(a)}, {len(cb)} in {os.path.basename(b)}")
    for ln, tag, w, text in cb:
        best, bs = None, 0.0
        for ln0, tag0, w0, t0 in ca:
            if not w or not w0: continue
            sim = len(w & w0) / min(len(w), len(w0))
            if sim > bs: best, bs = (ln0, tag0, t0), sim
        if best and bs >= 0.6 and RANK[tag] < RANK[best[1]]:
            ctx = lb[ln - 1] + (" " + lb[ln] if ln < len(lb) and not TAG_RE.search(lb[ln]) else "")
            if not REASON_RE.search(ctx):
                n += 1; print(f"  LOWERED without reason: {best[1]} (A:{best[0]}) -> {tag} (B:{ln}), overlap {bs:.2f}\n    A: {best[2][:140]}\n    B: {text[:140]}")
    print(f"tags: {n} lowered without a stated reason"); return 1 if n else 0
if "--tags" in sys.argv:
    fa = [a for a in sys.argv[1:] if a != "--tags"]
    if len(fa) != 2: sys.exit("usage: check_outputs.py --tags EARLIER.md LATER.md")
    sys.exit(tags_mode(*fa))

# ---- emotive-noun lint ----
EMOTIVE = re.compile(r"\b(heartbeats?|bells?|breath(?:s|ing)?|breathe[sd]?|sighs?|shivers?|ache[sd]?)\b", re.I)
LABEL = re.compile(r"\d|metaphor|figurative|literal", re.I)
def emotive_lint(v):
    hits = []
    for p in sorted(glob.glob(f"{root}/v1/analysis*/{v}/**/*.md", recursive=True)):
        t = open(p, errors="replace").read()
        for m in EMOTIVE.finditer(t):
            if not LABEL.search(t[max(0, m.start() - 100):m.end() + 100]):
                ln = t.count("\n", 0, m.start()) + 1; hits.append(f"{os.path.relpath(p, root)}:{ln} '{m.group(0)}'")
    return hits
PLACEHOLDER_RE = re.compile(r"\{\{[^}\n]*\}\}|\[(?:fill|insert|todo|tbd|tba)[^\]\n]*\]|<(?:fill|insert|todo|tbd|tba|your|artist|title|name|subject|video|unknown|placeholder)[^<>\n]{0,40}>|\b(?:TODO|TBD|FIXME)\b|\bXXX+\b|<!--\s*(?:fill|todo)", re.I)
args = sys.argv[1:]; blind = "--blind" in args; args = [a for a in args if a != "--blind"]
EXPECT = ["audio/song.wav", "contact_sheets/sheet_01.jpg", "frames_1fps/f_0001.jpg", "scenes/shots.json", "audio_features/summary.json",
          "audio_features/beat_times.json", "visual_features/per_second.json", "visual_features/cut_beat_alignment.json",
          "stems_raw/htdemucs/song/vocals.wav", "stems_raw/htdemucs/song/drums.wav", "stems_raw/htdemucs/song/bass.wav", "stems_raw/htdemucs/song/other.wav",
          "stems/stem_rms_per_second.json", "music_views/summary.json", "music_views/chords.json", "music_views/clap_tags.json", "sync/sync.json"]
if not blind: EXPECT.append("context.md")
TEMPLATE_MARKS = ("<!-- TEMPLATE", "Per-video facts discovered by agents (subject, artist, sources)")
vids = args or sorted(os.path.basename(p) for p in glob.glob(f"{root}/v1/data/*") if os.path.isdir(p))
bad = 0
for v in vids:
    D = f"{root}/v1/data/{v}"; miss = [e for e in EXPECT if not os.path.exists(f"{D}/{e}") or os.path.getsize(f"{D}/{e}") == 0]
    if not glob.glob(f"{D}/lyrics/*.txt") or not [p for p in glob.glob(f"{D}/lyrics/*.txt") if not p.endswith("_doubtful.txt")]: miss.append("lyrics/*.txt")
    if not glob.glob(f"{D}/music_views/window_*.png"): miss.append("music_views/window_*.png")
    try:
        dur = json.load(open(f"{D}/audio_features/summary.json"))["duration_s"]
        nf = len(glob.glob(f"{D}/frames_1fps/f_*.jpg"))
        if abs(nf - dur) > 2: miss.append(f"frames_1fps count {nf} != duration {dur:.1f} s (tolerance 2)")
        nw = len(glob.glob(f"{D}/music_views/window_*.png"))
        if nw and abs(nw - -(-dur // 20)) > 1: miss.append(f"music_views windows {nw} != ceil(duration/20)={int(-(-dur // 20))}")
    except Exception as e:
        miss.append(f"duration check impossible ({e.__class__.__name__}: {e})")
    cm = f"{D}/context.md"
    if not blind and os.path.exists(cm) and os.path.getsize(cm) > 0:
        t = open(cm).read()
        if any(m in t for m in TEMPLATE_MARKS) or len(t.encode()) < 400: miss.append("context.md is still the empty template")
        else:
            ph = PLACEHOLDER_RE.findall(t)
            if ph: miss.append(f"context.md has unfilled placeholders ({len(ph)}: {', '.join(sorted(set(x if isinstance(x, str) else '' for x in ph)))[:80]})")
    print(f"{v}: {'OK' if not miss else 'MISSING/BAD ' + '; '.join(miss)}"); bad += bool(miss)
    # warnings only (never change the exit code)
    if not os.path.exists(f"{D}/.done"): print(f"  WARN {v}: no .done marker in v1/data/{v}/")
    em = emotive_lint(v)
    if em: print(f"  WARN {v}: {len(em)} emotive-noun use(s) with no number/'metaphor' label nearby: " + "; ".join(em[:8]) + (" ..." if len(em) > 8 else ""))
sys.exit(1 if bad else 0)
