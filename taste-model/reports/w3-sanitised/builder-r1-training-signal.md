REPORT w3r1 "training-signal" (builder, round 1)

HEADLINE
- On TUNE the final predictor beats nonaudio_gbm clearly, and the training-signal and history-window changes explain most of the gain. On LATE (held-out dev) it does NOT hold up, and the artist_recent member (weight 2) hurts there. The null control FAILS for the final predictor. The learned part alone passes the null control and is no better than nonaudio_gbm on LATE.
- All gains on TUNE come with an unconstrained search over about 300 variants on TUNE. Treat the TUNE numbers as optimistic.

CODE (all in /home/user/Listener/taste-model/predictors/w3r1-training-signal/)
- predict.py: harness entry point. PREDICTORS = w3r1_final, w3r1_noaudio, w3r1_learned_only, w3r1_final_lovetarget.
- core.py: training rows, targets, weights, models, blends.
- feats.py: extra and audio features.
- build_clap.py: CLAP embeddings of the shared previews -> /home/user/Listener/taste-model/.cache/shared/w3r1-clap/emb.npz (15 MB, regenerable, one embedding per preview, no fitted transform).
- variants_{targets,exposure,time,window,rep,capacity,exposure2,blend,blend2,audio}.py: the stage comparisons.
- audit.py: leakage audit.
- diag_flip.py: diagnostic only, not a predictor.
- Logs are in /tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf3/w3r1/final/. Stage summaries: all_summary.txt. Full TUNE run: full_tune.log. Null control: null.log and null2.log. LATE run: late.log.

FINAL PREDICTOR (w3r1_final)
Score = standardised sum of three members. Standardisation uses mean and std of each member's predictions on the TRAINING rows, so it is candidate independent. The independence check passed (indep_p90 = 0.0).
1. HistGradientBoosting (60 iterations) on evalkit's nonaudio feature set (metadata + point-in-time artist history).
2. The same plus 5 CLAP audio features from the shared previews:
   - au_pos3 / au_neg3: mean of the 3 largest cosine similarities to loved / dismissed songs that matured before the song's first play, within the last 450 days.
   - au_cent60 / au_cent365: cosine similarity to the play-weighted centroid of everything played in the last 60 / 365 days.
   - au_missing: no-preview flag. Songs with no preview or embedding get NaN features, which HGB handles natively. The no-preview rate is about 13-18% of tried songs; this was not separately measured.
3. Two times the plain statistic artist_recent, standardised.
Members 1 and 2 are trained on a graded, period-normalised target: rank_plays, the percentile of plays90 within the quarter of the song's first play. Training rows are songs first played in the last 365 days before the cutoff (the window widens to at least 250 songs in the earliest folds) with a 120-day half-life recency weight. All baseline monotone constraints are kept; extras are constrained too.

WHAT I RAN (all via evalkit.run; stages used --fast on TUNE)
- Stage logs for the comparisons below.
- Full TUNE run: `python3 -W ignore -m evalkit.run predict.py`, nboot 300, independence on.
- `--null-control`: run twice. The second run added w3r1_learned_only to predict.py. Results below.
- `--late`: exactly one run. It also prints the full TUNE table; those numbers match the earlier TUNE run. The log line is in .cache/late_runs.log, sha256 04e41ef3...514e.
- Nothing sealed was touched. I never opened raw streams, PLAN.md or .sealed. The only stream access was through evalkit's loaders.
- CPU: at most 2 threads. The CLAP build used 1 thread for about 75 minutes.

COMPARISON TABLES (TUNE, --fast; sauc / wa / ww / ws / new-artist sauc)
Reference: nonaudio_gbm .557 / .540 / .553 / .535 / .473. artist_recent .619 / .500 / .602 / .590 / .502.
Within-group CIs are about +-0.04 or wider. Differences under about 0.02 are noise. Paired dSAUC lower bound vs nonaudio_gbm is in the last column where noted.

Stage 1: target, with the representation fixed (nonaudio features), all history, 180-day half-life weighting. Mostly the same table as the rest, so differences are small.
| target | sauc | wa | ww | ws | new |
|---|---|---|---|---|---|
| love 6/3 (= nonaudio_gbm exactly) | .557 | .540 | .553 | .535 | .473 |
| love 4/2 | .581 | .569 | .563 | .549 | .542 |
| love 10/4 | .565 | .563 | .566 | .523 | .462 |
| strong 15/5 | .569 | .571 | .575 | .558 | .460 |
| plays >= 2 | .562 | .534 | .554 | .485 | .521 |
| log plays90 | .581 | .581 | .564 | .519 | .496 |
| log days90 | .569 | .567 | .555 | .506 | .492 |
| log share90 (volume normalised) | .575 | .573 | .565 | .513 | .500 |
| grade 0-4 | .579 | .559 | .563 | .508 | .526 |
| rank_share (percentile of share90 within quarter) | .593 | .564 | .565 | .497 | .548 |
| rank_plays (percentile of plays90 within quarter) | .598 | .579 | .579 | .522 | .542 |
| love + share | .579 | .563 | .567 | .514 | .542 |
Finding: every graded or volume-normalised target beats binary love 6/3 by +0.02 to +0.04 sauc on the same features. The paired lower bounds vs nonaudio_gbm are about 0, so this is suggestive, not significant.

Stage 2: exposure context of HISTORY songs (number of new songs in the session of the first play, computed from train streams only)
- Run on a binary love target and the rank_plays target, with window 365 and half-life 120. Details are in exposure2 in all_summary.txt.
- Methods:
  - Weight each row by 1/nnew^a.
  - Drop rows from sessions with more than 5 new songs.
  - Keep only sole-new songs.
  - Residualise the target on log(nnew) after quarter fixed effects.
  - Marginalise: add nnew as a training feature, then average predictions over the training nnew distribution.
- GBM rank_plays results (sauc / wa / ww / ws / new):
  - none: .636 / .602 / .617 / .591 / .565
  - w0.5: .634 / .594 / .620 / .582 / .588
  - w1: .623 / .591 / .614 / .587 / .569
  - drop5: .627 / .596 / .624 / .598 / .569
  - sole: .605 / .524 / .617 / .595 / .588
  - resid: .644 / .611 / .617 / .574 / .544
  - marg: .638 / .611 / .618 / .571 / .545
- Training only on sole-new songs hurts (too few rows).
- Differences among the other methods are within +-0.01 to 0.02, i.e. noise. Exposure handling does not materially help.
- Binary love target: the same ordering, also within noise.

Stage 3: history length / recency (all rows, GBM), sauc
- Binary love target:
  - half-life none .525
  - 60 d .583
  - 120 d .564
  - 180 d .557
  - 365 d .542
  - 730 d .532
  - window 365 d .605
  - window 730 d .568
  - window 1095 d .560
  - skip first 120 days of data .569
  - no monotone constraints .511
- rank_plays target:
  - half-life none .583
  - 60 d .607
  - 120 d .602
  - 365 d .594
  - 730 d .593
  - window 365 d .626
  - window 730 d .608
  - window 1095 d .600
  - skip first 120 days .597
  - no monotone constraints .576
Finding: the least stationary, most recent data is best. Hard windows of 180-365 days beat decay-only weighting. The very old listening (2020-2022) helps only as down-weighted data. Removing the monotone constraints is clearly bad on TUNE. This is the biggest lever: baseline .557 -> about .62-.63.

Stage 4: window x half-life x target (min 250 rows). Windows 180-365 all give sauc .60-.63 regardless of target; 450 is slightly worse. Example rows for rank_plays: window 180 / hl none .634; 270 / 120 .627; 365 / 120 .625; 450 / 120 .619.

Stage 5: representation additions (window 365, hl 120)
- Extra artist/album/relative-meta features ("plus"): rank_plays .625 -> .572, binary love .599 -> .563. Worse with about 600 training rows, so I dropped them from the final predictor.

Stage 6: model capacity
- 60-iteration GBM: .636. 4 leaves: .633. min_samples_leaf 80: .626.
- Ridge: .611-.628, with wa only .52-.54.
- Capacity matters little; smaller GBM is marginally best.

Pairwise / within-context comparison
- Group-demeaned regression: by quarter .595, week .590, session .580, artist .513 (all full history, log-plays target).
- LambdaRank: quarter .553, week .568, session .591, artist .467.
- None of these beat the pointwise graded target.
- Reading: the information is in absolute engagement plus recency. Within-session grouping kills wa (.50).

Stage 8-9: blends and shrinkage
- Blends of targets or model types add +0.00 to +0.01.
- Blending with the standardised artist_recent ("listening statistics") gives ~.644 (m_gbm+ar1: sauc .644, wa .602, new .565, share90 Spearman .260).

Stage 10: audio features added to base (window 365, hl 120, GBM, rank_plays)
- Without audio: .636 / .602 / .617 / .591 / .565.
- With audio: .647 / .579 / .636 / .611 / .599.
- Audio also helps the volume-normalised target. It helps new-artist and between-artist ranking by +0.01 to +0.03 and lowers wa. Within noise individually.
- Final blend (rank_plays GBM, audio GBM, 2 x artist_recent): .650 / .594 / .633 / .627 / .588.

FINAL TABLES (full runs, nboot 300; 95% CI in brackets)

TUNE (10 folds; permutation band sauc (0.459, 0.537), wa (0.448, 0.552), ww (0.459, 0.538), ws (0.428, 0.577), new (0.422, 0.558)):
| model | sauc | wa | ww | ws | new | plift | Spearman share90 |
|---|---|---|---|---|---|---|---|
| w3r1_final | .650 (.583,.694) | .594 (.533,.631) | .633 (.559,.693) | .627 (.508,.707) | .588 (.512,.655) | 1.403 (1.119,1.703) | .261 |
| w3r1_noaudio | .644 | .602 | .624 | .603 | .565 | 1.469 | .260 |
| w3r1_learned_only | .646 (.585,.691) | .594 | .630 | .611 | .588 | 1.403 | .206 |
| w3r1_final_lovetarget | .624 | .561 | .609 | .575 | .503 | 1.294 | .248 |
| nonaudio_gbm | .557 (.512,.604) | .540 | .553 | .535 | .473 | 1.162 | .095 |
| artist_recent | .619 (.550,.653) | .500 | .602 | .590 | .502 | 1.386 | .226 |
- No CIs are printed by the harness for Spearman share90.
- Paired delta lower bounds for w3r1_final (95%, point delta in brackets):
  - vs nonaudio_gbm: sauc +0.042 (point +0.093). wa -0.011 (point +0.054, not significant).
  - vs meta_gbm: sauc +0.073.
  - vs artist_recent: sauc +0.011 (point +0.031).
  - vs pool_artist_siblings (diagnostic): sauc -0.015.
- Open pool, TUNE: open_sauc .781 (.711,.831), new-artist .592, known .848, open_wa .670 (.590,.737), p20 .360. For comparison: nonaudio_gbm .600 / .140; artist_recent .749 / p20 .371.
- Open dSAUC lower bound: vs nonaudio_gbm +0.123; vs artist_recent +0.014; vs pool_artist_siblings +0.024.
- Open-pool gains are mostly familiarity; the tried-vs-untried comparison is confounded by decoy construction.

LATE (4 folds, held out; band sauc (0.456, 0.550), wa (0.451, 0.565), ww (0.440, 0.544), ws (0.424, 0.571), new (0.394, 0.592)):
| model | sauc | wa | ww | ws | new | plift | Spearman share90 |
|---|---|---|---|---|---|---|---|
| w3r1_final | .491 (.423,.559) | .539 (.482,.607) | .549 (.465,.615) | .561 (.419,.653) | .592 (.479,.686) | 0.937 | .027 |
| w3r1_noaudio | .478 | .515 | .539 | .556 | .637 | 1.026 | .016 |
| w3r1_learned_only | .532 (.478,.591) | .542 | .566 | .570 | .597 | 1.294 | .087 |
| w3r1_final_lovetarget | .497 | .559 | .566 | .585 | .600 | 0.848 | .028 |
| nonaudio_gbm | .534 (.483,.583) | .551 | .582 | .561 | .632 | 0.937 | .072 |
| artist_recent | .436 (.375,.511) | .496 | .490 | .494 | .485 | 0.653 | -.051 |
| meta_gbm | .558 | .528 | .566 | .538 | .633 | n/a | n/a |
- Paired lower bounds for w3r1_final (point delta in brackets):
  - vs nonaudio_gbm: sauc -0.096. wa -0.076.
  - vs meta_gbm: -0.128.
  - vs artist_recent: sauc +0.019 (point +0.055).
  - vs pool_artist_siblings: -0.138.
- w3r1_learned_only: vs nonaudio_gbm sauc -0.045, wa -0.071; vs artist_recent sauc +0.022.
- Open pool, LATE: open_sauc final .682 (.614,.756), open_wa .656, p20 .163. artist_recent .641 / p20 .142; nonaudio_gbm .587 / p20 .087. learned_only .642 / .656 / .125.
- Open dSAUC lower bound vs nonaudio_gbm: final +0.038; vs artist_recent: final -0.012.
- Summary: on LATE the final is not above chance on sauc (band lower edge .456, point .491) and loses to nonaudio_gbm and meta_gbm. It is above artist_recent only because artist_recent is itself reversed on LATE.

NULL CONTROL
- First run (final, noaudio, lovetarget): sauc .575, .573, .557. All FAIL (band upper edge .537).
- The failure comes from the artist_recent member. artist_recent and artist_plays themselves score .602 and .595 under the control, because the identity shuffle keeps per-artist counts, so any familiarity-statistic score fails the strict check by construction (the engineer noted this).
- The learned part passes: w3r1_learned_only gets sauc .504 under the control, PASS (second run). nonaudio_gbm gets .496.
- Conclusion for the report: final = FAIL in the literal check. I attribute it to artist_recent and show the learned part is clean.
- w3r1_final_lovetarget also fails, for the same artist_recent reason.

BELOW CHANCE
- LATE per-fold AUC, w3r1_final: 2024-10 is .382, flagged by my own reading (the CI includes values below .5). 2024-01 is .468. artist_recent: 2024-10 .345, 2024-01 .433; artist_plays 2024-04 .407 is flagged by the harness.
- popularity 2023-04 .403 is flagged in ALL.
- Cause: the familiarity -> love relation reversed in the LATE era. On LATE folds new-artist tried songs are loved more often (30%) than known-artist ones (21%); on TUNE it was 23% vs 35%.
- diag_flip.py shows the signal is already fading in the pre-cutoff training window. Love rate of matured songs in the last 365 days before the cutoff, by familiarity tercile (low/mid/high): 2023-10 .13/.24/.40; 2024-04 .20/.26/.31; 2024-07 .20/.34/.24; 2024-10 .19/.34/.17.
- My monotone constraint (familiarity -> not less loved, inherited from the baselines) cannot learn the reversal, and neither can the artist_recent member. I did not change anything after seeing LATE.

STRONGEST CASE AGAINST MY RESULT
1. TUNE gains rest on about 300 variants chosen on TUNE with a noisy metric. Many variants sit at .60-.65, so the best one is partly selection.
2. LATE shows the TUNE winner (window 365 + artist_recent) fails to generalise. Most of the TUNE sauc is the artist-familiarity relation, which reverses. The audio part adds only about +0.01 sauc, new-artist +0.02 on TUNE, and on LATE learned_only is just equal to nonaudio_gbm.
3. The final fails the literal null control. It also fails to beat the pool_artist_siblings diagnostic's CI on LATE.
4. Between-artist gain is not within-artist gain. On TUNE wa lower-bound vs nonaudio_gbm is -0.011, so a gain in wa is not established; the sauc gain is between-artist. On LATE nothing holds up on wa_sauc, ws_sauc or new-artist sauc against nonaudio_gbm.
5. Only about 1000 training songs per cutoff, so every estimate has wide CIs.

LEAKAGE SELF-AUDIT (all checked)
- Every training row has first play < cutoff - 90 days, so its 90-day horizon is complete before the cutoff; labels (plays90, days90, share90, nnew) use train streams only. Songs first played in the last 90 days are not training rows (their plays still count in candidate history features).
- Rank targets are percentiles within the quarter of first play, computed only among kept training rows.
- audit.py recomputes the extra and audio features of 12 sampled training songs from the log truncated at their own first play, for two cutoffs. The first audit caught a real leak (a global prior over all songs) which I fixed (the prior is now the mean over songs matured before the row's time). After the fix: 0 mismatches for the extra features at both cutoffs; one audio mismatch in 12 at 2023-10.
- That mismatch is a known small deviation: a song's representative track is the earliest named stream, which for a song whose first stream is unnamed can be a later stream. It affects under 0.5% of songs and carries no label information.
- All fitted models are fit only on train songs. CLAP embeddings are per preview with no fitted transform. The blend standardisers use training-row predictions only. No pool, decoy or future tracks are used in any fit.
- The harness independence check passed (p90 relative change 0.0). Predictions are cached per cutoff.

ON THE LABEL (love 6/3)
- The evaluation's own label is not clearly the right target. Training on graded or volume-normalised targets gives better ranking of love 6/3 itself (+0.02 to +0.04 sauc on TUNE) than training on love 6/3: rank_plays .598 vs .557 with all else fixed; in the final blend .650 vs .624 for the binary target.
- Neighbouring thresholds are not worse: on TUNE the final scores love .650, love_4_2 .657, love_10_4 .640, strong .641. Spearman with share90 is .26, similar to days90 and log plays.
- Variable selection is noisy, but the data support (1) a graded, volume-normalised target as the training signal, and (2) reporting all thresholds. I would keep 6/3 as a headline label but not treat it as the only quantity.

FAILED OR REJECTED (code still present only where its score is reported above)
- Extra artist/album/relative-meta features ("plus"): worse.
- Pairwise/group-demean/LambdaRank variants: no gain.
- Ridge: no gain, wa lower.
- Sole-new-song training: worse.
- Removing monotone constraints: worse on TUNE.
- Nothing from failed attempts was deleted because each one is reported and kept in variants_*.py.

DEVIATIONS TO NOTE
- Early stage runs (s1-s9) used earlier core versions; I re-ran all stage files on the final core and the tables above are from the re-runs. The first rep/capacity reruns changed slightly (plus features after the prior fix). Stage logs are in the final/ folder.
- Two null-control runs instead of one: the second was needed to isolate the learned part and was run before the LATE run.
- One of the two permitted --late runs used.

Files: /home/user/Listener/taste-model/predictors/w3r1-training-signal/ (predict.py, core.py, feats.py, build_clap.py, audit.py, diag_flip.py, variants_*.py); logs in /tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf3/w3r1/final/.