DEVIL'S ADVOCATE round 2, direction "works". Report on the two round-2 builders (w3r2-integrated, w3r2-audio-taste) and the engineer's evalkit v3.1.

Scope: I checked the builders' code, their logs and the engineer's report. I did not read the evalkit code (run.py, metrics.py, data.py) line by line against the research lead's spec. Only the pieces needed to run the checks and to read the null-control cache keys were read.
No --sealed, .sealed/, raw streams, decoy file or PLAN.md was touched. The extra --late runs below were appended to .cache/late_runs.log by the harness. Note that late_runs.log already holds the builders' own --late runs, which is more than the engineer's README note about the late_runs.log audit window describes.
My scratch files are in /tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf3/da2/ (int_late.log, aud_late.log, era.py).

## What I ran
1. `python3 -W ignore -m evalkit.run predictors/w3r2-integrated/predict.py --late` (full, nboot 300, 2 threads). Output was byte-identical to the builder's integrated/late.log (diff empty).
2. `python3 -W ignore -m evalkit.run predictors/w3r2-audio-taste/predict.py predictors/w3r2-audio-taste/ref_ca_local.py --late` (full, 2 threads). Output was byte-identical to the builder's taste/late2.log. The builder's late.log and late2.log are also byte-identical to each other, so the "second --late run for a bug fix" changed no output.
3. Read both predict.py files, the round-1 cache-key code (w3r1-content-audio/predict.py line 44, w3r1-training-signal/core.py), the null-control logs, the variant logs (v1-v3, run1-6), the VERDICT/dSAUC tables and late_runs.log.
4. Two new tests of my own, using only the evalkit loaders and cached pools:
   - Release age of tried songs versus love (data.tried_release). This is a feature predictors never see.
   - audio_final's per-candidate scores on all 14 folds (score_predictor, indep_n=0, tried rows only), compared against release bucket `rb`.

## Claim table

| # | claim | what I ran | result | verdict |
|---|---|---|---|---|
| 1 | integrated final: sauc .667 / .535 / .616 (TUNE/LATE/ALL), wa .615/.583/.607, gc .622/.541/.590 | full --late rerun | bit-identical to builder log (ALL sauc .616, gc .590, gc_wa .565) | holds (reproduces) |
| 2 | integrated ALL paired deltas vs nonaudio_gbm: P(Δsauc>0)=1.00, lo95 +.018; wa P .98; gc P .997 | rerun, dSAUC/dWA/dGC tables | matches (lo95 +.018, wa lo +.008, P .983; gc P .997) | holds |
| 3 | integrated grades vs nonaudio_gbm: sauc NONE, wa STRONG, gc STRONG | VERDICT rerun | sauc NONE (point Δ on LATE negative), wa STRONG, gc STRONG | holds as a harness output (but see fragility below) |
| 4 | integrated vs duration: ALL sauc lo95 -.003, P .96 | rerun | lo95 -.003, P .963 | holds |
| 5 | integrated "dWA vs best meta on ALL = +0.008" | VERDICT rerun | 'dWA vs best meta' = duration, lo95 -0.020, P(d>0)=.807. The +.008 is the lo95 vs nonaudio_gbm, not a vs-duration value. | doesn't hold as worded. Within-artist ordering is not shown beyond duration (the builder does concede this). |
| 6 | integrated "pool_artist_siblings sauc P .87, lo -.027" | rerun | exactly .870 / -.027 | holds |
| 7 | integrated null v2 PASS for w2i_final / noaudio / nohist | read null.log and the round-1 cache code | w2i_nohist is .505 / .505 / .505 across seeds, identical on sauc, wa and new. The audio member's fit cache is keyed (cutoff, n, sum of timestamps), which the identity shuffle leaves unchanged. Seeds 2 and 3 reuse seed 1's fit, so for the audio member the 3-seed null test is really one seed. The builder missed this; the audio-taste builder found and fixed the same flaw. | doesn't hold. The PASS for nohist and for the audio part of the final is unverified. The H and AR members are valid, since their seeds vary. w2i_noaudio contains no audio member, so its PASS is unaffected. |
| 8 | integrated 11 TUNE variants, final chosen as "least tuned", not the TUNE max | counted the models in v1-v3 | 11 distinct variants, correct. The final (w2i_ha_eq_ar .667) ties the TUNE maximum (w2i_ha_meta_ar .667). hist_audio_ar is .666, ha_ar2 .664. | holds on the count. "Not the maximum" is only semantically true (a tie). |
| 9 | integrated LATE: the history-free audio ablation (.594) beats the final (.535); removing history gains .059 | rerun | LATE nohist beats the final. The builder's own table gives .594 vs .535, and the final is below nonaudio_gbm (.540) and duration (.564). | holds, and it undercuts the headline. The ALL .616 is carried by TUNE history members, which LATE shows fade. |
| 10 | integrated missingness-only ≈ chance (.493/.516/.502) | rerun (w2i_missing_only ALL sauc .502, ci .489-.516) | matches | holds |
| 11 | integrated open pool: final ALL open sauc .745, p20 .296 vs artist_recent .320 | rerun | final p20 .296 vs best_open_p20 .32 | holds. The open-pool gain over artist_recent is small, and the TUNE open sauc .787 is mostly known artists (builder says .84). |
| 12 | audio_final sauc .621/.633/.626, wa .598/.627/.606, gc .571/.581/.575 | full --late rerun | bit-identical to late2.log (ALL sauc .626 ci .592-.651, wa .606, gc .575, gc_wa .559) | holds |
| 13 | audio_final vs nonaudio_gbm ALL: sauc +.074 P 1.0 STRONG; wa +.055 P 1.0 STRONG; gc +.031 P .957 NONE | rerun VERDICT | matches (sauc 80% ci .044-.107, wa .025-.086, gc lo95 -.003) | holds |
| 14 | audio_final vs ca_local: sauc P .97 ALL, wa P .573 | rerun | dSAUC P .970 (lo95 -.002); ca_local vs nonaudio_gbm is also STRONG on sauc (.983) and SUGGESTIVE on wa (.967). Gain over round 1 is small and sits mostly on TUNE. | holds. The round-1 predictor already carries nearly all of the effect. |
| 15 | audio_final vs duration within artists: not beaten (ALL dWA lo95 -.037, P .80) | rerun | -0.037 / .800 | holds (the honest reading) |
| 16 | audio-taste "pool_artist_siblings sauc P=0.0, lower bound about -.30" (flagged unverified) | read the ALL dSAUC tables | Wrong column read. audio_final vs pool_artist_siblings: lo95 -0.018, P(Δ>0) = .890 on ALL. | the builder's figure doesn't hold. Corrected: P .89, lo -.018. |
| 17 | audio-taste null v2: audio_final FAILS sauc by .003 (.522 vs .519), reported honestly; random-direction calibration says 5% of random directions land outside | read null2.log, calib_randdir.py | per seed .498 / .518 / .550; log confirms the FAIL. The calibration was run against real labels, not a null, and I did not re-execute it. | the FAIL is reported accurately. The "mild chance outlier" explanation is unverified. Treat the null as FAIL. |
| 18 | audio-taste claim that the cache-key bug affected only the null control and was fixed | diff of late.log vs late2.log, predict.py key code | the real-fold output is identical. The fixed key is identity-aware (_fit key includes a hash of trackId and song). | holds. The second --late run was unnecessary but harmless; no model change followed it. |
| 19 | audio-taste 38 TUNE variants | counted model names across run1-6 | about 39 entries, including repeated final rows, consistent. Whole effort ran 09:58-10:15 UTC (about 17 min) against a stated 70 min budget, with about 30 s per batch. | holds as a count. The effort was far shorter than the brief's budget, which is plausible for cached features. |
| 20 | audio-taste: metadata adds nothing (-.004 to -.006), missing-indicator alone is chance (.518/.509/.514) | rerun | matches. Missing-indicator ALL sauc .514 (ci .500-.525) sits at the edge of the band (.472-.524); its grade is NONE and Δ vs nonaudio_gbm is negative. | holds |
| 21 | audio-taste missing-audio "excluded vs included" split | n/a | not done by the builder, and I did not run one | unverified (a gap, not a refutation) |
| 22 | audio-taste claim that audio picks up "the music" and not era (builder never tested this) | my release-age test (era.py) | Release recency alone (hidden from predictors): sauc .584 TUNE, .580 LATE, new-artist .567 / .657. audio_final's score has Spearman -0.03 with release bucket within fold, and sauc within fold x release bucket is .628 against .626 unconditioned. | audio_final survives this attack. Caveat: 88% of tried songs sit in the oldest coarse bucket, so the bucket test is weak. A day-level age test of the audio score was not run. |
| 23 | engineer: null-v2 band for history-count baselines is "probably too narrow", other checks on v3.1 | not re-run | not checked | unverified |

## Additional observations
- Under the harness's own null v2, 4 of 7 baselines FAIL. That includes duration and popularity (which use no history) and artist_plays / artist_recent. The v2 gate therefore does not cleanly certify anything, in either direction. The engineer's note that the band for artist-constant scores is too narrow is plausible but is the engineer's own unverified check.
- The headline numbers the two builders rest on (sauc .62-.63) are carried by TUNE for the integrated model, and by both slices for the audio-only model. Of the two, the audio-only model is the more robust one: positive point deltas on TUNE and LATE and above the permutation band in all three slices. The integrated model's LATE sauc (.535) is inside the band and below the history-free ablation.
- Evidence grades are brittle: integrated's sauc grade is NONE because of one negative LATE point delta (-0.005) against a P(Δ>0) of 1.0 on ALL. Under the graded scale it was meant to be lenient, so this is the grade definition doing the work and not the data.
- "Single design seen once": LATE is not untouched. The round-1 LATE results were public, and the late_runs.log now also holds the round-2 builders' runs (at least 4 more lines in this round) plus my two reruns. The sealed folds are the only untouched test.
- Neither builder's TUNE-selected final beats round-1 ca_local by more than about +0.02 sAUC (audio) or has a demonstrated advantage over duration within artists (both).

## Files
- /home/user/Listener/taste-model/predictors/w3r2-integrated/predict.py
- /home/user/Listener/taste-model/predictors/w3r2-audio-taste/predict.py, ref_ca_local.py, calib_randdir.py
- Scratch: /tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf3/da2/era.py, int_late.log, aud_late.log

## Beliefs, not run
- The audio-taste null FAIL is a chance outlier (builder's belief; calibration not re-executed).
- The pretrained-model-saw-later-songs caveat cannot be checked.
- I did not re-execute the null-control runs. My finding on the integrated seeds being identical comes from reading null.log plus the cache-key code, not from rerunning it.