# Workflow 5: research lead final report

Timing: /tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf5/lead-final/TIMING.txt (start 2026-11-21T23:53:00Z, end appended there). Deliverable: /home/user/Listener/taste-model/RESULTS-W5.md (plain-English results, no held-out numbers). This file adds the coverage list, what I re-derived and how I weighed each flag.

## 1. Files read (all in full)
- Inventories: inventory-evalkit.md, inventory-w3-predictors.md, inventory-w4r1-predictors.md, inventory-w4r2-predictors.md, inventory-features.md (counts taken from their summaries; tables spot-read), inventory-critic.md (full).
- Lead plans: lead-r1.md (first part), lead-r2.md (full).
- Engineer and prep: engineer-r1.md, engineer-r2.md, prep-r1.md.
- Builder reports (6): builder-r1-eval-frame-folds.md, builder-r1-tune-content-numbers.md, builder-r1-tune-signal-numbers.md, builder-r2-signal-fresh-and-averaging.md, builder-r2-music-recipe-numbers.md, builder-r2-score-calculation.md.
- Devil's advocate reports (12): devils-advocate-r1-{eval-frame-folds,tune-content-numbers,tune-signal-numbers}-{works,dismissed}.md and devils-advocate-r2-{signal-fresh-and-averaging,music-recipe-numbers,score-calculation}-{works,dismissed}.md.
All in /tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf5/docs/. I read no other agent's scratch folder and no held-out log contents. I only counted lines: .cache/late_runs.log has 29 lines, and .cache/holdout_budget.json reads {"round": "w5r1", "remaining": 0}.

## 2. Headline scores I re-derived
Harness v5.1, fast TUNE, 2 threads. Outputs are in my scratch folder: run_*.txt and the *.pkl dumps; deltas.py computes the paired deltas.

| model | my sauc | builder | paired deltas (1000 resamples, seed 20260511, from my dumps) |
|---|---|---|---|
| pair_z | 0.661 | 0.661 | vs listening +0.0094 [-0.0015, +0.0229]; vs music +0.0141 [+0.0004, +0.0261]; vs artist_recent +0.0417 [+0.0164, +0.0926]; vs pool_artist_siblings +0.0168 [-0.0080, +0.0751] |
| final_avg21 | 0.659 | 0.659 | vs listening +0.0079 [+0.0006, +0.0121]; vs artist_recent +0.0401 [+0.0140, +0.0847]; vs siblings +0.0153 [-0.0074, +0.0652]. FOLD_META vs listening: IV +0.006 [+0.001, +0.011], Q 4.4/9 |
| final_avg81 | 0.646 | 0.646 | vs music -0.0009 [-0.0033, +0.0017]; vs listening -0.0056; vs artist_recent +0.0267 [-0.0027, +0.0827] |
| w5_final_mat0s (r1 signal) | 0.657 | 0.657 | not recomputed |
| w5r1_stack3 (r1 frame) | 0.653 | 0.653 | not recomputed |
| w5_tuned_margin (r1 content) | not re-run by me | 0.625 | the round-2 lead plan re-ran it: 0.625 |

DA spot-check: my 1000-resample intervals for pair_z vs music [+0.0004, +0.0261] and vs listening [-0.0015, +0.0229] equal the values the score-calculation "works" devil's advocate reports from its own re-run (claim 13). My final_avg21 deltas equal both round-2 signal devil's advocates' re-runs (+0.0079 [+0.0008, +0.0125] at their seed; same point). The lead-r2 plan had already re-run all three round-1 finals.

## 3. Inventory counts (from the five inventory summaries plus the critic)
| inventory | rows | reason found | variation found |
|---|---|---|---|
| evalkit | 116 | 91 | 15 |
| W3 predictors | 109 | 51 | 45 |
| W4r1 predictors | 131 | 44 | 59 |
| W4r2 predictors | 84 | 37 | 44 |
| features | 112 | 83 | 27 |
| total | 552 | 306 | 190 (362 without) |

The critic added 15 missing items (M01-M15), with essentially no variation found. Rows overlap between the evalkit and features inventories and the inherited rows. The criteria differ between agents: some count a docstring as a reason, and the strict W4r1 rule does not. The totals are approximate counts of rows, not of distinct items.

## 4. Flags and verdicts, and how I weighed them
- **r1 signal works-DA flag: claim 11 (tuner drift) unverified.** The dismissed-DA verified it by counting choices_fs.jsonl. I use it only as a description of a noisy tuner, as lead-r2 did.
- **r2 music dismissed-DA flag: claim 8 (walk-forward) unverified.** The works-DA read the output but did not re-run it. It is a low-power side result (procedures are near-identical, optimism +0.003). No conclusion depends on it.
- **r2 score works-DA flag: claim 10 (label noise is not the limit) partly unverified.** Both score DAs say the evidence covers Poisson noise only; nested-label kappas measure threshold sensitivity; 29% of not-loved songs are borderline; a4 AUCs carry tie-break noise of about 0.012. I report "label noise is not the limit" as a belief, and only the Poisson result as a finding.
- **Verdicts of does_not_hold.** All are inference or wording errors; no number failed to reproduce.
  - r1 frame 6 (2023-Q1 is negative; slope rests on early tiny quarters).
  - r1 frame 12 (tune_y omitted from the bar study).
  - r1 frame 14 (seed, not nboot).
  - r1 content 5 (shared-noise-draw explanation not supported; seed 1 is a 3 sd outlier).
  - r1 content 7 (inner-setting differences not decided).
  - r1 signal 2 (chance benchmark mis-scaled; combos omitted).
  - r1 signal 5 (margin rule fails for geometry B).
  - r1 signal 8 (stub empty).
  - r1 signal 9 (4 not 5 of 10 folds; sign rule not unique).
  - r2 signal 3 (best-of-20 "within chance" contradicted by bootstrap P 0.17 under the 80% rule).
  - r2 signal 6 (dose-response comparison not like-for-like).
  - r2 music 3, counted by both DAs (all 8 NEG are low-fill).
  - r2 music 11 (2023 concentration not supported by per-fold meta).
  - r2 music 13, counted by both DAs (the open-pool has_preview inference is wrong by construction).
  These are reflected in RESULTS-W5.md: the trend caveat, the chance-calibration wording, undecided-versus-80% for avg21 and avg_mat, the missing-audio question marked unresolved, and the null-control number.
- **Recurring interpretive points I adopted.**
  - Defaults were chosen on TUNE, so "nothing beats the default" is regression to the mean (all content and music DAs).
  - avg81 ties by construction.
  - The pair_z and stack3 choices used TUNE scores of the references.
  - Score reliability is circular (references tuned on sauc).
  - The null-control gated statistic (0.568-0.569) sits about 0.011 below the band top for stack3, pair_z and avg81, and the quoted "gap" uses the seed mean. I report PASS with that caveat.
- **The 0.005 undecided margin versus the plain 80% rule.** The project's decision threshold is about 80% intervals. The harness adds a 0.005 margin because lo80 flips with the seed, which is measured: seed sd of lo80 is 0.0006-0.0019 at 1000 resamples. avg21 and avg_mat have lo80 +0.001. Under a plain lo80 > 0 rule they would be POS. I report both readings and do not decide the rule.
- **Shared inputs.** shared-w5r1: DONE present, and all 7 MANIFEST hashes match per eight DAs. The one "no DONE" report came from a check made at an earlier time. .cache/shared (W4) matches its hashed manifest entries per three DAs. No action.
- **Process flags.** A3 silently excludes one fold; the a5 output is NaN; grid.py and PREREG.md were modified after the runs; post-hoc combos were unreported; __pycache__ remains in six w5 predictor folders (listed in RESULTS-W5 section 7 for the cleanup agent; I did not delete them because folder cleanup is assigned to the cleanup agent).

## 5. What I ran versus believe
Ran: five fast harness runs and the dump delta script (section 2). Nothing else; no --late, --holdout or --sealed run, and no stats.fm query.

Believed:
- The newest-listening and averaging gain, if real, is about +0.004 to +0.008, below resolvable size.
- The missing-audio effect is more catalogue than taste.
- Part of the trend is a change in era.

## 6. Held-out numbers [REMOVED in sanitised copy: held-out numbers]
