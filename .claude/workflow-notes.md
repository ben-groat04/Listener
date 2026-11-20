# Notes for Workflow 3 brief (approved by user)
- Builder brief: mandatory null control, paired delta vs pool_artist_siblings and artist_recent, held-out dev slice (tune on early folds, report late); --fast for all iteration, full runs only for final scores.
- One Opus "research lead" agent between rounds (user approved): owns experiment design/protocol, resolves new-artist tie anomaly, judges whether lifts are real.
- Include user's message verbatim: "Ah ok. Is the score calculation good? In the next workflow a lot of things you've been treating as fixed need to be re-investigated. Because with the current scoring system let's be honest with the subjectivity you won't be going super super high" — scoring/label/pools/bar all open to re-investigation; no suggested alternatives.
- Open-pool decoy leak (decoys selected using post-cutoff listening) known.
- Workflow concurrency cap = 2 on 4 cores; consider plain background agents for parallel builders.
- Pre-launch Sonnet prompt audit; launch right after neutral user message.

# Added after Workflow 2 review
- Workflow tool runs max 2 agents at once on this 4-core box; state the real cap in briefs. Drop "1 CPU thread" rule; give a measured thread budget instead.
- Builders: require a minimum checklist of mandatory checks rather than relying on a time cap (some stopped after 8-13 min citing "no time").
- Builders must not see other builders' folders/scratch; shared artefacts are produced once up front and published to all builders at the same time (no builder owns them). Do not name methods/models when describing shared artefacts.
- Do not pass devil's-advocate "suggested priorities" verbatim to builders; next-step planning goes through the research lead.
- Devil's advocate: per-claim verification table, must read builder code, time floor; ~1 min DA runs are too shallow. Check self-reported durations against transcript timestamps.
- Known evaluation issues for the research lead to weigh (facts, not instructions): duration alone scores ~0.578 on the tried pool (no metadata baselines in harness); preview-missing → NaN audio features is a ~0.025 AUC shortcut; new-artist tie anomaly (identical artist-baseline metrics on zero-history subset) never checked; some feature transforms fitted on all dev embeddings incl. decoys/future tracks (transductive); decoy universe built from lifetime top-300 artists incl. post-cutoff plays (open pool inflated); below-chance results (e.g. 0.37-0.45) were dropped instead of investigated.
- Sealed runs need sealed-era data/features prepared first and sealed labels/manifest regenerated (candidate sets changed in evalkit v2.1).
