<!-- structured fields -->
start_utc: 2026-11-21T13:10:20Z
end_utc: 2026-11-21T13:51:51Z
late_runs_used: 2
null_control_result: w4r1_final: FLAG, marginal, on sauc only (3-seed null mean 0.529 vs 95% band 0.473-0.529; wa and new-artist inside their bands). Real-minus-null gap +0.122 (CI 0.089-0.171) on sauc, +0.114 on wa (CI 0.027-0.145) and +0.139 on new-artist (CI 0.060-0.222). Per-seed null sauc 0.513/0.549/0.526. Explanation: the content model recovers real structure that the shuffle destroys, and null seed 2 (0.549) is a high draw. The gap is clearly positive and the null mean sits on the band edge, so I do not read it as leakage. Not independently verified: the earlier random-label refits (5 seeds) are in scratch only. Other rows: w4r1_final_noart FLAG (sauc, null mean 0.529, gap +0.088); w4r1_newonly PASS (gap +0.109); w4r1_newonly_noart PASS; w4r1_panelonly and panelonly_noart FLAG on wa (null wa 0.545 and 0.543, band upper 0.533; gaps +0.059 and +0.044, CI includes 0), so the panel-only signal is the weaker one. Baselines: artist_plays, artist_recent, duration and popularity FLAG; artist_love_rate, meta_gbm and nonaudio_gbm PASS.

REPORT: builder round 1 "taste-from-all-listening", second attempt. Timing from TIMING.txt: attempt 1 started 2026-11-21T13:10:20Z, this attempt ran 13:47:20Z to 13:51:51Z of new work on top of attempt 1's files. Total self-reported span 13:10:20Z to 13:51:51Z = 41.5 min, inside the 120 min cap. I stopped because the declared design, the checklist and the extra secondary-model work were complete.

HEADLINE
- Question: does the whole pre-cutoff record give a better content-only taste model than new songs' 90-day outcomes alone?
- Dev: yes, by a small margin. On HOLDOUT, no. Most of the TUNE gain is artist recognition.
- Final model w4r1_final, content only, on MERT features.
  - TUNE sauc 0.651 vs ref_audio_final 0.632.
  - LATE 0.653 vs 0.621.
  - ALL 0.652 vs 0.628. Paired delta +0.024, 95% lower bound +0.004, P 0.99.
- HOLDOUT, run once and not graded: final 0.640 vs ref_audio_final 0.657. Delta -0.017, lower bound -0.058, P 0.16. wa 0.549 vs 0.586.
- With the candidate's own artist removed from the training signal, TUNE falls 0.651 to 0.617. The gain over the new-song-only recipe shrinks from +0.021 to +0.005.
- Duration within artist (wa 0.645 on TUNE) is not beaten on TUNE (final wa 0.629, P(d>0) 0.28).

WHAT THIS ATTEMPT ADDED (new work, all fast TUNE or LATE on a new file; the primary predictor was not touched)
New file: /home/user/Listener/taste-model/predictors/w4r1-taste-from-all-listening/predict_secondary.py. The primary predict.py is unchanged, sha256 9167ad6837b5a29bfe2eefb213f798771e285b5075685f6a8101ee1e1ed5b84b. Secondary models, all reported as secondary:
1. sec_hist_w0.3 and sec_hist_w1: final content score plus w times z-ish log1p(plays by the candidate's primary artist in the last 180 days). This is the combined content-plus-history variant (rule 1 allows it as secondary only). Its history input is exactly what the user's data shows reversing in 2024.
2. sec_cap: content-only. Panel members' PCA components are capped by the number of train songs (128 capped at n/6, 64 capped at n/12), a fix for the sparse early folds that hurt the declared model. It was chosen after seeing the TUNE and HOLDOUT results, so it is a post-hoc variant, not the declared final.

Fast TUNE (nboot 100, one run, 35 s), with sauc / macro / wa / new-artist sauc:
- w4r1_final .651 / .597 / .629 / .667 (from attempt 1)
- sec_hist_w0.3 .668 / .643 / .629 / .667
- sec_hist_w1 .651 / .634 / .629 / .667
- sec_cap .651 / .594 / .594 / .665

One --late run on the secondary file's hash, 1 of 2 allowed, about 4 min. The output is in scratch sec_late1.txt and in the harness late table.
- LATE sauc: sec_hist_w0.3 .557, sec_hist_w1 .495, sec_cap .653.
- LATE reference rows: final .653, ref_audio_final .621, duration .566, artist_recent .440.
- ALL sauc: sec_hist_w0.3 .627, sec_hist_w1 .593, sec_cap .652.
- ALL reference rows: final .652, ref_audio_final .628.
- Finding: adding artist history raises TUNE (+0.017 at w0.3) and collapses LATE (0.557, below ref_audio_final and below final). That matches the earlier observation that artist-history features reversed in 2024. Content-only is the safer model.
- sec_cap is no better than final on TUNE or ALL (.651 / .652), and its wa and macro on TUNE are lower. The early-fold sparsity explanation for the HOLDOUT shortfall is not supported by this one test.
- Total LATE runs for the primary file hash is 1 and for the secondary file hash is 1. No file hash exceeded 2.
- No HOLDOUT was run on the secondary file.

WHAT I BUILT (attempt 1, code in /home/user/Listener/taste-model/predictors/w4r1-taste-from-all-listening/)
- predict.py: harness entry with PREDICTORS w4r1_final, final_noart, newonly, newonly_noart, panelonly and panelonly_noart.
- build_compact.py: builds .cache/w4r1/compact.npz (160 MB, git-ignored, regenerable in 6 s) from the frozen shared MERT/CLAP/essentia caches. It has no fitted transform. I did not modify .cache/shared/.
- Candidate input: only the MERT-v1-95M clip features (4 windows, layers 4-8 averaged) of the candidate's preview. No artist id and no artist history. The listening record is used only to build training targets and weights from streams before the cutoff.
- Training signal, two kinds:
  - "new": the Workflow 3 recipe. Songs first played at least 90 days before the cutoff. Target = percentile of plays in the first 90 days within the quarter of first play.
  - "panel" (new here): each of the last 2 periods of 91 days before the cutoff. Every song, old or new, with at least 2 plays in the period gets target = percentile rank of its plays in that period. Rows are weighted by recency 0.5**(age/180 d).
- Models: weighted ridge on whitened PCA of MERT (PCA fit on train-stream songs only), solved by normal equations. Final = mean of 4 standardised members: new-signal local nc64 a1200, new-signal whole nc32 a150, panel local nc128 a2400, panel whole nc64 a300.
- Missing preview: block is zero and the score is the neutral 0 (ties in the middle). The preview-absent BREAKDOWN row scores 0.500 by construction (35 of 79 loved).
- *_noart variants: exact leave-own-artist-out ridge. The artist's sufficient statistics are subtracted per candidate artist, so the score depends only on the candidate's own artist id. PCA is not refit.
- The fit cache is keyed on hashes of train trackId, song, artist and timestamps, and is bypassed with EVALKIT_NO_FIT_CACHE.
- DECLARATION.txt was written 13:33:08Z, before the first --late run, and the primary file was not changed afterwards.

WHAT I TRIED (fast TUNE, nboot 100, about 85 variants in 14 batches; sauc / wa / new-artist; chance band 0.46-0.54; ref_audio_final .632 / .614 / .614)
- Pipeline check: the W3 recipe reimplemented (w3like_new) gives .630 / .615 / .600.
- Panel signal alone: .595-.635. About 20 panel settings (K, period, half-life, min plays, alpha) were compared on TUNE, so K=2 with min plays 2 is a TUNE selection (optimism).
- Ensemble new + panel(K2, m2): .649 / .609 / .651. Panel with 128 components: .651 / .629 / .667 (chosen). 256 components: .642-.644. 32 components: .632.
- Joint signal in one ridge: .645.
- Failed, code deleted:
  - kNN / Nadaraya-Watson on the same features (.538-.603)
  - unplayed active songs as zero rows (.584)
  - log-count target (.598)
  - retention signal alone (.589), in ensemble (.639)
  - completion filter (.634-.637)
  - artist-demeaned targets (.604-.644)
  - extra CLAP / essentia / lyrics blocks (.611-.648)
  - other MERT layer groups (.618-.643)
  - valid-play filter by playedMs (no change: no streams under 30 s in the loader output)
- Not tried: music-time structure beyond the 4 windows, session co-play embeddings, pairwise ranking losses. Essentia and lyrics blocks were tried only as plain additions, without tuned alphas.
- Final-file ablations on fast TUNE:
  - final .651 / .629 / .667
  - newonly .630 / .615 / .600
  - panelonly .627 / .603 / .673
  - final_noart .617 / .611 / .667
  - newonly_noart .612 / .606 / .600
  - panelonly_noart .583 / .587 / .673

FINAL RESULTS (full harness run, nboot 300, independence on, from the single --late run of the primary file; sauc / macro / wa / gc / new-artist sauc)
- TUNE:
  - w4r1_final .651 / .597 / .629 / .588 / .667
  - ref_audio_final .632 / .609 / .614 / .575 / .614
  - duration .577 / .562 / .645 / .544 / .515
  - artist_recent .619 / .606 / .500 / .601 / .498
  - nonaudio_gbm .555 / .530 / .557 / .560 / .479
  - meta_gbm .539 / .498 / .593 / .535 / .493
  - newonly .630 / .600 / .615 / .574 / .600
  - final_noart .617 / .559 / .611 / .564 / .667
- LATE:
  - final .653 / .637 / .677 / .589 / .675
  - ref_audio_final .621 / .606 / .609 / .571 / .602
  - duration .566, artist_recent .440, nonaudio_gbm .536
  - newonly .610
  - final_noart .659 / .639 / .668 / .587 / .675
  - panelonly .650 (noart .651)
- ALL:
  - final .652 / .609 / .640 / .589 / .670
  - ref_audio_final .628 / .608 / .613 / .573 / .610
  - newonly .623
  - final_noart .632 / .584 / .624 / .572 / .670

HOLDOUT (single run, verbatim from the log, 740 tried songs, 14 folds, not graded; predictor not changed afterwards)
- HOLDOUT-ALL, w4r1_final: sauc .640 (CI 0.561-0.709), macro .658, wa .549, ww .635, ws .598, wx .634, gc .598, gc_wa .536, new-artist .621.
- HOLDOUT-ALL, ref_audio_final: sauc .657, macro .658, wa .586, ww .648, ws .593, wx .648, gc .600, gc_wa .558, new-artist .637.
- Other rows: duration .510 (wa .498), artist_recent .521, nonaudio_gbm .540, meta_gbm .482, newonly .652, final_noart .625.
- Deltas of final vs each reference on HOLDOUT-ALL (d, lo95, P):
  - vs ref_audio_final: sauc -0.017 (-0.058, 0.16); wa -0.037 (-0.104, 0.11); gc -0.002 (-0.035, 0.37); macro -0.001 (-0.081, 0.43)
  - vs duration: sauc +0.130 (+0.038, 0.99); wa +0.051 (-0.140, 0.83); gc +0.077 (-0.002, 0.97); macro +0.167 (+0.063, 1.00)
  - vs artist_recent: sauc +0.119 (-0.028, 0.91); wa +0.049 (P 0.83)
  - vs nonaudio_gbm: sauc +0.100 (-0.012, 0.95)
  - vs meta_gbm: sauc +0.158 (+0.021, 0.99)
- HOLDOUT-early: final .604 vs ref .639 (delta -0.034, P 0.05). HOLDOUT-late: final .682 vs ref .678 (+0.004, P 0.57).
- On HOLDOUT, w4r1_newonly (.652) beat w4r1_final (.640). The log line is in .cache/holdout_runs.log.

PAIRED DELTAS OF FINAL (d, lo95, P(d>0))
- vs ref_audio_final:
  - TUNE: sauc +0.020 (-0.007, 0.92); wa +0.015 (-0.054, 0.65); gc +0.014 (-0.006, 0.90); macro -0.012 (-0.053, 0.31)
  - LATE: sauc +0.032 (-0.003, 0.96); wa +0.068 (-0.010, 0.93); gc +0.019; macro +0.031
  - ALL: sauc +0.024 (+0.004, 0.99); wa +0.027 (-0.024, 0.87); gc +0.016 (+0.001, 0.98); macro +0.001 (-0.032, 0.57)
- vs duration (the wa column is the within-artist comparison):
  - TUNE: sauc +0.075 (+0.022, 1.00); wa -0.016 (-0.074, 0.28); gc +0.044 (+0.004, 0.98)
  - LATE: sauc +0.088 (+0.003, 0.98); wa +0.139 (-0.025, 0.96)
  - ALL: sauc +0.079 (+0.024, 1.00); wa +0.019 (-0.040, 0.70); gc +0.048 (+0.016, 0.99)
- ALL sauc lower bound / P vs every harness row:
  - popularity .090/1.00
  - artist_plays .035/.993
  - artist_recent .038/.993
  - artist_love_rate .057/1.00
  - duration .024/.997
  - meta_gbm .059/1.00
  - nonaudio_gbm .038/1.00
  - has_preview .134/1.00
  - preview_source_itunes .107/1.00
  - ref_audio_final .004/.993
  - pool_artist_siblings -.009/.957
  - pool_album_siblings .042/1.00
  - exposure_before -.004/.967
  - Within-artist P vs artist_recent and vs pool_artist_siblings: 1.00 (artist_recent wa is 0.5 by construction).
  - TUNE vs artist_recent sauc +0.032 (-0.013, 0.93).
- The harness evidence grade vs best_ref is in .cache/late_tables/9167ad68...5d5.txt. I did not copy it here.

BREAKDOWN rows for w4r1_final (TUNE sauc; ref_audio_final in brackets)
- By fold: 2021-07 .494 [.374]; 2021-10 .492 [.524]; 2022-01 .564 [.644]; 2022-04 .535 [.566]; 2022-07 .587 [.604]; 2022-10 .577 [.553]; 2023-01 .667 [.637]; 2023-04 .588 [.627]; 2023-07 .695 [.693]; 2023-10 .666 [.629].
  - Mean of the first 6 folds .541 vs ref .544; last 4 .654 vs .646.
- New artist .667 [.59-.74] (89 of 377 loved; ref .614). Known artist .632 (253 of 697 loved; ref .625).
- exposure_before 0 / 1-2 / 3-8 / 9+: .615 / .672 / .641 / .782 (ref .593 / .669 / .633 / .718).
- Tercile of plays in the song's 90-day window, low / mid / high: .567 / .672 / .671 (ref .601 / .642 / .631). The model is weaker than ref when the user listens little.
- Release age <3m .714, 3-12m .429, 1-3y .732, >3y .657 (counts 6/19, 8/18, 9/50, 319/987).
- Preview present .663 (307 of 995 loved); absent .500 (35 of 79; neutral by construction).

OPEN POOL, primary (Spotify-preview subset, TUNE; 679 tried / 4601 decoys)
- w4r1_final: open_sauc all .736 (.656-.776), new .719, known .736, open_wa .604 (.424-.813), p20 .155 (.05-.268).
- ref_audio_final: .705 / .675 / .707 / .502 / p20 .115.
- artist_recent: .738, p20 .260.
- Both preview shortcuts score exactly .500 on this table.
- Open-pool deltas vs references are in the late table.
- Independence p90: 0.0.

ARTIST-RECOGNITION CHECKS (rule 2)
- TUNE: final .651 to .617 when own-artist training songs are removed; wa .629 to .611; new-artist unchanged at .667 (new artists have no train songs); newonly .630 to .612; panelonly .627 to .583. About 0.034 of final's TUNE sauc comes from the candidate's own artist's training songs.
- The final-minus-newonly gap is +0.021 with the artist and +0.005 without. ALL: final .652 to .632; gap +0.029 to +0.018. LATE: noart .659, no drop.
- The one gain not tied to own-artist: new-artist sauc .667 vs ref .614 and newonly .600 on 377 TUNE songs (CI .59-.74); LATE .675 vs .602. On HOLDOUT-ALL, new-artist .621 vs ref .637, so it did not replicate there.

BELOW-CHANCE ITEMS (investigated)
- w4r1_panelonly_noart, fold 2022-04: AUC 0.294 (CI upper 0.450; 12 of 31 loved). The panel pool is small in the 2022 folds (141 songs at 2021-10, 199 at 2022-04, 222 at 2022-07, vs 555 at 2023-10). A 128-component ridge on about 200 songs, minus the candidate's artist, leaves little to fit. panelonly with artist in that fold is .430 and final .535.
  - I read this as small-sample overfit in sparse early periods, not systematic inversion.
  - This attempt's sec_cap test (capping components by song count) did not improve TUNE or HOLDOUT-relevant scores, so the explanation is not confirmed. It remains a belief.
- Harness shortcuts has_preview (2023-10, 2024-01), preview_source_itunes (2023-10) and meta_gbm fold 2022-04 (.333) are below chance and not mine. has_preview is below .5 because tried songs without a preview are loved more often (44% vs 31%).
- sec_hist_w1 on LATE is 0.495, at chance. This is the known artist-history reversal in 2024, and the reason history is kept out of the primary.

STRONGEST CASE AGAINST MY RESULT
1. HOLDOUT, the only artist-disjoint look that was never tuned on, says final is no better than ref_audio_final (-0.017, P 0.16). newonly beat final there. The dev gain is within what selection on TUNE would produce (about 85 variants and 20 panel settings, with K2 m2 picked from them).
2. The gain over the new-song-only recipe is mostly own-artist information (+0.005 without it). The user's goal is new music, so artist recognition is what the project wanted to avoid.
3. Macro AUC is not better than ref (-0.012 TUNE, +0.001 ALL). The gain lives in the larger late folds.
4. LATE is partly used up by earlier workflows.
5. Duration within artist (.645 TUNE) is not beaten on TUNE.
6. The panel members do worse than newonly in low-activity periods (tercile T1 .567 vs ref .601) and in sparse early folds.
7. New: adding history to get a higher TUNE score (0.668) fails on LATE (0.557), a reminder that TUNE gains from artist-linked signals are not trustworthy.

WHAT I ACTUALLY RAN, with runtimes
- Attempt 1:
  - 14 fast TUNE batches, 25-85 s each
  - the primary file fast run, 50 s
  - the primary --late run, 202 s (this is also the nboot-300 TUNE run, so there was no separate full run)
  - --null-control, 3 seeds, about 4 min
  - random-label refits, 5 seeds, 79 s
  - --holdout once, 191 s
  - build_compact.py, 6 s
- This attempt:
  - fast TUNE on predict_secondary.py, 35 s
  - one --late on the secondary file hash, about 4 min
  - no HOLDOUT on the secondary file
- No job exceeded 10 minutes, so no runtime estimate or go/no-go was needed.
- I never touched sealed data, PLAN.md or git history. I used evalkit loaders only (load_streams with until dates before the cutoffs, for a panel-size count).
- Folder state: predictors/w4r1-taste-from-all-listening/ has predict.py, predict_secondary.py and build_compact.py. Failed-attempt code was deleted from the project; copies are in my scratch folder only. .cache/w4r1/compact.npz is git-ignored and regenerable.

WHAT I ONLY BELIEVE (untested)
- That the HOLDOUT shortfall is selection noise on TUNE. The sparsity explanation was not supported by the sec_cap test, which showed no gain.
- That tuned alphas for the CLAP / essentia / lyrics blocks could add a little. I only tried plain additions.
- That the null-control sauc FLAG is a high draw in one seed (0.549) plus real structure, not leakage. The gap CI is clearly positive.