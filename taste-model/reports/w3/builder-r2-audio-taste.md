REPORT w3r2-audio-taste (builder, round 2). Pre-declared final: audio_final.

SUMMARY
- The final audio-only model reaches sAUC 0.621 (TUNE), 0.633 (LATE), 0.626 (ALL).
- It beats nonaudio_gbm on ALL with grade STRONG for sauc and wa, and NONE for gc.
- The null control (v2) does NOT cleanly pass: audio_final FAILS by 0.003 on sauc (details below). I am not claiming a pass.

CODE (all in /home/user/Listener/taste-model/predictors/w3r2-audio-taste/)
- predict.py: harness entry, PREDICTORS = {audio_final, audio_final_meta, audio_missing_indicator}. Run from /home/user/Listener/taste-model: `python3 -W ignore -m evalkit.run --fast predictors/w3r2-audio-taste/predict.py`.
- ref_ca_local.py: wrapper exposing round-1 ca_local, with a null-safe cache clear.
- calib_randdir.py: random-direction calibration of the null band.
- No new caches. Existing MERT and CLAP caches were reused; no new extraction.
- Failed iteration variants were never saved as files. Only the final set is in predict.py.
- Scratch logs are in /tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf3/taste/. The final run logs are full_tune.log, late2.log and null2.log.

MODEL (declared before any --late run)
- Inputs: MERT-v1-95M (4 windows x 12 layers) and CLAP only. No artist identity, no artist history, no pool structure.
- audio_final is the standardised mean of 3 members. All three are ridge on a PCA-whitened representation, trained on the target `rank_plays`.
  - `rank_plays` is the percentile of plays90 within the quarter of first play, over songs whose 90-day horizon is complete before the cutoff.
  - Member 1: time-local, each 5 s window is a training row, layers 4-8, 64 components, alpha 1200, scored as the mean of window outputs.
  - Member 2: whole-clip mean, layers 4-8, 32 components, alpha 150.
  - Member 3: time-local, layers 3-7, 64 components, alpha 1200.
- Songs without audio get the train-median score (neutral).
- Ablations declared before LATE (2):
  - audio_final_meta: the same plus duration, explicit, popularity and a popularity-missing flag. This is the separate metadata variant.
  - audio_missing_indicator: no audio content, only the "no audio" flag. This is the missing-audio check.
- The missing-audio sensitivity variants (missing scored min or max) were run on TUNE in --fast only, as iteration variants.

TUNE ITERATION (what I ran)
- 38 distinct variants scored on TUNE with --fast (about 30 s per batch).
- Target: love (round-1 repro), rank_plays, rank_share, rank_mix.
- Regularisation and size: alpha 100/300/1000, 32/64/128 PCA components.
- Layers: 0-3, 2-6, 3-7, 4-6, 4-8, 5-9, 8-11.
- Representation: CLAP added, local vs whole, top2 aggregation, recency half-life 365 d, 730-day window.
- Learners: GBM, SVR.
- Artist-demeaned target: 0.5 and 1.0 (artist used for target construction only).
- Ensembles.
- Everything with the rank target sat in sAUC 0.59-0.62. The differences are within noise.
- Findings:
  - The graded target improved sAUC over the binary love target (0.590 -> 0.605) and wa (0.584 -> 0.591).
  - Layers 4-8 and 3-7 were best. Layers 0-3 (0.577) and 8-11 (0.552) were clearly worse.
  - Adding CLAP gave nothing.
  - The nonlinear learners (GBM, SVR) were no better than ridge.
  - The artist-demeaned target gave no gain.
  - Local versus whole clip: +0.00 to +0.01. This is weak, as in round 1.

FINAL RESULTS
Full TUNE run (nboot 300, independence on): independence p90 = 0.0 for every model. LATE run: the second --late run, after a cache-key fix (see "Second --late run" below).

Point estimates [95% CI] from the tried pool:

| slice | model | sauc | wa | ww | ws | gc | gc_wa |
|---|---|---|---|---|---|---|---|
| TUNE | audio_final | .621 [.581,.651] | .598 [.561,.625] | .624 [.568,.668] | .582 [.503,.674] | .571 [.543,.593] | .555 [.513,.593] |
| TUNE | audio_final_meta | .617 | .596 | .617 | .578 | .570 | .553 |
| TUNE | ca_local | .594 | .593 | .600 | .577 | .554 | .549 |
| TUNE | nonaudio_gbm | .559 | .552 | .560 | .543 | .557 | .534 |
| LATE | audio_final | .633 [.586,.681] | .627 [.563,.690] | .622 [.552,.688] | .641 [.493,.745] | .581 [.550,.609] | .567 [.506,.617] |
| LATE | audio_final_meta | .627 | .625 | .618 | .647 | .576 | .569 |
| LATE | ca_local | .622 | .637 | .629 | .661 | .573 | .579 |
| LATE | nonaudio_gbm | .540 | .547 | .588 | .582 | .523 | .527 |
| ALL | audio_final | .626 [.592,.651] | .606 [.576,.634] | .623 [.578,.665] | .604 [.54,.665] | .575 [.553,.593] | .559 [.525,.592] |
| ALL | audio_final_meta | .621 | .603 | .617 | .603 | .572 | .558 |
| ALL | ca_local | .605 | .604 | .611 | .608 | .561 | .558 |
| ALL | nonaudio_gbm | .551 | .551 | .571 | .557 | .544 | .532 |

- The sauc permutation band is TUNE (.459,.537), LATE (.456,.550) and ALL (about .475,.526).
- audio_final lies above the band in all three slices.
- audio_final_meta is slightly below audio_final in every slice, so metadata adds nothing.

Further metrics for audio_final:
- plift: TUNE 1.381, LATE 1.785, ALL 1.514.
- New-artist sauc (all-pool): ALL +0.074 vs nonaudio_gbm, P=1.0.
- I did not capture the CIs for new-artist sauc, plift and Spearman share90 in this report; they are in /tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf3/taste/late2.log (VERDICT and tried_love tables). The Spearman share90 value is also not captured here.
- Fast-run new-artist sauc on TUNE was about 0.61, versus 0.482 for nonaudio_gbm.

Open pool (sauc / new-artist / wa / p20):
- TUNE: .704 / .700 / .567 / .160.
- LATE: .715 / .721 / .581 / .175.
- ALL: .708 / .709 / .571 / .164.
- Reference open sauc, ALL: nonaudio_gbm .602, artist_recent .707, pool_artist_siblings .692.
- Caution: the decoy pool is matched on metadata only. audio_missing_indicator alone gets open sauc 0.533 and open p20 0.195 (ALL), so the open pool carries a missing-preview shortcut.
- The open p20 values are low and not clearly better than the baselines. artist_recent .320, audio_final .164 (ALL).

PAIRED DELTAS for audio_final (point delta; P(d>0) from the shared bootstrap; sAUC unless stated; ALL slice unless stated)
- vs nonaudio_gbm:
  - sauc +0.074 (80% interval .044-.107), P=1.0, grade STRONG.
  - wa +0.055 (.025-.086), P=1.0, grade STRONG.
  - gc +0.031, P=.957, 95% lower bound -0.003, grade NONE.
  - TUNE sauc +0.062, P=.98. LATE sauc +0.093, P=.997.
  - gc_wa is below nonaudio_gbm: lower bound -0.017 on ALL and -0.040 on LATE.
- vs meta_gbm: sauc lower bound +0.048 on ALL, P=1.0. wa lower bound +0.006, P=.987.
- vs duration:
  - sauc lower bound +0.023, P=1.0.
  - wa: P=.80 on ALL, but the lower bound is -0.037. TUNE P=.43 (duration wa .607 vs audio .598); LATE P=.987 (.627 vs .533).
  - Duration's within-artist AUC on TUNE is not beaten.
  - The VERDICT 'dWA vs best meta' (duration) on ALL has lo95 -0.037 and P=.80.
- vs artist_recent:
  - sauc ALL lower bound +0.026, P=.997. TUNE P=.597, lower bound -0.043. LATE lower bound +0.117.
  - wa lower bound +0.078, P=1. artist_recent has wa=0.5 by construction.
  - gc ALL P=.867, lower bound -0.019. gc on TUNE P=.18, so artist_recent is as good or better on gc on TUNE.
  - In the TUNE slice, history alone (artist_recent, sauc .619) matches the audio-only model.
- vs pool_artist_siblings (post-cutoff diagnostic, not a valid predictor): sauc P=0.0 per the P table, with lower bound about -0.30. It is on ALL sauc .590 vs audio .626 (point), so the point delta is positive but the paired table reads P=0. I did not resolve this, so treat the paired figure as unverified. I did not check the column mapping (the column was truncated).
- vs ca_local (round-1 reference):
  - sauc +0.021 point; P=.97 on ALL (TUNE .957, LATE .727).
  - wa P=.573 on ALL, so no difference in within-artist.
  - gc_wa P=.593 on ALL.
  - The round-1 predictor is nearly as good. The new gain is small: about +0.02 sAUC, mostly on TUNE.
- Metadata variant minus audio-only: sauc -0.004 to -0.006; evidence NONE. Metadata adds nothing.

Evidence grades (ALL VERDICT): sauc STRONG, wa STRONG, gc NONE (audio_final). audio_final_meta has the same grades. audio_missing_indicator is NONE on every metric, with negative deltas.

MISSING-AUDIO CHECK
- Coverage is 89-94% on tried songs, and about 99% on decoys.
- Rate of missing-audio songs: the harness does not expose the tried songs' audio coverage per candidate in a way I could use for a split. I could NOT produce a clean "excluded versus included" split. An in-harness restriction to audio-present songs was not available without changing the harness, so this part is not done.
- audio_missing_indicator (the flag alone, no audio content) scores:
  - sauc .518 / .509 / .514 (TUNE / LATE / ALL), wa .510 / .499 / .507.
  - gc .510 on TUNE, .511 on LATE.
  - That is within or near the permutation band, and far below audio_final.
  - The indicator does not drive the sauc result.
- Sensitivity on TUNE in --fast: the neutral score gave sauc .621. Scoring missing as lowest gave .592, as highest .627 and p20 up to .219 on the open pool. So the missing flag is informative on the open pool; neutral is the honest choice.
- audio_missing_indicator shows one below-chance fold (2024-07, AUC .475).

TIME-LOCAL RESULT (user's "specific parts" remark; I decided to test it this way)
- Each 5 s window was a training row, aggregated by mean, top2, or max, compared with the whole-clip mean.
- TUNE, rank_plays: local alpha 1200 sauc .614 / wa .601, vs whole nc64 .605 / .591.
- top2 aggregation: .610. Max-type aggregation gave no gain.
- Round-1 ca_local vs the new ensemble gives +0.02 sAUC at most.
- Difference local minus whole is +0.00 to +0.01, within noise. This is the same weak test as round 1.
- It does not show that specific parts of a clip matter, and it does not rule it out.
- Only 4 fixed windows of a 30 s preview were available; I did not test an alternative window set.

NULL CONTROL v2 (3 seeds, TUNE; band of the 3-seed mean: sauc .475-.519, wa .476-.533, new .454-.536)

| model | sauc s1 / s2 / s3 (mean) | wa mean | new mean | result |
|---|---|---|---|---|
| audio_final | .498 / .518 / .550 (.522) | .493 | .523 | FAIL (sauc out by .003) |
| audio_final_meta | .500 / .498 / .532 (.510) | .488 | .511 | PASS |
| audio_missing_indicator | .518 (constant) | .510 | .536 | PASS |
| ca_local | .494 / .518 / .507 (.507) | .485 | .504 | PASS |

- audio_final's null sauc is just above the band (0.522 vs 0.519). It is a FAIL by the harness rule. I report it as a fail, not a pass.
- I did not re-seed or retune to get a pass. That would not be a legitimate fix.
- Calibration check (calib_randdir.py): random linear directions in the fitted whitened audio space, scored against the REAL labels on TUNE.
  - 3-draw means ranged .468-.516, with 5% of them outside the harness band (.475,.519).
  - So a mean of .522 is a mild outlier of the same kind that random directions produce about 5% of the time. It is not evidence of a leak. It does not make the result a pass.
  - The model sees no artist or history. All the audio-model nulls use audio of songs that are shuffled against labels.
- A first null run (null.log) returned identical scores across the 3 seeds for audio models. Cause: my fit cache was keyed on (cutoff, n, sum of timestamps), which the identity shuffle leaves unchanged, so seeds 2 and 3 reused seed 1's fit. This bug affected only the null control, not the real runs. I fixed the key by adding an identity hash of trackId and song, in predict.py and in the ca_local wrapper. null2.log is the corrected run and is the one reported.
- The round-1 ca_local file has the same cache-key flaw. In my wrapper it is neutralised.

SECOND --late RUN (stated bug fix)
- Run 1: the file before the cache-key fix. Run 2: after the fix, which changes the file hash.
- The cache-key fix does not affect real-fold scores. I did not diff run 1 against run 2 numerically. Both logs are in the scratchpad (late.log and late2.log). The reported numbers are from late2.log (the final file).
- The model was not changed after seeing LATE. The ablation set was fixed beforehand.

BELOW-CHANCE FOLDS (harness flags)
- artist_plays, fold 2024-04: AUC .407.
- popularity, fold 2023-04: AUC .403.
- audio_missing_indicator, fold 2024-07: AUC .475.
- None of these is my final model. I did not investigate the first two in depth. They are baselines, and a history-based score being anti-predictive in one quarter fits a shift in taste.
- audio_final per-fold AUC (ALL): below .5 only in 2021-07 (.363, a tiny fold of about 50 tried songs) and 2021-10 (.490). The 2021-07 fold is noisy; the 2021-07 and 2021-10 pools were regenerated by the engineer, so these two folds are not comparable with older scores.
- Per-fold AUC range for audio_final in 2022+ folds: .519-.691.

LEAKAGE SELF-AUDIT (beliefs unless marked "ran")
- Ran: independence check p90 = 0.0 for all my models.
- Ran: the null control (above).
- Standardiser, PCA and ridge are fitted per cutoff on train-stream songs only. This is by code inspection.
- Training rows use songs first played at least 90 days before the cutoff, so label horizons are complete. Quarter ranks for the target are computed within those songs only.
- Features are independent per clip, by FEATURES.md.
- The MERT and CLAP encoders were pretrained externally and may have seen sealed-era songs. This cannot be controlled.
- I never ran --sealed and never read sealed data, streams.jsonl, listening_stats.csv or decoy files.
- Metadata (duration etc.) is used only in the audio_final_meta variant.
- The artist field was used only for the artist-demeaned target in a discarded variant; the final model does not use it at all.
- Under the null control, audio_final's mean sauc exceeds the band. I cannot rule out a mild unconsidered leak from this alone. The random-direction calibration suggests chance structure.

STRONGEST CASE AGAINST THE RESULT
- The advantage over the round-1 audio predictor is small, about +0.02 sAUC, and arrived after about 38 TUNE variants.
- The final model was chosen as the best TUNE variant, with the TUNE gains inside noise.
- On the within-artist metric, duration (a single number) beats audio on TUNE (.607 vs .598), and the graded 'dWA vs best meta' has P=0.80 and lower bound -0.037 on ALL. There is no evidence the audio beats duration within artists.
- On gc, audio_final is not STRONGER than nonaudio_gbm (NONE), and on TUNE artist_recent matches the audio model (sauc .619 vs .621), so history alone is as good on TUNE.
- The null control fails by a hair for the final model.
- LATE is a seen-once-per-design slice and round-1 LATE results were public, so the LATE improvement is not an untouched test.
- The open-pool numbers are inflated by the metadata-matched decoys and the missing-preview shortcut (flag alone gives open sauc .533).
- The ALL-slice evidence grade (STRONG on sauc) rests on both slices with positive point deltas.

NOT DONE
- A clean excluded-versus-included missing-audio split.
- New-artist sauc CIs and Spearman share90 values are not captured in this report (see scratchpad late2.log).
- No new audio feature extraction. A different window set was not tested.
- The pool_artist_siblings paired comparison needs re-checking (see above).
- I did not commit.