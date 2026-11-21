RESULTS REVIEWER REPORT (Workflow 3 results). Start 2026-11-21T10:42:14Z, end 10:44:02Z (TIMING.txt in /tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf4/reviewer-results/). The review was shallow because of the time cap and rests mostly on reading plus one rerun.

## A. What I actually ran
1. `python3 -W ignore -m evalkit.run --fast predictors/w3r2-audio-taste/predict.py` (2 threads, TUNE only, nboot 100). It took about 2.5 minutes and the log is in my scratch folder as fast_audio.log. No --late run, so I added nothing to LATE use. I did not rerun the null control or any LATE number myself.
   - audio_final reproduced: TUNE sauc 0.621 (0.577-0.652), wa 0.598, gc 0.571, gc_wa 0.555, new-artist 0.612, known 0.611, plift 1.38.
   - audio_final_meta is 0.617 and audio_missing_indicator is 0.518. This matches the report.
   - Baselines on TUNE matched RESULTS: nonaudio_gbm 0.559, duration 0.559 (wa 0.607), popularity 0.471, meta_gbm 0.528, artist_plays 0.619, artist_recent 0.619.
2. `python3 -m evalkit.selftest` gave "selftest OK". It covers the metrics engine against brute force, point-in-time artist features, independence checks, the 7-day oracle AUC of 0.89, and tried-vs-decoy metadata AUC of 0.568 (0.590 with release age). The null v2 section is only printed on 3 folds, not asserted.
3. I read RESULTS.md, builder-r2-audio-taste.md, devils-advocate-r2-works.md and devils-advocate-r2-dismissed.md, the evalkit README, w3r2-audio-taste/predict.py, .cache/late_runs.log and .cache/shared/FEATURES.md.

Not read or run by me: the other round reports, the integrated predictor code, evalkit run.py/metrics.py/data.py line by line, and the null runs. Items that depend on these are tagged "relayed".

## B. Claims that hold
- **audio_final TUNE numbers** reproduce exactly from code (run 1).
- **Baseline TUNE numbers** reproduce (run 1).
- **LATE and ALL numbers** (0.633 / 0.626 and the other columns) are relayed. Both round-2 devil's advocates report byte-identical reruns of the full --late logs. I have not verified them independently.
- **No fitted transform leaks pool or future tracks** in audio_final. I checked `_fit` in predict.py:
  - standardiser, PCA and ridge are fitted only on `song_table(train)` songs that have audio;
  - training targets use only songs whose 90-day horizon ended before the cutoff (`first < cutoff-90d`), and the rank target is normalised within the quarter of first play;
  - scores depend only on the candidate's own clip.
  The "transductive transforms" concern from before Workflow 3 does not apply to this predictor. I did not check the round-1 audio predictor or the integrated predictor for it.
- **Not an artist or metadata lookup.** audio_final uses only MERT embeddings, with no artist or history input. It scores 0.612 on new-artist songs on TUNE (nonaudio_gbm 0.482) and about 0.61 on known-artist songs. Metadata adds nothing (0.617 vs 0.621). The missing-preview flag alone scores 0.518, so a missing-audio shortcut does not explain the tried-pool score.
- **Round-2 gain over round 1 is small.** I did not check this directly; it is relayed from the devil's advocate reports (+0.02 sauc, P 0.97, lower bound -0.002).
- **The null-control FAIL is reported honestly** (0.522 vs band edge 0.519). The "random-direction chance outlier" explanation was not re-executed by anyone and is unverified. Treat the null as FAIL.
- **The open-pool shortcut** (missing-preview flag open sauc 0.533, p20 0.195) is relayed, and the claim in RESULTS is correct.
- **Integrated blend fades on LATE** (0.535, below its own audio-only version) is relayed as reproduced by two devil's advocates.
- **The headline "audio is modest, about 0.62-0.63" is consistent with everything I saw.**

## C. Claims that do not hold, or are misleading as worded
1. **"Beats nonaudio_gbm, the bar to beat" is a weak bar.**
   - On TUNE, `artist_plays` alone (one number per song) scores 0.619 sauc, equal to audio_final (0.621). `artist_recent` and `pool_artist_siblings` also score 0.619. The gradient-boosted nonaudio_gbm that uses the same history plus metadata scores only 0.559, worse than its own single feature.
   - In my TUNE run audio_final's gap to artist_recent is -0.002 (lower bound -0.044).
   - The STRONG grade for audio therefore rests on LATE, where the artist baselines flip below 0.5. It is not evidence that audio is better than familiarity in general.
   - The report's section 6 phrase "beats a metadata-plus-artist-history model" is accurate only for that one weak model.
2. **"Stable across 2021-2024" is stronger than the data.**
   - The TUNE (0.621) and LATE (0.633) point estimates agree, but the intervals are wide (+/-0.05).
   - audio_final's 2021-07 fold is 0.363 and 2021-10 is 0.490. These are small folds whose pools were rebuilt and are not comparable with older scores.
   - The 2022+ per-fold range 0.519-0.691 comes from the builder report (relayed).
3. **"New-artist advantage" was mislabelled in the builder report.** The +0.074 is the overall delta; the real new-artist values are 0.621 vs 0.532. On LATE there is no new-artist advantage (0.641 vs 0.637).
4. **"Integrated dWA vs best meta +0.008" is misquoted.** The best meta is duration, with lower bound -0.020 and P 0.807.
5. **Integrated null-v2 PASS for the no-history variant and the audio member is invalid.** Seeds 2 and 3 reuse seed 1's fit through a cache key (relayed from both devil's advocates, who read the code and null.log).
6. **The "pool_artist_siblings P=0.0" figure in the builder report was a wrong-cell read.** The correct value is P 0.89, lower bound -0.018 (relayed).
7. **"Final chosen as least tuned, not the TUNE maximum"** is only a tie, not true as phrased (relayed).
8. **Second --late run "for a bug fix"** was unnecessary. The outputs were byte-identical (relayed). It still adds to LATE contamination.

## D. What the evaluation does not measure (my judgment)
- **Sample size.** TUNE has only 1,490 tried songs and 493 new-artist songs across 10 folds. Intervals of +/-0.04-0.05 mean differences of 0.02-0.03 between candidates (38 tuned variants, many ablations) are not resolvable.
- **Selection on TUNE, LATE partly used.**
  - 38 variants were tuned on TUNE and the final was "pre-declared" before the builder's own --late run. Round-1 ca_local LATE results were public to the builder. LATE has at least 17 log lines, including repeated runs of the same files.
  - Treat LATE as one partly informative look, not a clean holdout. Only sealed data is clean, and I did not touch it.
- **"Specific parts of the music"** was tested only as four fixed 5-second windows from a 30-second preview, which is a weak test. Local vs whole-clip was +0.00-0.01. The claim "not supported yet" is the honest reading, and the claim is neither supported nor refuted.
- **Label is partly behaviour.** My run's diagnostics show exposure_before (which is fixed before the first listen, so it cannot be a consequence of liking) at 0.623 sauc on TUNE, equal to audio_final, and exposure_session at 0.658. Where in a session a song is first heard predicts love as well as the audio does. This supports the report's statement that much of the label is behavioural. The oracle numbers (plays in the first 7 days gets 0.89 in selftest) reproduce. The unvetted idea that session count and love run in reverse is untested: `exposure_before` being as predictive as `exposure_after` argues that at least part of the link is not a consequence of liking.
- **Open pool is not a candidate-search test.**
  - On TUNE, artist_plays open sauc is 0.725 vs audio 0.704.
  - Audio's p20 is 0.16, vs 0.32 for artist_recent (relayed in RESULTS and by the devil's advocates).
  - Decoys are drawn from artists known before each cutoff, so the open pool tests mostly within-familiar-artist ranking.
  - The report's conclusion that the model is not ready for candidate search is right.
- **Null control cannot certify.** 4 of 7 baselines (including duration and popularity) fail it (relayed). The band may be too narrow for artist-constant scores (engineer's unverified belief).
- **Below-chance folds** were flagged but never investigated: artist_plays 2024-04, popularity 2023-04, missing-only 2022-07 and 2024-07, audio_final 2021-07. Cause unknown.
- **Duration** gets 0.607 within artist (my TUNE run) vs audio 0.598. Audio is not shown to beat the simplest metadata feature inside the same artist, which is the cleanest "music, not artist" test available.
- **Metadata-leak notes.** Popularity is measured in 2026 (mild look-ahead; README). The release-age test by the devil's advocate was coarse (88% in one bucket).

## E. Unverified
- LATE and ALL numbers and all CIs on them, null-control runs, integrated predictor and round-1 numbers (relayed, not rerun by me).
- That audio_final's null FAIL is a chance outlier.
- Whether MERT or CLAP were exposed to sealed-era songs.
- A clean "songs with audio only" split for round 2.
- Whether the 0.02 gain from round 1 to round 2 is real.
- Every item in the round reports for builder-r1-* and the engineer reports; I did not read them.

## F. Time taken by jobs (as far as I can see)
No job of mine ran longer than 3 minutes (the fast run about 2.5 minutes, the selftest about 1.5 minutes). The MERT extraction of about 1.8 s per clip is documented in FEATURES.md. The round-2 builders' 17-minute sessions are relayed.

## G. Bottom line
RESULTS.md is mostly accurate. The one result that survived on both TUNE and LATE is the audio-only AUC of about 0.62-0.63. That is above chance and above nonaudio_gbm, but it only equals single-number artist-familiarity baselines on TUNE and does not beat duration within artist. The strongest points against over-reading are the weak "bar" (C1), the unresolvable differences at this sample size, and the partly used LATE slice.

Files: /home/user/Listener/taste-model/predictors/w3r2-audio-taste/predict.py, /home/user/Listener/taste-model/.cache/late_runs.log, /tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf4/reviewer-results/fast_audio.log