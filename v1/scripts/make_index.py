#!/usr/bin/env python3
"""Regenerate the status tables in v1/analysis/INDEX.md from what exists on disk.

Usage: python3 v1/scripts/make_index.py [--write]
  no flag : print the generated INDEX.md to stdout
  --write : write v1/analysis/INDEX.md (the only file this script ever writes)

Stdlib only. Status per deliverable: done = file(s) exist with non-zero size;
partial = some of the expected files exist, or a file is 0 bytes; missing = none.
0-byte files are always listed. Video names come from v1/data/*, v1/analysis*/ dirs.
The header (everything above the first '## ' heading) and the '## Research and logs'
section of the existing INDEX.md are kept verbatim.
"""
import os
import re
import sys

V1 = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
INDEX = os.path.join(V1, "analysis", "INDEX.md")
DEFAULT_HEADER = (
    "# Analysis index: every video by deliverable\n\n"
    "**Rule:** the final pieces are `REPORT.md` > `interpretation.md` > `music_reading.md` "
    "(best available first). Everything else (windows, specialists, panels, dossiers, segment "
    "notes, research) is working material. Paths are relative to `v1/`. Back to [README](../README.md).\n"
)


def rel(p):
    return os.path.relpath(p, V1)


def size(p):
    try:
        return os.path.getsize(p) if os.path.isfile(p) else None
    except OSError:
        return None


def files_in(d, pat=None):
    if not os.path.isdir(d):
        return []
    out = [os.path.join(d, f) for f in sorted(os.listdir(d)) if os.path.isfile(os.path.join(d, f))]
    if pat:
        out = [f for f in out if re.search(pat, os.path.basename(f))]
    return out


def single(path, note=""):
    """Status of one expected file."""
    s = size(path)
    if s is None:
        return "missing"
    if s == 0:
        return "partial: `%s` is 0 bytes" % rel(path)
    return "done: `%s`%s" % (rel(path), note)


def perceive(d):
    segs = files_in(d, r"^seg_\d+\.md$")
    ok = [f for f in segs if size(f)]
    extras = [n for n in ("music.md", "words.md") if size(os.path.join(d, n))]
    missing = [n for n in ("music.md", "words.md") if n not in extras]
    if not segs and not extras:
        return "missing"
    label = "`%s/` (%d segments%s)" % (rel(d), len(ok), "".join(", `%s`" % n for n in extras))
    bad = len(segs) - len(ok)
    if ok and not missing and not bad:
        return "done: " + label
    why = []
    if missing:
        why.append("no " + ", ".join("`%s`" % m for m in missing))
    if bad:
        why.append("%d empty segment file(s)" % bad)
    if not ok:
        why.append("no segment notes")
    return "partial: %s; %s" % (label, "; ".join(why))


def compare_for(vid):
    base = os.path.join(V1, "analysis", "compare")
    if not os.path.isdir(base):
        return "n/a"
    hits = []
    for setname in sorted(os.listdir(base)):
        sd = os.path.join(base, setname)
        if not os.path.isdir(sd):
            continue
        blob = setname
        for root, _, fs in os.walk(sd):
            for f in fs:
                if f.endswith(".md") and size(os.path.join(root, f)):
                    with open(os.path.join(root, f), errors="replace") as fh:
                        blob += fh.read()
        if not re.search(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(vid), blob):
            continue
        comp = os.path.join(sd, "comparison.md")
        rounds = sorted(d for d in os.listdir(sd) if d.startswith("round_") and os.path.isdir(os.path.join(sd, d)))
        if size(comp):
            hits.append("done: `%s` (%d round dirs)" % (rel(comp), len(rounds)))
        elif rounds:
            hits.append("partial: `%s/%s/` (no comparison.md)" % (rel(sd), rounds[-1]))
        else:
            hits.append("partial: `%s/`" % rel(sd))
    return "; ".join(hits) if hits else "n/a"


def data_state(vid):
    d = os.path.join(V1, "data", vid)
    if not os.path.isdir(d):
        return "no data dir"
    def n(sub):
        p = os.path.join(d, sub)
        return len([f for f in os.listdir(p) if not f.startswith(".")]) if os.path.isdir(p) else 0
    parts = []
    for sub, lab in (("frames_1fps", "frames"), ("lyrics", "lyrics"), ("stems", "stems"),
                     ("music_views", "music_views"), ("sync", "sync")):
        if n(sub):
            parts.append(lab)
    missing = [lab for sub, lab in (("stems", "stems"), ("music_views", "music_views")) if not n(sub)]
    ctx = " + context.md" if size(os.path.join(d, "context.md")) else ""
    if not parts:
        return "empty data dir"
    tag = "complete" if not missing else "partial (no %s)" % ", ".join(missing)
    return "%s: %s%s" % (tag, ", ".join(parts), ctx)


def zero_files():
    out = []
    for top in ("analysis", "analysis_blind"):
        for root, _, fs in os.walk(os.path.join(V1, top)):
            for f in fs:
                p = os.path.join(root, f)
                if size(p) == 0:
                    out.append(rel(p))
    return sorted(out)


def videos():
    names = set()
    for sub in ("data", "analysis/music", "analysis/perceive", "analysis_blind/music", "analysis_blind/perceive"):
        d = os.path.join(V1, sub)
        if os.path.isdir(d):
            names.update(x for x in os.listdir(d) if os.path.isdir(os.path.join(d, x)))
    for sub in ("analysis", "analysis_blind"):
        d = os.path.join(V1, sub)
        for x in os.listdir(d) if os.path.isdir(d) else []:
            if x in names and os.path.isdir(os.path.join(d, x)):
                names.add(x)
    # only real videos: those with a data dir
    data = os.path.join(V1, "data")
    names = {x for x in names if os.path.isdir(os.path.join(data, x))}
    return sorted(names, key=lambda s: (not re.match(r"video\d+$", s), s))


def interp_blind(vid):
    p = os.path.join(V1, "analysis_blind", vid, "interpretation.md")
    s = single(p)
    if s != "missing":
        return s
    d = os.path.join(V1, "analysis_blind", vid)
    bits = [n for n in ("dossier.md",) if size(os.path.join(d, n))]
    pan = sorted(x for x in os.listdir(os.path.join(d, "panel"))) if os.path.isdir(os.path.join(d, "panel")) else []
    if bits or pan:
        return "partial: only %s" % " and ".join(["`dossier.md`"] * bool(bits) + (["`panel/%s`" % ("-".join([pan[0], pan[-1]]) if len(pan) > 1 else pan[0])] if pan else []))
    return "missing"


def build(vids):
    L = []
    L.append("## Informed (`analysis/`)")
    L.append("| Video | REPORT | interpretation | music_reading | perceive | compare | blind-vs-informed (blindcmp) |")
    L.append("|---|---|---|---|---|---|---|")
    for v in vids:
        a = os.path.join(V1, "analysis")
        L.append("| %s | %s | %s | %s | %s | %s | %s |" % (
            v,
            single(os.path.join(a, v, "REPORT.md")),
            single(os.path.join(a, v, "interpretation.md")),
            single(os.path.join(a, "music", v, "music_reading.md")),
            perceive(os.path.join(a, "perceive", v)),
            compare_for(v),
            single(os.path.join(a, "blind_vs_informed", v + ".md")),
        ))
    L.append("")
    L.append("## Blind (`analysis_blind/`, no context)")
    L.append("| Video | blind interpretation | blind music_reading | blind perceive |")
    L.append("|---|---|---|---|")
    b = os.path.join(V1, "analysis_blind")
    for v in vids:
        L.append("| %s | %s | %s | %s |" % (
            v, interp_blind(v),
            single(os.path.join(b, "music", v, "music_reading.md")),
            perceive(os.path.join(b, "perceive", v)),
        ))
    L.append("")
    L.append("## Extracted data (`data/<video>/`)")
    L.append("| Video | State |")
    L.append("|---|---|")
    for v in vids:
        L.append("| %s | %s |" % (v, data_state(v)))
    L.append("")
    L.append("## Zero-byte files (flagged)")
    z = zero_files()
    L.extend(["- `%s`" % p for p in z] if z else ["- none"])
    return "\n".join(L) + "\n"


def main():
    old = ""
    if os.path.isfile(INDEX):
        with open(INDEX, errors="replace") as fh:
            old = fh.read()
    m = re.search(r"^## ", old, re.M)
    header = old[:m.start()].rstrip("\n") + "\n" if m else DEFAULT_HEADER
    header = re.sub(r"\n*(_Tables below are generated by[^\n]*_\n*)+$", "\n", header)
    f = re.search(r"^## Research and logs", old, re.M)
    footer = old[f.start():] if f else ""
    note = ("\n_Tables below are generated by `python3 v1/scripts/make_index.py --write` "
            "(file existence and size only; do not edit by hand)._\n\n")
    text = header + note + build(videos()) + ("\n" + footer if footer else "")
    if "--write" in sys.argv[1:]:
        with open(INDEX, "w") as fh:
            fh.write(text)
        print("wrote " + rel(INDEX))
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
