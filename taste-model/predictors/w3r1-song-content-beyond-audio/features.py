"""Per-song lyric features, each computed from that song's own lyrics only (no cross-song fitting). Cached by build_features.py."""
import re, json, math
import numpy as np
from collections import Counter

PROF = set("fuck fucking fucked shit bitch bitches nigga niggas ass dick pussy damn hoe hoes cunt motherfucker".split())
STOP = {"en": set("the and you i to a of in it is that me my on for with but this your we be all so not like just do".split()),
        "es": set("el la que de y en un los te mi se por con una no es lo me las para".split()),
        "fr": set("le la les de et je tu il un une que pas est vous en du pour dans qui".split()),
        "de": set("der die das und ich du nicht ist ein es mit den zu sie auf wir".split()),
        "pt": set("o a que de e eu voce nao um uma os para com se em do da".split())}
LRC = re.compile(r"^\[(\d+):(\d+(?:\.\d+)?)\]\s*(.*)$")
NAMES = ["n_words", "n_lines", "uniq_ratio", "line_rep", "avg_line_words", "std_line_words", "words_per_sec", "instrumental", "prof_rate", "q_rate", "excl_rate", "paren_rate",
         "i_rate", "you_rate", "we_rate", "they_rate", "ascii_ratio", "en_rate", "es_rate", "fr_rate", "de_rate", "pt_rate", "long_word_rate", "avg_word_len", "chorus_share",
         "n_stanzas", "first_lyric_frac", "lyric_span_frac", "line_gap_mean", "line_gap_cv", "gap_long_frac", "digit_rate", "caps_rate", "ooh_rate", "synced"]

def feats(rec):
    f = dict.fromkeys(NAMES, np.nan)
    if not rec or not rec.get("found"): return None
    dur = float(rec.get("dur") or 0)
    plain = rec.get("plain") or ""
    f["instrumental"] = 1.0 if rec.get("instrumental") else 0.0
    f["synced"] = 1.0 if rec.get("synced") else 0.0
    lines = [l.strip() for l in plain.split("\n")]
    nz = [l for l in lines if l]
    words = re.findall(r"[^\W\d_]+(?:'[^\W\d_]+)?", plain.lower())
    if len(words) >= 5:
        n = len(words); c = Counter(words)
        f["n_words"] = math.log(n); f["n_lines"] = math.log(len(nz) + 1)
        f["uniq_ratio"] = len(c) / n
        lc = Counter(l.lower() for l in nz); f["line_rep"] = 1 - len(lc) / len(nz)
        lw = np.array([len(l.split()) for l in nz]); f["avg_line_words"] = lw.mean(); f["std_line_words"] = lw.std()
        if dur > 0: f["words_per_sec"] = n / dur
        f["prof_rate"] = sum(c[w] for w in PROF) / n
        f["q_rate"] = plain.count("?") / len(nz); f["excl_rate"] = plain.count("!") / len(nz); f["paren_rate"] = sum(1 for l in nz if "(" in l) / len(nz)
        f["i_rate"] = sum(c[w] for w in ("i", "i'm", "i'll", "i've", "me", "my", "mine")) / n
        f["you_rate"] = sum(c[w] for w in ("you", "you're", "your", "you'll", "yours")) / n
        f["we_rate"] = sum(c[w] for w in ("we", "us", "our", "we're")) / n
        f["they_rate"] = sum(c[w] for w in ("they", "them", "he", "she", "his", "her")) / n
        f["ascii_ratio"] = sum(ch.isascii() for ch in plain) / max(len(plain), 1)
        for k, s in STOP.items(): f[k + "_rate"] = sum(c[w] for w in s) / n
        f["long_word_rate"] = sum(1 for w in words if len(w) >= 7) / n; f["avg_word_len"] = np.mean([len(w) for w in words])
        f["chorus_share"] = sum(v for l, v in lc.items() if v > 1) / len(nz)
        f["n_stanzas"] = math.log(1 + sum(1 for i, l in enumerate(lines) if l and (i == 0 or not lines[i - 1])))
        f["digit_rate"] = sum(ch.isdigit() for ch in plain) / max(len(plain), 1)
        f["caps_rate"] = sum(1 for l in nz if l.isupper()) / len(nz)
        f["ooh_rate"] = sum(c[w] for w in ("ooh", "oh", "ah", "yeah", "na", "la", "woah", "hey", "uh", "mmm", "whoa")) / n
    syn = rec.get("synced")
    if syn and dur > 0:
        t = [int(m.group(1)) * 60 + float(m.group(2)) for m in (LRC.match(l.strip()) for l in syn.split("\n")) if m and m.group(3).strip()]
        if len(t) >= 4:
            t = np.array(sorted(t)); g = np.diff(t)
            f["first_lyric_frac"] = min(t[0] / dur, 1.0); f["lyric_span_frac"] = min((t[-1] - t[0]) / dur, 1.0)
            f["line_gap_mean"] = float(np.log(g.mean() + 1e-3)); f["line_gap_cv"] = float(g.std() / (g.mean() + 1e-3)); f["gap_long_frac"] = float((g > 8).mean())
    return f

def text_chunks(rec, maxc=6, words=90):
    """Lyrics text chunks for the sentence embedding (deduplicated consecutive repeats)."""
    if not rec or not rec.get("found") or not rec.get("plain"): return []
    lines = []; 
    for l in rec["plain"].split("\n"):
        l = l.strip()
        if l and (not lines or lines[-1] != l): lines.append(l)
    w = " ".join(lines).split()
    if len(w) < 5: return []
    ch = [" ".join(w[i:i + words]) for i in range(0, len(w), words)]
    if len(ch) > maxc: idx = np.linspace(0, len(ch) - 1, maxc).round().astype(int); ch = [ch[i] for i in idx]
    return ch
