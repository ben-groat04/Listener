# Notes for Workflow 3 brief (approved by user)
- Builder brief: mandatory null control, paired delta vs pool_artist_siblings and artist_recent, held-out dev slice (tune on early folds, report late); --fast for all iteration, full runs only for final scores.
- One Opus "research lead" agent between rounds (user approved): owns experiment design/protocol, resolves new-artist tie anomaly, judges whether lifts are real.
- Include user's message verbatim: "Ah ok. Is the score calculation good? In the next workflow a lot of things you've been treating as fixed need to be re-investigated. Because with the current scoring system let's be honest with the subjectivity you won't be going super super high" — scoring/label/pools/bar all open to re-investigation; no suggested alternatives.
- Open-pool decoy leak (decoys selected using post-cutoff listening) known.
- Workflow concurrency cap = 2 on 4 cores; consider plain background agents for parallel builders.
- Pre-launch Sonnet prompt audit; launch right after neutral user message.
