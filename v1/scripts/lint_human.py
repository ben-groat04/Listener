#!/usr/bin/env python3
"""Deterministic lint for a human-voice listening piece (stdlib only, video-agnostic).

The mechanical half of the Turing/acceptance check. Rules come from the BRIEF in
v1/workflows/listening.js and from v1/analysis/human_listening/VERDICT.md
('What is still not human', 'Next changes').

Usage: python3 v1/scripts/lint_human.py <file.md> [--corpus DIR] [--json]
Exit 1 on any hard fail, 0 otherwise. Warnings never change the exit code.

Hard fails: more than 2 clock times; any banned jargon; any scaffolding;
no first person at all; hedge density above HEDGE_FAIL per 100 words.
Warns: word count outside 700-1,200 (LISTENING-style pieces); hedge density above HEDGE_WARN.
The hedge thresholds are lint settings chosen here, not measured human norms.

The corpus comparison is descriptive only. The corpus is small (STYLE.md says so),
mostly fragments, and no claim of statistical significance is made.
"""
import argparse, json, re, statistics, sys
from pathlib import Path

DEFAULT_CORPUS = "v1/analysis/human_listening/corpus"
MAX_CLOCK = 2
WORDS_MIN, WORDS_MAX = 700, 1200
HEDGE_WARN, HEDGE_FAIL = 1.5, 3.0  # per 100 words (lint settings)

CLOCK_RE = re.compile(r"(?<![\d:])\d{1,2}:\d{2}(?::\d{2})?(?![\d:])")
BANNED = [  # (label, regex)
    ("on the one", r"\bon the one\b"), ("no fill", r"\bno fill\b"),
    ("held sound", r"\bheld sound\b"), ("subtraction", r"\bsubtraction\b"),
    ("the wall", r"\bthe wall\b"), ("pedal", r"\bpedal\b"), ("taught", r"\btaught\b"),
    ("dB", r"\bdB\b|\bdecibels?\b"), ("Hz", r"\b\d*\s?k?Hz\b"), ("BPM", r"\bBPM\b"),
    ("stems", r"\bstems?\b"), ("chroma", r"\bchroma\b"),
    ("p= (statistic)", r"\bp\s*[=<]\s*0?\.\d+"),
    ("LUFS", r"\bLUFS\b"),
    ("process talk: hedge disclaimer", r"as far as i can tell|i can'?t swear to|i cannot swear to"),
    ("OBS tag", r"\bOBS\b"), ("INT tag", r"\bINT\b"),
    ("process talk: transcript", r"\btranscripts?\b"),
    ("process talk: measurements", r"\bmeasurements?\b"),
]
SCAFFOLD = [
    ("Worth five minutes", r"worth five minutes"), ("Not for you if", r"not for you if"),
    ("Two questions for you", r"two questions for you"), ("Which sentence", r"which sentence"),
    ("persona: cold first-timer", r"cold first-timer"), ("persona: who hears what", r"who hears what"),
    ("Best on headphones", r"best on headphones"), ("What nobody here could hear", r"what nobody here could hear"),
]
FIRST_RE = re.compile(r"\b(i|i'm|i've|i'd|i'll|im|me|my|mine|myself)\b", re.I)
HEDGE_RE = re.compile(r"\b(maybe|perhaps|seems?|seemed|might|possibly)\b", re.I)
TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)+\|?\s*$")
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:['’][A-Za-z]+)?")


def clean(text):
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"^\s{0,3}#{1,6}\s*", "", text, flags=re.M)
    text = re.sub(r"[*_`>]", "", text)
    return re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)


def sentences(text):
    t = re.sub(r"\s+", " ", clean(text)).strip()
    return [s for s in re.split(r"(?<=[.!?])[\"')”’]*\s+", t) if WORD_RE.search(s)]


def stats(text):
    words = WORD_RE.findall(clean(text))
    n = len(words) or 1
    lens = [len(WORD_RE.findall(s)) for s in sentences(text)] or [0]
    return {
        "words": len(words),
        "sentences": len(lens),
        "sent_len_mean": round(statistics.mean(lens), 1),
        "sent_len_var": round(statistics.pvariance(lens), 1),
        "first_person_per_100w": round(100 * len(FIRST_RE.findall(clean(text))) / n, 2),
        "hedge_per_100w": round(100 * len(HEDGE_RE.findall(clean(text))) / n, 2),
        "exclaim_per_100w": round(100 * text.count("!") / n, 2),
        "question_per_100w": round(100 * text.count("?") / n, 2),
    }


def lint(text):
    st = stats(text)
    res = {"stats": st, "hard": [], "warn": []}
    clocks = CLOCK_RE.findall(text)
    clocks += re.findall(r"\babout \d{1,2}[:.]\d{2}\b", text)  # 'about 4.37' style
    res["clock_times"] = clocks
    if len(clocks) > MAX_CLOCK:
        res["hard"].append(f"clock times: {len(clocks)} (max {MAX_CLOCK}): {', '.join(clocks[:12])}")
    hits = {}
    for label, rx in BANNED:
        m = re.findall(rx, text, flags=0 if label in ("OBS tag", "INT tag", "dB", "Hz", "BPM", "LUFS") else re.I)
        if m:
            hits[label] = len(m)
    res["banned"] = hits
    fr = re.findall(r"\bframes\b|\bframe \d+", text, flags=re.I)  # 'the frame' is ordinary film talk; only flag process-style use
    if fr:
        res["warn"].append(f"possible process talk ('frames'/'frame N') x{len(fr)}: check it is not about the analysis")
    if hits:
        res["hard"].append("banned jargon: " + ", ".join(f"{k} x{v}" for k, v in hits.items()))
    scaf = []
    for label, rx in SCAFFOLD:
        if re.search(rx, text, re.I):
            scaf.append(label)
    lines = text.splitlines()
    if any(TABLE_SEP_RE.match(l) for l in lines):
        scaf.append("table")
    res["scaffolding"] = scaf
    if scaf:
        res["hard"].append("scaffolding: " + ", ".join(scaf))
    if st["first_person_per_100w"] == 0:
        res["hard"].append("no first person (no I/my/me): one voice, someone who listened")
    if st["hedge_per_100w"] > HEDGE_FAIL:
        res["hard"].append(f"hedge density {st['hedge_per_100w']}/100w > {HEDGE_FAIL}")
    elif st["hedge_per_100w"] > HEDGE_WARN:
        res["warn"].append(f"hedge density {st['hedge_per_100w']}/100w > {HEDGE_WARN}")
    if not (WORDS_MIN <= st["words"] <= WORDS_MAX):
        res["warn"].append(f"word count {st['words']} outside {WORDS_MIN}-{WORDS_MAX:,} (LISTENING-style pieces)")
    res["pass"] = not res["hard"]
    return res


def corpus_text(path):
    """Extract the human-written excerpts from a corpus file: blockquote lines, plus
    double-quoted spans of 3+ words on list items. Headers and notes are skipped."""
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith(">"):
            out.append(s.lstrip("> ").strip())
        elif re.match(r"^(\d+\.|[-*])\s", s):
            for q in re.findall(r"[\"“]([^\"”]{12,})[\"”]", s):
                if len(q.split()) >= 3:
                    out.append(q)
    return "\n".join(out)


def corpus_stats(d):
    rows = {}
    for p in sorted(Path(d).glob("*.md")):
        t = corpus_text(p)
        if len(WORD_RE.findall(t)) >= 20:
            rows[p.name] = stats(t)
    return rows


def table(piece_name, st, corp):
    cols = [("words", "words"), ("sent_len_mean", "sent mean"), ("sent_len_var", "sent var"),
            ("first_person_per_100w", "1st/100w"), ("hedge_per_100w", "hedge/100w"),
            ("exclaim_per_100w", "excl/100w"), ("question_per_100w", "ques/100w")]
    rows = [(piece_name[-28:], st)] + [("corpus/" + k, v) for k, v in corp.items()]
    w = max(len(r[0]) for r in rows)
    lines = [f"{'':<{w}}  " + "  ".join(f"{c[1]:>10}" for c in cols)]
    for name, s in rows:
        lines.append(f"{name:<{w}}  " + "  ".join(f"{s[c[0]]:>10}" for c in cols))
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("file")
    ap.add_argument("--corpus", default=DEFAULT_CORPUS)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    text = Path(a.file).read_text(encoding="utf-8")
    res = lint(text)
    cdir = Path(a.corpus)
    if not cdir.is_dir() and not cdir.is_absolute():  # fall back to repo root (script is v1/scripts/)
        cdir = Path(__file__).resolve().parents[2] / a.corpus
    corp = corpus_stats(cdir) if cdir.is_dir() else {}
    res["corpus"] = corp
    if a.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"lint_human: {a.file}")
        for h in res["hard"]:
            print("  HARD FAIL:", h)
        for w in res["warn"]:
            print("  warn:", w)
        print("  RESULT:", "PASS" if res["pass"] else "FAIL")
        print()
        if corp:
            print("Descriptive comparison with the real corpus (corpus is SMALL, mostly short fragments;")
            print("extracted excerpts only; no claim of statistical significance):")
            print(table(a.file, res["stats"], corp))
        else:
            print(f"(no corpus found at {a.corpus}; comparison skipped)")
    sys.exit(0 if res["pass"] else 1)


if __name__ == "__main__":
    main()
