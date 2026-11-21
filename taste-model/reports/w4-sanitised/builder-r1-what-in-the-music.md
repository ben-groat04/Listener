<!-- structured fields -->
start_utc: 2026-11-21T13:10:19Z
end_utc: 2026-11-21T14:10:32Z
null_control_result: FLAG on all 5 models (TUNE, 3 seeds, v3), explained as mild. final_content: real sauc 0.646, null mean 0.538 (seeds 0.526/0.525/0.563), band 0.473-0.529, real-minus-null gap +0.108 (95% CI 0.064-0.158); wa and new-artist inside band. abl_no_mert 0.623 vs null 0.533 (gap +0.090); abl_no_dur 0.639 vs 0.535 (+0.104); abl_no_essentia 0.623 vs 0.530 (+0.094); abl_act_only 0.611 vs 0.533 (+0.078). The null means exceed the band edge by only 0.001-0.009, and the harness's identity-free duration baseline shows the same excess (null mean 0.527), so the excess looks harness-level. Cause not established. The real gaps are clearly positive.
late_runs_used: 1

# Builder r1 "what-in-the-music": report

Predictor: /home/user/Listener/taste-model/predictors/w4r1-what-in-the-music/predict.py (sha256 d3e6eedb391a1d830fc84f7aa1745d90411baded467dbba28a304a95d9437c64). Scratch: /tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf4/builder-r1-what-in-the-music/. Start 13:10:19Z, end 14:10:32Z (60 min of a 120 min cap; I stopped because every checklist item was done, not for lack of time). No git, no sealed data. I used 1 --late run (1 line in .cache/late_runs.log, table in .cache/late_tables/d3e6eedb...txt) and 1 --holdout run.

## 0. Short answer
- **Which properties.** On TUNE, new songs the user comes to love are more often dark, heavy, aggressive, atonal, non-acoustic, vocal, louder, drum/synth-driven and electronic-industrial. Songs that get dropped are more often vintage, acoustic or "easy": blues, jazz, country, chanson, swing, piano, calm or relaxing, instrumental. Single properties reach only about 0.58-0.63 AUC.
- **Time-local or whole-clip.** The signal is mostly whole-clip. The only time structure is a modest edge for the 2nd half of the 30 s clip (0.612 vs 0.578 for the first half, P=0.93, lower bound -0.005). There is no evidence of a "peak moment". This is not distinguishable from noise at 95%.
- **Beating earlier models.** The final model (MERT audio_final plus essentia heads plus a duration GBM) scores 0.646 on TUNE, 0.642 on LATE, 0.645 on ALL and 0.664 on HOLDOUT. The ref_audio_final reference scores 0.632, 0.621, 0.628 and 0.657. The gain is small: +0.015 on TUNE (P=0.90, lower bound -0.008), +0.017 on ALL (lower bound -0.001), +0.007 on HOLDOUT (lower bound -0.012). The harness grade is SUGGESTIVE on sauc, NONE on wa and STRONG on gc. This is evidence that essentia adds a little to MERT, not that it is clearly better.
- **Essentia alone.** The heads alone (heavily regularised ridge) match MERT-level performance: 0.611 on TUNE, 0.611 on ALL, 0.621 on HOLDOUT, with new-artist sauc 0.564 on TUNE.

## 1. Final model (declared 13:51:52Z, before any --late run; the file did not change afterwards)
`final_content` is a sum of standardised members. Each member is z-scored with its own train-song mean and SD, so a candidate's score is independent of the other candidates (independence p90 = 0.0 in the full run).
1. A: essentia head activations (605 columns: Discogs-400 styles, MTG moods, instruments, genre, danceability, voice, 7 moods, tonal/atonal, approachability, engagement). Clip mean, logit, standardised, ridge alpha 1e4. Weight 1.
2. SL: the same heads as the mean over 5-s segments 3-5 (15-30 s of the clip). One training row per segment, score is the mean over segments. Weight 1.
3. DUR: GBM on duration, explicit flag and popularity (track metadata, no artist). Weight 1.5.
4. Plus 1.0 times Workflow 3's MERT audio_final (loaded from its own file).

Targets: per-song percentile of plays90 within the quarter of first play, for mature train songs only (first play at least 90 d before the cutoff). The listening record is used only for this target; no artist history enters as an input. All fits use train-stream songs only. The fit cache is keyed on a hash of train trackId, song and artist, and skipped when EVALKIT_NO_FIT_CACHE is set.

Declared ablations: abl_no_mert, abl_no_dur, abl_no_essentia (MERT plus DUR), abl_act_only. No artist-history combined variant was built.

## 2. Scores (full harness runs; TUNE nboot 300 with independence check)
Format: sauc [95% CI] (new-artist sauc), wa [CI]. wa is within-artist sauc.

| model | TUNE | LATE | ALL | HOLDOUT-ALL (run once) |
|---|---|---|---|---|
| **final_content** | 0.646 [0.601,0.681] (new 0.613); wa 0.620 [0.57,0.70] | 0.642 [0.59,0.684] (new 0.595); wa 0.642 | 0.645 [0.612,0.673] (new 0.606); wa 0.625 | 0.664 [0.608,0.715] (new 0.624); wa 0.586 [0.50,0.663] |
| ref_audio_final | 0.632 (new 0.614); wa 0.614 | 0.621 (new 0.602); wa 0.609 | 0.628 (new 0.610); wa 0.613 | 0.657 (new 0.637); wa 0.586 |
| abl_no_mert | 0.623 (new 0.594) | 0.624 | 0.624 (new 0.585) | 0.608 |
| abl_no_dur | 0.639 (new 0.594) | 0.628 | 0.635 | 0.664 |
| abl_no_essentia (MERT+DUR) | 0.623 | 0.631 | 0.626 | 0.628 |
| abl_act_only | 0.611 (new 0.564) | 0.610 | 0.611 | 0.621 |
| duration | 0.577; wa 0.645 | 0.566; wa 0.538 | 0.573; wa 0.621 | 0.510; wa 0.498 |
| artist_recent | 0.619 | 0.440 | 0.553 | 0.521 |
| nonaudio_gbm | 0.555 | 0.536 | 0.548 | 0.540 |

Other final_content figures:
- macro_sauc: TUNE 0.618, LATE 0.632, ALL 0.623, HOLDOUT 0.666.
- gc: TUNE 0.593, ALL 0.587. gc_wa: TUNE 0.570.
- Open pool, Spotify-preview subset (primary): TUNE open_sauc 0.740 [0.675,0.782], p20 0.120 [0.05,0.20] (ref 0.705, 0.115). ALL 0.745, p20 0.132. HOLDOUT 0.770, p20 0.135. New-artist open_sauc: TUNE 0.704, ALL 0.725.
- The open-pool number is not evidence of beating artist familiarity: artist_recent has 0.738 on TUNE open, because decoys come from the same known artists.
- Evidence grade (ALL, vs best_ref = ref_audio_final): sauc d=+0.017, P=0.967, SUGGESTIVE. wa d=+0.012, P=0.90, NONE. gc d=+0.014, P=0.997, STRONG. TUNE d_sauc +0.017 (P 0.967), LATE d_sauc +0.020 (P 0.937).

Paired deltas of final_content in sauc (lower 95% bound / P(d>0)):

| comparison | TUNE | ALL | LATE |
|---|---|---|---|
| ref_audio_final | +0.015, -0.008 / 0.90 | +0.017, -0.001 / 0.967 | +0.020, -0.009 / 0.94 |
| duration | +0.070, +0.020 / 1.00 | +0.072, +0.022 / 1.00 | +0.076, +0.009 / 0.98 |
| nonaudio_gbm | +0.091, +0.007 / 0.98 | +0.097, +0.032 / 1.00 | +0.106, +0.021 / 0.99 |
| meta_gbm | +0.108, +0.039 / 1.00 | +0.101, +0.048 / 1.00 | +0.088, +0.018 / 1.00 |
| artist_recent | +0.028, -0.020 / 0.89 | +0.092, +0.029 / 0.99 | +0.202, +0.075 / 1.00 |
| artist_plays | lower -0.018 / 0.88 | +0.026 / 0.99 | +0.068 / 1.00 |
| artist_love_rate | -0.010 / 0.94 | +0.051 / 1.00 | +0.073 / 1.00 |
| pool_artist_siblings (post-cutoff diagnostic) | -0.045 / 0.64 | -0.018 / 0.88 | -0.026 / 0.94 |
| pool_album_siblings (diagnostic) | +0.001 / 0.98 | +0.034 / 1.00 | +0.040 / 1.00 |
| has_preview | +0.123 | +0.132 | +0.103 |
| preview_source_itunes | +0.104 | +0.100 | +0.041 |
| popularity | +0.082 | +0.078 | +0.030 |

Within-artist (wa) deltas vs duration, which is the within-artist bar:
- TUNE d=-0.025 (lower -0.088, P=0.32). Duration's own TUNE wa (0.645) is not beaten.
- LATE d=+0.104 (lower -0.022, P=0.93).
- ALL d=+0.004 (lower -0.061, P=0.62).
- HOLDOUT d=+0.088 (lower -0.083, P=0.92). Duration scores 0.498 on HOLDOUT, so its within-artist edge does not transfer to new artists.
- wa vs ref_audio_final: TUNE +0.006 (P=0.77), HOLDOUT +0.000 (P=0.45).
- wa vs nonaudio_gbm: TUNE d=+0.064 (lower -0.013, P=0.94).
- wa vs artist_recent: TUNE d=+0.120 (lower +0.070, P=1.00). This delta is mostly mechanical, because artist_recent is a constant within artist (wa 0.500).

HOLDOUT vs ref_audio_final (verbatim from the HOLDOUT-ALL VERDICT_DELTAS row): sauc d=+0.007 lo95=-0.012 P=0.73 80%[-0.007,+0.023]; wa d=+0.000 lo95=-0.034 P=0.45; gc d=+0.010 lo95=-0.011 P=0.78; macro_sauc d=+0.007 lo95=-0.053 P=0.62. HOLDOUT-late: sauc 0.706 vs ref 0.678 (d=+0.029, lo95=-0.005, P=0.96). HOLDOUT-early: 0.627 vs ref 0.639 (d=-0.011, P=0.18). The full HOLDOUT output is in .../builder-r1-what-in-the-music/holdout.txt and in .cache/holdout_runs.log. I did not change the predictor after seeing HOLDOUT.

Folds are small and noisy: per-fold sauc for final_content on TUNE ranges 0.444 to 0.722, with n between 35 and 283 tried songs.

BREAKDOWN rows on TUNE (sauc [95% CI]), final_content vs ref_audio_final:
- Fold (final / ref): 2021-07 0.444 / 0.374; 2021-10 0.464 / 0.524; 2022-01 0.722 / 0.644; 2022-04 0.553 / 0.566; 2022-07 0.650 / 0.604; 2022-10 0.525 / 0.553; 2023-01 0.656 / 0.637; 2023-04 0.682 / 0.627; 2023-07 0.670 / 0.693; 2023-10 0.642 / 0.629.
- New vs known artist: new 0.613 [0.54,0.69] / ref 0.614; known 0.650 [0.60,0.70] / ref 0.625.
- exposure_before 0 / 1-2 / 3-8 / 9+: 0.613 / 0.661 / 0.680 / 0.725 (ref 0.593 / 0.669 / 0.633 / 0.718).
- 90-day-window play tercile low / mid / high: 0.634 / 0.659 / 0.641 (ref 0.601 / 0.642 / 0.631).
- Release age: only the ">3 y" bucket is large (987 tried songs): 0.658 [0.61,0.69] vs ref 0.640. The other buckets have n<=50 and CIs spanning the whole range.
- Preview present 0.652 [0.60,0.69] (n=995); preview absent 0.594 [0.42,0.80] (n=79).

## 3. Findings table (TUNE tried songs, 974 with audio, 307 loved; analyze_heads.py, analyze_desc.py, analyze_duration.py)
Columns: D = descriptive AUC of the feature for "loved" over all TUNE tried songs (fold-stratified pairs, artist-cluster bootstrap CI, 60 resamples). WA = within-artist AUC. OOS = signed AUC where the sign of the relation is learned only on each fold's train songs and the fold is then scored (out of sample). A permutation test (labels permuted within fold, 30 permutations, over 605 heads) gives a null max |AUC-0.5| of mean 0.070, max 0.089, p95 0.085. The best head deviates by 0.127, so the top rows beat a 605-way multiple-comparison null. The rows below are listed after looking at all heads, so D is descriptive.

| property (direction for "loved") | D [CI] | WA [CI] | OOS [CI] |
|---|---|---|---|
| Industrial rock (Discogs) | 0.627 [0.570,0.677] | 0.602 [0.540,0.674] | 0.627 [0.570,0.677], sign stable in all 10 folds |
| Nu metal | 0.622 [0.549,0.676] | 0.615 [0.551,0.726] | 0.622, stable |
| New wave (MTG genre) | 0.626 [0.564,0.672] | 0.571 [0.452,0.688] | 0.626, stable |
| Electronic industrial / EBM / gothic metal / goth rock | 0.597-0.609 | 0.54-0.59 | 0.597-0.609, stable |
| Synthesizer | 0.614 [0.556,0.669] | 0.602 [0.435,0.656] | 0.604 [0.533,0.667], sign 71% |
| Aggressive | 0.592 [0.531,0.642] | 0.554 [0.503,0.697] | 0.592, stable |
| Atonal | 0.591 [0.530,0.656] | 0.565 [0.432,0.625] | 0.591, stable |
| Non-acoustic | 0.591 [0.529,0.659] | 0.580 [0.468,0.651] | 0.591, stable |
| Engagement (regression head) | 0.577 [0.523,0.646] | 0.512 [0.441,0.639] | 0.577, stable |
| Voice present (vs instrumental) | 0.575 [0.526,0.616] | 0.594 [0.491,0.654] | 0.576 [0.529,0.616] |
| Drums | 0.564 [0.504,0.609] | 0.569 [0.531,0.717] | 0.564, stable |
| Loudness, librosa dB (clip mean) | 0.584 [0.521,0.635] | not computed | 0.584, stable |
| Spectral flatness | 0.560 [0.509,0.611] | not computed | 0.560, stable |
| Longer duration | 0.560 [0.528,0.611] | 0.557 | 0.545 [0.502,0.605] |
| Lower loudness variation / dynamic range | 0.441-0.445 [0.395,0.475] | not computed | 0.555-0.559 [0.525,0.605] |
| Chanson / poetry / honky-tonk / country / blues / jazz / swing (all "dropped") | 0.384-0.404, CIs mostly within [0.33,0.47] | about 0.40-0.44 | signed 0.59-0.62, sign stable in all folds |
| Piano | 0.436 [0.383,0.479] | 0.466 | 0.564 |
| Calm / relaxing / acoustic / instrumental / tonal | 0.41-0.44 | 0.41-0.47 | 0.56-0.59 |
| Tempo (log2 bpm/120) | 0.501 [0.434,0.549] | not computed | 0.500: no signal |

Duration, descriptive: love rate by duration is 0% (<90 s, n=7), 9.5% (90-150 s), 21% (150-180 s), 23% (180-210 s), 31% (210-240 s), 38% (240-300 s) and 33-35% (>300 s). Titles with "live" (n=24) are loved at 21% vs 32% for the rest; "feat." (n=19) at 42%. The within-artist AUC of duration in my own tabulation is 0.557 (3,045 pairs). The harness's duration GBM wa of 0.645 is higher than this, and I did not explain the gap. I did not establish why duration scores within artist; "interlude/edit" title flags are too rare (2 and 11 songs) to test.

Descriptors with an unstable sign (onset strength, spectral bandwidth, rolloff) and tempo carry no usable out-of-sample signal.

**Taste drift (descriptive, plus out-of-sample).** Some properties are positive over all of TUNE but were not positive on the train data of earlier cutoffs: danceable (D 0.607, OOS 0.448), energetic (0.594, 0.445), party (0.570, 0.432), electro (0.598, 0.430), breakbeat, drum and bass, grime and hip-hop tags (D 0.56-0.58, OOS 0.42-0.45). Training on the past would have predicted the wrong sign for them. The ridge coefficient vector learned at the first TUNE cutoff (165 mature train songs) has cosine 0.38 with the one at the last cutoff (1,032 songs); consecutive cutoffs are 0.85-0.97. The Spearman of per-head target correlations between the first and the last cutoff is 0.58. This mixes real drift with estimation noise from the small early training sets. Scores also rise with training size: the first two TUNE folds are at or below chance for all audio models (final 0.444 and 0.464, ref 0.374 and 0.524).

**Out-of-sample tests of time-locality** (essentia heads by segment, ridge alpha 3000, fast TUNE sauc; the model is fit on train songs and scored on the fold). Seg 0 (0-5 s) 0.576, seg 1 0.567, seg 2 0.578, seg 3 (15-20 s) 0.611, seg 4 0.605, seg 5 (25-30 s) 0.593. First half 0.578, second half 0.612, middle four 0.598. Mean over all six segments 0.602, max over segments 0.599, clip-mean features 0.611. Second half vs first half: P(d>0)=0.93, lower bound -0.005. The preview is a fixed 30 s excerpt of unknown position in the song, so "late in the clip" is not "late in the song".

## 4. Artist-proxy checks
- **No artist input.** The model has no artist or history input. The new-artist sauc (final 0.613 TUNE, 0.606 ALL, 0.624 HOLDOUT; abl_act_only 0.564 TUNE) is by construction free of same-artist training songs. Essentia alone scores 0.564 on TUNE new artists, versus 0.614 for ref_audio_final, so MERT carries more of the new-artist signal.
- **Four-bucket artist-excluded refit** (artist_excluded_cv.py; the 4-bucket split is random). The predictor is refitted on train streams without any stream by the bucket's artists, then scores that bucket's tried songs. TUNE sauc, normal then excluded:

| model | all | known artists |
|---|---|---|
| final_content | 0.646 to 0.635 | 0.650 to 0.637 (delta -0.013, CI [-0.027,0.004]) |
| ref_audio_final | 0.632 to 0.624 | 0.625 to 0.616 |
| abl_act_only | 0.611 to 0.604 | 0.614 to 0.610 |
| abl_no_mert | 0.623 to 0.612 | 0.631 to 0.618 |
| abl_no_essentia | 0.623 to 0.610 | 0.627 to 0.611 |

  The signal mostly survives, with a loss of 0.01 or less overall. Unlike the other check, this one used the harness's own scoring, including missing-audio songs.
- **Leave-one-artist-out ridge refit** (artist_proxy.py; essentia ridge members only, audio-present songs only, 974 songs; the 'normal' scores here are higher than the harness's because songs without audio are excluded). Known-artist sauc, normal then excluded: heads 0.629 to 0.597, late segments 0.636 to 0.607, effnet embedding 0.612 to 0.566. The deltas' CIs include 0 (the heads' is [-0.069,+0.012]). So up to about 0.03 of the essentia known-artist signal may be an artist proxy (style as artist fingerprint). The two checks disagree on the size of that loss (-0.004 vs -0.03) and I did not resolve why. A devil's advocate should treat the proxy effect as between 0 and 0.03.
- **Which feature families carry the signal.** MTG moods, instruments and the Discogs genre columns each score 0.575-0.58 on their own, and the 87 MTG-genre columns alone score 0.609. Style or genre tags are therefore not the only carrier.
- **Target de-meaning** (subtracting the artist's mean target from the training target, so the model cannot learn artist identity from the target): sauc 0.611 to 0.612-0.614. This is a null result and was not adopted.

## 5. What I tried (fast TUNE, nboot 100; about 80 variant evaluations in 11 fast harness runs; sauc, new-artist sauc)
- Essentia heads, ridge alpha: 100 0.571; 300 0.578; 1000 0.590; 3000 0.604; **10000 0.611**; 30000 0.606. Clearly better with strong regularisation (alpha 1e4 is what I picked and declared).
- Feature variants (at alpha 300 unless stated): raw activations instead of logit 0.561; heads at max over patches 0.564; PCA64-whitened ridge 0.558; GBM on PCA40 0.589; PCA8 + ridge 0.612 (not adopted: same level, fewer parameters); love label instead of rank target 0.570; share90 target 0.576; half-lives 730/365 d 0.607/0.601 (alpha 1e4).
- Effnet embedding ridge: alpha 3000 0.573; 10000 0.587; 30000 0.594. Embedding mean+std 0.567-0.595.
- Head subsets (alpha 300): Discogs genres 0.579, moodtheme 0.580, instruments 0.575, MTG genre 0.609 (alpha 300-1000 0.606-0.609), misc 0.571.
- Segments: the per-segment results are in section 3. Pooling six segments gave 0.602.
- kNN on embeddings or heads (cosine, k 50-150): 0.539-0.543, one at 0.579 with PCA16. Failed, code deleted.
- librosa descriptors (loudness, centroid, rolloff, flatness, bandwidth, onset, zero crossing, tempo; my own cheap extraction): ridge 0.522-0.532, GBM 0.544, descriptors+metadata GBM 0.596 (duration GBM alone 0.559). Adding them to the final model gave 0.645-0.646, no gain.
- Blends with MERT audio_final: heads+MERT 0.621-0.639; with MTG 0.637; +embedding 0.627-0.641; +duration GBM 0.644-0.646; weights 1/1.5/2 all within 0.642-0.646. Chosen: heads, late-segments, DUR (1.5) and MERT at 1.0 = 0.646.
- Failed or not adopted: kNN, target de-meaning (null), love target, half-life weights (flat), descriptors in the blend (no gain).
- The tuning was only coarse: alpha, a handful of blend weights, one segment subset. Because ~80 variants were scored on TUNE, TUNE gains over ref have a selection bias of unknown but probably small size; LATE and HOLDOUT agree in direction (+0.020 and +0.007).

## 6. Null control v3 (TUNE, 3 seeds, fresh process each; ~4 min)
All five of my models FLAG; the baselines duration and artist_recent also FLAG, as the README says.

| model | real sauc | null mean sauc | gap (95% CI) | label detail |
|---|---|---|---|---|
| final_content | 0.646 | 0.538 (seeds 0.526, 0.525, 0.563) | +0.108 (0.064, 0.158) | sauc outside band 0.473-0.529; wa and new inside |
| abl_no_mert | 0.623 | 0.533 | +0.090 | sauc and wa outside |
| abl_no_dur | 0.639 | 0.535 | +0.104 | sauc outside |
| abl_no_essentia | 0.623 | 0.530 | +0.094 | sauc outside |
| abl_act_only | 0.611 | 0.533 | +0.078 (0.025, 0.121) | sauc and wa outside |

Explanation: all real-minus-null gaps are clearly positive and significant. The null means sit 0.001-0.009 above the upper band edge of 0.529. The harness's own duration baseline, which has no identity input, shows the same pattern (null mean 0.527, wa null 0.535 vs band 0.467-0.533), so part of the excess is harness-level, probably residual structure left when only identities are shuffled and per-song features stay attached; I did not establish its cause. I cannot rule out that a small part of the final model's score comes from effects such as target structure that survive the shuffle. I judge the FLAG a mild excess over the band that does not explain the real gap of +0.108.

## 7. Below-chance scores (investigated, none are for final_content on TUNE or ALL)
- TUNE: meta_gbm fold 2022-04 AUC 0.333 [0.14,0.49] (12 loved of 31 tried; a harness baseline, small fold). preview_source_itunes fold 2023-10 0.419 and has_preview folds 2023-10 and 2024-01 are shortcut rows. All are in small or noisy folds.
- HOLDOUT: final_content fold 2022-10 AUC 0.389 (6 loved of 12 tried, 36 pairs; the CI collapses to a point because the bootstrap draws too few distinct artists in that fold). ref_audio_final scores 0.278 in the same fold. It is noise from a tiny fold. Several baselines are also flagged there.
- The first two TUNE folds are at or below chance for all audio models (final 0.444 and 0.464; ref 0.374 and 0.524) with 165-178 training songs.

## 8. The strongest case against my result
1. **The gain over the reference is statistically thin.** TUNE +0.015 (lower bound -0.008), HOLDOUT +0.007 (lower bound -0.012), HOLDOUT-early -0.011, wa +0.006 / +0.000. The honest summary is "no worse than ref_audio_final, probably +0.01-0.02 on pooled sauc". Essentia added about +0.014 to MERT; I cannot claim a new best model.
2. **The duration member does not transfer to new artists.** Duration scores 0.510 on HOLDOUT (wa 0.498) and abl_no_dur scores 0.664, the same as final_content. Its inclusion rests on TUNE.
3. **Selection on TUNE.** About 80 variants were scored on TUNE; the final's tuning is coarse but nonzero.
4. **Artist proxy not excluded.** Up to about 0.03 of the known-artist signal may be an artist fingerprint (second check above). Essentia alone has new-artist sauc of only 0.564.
5. **Null control FLAG** (mild, harness-wide, unexplained).
6. **Taste drift and small training sets.** The sign of several "properties" flipped across cutoffs; early folds have fewer than 200 mature training songs. The "findings" are descriptive over 2021-2023 and may not describe the user's later taste.
7. **The open-pool score is not a discriminating gain**: artist_recent matches it on TUNE.
8. **Loudness and darkness may proxy something else.** Loudness (0.584) could be a proxy for release age/era (modern masters are louder), which I did not test, because release age is not an input I could use. The label is partly set by listening behaviour (the exposure_before diagnostic scores 0.603 with no music), so the model may be picking up content that goes with how songs are first heard.

## 9. What I actually ran vs. what I believe
Ran (all in the scratchpad or the predictor folder):
- 11 fast TUNE harness runs (20 s to 2 min each); full TUNE run 155 s; `--late` once 302 s (the one log line); `--null-control` ~4 min (estimate 6-10 min); `--holdout` once 159 s (estimate 5-8 min).
- analyze_heads.py 28 s; analyze_duration.py, analyze_desc.py, taste_drift.py (seconds each); artist_proxy.py 2 min 20 s (it ran in the background because it hit the 120 s foreground timeout); artist_excluded_cv.py ~3 min (estimate 8-15 min).
- build_compact.py 3.5 s; build_desc.py: estimate 17-22 min with 2 workers, go; actual 20 min (13:26-13:46), 10,288 clips, librosa at 16 kHz (no HPSS, no chroma or key). Nothing else exceeded 10 minutes.
- No sealed data was touched. The harness's .cache/late_tables file exists for my sha.
- Files kept: predict.py, build_compact.py, build_desc.py, analyze_heads.py, analyze_duration.py, analyze_desc.py, artist_proxy.py, artist_excluded_cv.py, taste_drift.py. Caches (git-ignored): .cache/w4r1-what-in-the-music/compact.npz and desc/shard_*.npz, regenerable from the two build scripts.
- Deleted code from failed attempts: the kNN learner and the target de-meaning option (both in predict.py), and the temporary "adem" and descriptor variants in PREDICTORS. The earlier librosa version with chroma/key/HPSS-free 22 kHz decode was replaced by the 16 kHz cheap version before any shard was kept.

Only believed, not tested: that the late-half advantage reflects clip structure rather than noise; that loudness proxies era; that the null excess is harness-level; why the two artist-exclusion checks differ.
