# Engineer round 1: evalkit v4.1 -> v5.0

Start 2026-11-21T18:18:12Z, end 2026-11-21T18:49:45Z+ (TIMING.txt in the scratch folder).

## What changed (code in /home/user/Listener/taste-model/evalkit/)
- New: `folds.py` (fold-set definitions), `inner.py` (inner folds), `holdout_budget.py`, `v41_fast_reference.json` (recorded v4.1 fast TUNE tried_within_group table and VERDICT point values).
- Edited: `run.py` (VERSION v5.0; --folds, --pair-group, --dump-scores, --refs; prepare_alt / split_alt / _alt_main; 80% grade; FILE_DELTAS80; macro qualifying count; version label on every table heading; holdout output change), `metrics.py` (dump_frame / dump_block / dump_sauc / dump_sauc_delta), `selftest.py` (`--v5`, also run at the end of the full selftest), `README.md` (v5.0 section, comparability, commands). data.py and make_decoys.py are NOT touched, so the pool hash and the pool cache are unchanged (no pool or decoy rebuild). Code hash changed because run.py etc. changed (all baseline / reference caches rebuilt once). Nothing under .cache/shared/ or shared-w5r* touched.
- HOLDOUT budget: ran `python3 -m evalkit.holdout_budget --round w5r1 --runs 3` once; .cache/holdout_budget.json = {"round": "w5r1", "remaining": 3}. The module refuses to overwrite a file of the same round.

## Spec items
1. --folds: done for tune, tune_q1 (11 folds), tune_q2 (11), tune_m (30), tune_h (5), tune_y (3). Tried pool only; pools built from data.load_streams() (dev only) without the decoy universe; cached in .cache/evalkit-cache/evalkit-altpools-*.pkl. Efficiency implemented: one predictor call per distinct cutoff on the union of candidates (30 cutoffs for all five sets), then split (selftest: 30 calls; scores equal when a set is scored alone). Tables per set, labelled. --walkforward with exactly one non-default set (tested on tune_h). macro_sauc keeps min_each 10; qualifying count printed (tune_m 13/30, tune_q1 10/11, tune_q2 8/11, tune_h 5/5, tune_y 3/3). Refused with --late/--holdout/--sealed/--null-control. Decision recorded: in alternative-set runs best_ref is the highest point sauc among the references scored on that fold set itself (not fixed from the default TUNE folds), printed and labelled.
2. --pair-group fold|quarter: implemented in the harness (fold column replaced by calendar-quarter label). No-op on the default folds (printed). Selftest: tune with quarter == fold pairing; tune_q1 harness sauc equals a brute-force pooled AUC within calendar quarters and differs from fold pairing. Also on dumps via metrics.dump_sauc(group='quarter'). Refused with --late/--holdout/--sealed/--null-control (my choice; spec silent).
3. --dump-scores PATH: implemented (.pkl or csv[.gz]); columns as specified; score columns are `score__<model>` (prefix needed because diagnostic model names collide with the exposure_before / exposure_after columns). Horizon counts plays_h/days_h for 30/60/180/365 (first play included); assertion that all windows end before DEV_END. Selftest: horizon counts equal plays90/days90 at 90 d and raw streams at all horizons; dump_sauc equals harness sauc and brute force. How to compute sauc with the artist-cluster bootstrap on a dump: README v5.0 item 3 (metrics.dump_sauc / dump_block + Block.stats).
4. inner.py: make_inner_folds / inner_sauc as specified (nboot optional, returns (sauc, lo, hi)). Windows are contiguous, inner_cutoff + spacing + horizon <= cutoff. Selftest: raw loaders disabled during the call and train unchanged; labels equal harness labels from raw dev data for the same songs (love, plays90, days90, share90); a predictor selecting configs with it has independence p90 = 0 and runs under the null control with labels from the null train.
5. 80% grade: lo80_<m> and evidence80_<m> added to VERDICT (sauc, wx, new_artist, wa, gc); TUNE80+/-, SUPPORTED80/NOT80 (synthetic selftest cases), HOLDOUT ungraded with lo80 and P printed. FILE_DELTAS80 table added. README states the 80% decision rule.
6. Done (see above); README documents the fingerprint/exact-copy rule.
7. --refs NAMES|none: done for --fast and --folds runs; for --late/--holdout/--sealed/full default runs it prints a note and forces all three refs (interpretation of "refused (all refs forced)"). With skipped refs best_ref is among scored references and labelled.
8. Housekeeping done; selftest --v5 takes 71 s (47 s inside the full selftest).

## Standing requirements
- Default run reproduces v4.1: fast TUNE tried_within_group (20 rows, all point values and CIs) and VERDICT point values identical to v41_fast_reference.json (asserted in selftest --v5; also checked by hand before editing further).
- Version bumped to v5.0 with README changelog and comparability statement.
- Null seeds differ: existing assertions in the full selftest still pass (full selftest OK).
- Holdout hygiene: removed the pooled DEV+HOLDOUT slice (printed and in the log line) and the scoring of the main folds in a --holdout call; the TUNE best_ref scores are not printed in a --holdout run. This changes --holdout output only (HOLDOUT-ALL/-early/-late numbers are unchanged).
- Not done / could not do: (a) I did NOT run --late or --holdout live (the permission classifier denied a --late run with a temporary --log-dir, and I did not work around it); those code paths are verified only by import, the argument refusal tests, synthetic finish_verdicts cases and code reading. The first real --late or --holdout use should be checked for errors by whoever runs it (budget is 3 for HOLDOUT, so a failed run before the budget line is written costs nothing; the log line and budget unit are written before printing). (b) The default prepare_folds still calls data._load_all() (it needs the full history for the decoy exclusion and has done so since v3); all new v5.0 code uses data.load_streams() only. (c) One run.py invocation right after I deleted stale cache files returned exit code 1 (stderr discarded); repeated runs, including with the baseline cache deleted, returned 0 and I could not reproduce it.

## Runtimes (4 cores shared, 2 threads)
- Fast default run: 13-14 s warm; 65 s with the baseline / reference caches rebuilt (after a code change).
- --fast --folds tune_m,tune_q1,tune_q2,tune_h,tune_y (baselines + shortcuts + all three references, 30 cutoffs): 185 s with caches rebuilt (about 100 s of that is the three references), 22 s warm.
- Full default run (baselines + references, nboot 300, indep check): 69-100 s.
- selftest --v5: 71 s; full selftest: 147 s.

## Current dev baseline scores (harness v5.0, TUNE default folds, full run, nboot 300; sauc [95% CI])
popularity 0.476 [0.43,0.54]; artist_plays 0.619 [0.53,0.65]; artist_recent 0.619 [0.53,0.65]; artist_love_rate 0.543 [0.44,0.64]; duration 0.577 [0.51,0.62]; meta_gbm 0.539 [0.48,0.59]; nonaudio_gbm 0.555 [0.49,0.62]; ref_audio_final 0.632 [0.58,0.67]; ref_w4r1_listening 0.651 [0.61,0.68] (best_ref); ref_w4r1_music 0.646 [0.60,0.68]. Identical to v4.1 point values.
Alternative fold sets (fast, point sauc; all 1074 tried songs scored in every set): best_ref per set tune_m ref_w4r1_listening 0.656 (refs 0.637/0.656/0.655; artist_recent 0.614); tune_q1 ref_w4r1_listening 0.657 (artist_recent 0.608); tune_q2 ref_w4r1_music 0.643 (artist_recent 0.573); tune_h ref_w4r1_music 0.641 (artist_recent 0.604); tune_y artist_recent 0.612 is the best reference (refs 0.591/0.585/0.605).

## Comparability
Every v4.1 default-fold number is comparable (identical). New columns, tables and flags are additions. Alternative fold sets give new numbers (not comparable with default-fold numbers except as sensitivity analysis); CIs of an alternative-set run differ slightly from default-run CIs because of row order (different cluster resamples), point values agree. v4.1 DEV+HOLDOUT pooled numbers no longer exist.

## Failed attempts / deleted code
None kept; temporary patch scripts were removed. Stale cache files of earlier code hashes were deleted from .cache/evalkit-cache/ (regenerable).
