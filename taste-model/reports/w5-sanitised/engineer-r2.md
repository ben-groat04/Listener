# Engineer round 2: evalkit v5.0 -> v5.1 (report)

Changed: evalkit/run.py, metrics.py, selftest.py, README.md; new: evalkit/selftest_builder.py (3 cheap deterministic models for tests), evalkit/v50_fast_reference.json. data.py, make_decoys, pools, decoys, .cache/shared, shared-w5r* untouched. No held-out run, no budget change.

## Implemented
1. metrics.fold_meta(dump, fold_set, model_a, model_b, label, nboot=400, seed=0) + metrics.iv_meta. IV mean with 80% interval, Q/df/p, I2, DL tau, IV-weighted trend per year of cutoff (SE, 80%), per-fold table, n_excluded (<5 pos or <5 neg, or zero SE). FOLD_META table (sauc only) printed in every TUNE-era run (default, --folds; also the TUNE slice of --late; not --holdout/--sealed) for each builder model vs best_ref, artist_recent, and the --best-ref reference (duplicates dropped).
2. --best-ref NAME: fixes best_ref in VERDICT/FOLD_META (default and every --folds set); FILE_DELTAS80 gets extra rows model-vs-reference when given. Refused with --late/--holdout/--sealed/--null-control and for unknown names. Alternative-set runs always print "FIXED COMPARATOR" (sauc delta, 80%, decision80 vs ref_w4r1_listening).
3. FILE_DELTAS80: 1000 resamples, fixed seed 20260511 (also --fast, independent of --nboot); decision80 column; README states |lo80| < 0.005 is undecided.
4. HOLDOUT: budget file untouched (w5r1, 0); --holdout refused (selftest asserts file content and the REFUSED exit). README says exhausted for this workflow. LATE caps unchanged.
5. Dumps: first_play_date column; selftest asserts fold_set='tune' labelling for a --folds tune,tune_h run.
6. README v5.1 section + comparability; VERSION v5.1; code hash changed (selftest_builder.py excluded from hash like selftest.py). selftest --v51 added and called by the full selftest.

## Reference recorded before editing
v5.0 fast default run (baselines only, and with the test builder): tried_within_group (20 rows baselines-only; 23 with builder) and VERDICT point values, plus FILE_DELTAS80 point deltas, stored in evalkit/v50_fast_reference.json and asserted in selftest --v51: identical under v5.1.
Also compared by hand: v5.0 `--fast --folds tune_h,tune_y` text saved in scratch (v50_alt_hy.txt); not asserted in selftest.

## Verified (actually run)
- selftest --v51: pass (98 s warm; 140 s on first run after the code change). Full selftest: pass, 197 s (incl. v5.1 checks 41 s with warm caches; null-control 3-seed-differs assertion still in and passing).
- fold_meta deltas equal sklearn AUC differences (<1e-12) on both dump fold sets; synthetic homogeneous: Q/df 0.91 (mean over 1500 simulations 1.00).
- Runtimes: fast default run with builder 17 s warm (64 s first after code change); 6-set --fast --folds tune,tune_q1,tune_q2,tune_m,tune_h,tune_y --best-ref ref_w4r1_listening with builder 143 s (builder scored on 30 cutoffs, not cached); full default baselines-only run (nboot 300, dev only) 71 s.

## Dev baselines (harness v5.1, TUNE, tried_within_group sauc [95% CI]; identical to v5.0)
popularity 0.476, artist_plays 0.619, artist_recent 0.619, artist_love_rate 0.543, duration 0.577, meta_gbm 0.539, nonaudio_gbm 0.555, has_preview 0.476, preview_source_itunes 0.482, ref_audio_final 0.632, ref_w4r1_listening 0.651 (best_ref), ref_w4r1_music 0.646. Full table: scratch baselines_full.txt.

## Comparability
Default output unchanged (asserted). Only changed existing numbers: 80% bounds and P inside FILE_DELTAS80 (1000 fixed-seed resamples); its point deltas are identical. Everything else added.

## Not done / caveats
- FILE_DELTAS80 has no reference in its definition (pairs of builder models); I interpreted "fixes the reference for FILE_DELTAS80" as extra model-vs-fixed-reference rows under --best-ref.
- FOLD_META prints the summary only; per-fold tables come from metrics.fold_meta on a dump.
- --late runs print FOLD_META for the TUNE slice only.
