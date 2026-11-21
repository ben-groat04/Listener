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
- User on stats strictness (pass verbatim to Opus leads): "you're being very strict on confidence intervals etc, not sure if this is a good idea given how subjective music is" / "Yes get the harness to think about whether it needs to be less strict based on what's come so far wrt stats." Also: W3 works-DA spent 6m50s but claimed ~15 min; DA time must be checked from transcript timestamps.
- User: "my suggestions in chat about how to work might not be the best" -> audit each in-chat suggestion on merit before it reaches a workflow; present as suggestions to weigh.
- LEAK: W3 round-1 review lead read .claude/workflow-notes.md (CLAUDE.md tells briefs-drafters to read it), so it saw un-audited chat notes (e.g. the session question). Future briefs must forbid reading .claude/.

## User suggestion after W3 results (to weigh, not an instruction)
- Verbatim: "I still disagree with one score summarising everything. Surely each test will be different levels of good at different times/listening frequencies/etc. but that's again for an agent to weigh as it's just my idea"
- Added to W4 CONTEXT with the "my suggestions… might not be the best" caveat; the pre-launch audit must merit-check it.
- User (after W3): do NOT present their method suggestions as "the user said" — agents over-weight them. Briefs list them unattributed, neutrally paraphrased, under "Unvetted ideas raised in discussion" (may well be wrong, weigh on evidence only). This supersedes the verbatim-quote framing for method suggestions; the audit checks paraphrase fidelity and neutrality instead of quote accuracy.

## Lessons from W3 post-review (apply in W4 before launch)
1. Shared inputs (iTunes fill, previews, pools, needed-clip feature extraction) must be complete and frozen before builders start; no cache/pool changes mid-round; brief asks for runtime estimate with go/no-go. (W3: one builder ran 7.5 h extracting MERT; ~2.5k clips extracted for nothing.)
2. Don't make a round wait on the slowest builder: per-builder wall-clock cap; start each DA as its builder finishes, or make heavy extraction its own shared step.
3. Both W3 Opus leads read .claude/workflow-notes.md. Every prompt must forbid reading /home/user/Listener/.claude/ and CLAUDE.md pointers for leads.
4. DAs ignored the 20-min floor (6.9-14.4 min) and one skipped reading evalkit code; enforce with timing/rejection, require re-running builders' null-control checks.
5. Fit-cache keys must include seed/relabelled identities; selftest should assert 3 null seeds differ (3 cache bugs found only by DAs).
6. LATE hygiene: 16 late runs logged; cap per predictor hash in run.py; DAs get read-only LATE tables; LATE is no longer clean after W3 — consider a new held-out slice.
7. Round 2 was shallow (~19 min/builder); give round 2 a time floor/checklist.
8. One source of truth for folder names (lead brief vs template conflicted).
- User declined the sealed test after W3: "No it's not good enough". No sealed run before W4.
- W4 injects sanitised W3 copies (taste-model/reports/w3-sanitised/): user-attributed method ideas and W3's next-step recommendations removed. Future workflows: inject sanitised copies of prior results the same way.

## For W5: new suggestion from chat (unvetted; present unattributed in "Unvetted ideas raised in discussion", audit on merits)
- Verbatim (for the audit only, never paste attributed into a brief): "For wf5: it should think about how people listen to and discover music"
- Neutral paraphrase candidate: "It may help to consider how people actually listen to and discover music." Audit must check this paraphrase adds no method hints beyond the original.
- W4 lesson: the builder time floor (40 min) auto-retried a builder that had legitimately finished its pre-declared design in 36 min after using its one HOLDOUT run. Floors must not trigger retries once the checklist is complete / HOLDOUT is used; flag only.
