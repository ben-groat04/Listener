# Workflow 5, round 2: research lead plan
Start: see /tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf5/lead-r2/TIMING.txt (first line 2026-11-21T21:45:58Z).

## 1. What I read
All round-1 builder reports (eval-frame-folds, tune-content-numbers, tune-signal-numbers), all six devil's advocate reports, engineer-r1, prep-r1, my lead-r1 plan, and the round-1 summaries in my prompt. I did not read any held-out log or table myself; held-out numbers I saw are only those inside the builder/DA report files and are repeated nowhere outside section 6 of this file.

## 2. What I ran (dev only, harness v5.0, fast TUNE, 2 threads; outputs in my scratch folder lead-r2/)
1. `evalkit.run --fast --dump-scores sig.pkl predictors/w5r1-tune-signal-numbers/final.py` (51 s): w5_final_mat0s sauc 0.657 vs ref_w4r1_listening 0.651. Reproduces the builder's headline (0.657, +0.006).
2. `evalkit.run --fast --dump-scores ef.pkl predictors/w5r1-eval-frame-folds/predict.py` (19 s, warm cache): w5r1_stack3 sauc 0.653; vs artist_recent +0.034 80% [+0.003,+0.077]; vs best_ref +0.002 [-0.009,+0.011]; TUNE80-. Reproduces the builder (full run +0.034 [+0.004,+0.084]; the lo80 differs by the bootstrap-seed/nboot effect the builder documented).
3. `evalkit.run --fast --dump-scores con.pkl predictors/w5r1-tune-content-numbers/final.py` (119 s): w5_tuned_margin 0.625 vs ref_audio_final 0.632. Reproduces the builder.
4. Stub check for the critic's M12 / DA claim (signal, dismissed side, claim 8): with load_streams + song_table, the number of songs first played in the 1-2 day stub between the quarter start and cutoff-90 d is 0,0,1,0,0,0,1,0,0,0 for the 10 TUNE cutoffs (before the meta filter). Confirms the DA: the stub exists by date arithmetic but is practically empty, so the "quarter-stub fix" comparison tests almost nothing.
5. Early-slice check: tried, non-HOLDOUT songs first played 2020Q4-2021Q2 = 17+16+10 = 43 (love rate 0.44-0.71). An earlier-start fold set would add too few songs to matter; not pursued.
6. hetero.py on ef.pkl (per-fold paired AUC delta with artist-cluster bootstrap SE, 400 resamples; Cochran Q; inverse-variance (IV) weighted mean and linear trend):
   - stack3 - artist_recent: IV mean +0.039, Q = 10.6 on 9 df (p 0.30), I2 0.15; IV-weighted slope +0.107/yr (se 0.042, 80% [+0.053,+0.161]).
   - ref_w4r1_listening - artist_recent: IV mean +0.032, Q = 12.4 (p 0.19), I2 0.28; slope +0.113/yr (80% [+0.060,+0.166]).
   - ref_audio_final - artist_recent: IV mean +0.022, Q 11.1 (p 0.27).
   Reading: per-fold deltas are consistent with one common delta plus sampling noise (small folds have SE 0.12-0.15); the IV-weighted mean is close to pooled sauc. Equal-weight-per-quarter / half-year / year "macros" give 31-45-song folds the weight of 283-song folds and are dominated by noise, so their sign flips are not evidence that pooled weighting misleads. The time trend survives IV weighting (unlike the DA's equal-weight restriction to large quarters), but it is confounded with growing training history. This is a lead check, not a final result; round 2 task score-calculation is asked to test it properly.
7. Missing-audio partial check (con.pkl): rows whose ref_audio_final score equals the fold's most common tied value (neutral fill) number 57, love rate 0.368 vs 0.316. Same direction as the content DA's count (79 songs without a MERT clip, 0.44 vs 0.31); my tie heuristic does not identify all missing rows, so the count is not an exact re-derivation.
8. DA spot checks against builder files in the project folder: (a) eval-frame works-DA claim 6: results/a2_weights.txt line 48 shows 2023Q1 per-quarter delta vs artist_recent -0.068/-0.038/-0.048/-0.038 (audio/listening/music/stack) -> the DA verdict "does_not_hold" for "positive from 2022-Q4" is correct. (b) signal dismissed-DA claim 8 (stub empty) confirmed by my item 4. (c) content: both DAs' null-control re-runs report seed values 0.523/0.532/0.509/0.521/0.493, mean 0.516, identical to each other and to the builder's summary; I did not re-run the 15-min null control myself (cost), but my fast run reproduces the real score 0.625 they compare against.

## 3. Where the goal stands
### 3.1 Assumptions/numbers and whether tuning helps
Evidence (all TUNE, harness v5.0, reproduced by DAs and partly by me):
- Audio-content numbers of the W3 audio_final recipe (layers, windows, aggregation, PCA, whitening, alpha, member weights/subsets, missing-audio fill): no setting beats the default beyond noise; most moves hurt. Nested in-train tuning (5 procedures) loses 0.006-0.033; four of five have 80% intervals entirely below zero. Inner-vs-outer agreement across recipes is weak (mean Spearman 0.25).
- Training-signal/time numbers of the W4 listening recipe: no config clearly beats the default; nested tuning neutral to harmful (no procedure has lo80 > 0). Freshness of the listening record matters a lot (cutting back 30/90/180 d costs 0.010/0.040/0.079); half-lives/windows do not help.
- Supported at 80%: "tuning these numbers by selection on inner folds does not help" (both areas); "these default numbers sit at a TUNE optimum". Not supported: "the defaults are good" in any absolute sense (they were chosen on TUNE, so the landscape is biased toward them; no clean slice exists to measure that bias).
- Open, weak leads: (i) the newest-listening family in the signal recipe (partial-horizon targets, maturity < 90 d, grouping) shows a monotone dose-response and small positive deltas (+0.004 to +0.011) on most fold sets; one config has lo80 > 0 but was the best of 87; the declared final's gain rests largely on one fold. (ii) Selection-free averaging over configurations had lo80 > 0 in a post-hoc DA computation for signal configs but hurt for content recipes. (iii) Missing-audio policy: positive on six fold sets but driven by 79 songs and possibly catalogue availability rather than taste. (iv) Untested: the W4 music recipe's numbers (essentia logit clip, alpha, segments, GBM, member and MERT weights).
### 3.2 Is the set of folds arbitrary?
- Boundary shifts of 1-2 months, 1- vs 3-month cutoffs, fold vs calendar-quarter pairing, session gap and most exposure edges, artist_recent half-life and GBM baseline settings: harmless at 80% (rankings stable; paired 1-vs-3-month deltas inside noise).
- Matter: training staleness of 6-12 months (tune_h/tune_y) hurts content and listening models much more than artist history; the identity of best_ref changes with the fold set (chosen on the evaluated set, a winner's curse); label horizon 180/365 d removes the lead over artist_recent; wa must be paired within one cutoff.
- The pair-weighting claim needs a correction (my item 6): per-fold deltas are homogeneous within noise, so the equal-weight macros mainly add noise; pooled (about IV-weighted) is the defensible primary. The builder's proposed rule "half-year equal-weight point delta >= 0" is not supported (also definition-dependent per the dismissed DA). A positive time trend of content/listening over artist history survives IV weighting but is confounded with training-history length.
### 3.3 80% threshold
Applied throughout; harness grades exist. One residual issue: lo80 values within about 0.005 of zero flip with the bootstrap seed even at nboot 1000; they must be read as undecided.

## 4. Flags weighed
- tune-signal works-DA flag "claim 11 unverified" (tuner drift): the dismissed DA verified it by counting choices_fs.jsonl. It is descriptive of a noisy tuner; I treat drift as weak evidence and do not use it for decisions.
- Verdicts does_not_hold: eval-frame claim 6 (sign wording, confirmed by me; slope itself robust under IV weights), claim 12 (bar study omitted tune_y; the half-life choice changes the bar there: noted, tune_y is not a recommended frame anyway), claim 14 (nboot: seed not nboot is the noise; adopted as "undecided band"); content claim 7 (inner-setting differences not significant at 80%: accepted, "inner fold choice matters" is descriptive only), claim 5 (shared noise draw unsupported: accepted; no systematic bias); signal claims 2, 5, 8, 9 (calibration mis-scaled for near-default tweaks, margin rule fails for geometry B, stub practically empty, mat0_scale not uniquely sign-consistent and 4 not 5 of 10 folds): accepted; they turn "inside chance" into "about chance-sized" for the newest-listening family, which is why round 2 re-tests that family pre-registered. The harness LATE/ALL grade omission for the signal final is noted in section 6.
- shared-w5r1 "no DONE file" (eval-frame works-DA) vs DONE present (other DAs): timing artefact (checked at different times); all 7 files hash-match per four DAs. No action.

## 5. Decisions for round 2
### 5.1 Evaluation (engineer, v5.0 -> v5.1)
Small additions only; default output must stay identical to v5.0. (1) A per-fold meta-analysis helper and table (IV-weighted delta, Cochran Q, I2, tau, IV-weighted trend) so the weighting question is read correctly. (2) --best-ref to fix the comparison reference across fold sets (removes the per-set winner's curse). (3) FILE_DELTAS80 with 1000 resamples and an UNDECIDED marker for |lo80| < 0.005. (4) HOLDOUT closed for round 2 (budget stays 0; no regeneration): all three w5r1 units are spent and further use adds no independent evidence. LATE caps unchanged.
### 5.2 Shared prep: none. All inputs exist (shared-w5r1 MERT and essentia stores, .cache/w4r1 and .cache/w4r1-what-in-the-music compacts, regenerable from their build code).
### 5.3 Builders
1. signal-fresh-and-averaging: pre-registered test of the newest-listening family and of selection-free averaging vs choosing, with a null control of the procedures themselves and model staleness separated from record staleness.
2. music-recipe-numbers: the W4 music recipe's numbers (untested so far), the missing-audio policy (taste vs catalogue artefact), and averaging vs choosing for content.
3. score-calculation: validity and reliability of the score itself (metric, weighting, label, ceiling), with a pre-registered decision rule for later workflows.
Held-out: no HOLDOUT; at most one --late per builder on its declared final, confirmation only.
### 5.4 Runtime / go-no-go
- Task 1: fast runs of the listening recipe 0.5-1 min per few models; round-1 builder needed 44 min for 102 models; null control about 1-2 min for this recipe. Go (90 min cap).
- Task 2: the music recipe is the slowest reference (about 1/3 of 100 s per 30-cutoff pass for three refs); grid of about 40-60 recipes plus nested procedures 30-50 min; null control up to 15 min. Go if the builder caps the grid after timing one recipe; brief says so.
- Task 3: dump-based analyses; one multi-fold-set run about 4-6 min. Go.

## 6. Held-out numbers [REMOVED in sanitised copy: held-out numbers]

## 7. Ran vs believed
Ran: section 2. Believed, not tested: that the time trend is partly training-history growth; that the newest-listening family's gain, if real, is about +0.005; that no further clean dev slice exists (checked only the 2020-21 early slice size).
