# Workflow 5, round 1: research lead plan

Start time: see TIMING.txt in the lead-r1 scratch folder (first line 2026-11-21T18:11:06Z).

## 1. What I read and what I ran

Read in full: the five inventories (evalkit, w3-predictors, w4r1-predictors, w4r2-predictors, features) and the coverage critic; W4 sanitised RESULTS.md and W3 sanitised RESULTS.md; the evalkit README (v4.1); evalkit/data.py (labels, folds, HOLDOUT, song identity, song_table, make_folds); run.py prepare_folds, keep_label, score_predictor, main() argument handling. I did not read any held-out log (late_runs.log, holdout_runs.log, late_tables) and quote no held-out number anywhere.

Ran (dev only, through evalkit.data.load_streams, never _load_all, nothing after 2025-04-01): `foldcheck.py` in my scratch folder. It builds song_table on dev streams, removes HOLDOUT artists, and tabulates songs first played per calendar quarter, loved count, love rate and the pair weight n1*n0 (approximation of the harness pools: before the harness's metadata filter, so counts are a few % higher than the pools).

Results of that check (facts):
- Dev streams 2020-06-03 .. 2025-03-31 (106,188 rows after dedupe).
- Love rate of newly tried songs falls from 0.41-0.68 per quarter in 2021-Q3..2022-Q4 (34-82 songs per quarter) to 0.21-0.29 from 2023-Q1 on (115-289 songs per quarter). Songs first played in 2020 have love rate 0.71-0.78: the stream log starts 2020-06, so these are largely existing library songs, which is the only reason I can see for a burn-in before the first fold.
- TUNE pair-weight shares by fold: 2023-Q1 0.401, 2023-Q4 0.287 (together 0.69, confirming the W4 reviewer's 68%), the six 2021-2022 folds together 0.13. So the pooled TUNE score is essentially a score on two quarters.
- Date arithmetic for the critic's M12: cutoff minus 90 days lands on the 1st or 2nd day of a quarter for 12 of 14 cutoffs (exactly on a boundary for 2022-04-01 and 2023-04-01), so the newest calendar-quarter group of the rank_plays target is a 1-2 day stub in 12 of 14 folds. Confirmed.

## 2. Diagnosis

1. Almost every number in the models was chosen on TUNE among 30-300 variants, or inherited without test. TUNE's pooled score is dominated by two quarters, and the W4 random-label refits scatter by about 0.04. A one-at-a-time TUNE sweep therefore cannot tell whether "tuning helps": the best of N configurations on TUNE is biased upward by an amount of the same order as any plausible gain.
2. The honest way to ask "does tuning help" is to evaluate the tuning PROCEDURE, not the tuned values: tune inside each fold using only that fold's training streams (inner time-split folds built from train), then score the outer fold. Then TUNE is out-of-sample for the hyper-parameter values, however large the grid, and only the handful of procedures compared on TUNE count as selection (walk-forward measures that). This also gives usable held-out evidence despite LATE and HOLDOUT being partly used.
3. The fold set is a choice with three separate effects: (a) grouping (pairs are only formed within a fold, and pair weights decide which quarters dominate), (b) training staleness (a candidate is scored with a model trained up to its fold's start, 0-3 months stale, plus the 90-day maturity rule that hides the newest training songs, so 3-6 months in total), (c) the start, end and TUNE/LATE split. All quarterly phase shifts and the half-yearly / yearly sets are subsets of monthly cutoffs, so one monthly scoring pass can give all of them if the harness calls the predictor once per distinct cutoff on the union of candidates (valid because scores must be candidate-independent).
4. The label (6 plays / 3 days / 90 days) and the evaluation numbers (session gap 30 min, exposure bucket edges, pooled-pair weighting, baseline half-life 180 d and GBM settings that define best_ref) are also untested choices. W4 showed model scores move by at most 0.02 across four label variants; nobody checked whether model RANKINGS or deltas move, or horizons other than 90 days.
5. Decision threshold: about 80% intervals. The harness prints 80% intervals but grades on 95% bounds / P>=0.8. It needs an explicit 80%-interval grade.

## 3. Decisions

### 3.1 Evaluation (engineer)
- evalkit v5.0: named alternative fold sets restricted to the TUNE era (quarterly phase shifts, monthly, half-yearly, yearly), tried pool only, one predictor call per distinct cutoff on the union of candidates, optional pairing by calendar quarter; score dumps for TUNE-era runs; an inner-fold helper (evalkit.inner) so in-train time-split tuning is standard and leakage-free; an 80%-interval evidence grade; regenerable HOLDOUT budget for round w5r1 (3 runs: one per builder on its pre-declared final); a reference-row subset flag for speed. Default runs must reproduce v4.1 tables exactly. Full spec in the structured result (evaluation_changes).
- Reason for re-opening HOLDOUT: no builder of this workflow has tuned on it, the comparisons here (tuned procedure vs fixed default) are new, and its rows were never used to choose any of the numbers under study. It is reported as "partly used", one run per builder, final pre-declared, never graded. LATE: at most the existing cap; one run on the declared final is expected.
- Primary decision evidence: TUNE with nested (in-train) tuning, 80% intervals of paired deltas, plus walk-forward over the procedures a builder compared. LATE / HOLDOUT are confirmation only.

### 3.2 Shared prep (parallel with the engineer)
Consolidated, memory-mappable MERT store (all 12 layers x 4 windows) and essentia store, plus a small MERT fidelity check (fp32 vs int8, and denser windows) on a seeded sample of dev clips. No large extraction: a full MERT re-extraction is about 5 h at 2 threads and does not fit. Prep does not need the new harness, so prep_after_engineer = false.

### 3.3 Builders (round 1)
1. eval-frame-folds: is the fold set (and the other evaluation numbers) arbitrary? Fixed existing models only, across fold sets, pairings, weightings, labels and baseline settings; recommends a frame with evidence.
2. tune-content-numbers: the content-representation and learner numbers (MERT layers, windows/aggregation, PCA, alpha, missing-audio policy, member weights, essentia settings): sensitivity map + nested in-train tuning vs fixed defaults.
3. tune-signal-numbers: the training-signal and time numbers (target construction incl. the quarter-stub issue, maturity 90 d and partial-horizon targets, recency half-life, window, panel K/P/half-life/min plays, signal weights, retraining staleness): sensitivity map + nested tuning vs fixed defaults.

Tasks 2 and 3 split the inventory by kind of number so they are independent; both use one or more of the three reference recipes as base, copied into their own folder (not imported, because of the cap / wrapper rules).

### 3.4 Handling of method ideas [REMOVED in sanitised copy: mapping of unvetted ideas to tasks]

## 4. Runtime notes (go/no-go)
- Task 1's main job: one multi-fold-set run of baselines + 3 references over 30 monthly TUNE-era cutoffs. Estimate 30-50 min at 2 threads (refs dominate; one fit per cutoff). Go, provided the builder times one cutoff first and drops the heaviest reference from the monthly pass if the estimate exceeds 60 min.
- Tasks 2/3: fast TUNE run 0.5-3 min per file; nested tuning multiplies the per-fold fit cost by (inner folds x configs); with ridge on cached PCA this is seconds per outer fold. Null control 7-14 min; --late / --holdout 2.5-8 min each. Go.
- Shared prep: consolidation 10-20 min; fidelity sample capped at 45 min. Go.

## 5. What I did not do
- I did not re-run any evalkit scoring; all model numbers above come from the sanitised results files. The fold-weight and stub checks are mine (section 1).
- I did not look at any held-out log or table.
