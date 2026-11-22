# Workflow 5 review

Run: 30 agents (6 inventory, 3 Opus leads, 2 engineers, 1 prep, 6 builders, 12 DAs), 17:57 to 00:01 UTC (~6.1 h). Result: null on "does tuning the numbers help" (all three areas), fold-set findings (staleness, label horizon, comparator, weighting matter; 1-3 month shifts do not), no W5 model beats the W4 listening reference at 80%. Reproducibility good (every headline number regenerated bit-for-bit by DAs).

## 1. Process improvements

What worked: flag-only gates, no time floors, no auto-retry, no sleep-to-pass-a-timer behaviour; all 12 DAs re-ran numbers and the null control; 190 claim checks (170 hold / 17 not / 3 unverified), the failures being wording/inference not numbers. No agent read /home/user/Listener/.claude or CLAUDE.md; no .sealed, decoy_universe or --sealed access found in transcripts (grep hits were only the words in report text); DAs did not run --late/--holdout (only selftest --v51).

Problems and waste:
- **Serial critical path through the 2-agent cap.** Timeline: inventory 18 min wall + critic 4 min, plan lead 7 min, round 1 ran 18:18 to 21:45 (3.5 h), lead review 8 min, engineer-r2 18 min, round 2 22:12 to 23:53. Builders+DAs queue behind each other: builder r1 content-numbers ran 99 min while the other two ran sequentially behind the engineer. DA starts waited for a free slot, not for the builder (e.g. DA signal-works started 20:11, builder done 20:11, fine, but content DAs waited until 20:56 to 21:38). Idle CPU headroom was small (4 cores), so the main lever is fewer/shorter agents, not more parallelism.
- **Round 2 partly re-trod round 1.** r2 music-recipe-numbers re-ran the same grid/inner-tuning procedure design as r1 content-numbers on another recipe (82 variants, 4 procedures) and r2 signal-fresh re-tested the r1 signal "fresh data" lead; the answers (no gain; averaging neutral) were the same as r1 predicted. Only r2 score-calculation and the pre-registered fresh-listening test added new information. Lead r1 should have been asked to justify each r2 task as "what could change the conclusion", and tasks whose r1 analogue was null should be shared-design checks, not full rebuilds.
- **Inventory phase heavy, low yield.** 567 rows, 362 with "no variation found"; the final report needed only the ~8 classes (fold set, label horizon, session gap, buckets, thresholds, HOLDOUT share, decoy ratio, 90-day). A single inventory agent plus a critic, or a table keyed by class, would have saved ~10 min of wall and large prompt payloads; the point of the inventory (what was never varied) could be a script-generated grep of constants.
- **Harness changed between rounds** (v5.0 in round 1, v5.1 in round 2: new fixed-comparator table, per-fold IV deltas, fold_meta, alt fold-set options). Mitigated well this time: additive/flagged, default output identical to v4.1 and checked by selftest, tables labelled with version, round-1 numbers called v5.0. Still, "best_ref chosen on the scored fold set" was only found as a problem in round 1 and fixed in round 2, so numbers across rounds were not all on one comparator. Prefer one engineer pass before builders that includes the known gaps.
- **Held-out use and leakage.** HOLDOUT budget (3 runs) fully spent in round 1, 1 per builder; budget 0 in round 2 (good, W4 lesson applied). LATE: 29 logged runs, 6 new, cap 2 per bundle worked. Leakage of held-out numbers: briefs said held-out numbers only in report files; I found no held-out numbers in structured results/journal, but leads' final section 6 holds them, so RESULTS-W5 correctly omits them. The LATE slice is worn out (seen by all agents since W4); HOLDOUT is spent. The next honest evidence is only the sealed slice.
- **Pre-registration gaps.** Grid/pre-reg files last modified after first scored runs (declarations appended); one r1 report omitted four scored post-hoc combinations; null-control statistic misquoted in three reports (per-seed mean vs gated value). Fix: harness should print a hash-stamped "declared before scoring" file, and the report template should have a fixed null-control line copied from harness output.
- **Wait loops.** Three builders used `sleep 60/120` polling loops (r1 eval-frame 8, r1 signal 6, r2 music 10) while jobs ran; these were legitimate waits for background runs, not gaming, but cost tokens. Use the Monitor tool / one `wait` instead of repeated polling.
- **Under-use by DAs** noted (calibration stopped at 10 of 12 seeds; unrun items) although coverage gates passed; 3 claims left unverified (one explicitly "not re-run by either DA"). Add to DA gate: any claim marked "not re-run" must be handed to the other DA of the pair.
- **Reporting slips caught late.** Empty/NaN output files (a5_trend_abs all NaN; one analysis silently dropped a fold), FILE_DELTAS80 empty for single-model files, round-1 stack failing independence by construction. Add output sanity assertions (no NaN tables, fold counts match) to analysis scripts.
- **Timing report in RESULTS says 6 h; actual 6.1 h wall**, consistent. Builders used 23-99 min of 90/120 caps; no cap breached.

## 2. How much the instructions steered the outcome

- Goal framing (arbitrary numbers, fold set also arbitrary) came from the user quotes; paraphrases followed the W5 paraphrase rule, and agents did not cite user-attributed method ideas. The unvetted-ideas list was weighed, not obeyed: e.g. "act on loose trends" and the 80% bar were used as the decision threshold, but the final report still demanded stability checks (secondary sign checks, 0.005 undecided margin), i.e. the agents leaned toward more strictness than the user's 80% preference. The README's 0.005 margin is stricter than plain 80%; two round-2 results sit between the two and were reported as "undecided". That is a framing choice made by the engineer/lead, not the user's rule: flag it as an open decision.
- Plan lead set the three round-1 directions and the "dismissed" directions; DAs were split into "works" and "dismissed" roles. This means the *question* was largely fixed by the lead, and all three answers were null; the stated area (tuning numbers) was tested thoroughly, but alternatives (new information sources, untested families) are only recommended, not tested. The brief steered toward evaluating tuning, which is what the user asked, so appropriate, but the builders' null conclusions partly reflect that every default had already been tuned on TUNE (regression to the mean), which agents stated honestly.
- Agents followed the evidence over framing in several places: the "trend grows +0.10/yr" claim was downgraded after DAs; "label noise is not the limit" kept as a belief; missing-audio effect declared likely a catalogue artefact.
- Hard-coded constants in the brief (LATE_CAP=2, caps 90/120 min, "decisions at 80%") shaped scope; these are risk-preference or logistics, not method, and were respected.

## 3. W4-review lessons (workflow-notes.md) applied?

1. No time floors, no auto-retry: applied (G1-G5). Helped: no gaming, no retried post-hoc modelling. (DAs finished 7-45 min; fine.)
2. Don't relay held-out numbers; don't print pooled dev in held-out runs: applied (brief says so; harness prints only held-out slice). Helped: no leakage found. But HOLDOUT is now spent anyway.
3. Freeze/version harness before builders: partly. Engineer-r1 bumped to v5.0 before builders; engineer-r2 produced v5.1 for round 2 with additive changes and selftest --v51 guaranteeing identical defaults. Numbers labelled by version. Worked, but cross-round comparability required careful wording in RESULTS-W5.
4. Leads/reviewers too short: partly. Review lead 8 min, final lead 8 min, plan lead 7 min; leads did re-run fast checks (lead re-ran five of six finals). Better than W4 but still short for the amount of material; coverage checklist helped.
5. Trim prompts, point to files: applied (file-based report docs, structured results short). Prompts still ~50 KB script; fine.
6. Shared prep long / overlap extraction: improved: prep-r1 took 18 min (vs 1h50). Round 2 had no prep.
7. Reproducibility: improved (every headline regenerated); remaining gaps: scratch-only dumps and null-refit pickles regenerable only by re-running, grid files edited after use.
Also applied: sanitised W3/W4 copies injected, DAs judged on coverage, no sleep-to-pass-timer, no dead conditional steps (G4). Sanitised inputs worked; no leak of chat notes (the forbid-.claude rule held: zero reads).

## 4. Lessons for W6
1. Make the round-2 task list answer "what could change a decision?"; do not rebuild a null round-1 design on another recipe.
2. The next clean test is sealed only: fix the evaluation and the decision rule (primary score, comparator ref_w4r1_listening + artist_recent, 80% cluster interval, margin yes/no) before building; ask the user once for margin choice.
3. Cut inventory to class-level; generate constants lists by script.
4. Require analysis scripts to assert no NaN/dropped folds and print the harness's own null-control line verbatim; have the harness hash declarations before scoring.
5. Replace builder polling sleeps with Monitor; give DAs hand-off of any "not re-run" claim.
6. Consider a single engineer pass before builders that includes every known harness gap (fixed comparator, fold-weight checks) so no mid-run harness bump is needed.
7. Next work should add new information (new-song context features, monthly retrain, missing-audio fill learned from training) rather than more tuning of existing recipes; the W6 goal is candidate-ready groundwork, with models averaged over plausible numbers.

## Proposed notes additions
- W5 lesson: round-2 builders must each state which round-1 conclusion they could overturn; no re-running of the same tuning design on another recipe unless the lead justifies it.
- W5 lesson: analysis scripts assert no NaN output and fold counts; report null-control statistic copied verbatim from harness (3 reports misquoted it).
- W5 lesson: pre-registration files must be written and hashed before first scored run; do not append afterwards.
- W5 lesson: use Monitor not sleep-loops for builder job waits.
- W5 fact: HOLDOUT budget spent (0), LATE worn out (29 runs, seen by all W4/W5 agents); only the sealed slice remains clean. Sealed untouched.
- W5 open decision for the user: undecided margin 0.005 vs plain 80% interval rule (two W5 results fall between).
- W5 fact: harness v5.1 (default output identical to v4.1; selftest and selftest --v51 pass); fixed comparator ref_w4r1_listening; pooled sauc resolves only differences >= ~0.02.
- W5 fact: 6 predictors folders contain results/*.log, npz untracked now; regenerable data goes to .cache or is gitignored.
