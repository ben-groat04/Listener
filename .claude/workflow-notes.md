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

## Overnight run (user-approved, 2026-11-21)
- User asleep ~9h; wants ~4 workflows total overnight, including one full review of the project so far ("full up to now project research to keep it moving in the right direction"), run back to back without waiting on the user ("I will be very unhappy if I wake up to you waiting on me for something").
- Waived for tonight: showing the brief to the user before launch; Opus allowed where the design needs it; hook approval prompt off via .claude/hooks/.overnight-until (expires automatically ~11:10 UTC).
- Still NOT allowed until the user is awake: candidate-song search.
- Sealed test run: user approved ONE, VERY CAREFULLY executed, near the end of the night, only if a dev result survives the devil's advocates and beats baselines (else skip). Pre-registered predictor(s)+baselines, no tuning after. Prep (labels/manifest/sealed-era features) by an isolated agent writing only to git-ignored .sealed/, never seeing scores. Only the main session registers/runs; results go to the user only, never to workflow agents.
- Still required: post-workflow Sonnet review + cleanup, pre-launch Sonnet audit with fixes, neutral launch (the latest user message is forwarded to all agents).
- User's challenge to W3's "exposure-driven label" reading, to pass verbatim (no added interpretation) in the next brief: "Are you sure this is the right way round? Is it not more of if I find I really like it I'll listen to that more than everything else. I don't have a preselected "listening session"" (Context: harness sessions = 30-min gaps; nnew_sess counts new songs in the whole session incl. after the song.) User: "do not steer".
