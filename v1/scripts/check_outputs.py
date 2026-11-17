"""Verify the extraction pipeline produced every expected, non-empty, plausible output for each video. Exit 1 if anything is wrong.
Usage: check_outputs.py [--blind] [video ...]   (default: every folder in v1/data)
       check_outputs.py --tags EARLIER_STAGE.md LATER_STAGE.md   (tag-lowering report; exit 1 if any lowered without a stated reason)
       check_outputs.py --report REPORT.md   (two-tier report rules; prints PASS/FAIL per rule, exit 1 on any FAIL)
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

# ---- two-tier report check (--report) ----
DNC_RE = re.compile(r"\b(fur|hand-\w*|policeman)\b", re.I)  # DO_NOT_CLAIM words (v1/DO_NOT_CLAIM.md items 1, 2, 4)
STAT_RE = re.compile(r"\d(?:[.,]\d+)*\s?(?:k?Hz|dB(?:FS)?|%)|\b[pr]\s?=\s?[-+~<>]?\s?\d|\b[pr]\s?=", re.I)
BANNED_NOUN = re.compile(r"\b(heartbeats?|bells?|breath(?:s|ing)?)\b", re.I)
APPX_RE = re.compile(r"^#{1,6}\s*(?:Tier\s*2\W*)?Evidence appendix\b", re.I | re.M)
def sentence_around(t, a, b):
    s0 = max(t.rfind(". ", 0, a), t.rfind("\n", 0, a)); e = [x for x in (t.find(". ", b), t.find("\n", b)) if x >= 0]
    return t[s0 + 1:(min(e) if e else len(t))]
def report_mode(path):
    t = open(path, errors="replace").read(); res = []
    def rule(name, ok, detail=""): res.append((name, ok, detail))
    m = APPX_RE.search(t); tier1 = t[:m.start()] if m else t
    rule("listener heading ('What it is like to listen')", bool(re.search(r"^#{1,6}[^\n]*What it is like to listen", t, re.I | re.M)),
         "missing heading '## What it is like to listen (interpretation)'")
    lm = re.search(r"^#{1,6}[^\n]*What it is like to listen[^\n]*\n(.*?)(?=^#{1,6}\s|\Z)", t, re.I | re.M | re.S)
    if lm: rule("listener section tagged (interpretation) and first person", bool(re.search(r"interpretation", t[lm.start():lm.start() + 200], re.I)) and bool(re.search(r"\bI\b|\bmy\b", lm.group(1))), "heading lacks '(interpretation)' or section has no first person")
    rule("Tier 2 evidence appendix heading", bool(m), "no 'Evidence appendix' heading")
    if m: rule("appendix has 'Checked against'", bool(re.search(r"checked against", t[m.start():], re.I)), "appendix lacks a 'Checked against' line")
    rule("'Where it sits' present in Tier 1", bool(re.search(r"where it sits", tier1, re.I)), "no 'Where it sits' paragraph (or the 'not established from the sources' line)")
    hits = [f"line {tier1.count(chr(10), 0, x.start()) + 1} '{x.group(0)}'" for x in STAT_RE.finditer(tier1)]
    rule("no Hz/dB/%/p=/r= in Tier 1", not hits, "; ".join(hits[:8]) + (" ..." if len(hits) > 8 else ""))
    nb = [f"line {tier1.count(chr(10), 0, x.start()) + 1} '{x.group(0)}'" for x in BANNED_NOUN.finditer(tier1)
          if not re.search(r"\(metaphor\)", sentence_around(tier1, x.start(), x.end()), re.I)]
    rule("emotive sound nouns (heartbeat/bell/breath) labelled '(metaphor)'", not nb, "; ".join(nb[:8]))
    dn = [f"line {tier1.count(chr(10), 0, x.start()) + 1} '{x.group(0)}'" for x in DNC_RE.finditer(tier1)]
    rule("DO_NOT_CLAIM words (fur, hand-, policeman) absent from Tier 1", not dn, "; ".join(dn[:8]))
    paras = [p for p in re.split(r"\n\s*\n", tier1) if p.strip() and not p.lstrip().startswith("#")]
    lim = re.compile(r"(through|by) (measurements|stems|spectrograms)|not by ears|measured, not heard|heard it only", re.I)
    early = any(lim.search(p) for p in paras[:2])
    rule("limitation statement not in the opening paragraphs", not early, "limitation wording found in the first two paragraphs; put it in one sentence at the end of Tier 1")
    ctx_early = bool(paras) and re.search(r"context\.md|according to (the )?(research|context)", paras[0], re.I) and "[CONTEXT:" not in paras[0]
    rule("opening paragraph context facts carry [CONTEXT: file, confidence]", not ctx_early, "opening mentions context/research but has no [CONTEXT: file, confidence] tag")
    bad = 0
    print(f"report check: {path}")
    for name, ok, d in res:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}" + ("" if ok else f"  -> {d}")); bad += (not ok)
    print(f"report: {bad} rule(s) failed"); return 1 if bad else 0
if "--report" in sys.argv:
    fa = [a for a in sys.argv[1:] if a != "--report"]
    if len(fa) != 1: sys.exit("usage: check_outputs.py --report REPORT.md")
    sys.exit(report_mode(fa[0]))

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
