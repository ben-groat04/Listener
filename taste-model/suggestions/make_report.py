import sys, pandas as pd
sys.path.insert(0, '/home/user/Listener/taste-model')
from evalkit import data
R = "/home/user/Listener/taste-model/suggestions/"
d = pd.read_csv(R + "candidates_scored.csv"); d = d[d.has_mert].sort_values("score", ascending=False)
def pick(x, n):
    out, cnt = [], {}
    for r in x.itertuples():
        if cnt.get(r.artist_id, 0) < 2 and (data.song_key(r.title), r.artist.lower()) not in {(data.song_key(o.title), o.artist.lower()) for o in out}:
            out.append(r); cnt[r.artist_id] = cnt.get(r.artist_id, 0) + 1
        if len(out) == n: break
    return out
new, old = pick(d[~d.known_artist], 20), pick(d[d.known_artist], 10)
def sec(title, rows, start):
    s = f"\n## {title}\n\n| # | Title | Artist | Deezer | Score pct |\n|---|---|---|---|---|\n"
    for i, r in enumerate(rows, start): s += f"| {i} | {r.title} | {r.artist} | [link]({r.link}) | {r.pct:.1f} |\n"
    return s
n = len(d); nn = (~d.known_artist).sum()
hdr = (f"# Song suggestions 1 (2026-11-23)\n\nMade with model `avg21_dev` (w6r1-content-ranker-final, unchanged, no retuning): each song is scored from MERT features of its 30 s preview against a taste profile trained on the owner's full listening history through 2026-11-23 (cutoff = today, all streams). "
       f"Candidates: Deezer related-artist walk (2 hops from the owner's top 49 artists by plays in the last 12 months; top tracks of the 260 best-connected related artists plus the seed artists' own top tracks) and Deezer genre charts (rock, alternative, pop; 100 tracks each; singer-songwriter genre not matched). "
       f"2,821 tracks with a preview were collected; 781 were removed as already played (normalised title + primary artist; Deezer ids cannot be matched to the history's ids), leaving 2,040 candidates, of which {n} were scored ({nn} by artists never played). Scores are shown as percentile among scored candidates. "
       f"Shortcuts: hop 2 was run from all 573 hop-1 artists; at most 8 top tracks per walk artist; played-matching is by name only (title with brackets/remaster suffixes stripped + artist; 3.4% of plays have no artist name in the metadata and were matched by title only; a remix or differently titled version could still slip through; checked by hand for all 30 listed songs); Spotify links not looked up. No tuning or sealed data used.\n")
open(R + "SUGGESTIONS-1.md", "w").write(hdr + sec("New artists (never played)", new, 1) + sec("Artists you already know", old, len(new) + 1))
print(len(new), len(old))
