# Devil's advocate r2 (dismissed direction): music-recipe-numbers

## Per-claim verification (what I re-ran)
Re-ran on fast TUNE: chunk_0-5.py (82 variants + default), procs_main.py (avg81 + 4 selectors), final.py full TUNE run (nboot 300), null control (5 seeds), analyse_grid.py, analyse_missing.py. Used 2 threads; member score caches in .cache/w5r2-... were reused (so these re-runs check the harness/analysis path, not the member fits from scratch). Did NOT re-run the 20 random-label refits (about 25 min of compute) - numbers re-derived from null_deltas.csv only. Did not run --late/--holdout; the LATE claim is not assessed here beyond reading the report.

| # | verdict | evidence |
|---|---|---|
| 1 | holds | per-fold Spearman default vs ref_w4r1_music 1.0 (0.99999 on 2023-07-01); pooled sauc 0.6465 both; paired delta 0.0 |
| 2 | holds | my grid_table identical to builder's (max abs diff 0.0): POS 0, NEG 8, UNDECIDED 74 |
| 3 | does not hold as worded | All 8 NEG are low-fill variants (oat_fill_1, oat_mfill_1 = MERT-only low fill, joint_00/02/10/17/37/38). Dropping MERT (oat_wm_0, -0.023 [-0.0385,-0.0016]) is UNDECIDED under the rule (hi80 > -0.005), not one of the 8. Stats for the 64 no-fill variants hold (mean -0.0024, sd 0.0036, max +0.0034). Also: 50 of 64 are negative, 27 of 35 OAT no-fill/no-MERT-drop moves negative |
| 4 | holds | max |delta| of the 35 other OAT moves = 0.0073; wm 0 = -0.0230 [-0.0385,-0.0016] |
| 5 | numbers hold, reading weak | from null_deltas.csv: best-of-64 median +0.0167, range +0.008..+0.061; null sd median 0.0066, above 0.0036 in 20/20. But the null is models trained on random targets scored on real labels, so it measures instability of noise models, not selection noise of real-trained variants; it cannot calibrate the grid. Builder says so itself. Not re-run |
| 6 | holds | sel_m005 -0.0055 [-0.0125,+0.0028], sel_pen003 -0.0044 [-0.0093,+0.0003], sel_m010 +0.0003, sel_m020 0; reproduced. Non-default chosen at 1 of 10 cutoffs for m010 (2022-10, oat_seg_2), 5 for m005, 5 for pen003. Selection is also uninformative by design: the first 5 cutoffs always fall back to default, inner folds are 3 months with few loved songs, and only 4 of them |
| 7 | holds | avg81 -0.0009 [-0.0032,+0.0017]; full run -0.001 [-0.004,+0.002] (mine) |
| 8 | holds (not re-run) | walkforward output read: composite 0.644, about -0.0025 vs default, P 0.31 |
| 9 | holds, with caveat | altfolds_output.txt shows -0.001/-0.002 UNDECIDED in all five sets; the same songs and same data in every set, so no replication |
| 10 | holds | analyse_missing.py re-run: output identical (261 missing = 240 no URL + 21 no clip; love 0.375 / 0.298) |
| 11 | numbers hold; "concentrated in 2023" not supported | +0.0192 [+0.0011,+0.0381] reproduced. But the per-fold meta of the same gain is homogeneous (Q 8.1/8, I2 0.01, trend +0.017/yr [-0.011,+0.045]); fold deltas in 2023 are +0.034, +0.026, -0.044, +0.029 and 2021-10 is +0.110. 71% of rows are in 2023, so "2023 only" is largely sample size. The love-rate gap (missing vs audio) is 2023-only, true |
| 12 | holds | indicator alone 0.5445 / wa 0.5453 / wx 0.532 reproduced. Its own 80% interval for sauc is [0.519,0.570], lo80 above 0.5 |
| 13 | does not hold | has_preview = 0.500 in open_love is by construction: the primary open pool is defined as the subset where BOTH tried songs and decoys have Spotify-CDN previews (README, run.py open_pool), so the baseline is constant whatever the catalogue. It says nothing about whether candidates lack audio. The recommendation may still be reasonable, the evidence is not |
| 14 | holds | my full run: sauc 0.646 [0.598,0.677]; vs ref_w4r1_music -0.001 [-0.004,+0.002]; vs ref_audio_final +0.014 [+0.001,+0.028]; vs ref_w4r1_listening -0.006 [-0.028,+0.018]; vs artist_recent +0.027 [-0.001,+0.077] (bootstrap seed differences only) |
| 15 | holds | +0.002 [-0.027,+0.060], P 0.64 (builder +0.002 [-0.025,+0.062], 0.67) |
| 16 | holds, caveat | my null control reproduces the per-seed numbers exactly (avg 0.529; per-seed 0.457-0.576; cluster-band (0.497,0.580) PASS). The song-level band FLAGs it; the PASS rests on a wide band, and the per-seed spread of 0.12 means the control has little power to detect a 0.02 leak |
| 17 | holds | the builder's own caveat is accurate; I add that the grid is biased toward the default (see below) |

## Attacks (dismissal direction)
1. The paired test is stacked in favour of the default. The default was tuned in earlier workflows on this same TUNE data. 50 of 64 no-fill variants are below it and the 82-variant mean is negative; this is the signature of a selected optimum (regression to the mean), not evidence that the neighbourhood is flat. "Nothing beats the default on TUNE" cannot show "the numbers do not matter". The only unbiased check would be data not used to choose the default, and LATE (partly used) / HOLDOUT (spent) do not provide it; this limitation is not stated in the report.
2. Many recipe numbers were never varied, although the task is about the arbitrary numbers of the recipe: the MERT members' PCA components (64/32), ridge alphas (1200/150), layer ranges and whole/local mode, the 90-day plays window, the quarter-rank target, the 90-day maturity gap, the 1%/99% percentile fill anchors, the clip-mean vs 5-s segment structure. The builder reassigned target/time numbers to another task, but MERT member hyperparameters are not in anyone's scope in the report. "Numbers do not matter" is therefore only shown for the essentia ridge, GBM, blend weights, clip eps and a few segments.
3. The missing-audio fill is tried with only three constants. Not tried: a fill learned from the training data (love/plays rate of missing-audio songs in train, which is time-honest), or an indicator feature in the model. The best joint (+0.022, joint_33) and fill high (+0.019) are the only moves with lo80 > 0. Sub-analyses give lo80 above the harness margin (new-artist rows +0.038 [+0.007,+0.074]; excluding top-3 artists +0.032 [+0.010,+0.057]), yet the whole is called UNDECIDED and then dropped from the final on reasoning alone. With a plain 80% threshold (lo80 > 0) the fill-high move is POS. The report's catalogue-artefact reasoning (item 13) rests on a wrong inference.
4. avg81 ties the default by construction: its 81 members span only 3 levels of 4 parameters (eps, alpha, GBM size, MERT weight) that single moves showed to be worth under 0.005 each, and all members share the same default blend, fill and segment structure. The tie is expected and is not evidence about the numbers either way.
5. The selection experiment has little power to find improvement: 4 short inner folds, first 5 of 10 cutoffs forced to default, and a family from which fill moves are excluded (the only moves that mattered). Negative results are specific to this design (builder says this too).
6. The random-label calibration measures the wrong thing (see claim 5). A better null: real-trained variants, test labels permuted within artist blocks.
7. Possible harness issue (not tested): the v5.0 reference file mtime (21:57) is later than metrics.py edit (21:55), so I cannot confirm the reference was recorded strictly before editing. The additions were additive, and my TUNE reproduction of builder numbers is exact, so no effect on this builder.

## Checklist re-check (code / files)
fast_mode: grid, procedures, walkforward, alt-fold runs all --fast per times.txt and outputs (first line "fast=True"); full run and null control non-fast, single --late. OK.
full_run_final_scores: matches my re-run. OK.
held_out_slices_reported_separately: LATE numbers appear only in a separate report section; summary and claims given to me carry none. HOLDOUT budget file {"round":"w5r1","remaining":0}. OK.
null_control: re-run, identical. OK (caveat above).
paired_baselines incl artist_siblings and artist_recent: present (items 14, 15). OK.
below_chance: has_preview 0.476 explained by tried-song effect; plausible.
variants_counted_and_selection_accounted: counts verified (82 + default; 57 select configs; 81 family; 4 selectors). The selection of the final family was declared before scoring per the report; I cannot check ordering beyond file mtimes (grid.py 22:14, chunks 22:15, results after).
strongest_case_against: present; misses attack 1 (default is the tuned optimum on this data), 2 and 3.
runtime estimates/actuals: TIMING.txt 22:12:22 to 22:58:50 = 46.5 min of a 90 min cap, consistent with file mtimes (code 22:13-22:44, results copied 22:57). Reported "about 50 min" OK. Reported jobs match times.txt.
code_behind_every_reported_score_kept: all scripts present and regenerate the numbers I re-ran; walkforward/alt-fold command lines are not written down in the folder (only outputs).
ran_vs_believed: fair, except item 13 inference.

## Shared inputs
.cache/shared-w5r1/ has DONE; sha256 of README.md, essentia_compact.npz, essentia_meta.json, fidelity_sample.npz, mert_full.npy, mert_layer_mean.npy, mert_md5.npy all match MANIFEST.txt. The recipe also reads .cache/w4r1-what-in-the-music/compact.npz (not a shared dir, no manifest, not checked). Nothing under .cache/shared/ used directly by builder code.

## Engineer vs spec (read, partly run)
Present in code: fold_meta (metrics.py 304), iv_meta, --best-ref refused with late/holdout/sealed/null-control (run.py 1018), FILE_DELTAS80 nboot 1000 seed 20260511 with decision80 (DEC_EPS 0.005), FIXED COMPARATOR table, first_play_date dump column, VERSION v5.1, holdout budget untouched (remaining 0). I did not run selftest --v51 or the full selftest. Note: fold_meta uses 400 bootstrap resamples per fold; with folds at 35-80 rows the per-fold SE is noisy, and folds with SE <= 0 or fewer than 5 per class are dropped (5 dropped for sel_pen003).

Time: start 2026-11-21T23:22:49Z.
