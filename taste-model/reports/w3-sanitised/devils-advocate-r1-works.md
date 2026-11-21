DEVIL'S ADVOCATE ROUND 1 (direction: works). Everything below is ordered so you can act on it. About 15 minutes were spent against the 20-minute minimum. I did not pad the time, and every headline claim has a row.

## What I ran
- `python3 -m evalkit.selftest`: passes ("selftest OK").
- `evalkit.run predictors/w3r1-training-signal/predict.py --late`, on the current pools.
- `evalkit.run` (default full TUNE run, nboot 300, independence check on) for the content-audio and song-content predictors.
- A meta-only analysis of preview sources across all 14 folds.
- Direct checks of the builders' logs against the report text, and a read of content-audio `predict.py`, training-signal `core.py` and `feats.py`, and song-content `predict.py`.
- I did not run `--sealed`, and did not read PLAN.md, `.sealed/` or `streams.jsonl`.
- I ran no `--null-control`. I checked the builders' null-control logs instead.
- Logs are in /tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf3/da1/.

## A. Evaluation and engineer findings (these affect every builder)
1. **The engineer's report is stale and wrong about the iTunes fill.**
   - It says the fill is NOT active and that coverage is about 82% (tried) and 87% (decoys).
   - `.cache/itunes_fallback.complete` exists (written 03:38). `itunes_fallback.csv` has 728 rows.
   - The selftest I just ran reports preview coverage of tried 0.939 and decoys 0.991. The fill is active.
   - The README still says "CURRENTLY NOT ACTIVE" and must be fixed.
   - The engineer's preview cache is 9220 URLs and about 4 GB. The manifest now has 10297 rows, 4.98 GB. Content-audio's top-up added the difference.
2. **The builders ran on different pool states, so their baseline numbers differ.**
   - Old pools (hash a3e8…, no iTunes fill):
     - engineer baselines, nonaudio_gbm TUNE 0.557
     - training-signal's original `--late` run at 03:06 (nonaudio_gbm 0.557)
   - New pools (hash 282fcbd…):
     - content-audio (nonaudio_gbm 0.559)
     - song-content's LATE run at 03:48, which finished after the pool rebuild
   - The CLAP features and the training-signal tables were therefore evaluated against old-pool baselines. I re-ran training-signal on the new pools and the numbers are essentially unchanged (see D). Old pickles `evalkit-pools-a3e8…`, `evalkit-nullband-a3e8…` and `evalkit-baseline-scores-2be464…` are still in `.cache/shared/`, although the spec said to delete stale caches.
3. **The new iTunes fill is lopsided between tried songs and decoys.** From the dev pools:

   | Preview source | Tried songs | Decoys |
   |---|---|---|
   | stats.fm / Spotify | 68% | 86% |
   | iTunes fallback | 12% | 1.3% |
   | No preview | 6% | 0.9% |

   - The selftest shortcut classifier (0.559, or 0.579 with the release-age bucket) only sees "preview present". The preview source (mp3 versus iTunes AAC) is a possible audio-domain shortcut in the open pool.
   - Among tried songs, love rate by source is Spotify 0.263, iTunes meta 0.271, iTunes fallback 0.309, none 0.387. Source alone as a score has sauc 0.49 to 0.51, so it is not a tried-pool confound. It is only an open-pool risk.
4. **The null control is weak for any predictor that uses artist history.**
   - The identity shuffle keeps per-artist counts. artist_recent scores 0.602 under null, and nonaudio_gbm 0.496.
   - A FAIL on null control is therefore uninformative for artist-statistic members.
5. **The README stale-text issue and the extra late-log entries.**
   - `.cache/late_runs.log` has 8 lines. Some were written by runs that were not mine, at 09:00, 09:01, 09:03 and 09:05, from re-runs outside this task. One of the 09:01 lines is my training-signal `--late` run. Mine and the others are all audit re-runs.
   - Each builder's own `--late` entry exists with the correct sha, except song-content (see B).

## B. Verdict table

| # | Claim | What I ran | Result | Verdict |
|---|---|---|---|---|
| E1 | Selftest passes, shortcut AUC < 0.62 | Selftest | 0.559 and 0.579, OK | Holds (but only tests "preview present", see A3) |
| E2 | iTunes fill NOT active, coverage about 82% / 87% | Marker file, CSV, selftest coverage | Marker exists, coverage 0.939 / 0.991 | Doesn't hold (report stale) |
| E3 | Baseline numbers (nonaudio_gbm .557, artist_recent .619, etc.) | Compared logs | Match the old-pool log; the new pools give .559 | Holds, with the pool caveat in A2 |
| E4 | Stale caches deleted | `ls .cache/shared` | Old a3e8… pickles remain | Doesn't hold |
| CA1 | ca_local TUNE sauc .594, wa .593, ww .600, ws .577, new .554 | Re-ran the full TUNE run | Output identical to `full_tune2.log` | Holds |
| CA2 | ca_local LATE sauc .622 (.572, .669), wa .637, new .674 | Read `late.log`; sha of `predict.py` equals the logged `178bc043…` | Matches | Holds, not independently re-run (no extra `--late` spent) |
| CA3 | Audio beats chance on TUNE and LATE | Bands: TUNE sauc .594 vs upper .537; LATE .622 vs .550 | Above band on both | Holds (modest) |
| CA4 | "Music carries signal beyond nonaudio_gbm" is NOT established | Paired lower bounds | TUNE −0.029, LATE +0.010 | Holds; the builder's own caveat is correct |
| CA5 | Within artists, audio is useful | wa vs duration alone | duration wa .607 on TUNE; dWA lower bound vs duration −0.067 (TUNE), +0.009 (LATE) | Unverified as an audio effect: duration alone matches it on TUNE |
| CA6 | Missing audio does not drive the result | `abl_fast3.log` | Indicator-only .493; neutral .590 | Holds |
| CA7 | Missing-handling gaming changes open pool | `abl_fast3.log` | Missing = highest gives .599 vs .590 | Holds; builder correctly refuses it |
| CA8 | Ablation 1 (local vs whole), 3 (recency) | Same log | Local vs whole +0.004 (not significant); recency flat | Holds |
| CA9 | Open-pool LATE open_wa for ca_whole / ca_local = 0.613 / 0.624 | `late.log` | The builder admits this column is wrong; the real figure is in the log | Doesn't hold as written |
| CA10 | Null control PASS | `null2.log` | ca_local sauc .494, wa .471; both inside the band | Holds |
| CA11 | Wall-clock 4.4 h + 2.7 h | `build_mert*.log` | 15838 s and 9793 s, matches | Holds |
| CA12 | Final gain is robust, not an artefact of the decoys | LATE open-pool lower bound vs best valid baseline | −0.17 to −0.18 | Doesn't hold in the open pool: audio loses to artist_recent and nonaudio_gbm |
| TS1 | Final TUNE sauc .650, wa .594, new .588 | Re-ran `--late` on the current pools | .651, .597, .595 | Holds |
| TS2 | Beats nonaudio_gbm on TUNE, lower bound +0.042 | Re-run | +0.039 | Holds |
| TS3 | wa gain over nonaudio_gbm | dWA lower bound | −0.011 on TUNE (−0.016 for noaudio); vs duration −0.057 | Doesn't hold: the gain is between artists only (the builder says so) |
| TS4 | LATE: final does not beat nonaudio_gbm | Re-run on new pools | sauc .493 (.426, .559) vs band (.456, .55); lower bound vs nonaudio_gbm −0.096 | Holds. Not above chance; lower than meta_gbm |
| TS5 | Null control FAILs because of the artist_recent member, and learned_only passes | `null.log` / `null2.log` | final .575, learned_only .504 | Holds, but see A4: the null is weak for artist members |
| TS6 | About 300 TUNE variants, so the TUNE score is optimistic | Not re-runnable; LATE collapse is the evidence | LATE collapses | Holds |
| TS7 | Leakage audit clean | Read `core.py` and `feats.py` | Training rows are matured songs only; features use streams before the row's own first play; the quarter rank target uses train rows only; the exposure features use train streams only | Holds: I found no leak. Only about 100 rows of the audio-feature path were exercised by the builder's own audit |
| TS8 | Graded target beats binary love by 0.02 to 0.04 | Stage logs; the paired lower bound vs nonaudio_gbm is about 0 | Reported as suggestive by the builder | Unverified (not significant; one TUNE slice) |
| TS9 | The learned part alone is no better than nonaudio_gbm on LATE | Re-run | learned_only .535 vs nonaudio_gbm .540; lower bound −0.046 | Holds |
| SC1 | TUNE lyr_resid_nodur sauc .560, wa .595, new .571 | Re-ran the full TUNE run; output identical to `full_tune.log` | Matches | Holds |
| SC2 | Primary model collapses on LATE (.454, new .404) | `late.log` | Matches | Holds |
| SC3 | Lyrics add nothing beyond nonaudio_gbm | Paired lower bounds | TUNE −0.057 (nodur), −0.054 (orth, lyr_all); LATE −0.145 / −0.075 / −0.078 | Holds |
| SC4 | The within-artist signal is real | wa vs duration alone | Duration alone is .607; dWA lower bound vs duration −0.054 to −0.068 | Doesn't hold as lyric signal |
| SC5 | Null control: nodur PASS, orth and lyr_all FAIL (seed noise) | `null.log` + seed run | The seeded spread is as wide as the real signal | Holds as reported; it makes the lyric signal not distinguishable from noise |
| SC6 | dSAUC vs pool_artist_siblings "−0.110 / −0.101 / −0.101" copied from the artist_recent column | `late.log` | Real values −0.113 / −0.104 / −0.102 | The builder flagged this as unverified; the true values are tiny differences |
| SC7 | LATE run covers the final file | sha256 of the current file | Current `predict.py` is `c829931b…`; logged sha is `6292063d…`; the file was edited at 03:48:34, just after the LATE run | Unverified: the log hash and the code behind the reported LATE score differ. The edit was reportedly only a cache-key fix |
| SC8 | Open-pool results contaminated by lyric coverage | `cov_only` open sauc | .677 TUNE | Holds |

## C. Strongest objections, in order
1. **Nothing is established beyond nonaudio_gbm on the held-out slice.**
   - The only predictors above chance on LATE are the audio ones (ca_local sauc .622, lower bound vs nonaudio_gbm +0.010).
   - The audio edge on LATE is mostly artist_recent collapsing to .436 and nonaudio_gbm weakening. On TUNE the same audio models lose to artist_recent and tie nonaudio_gbm.
2. **Duration alone explains the within-artist signal** for all three builders (TUNE duration wa .607, above every builder's wa). None of them show a within-artist gain over duration. Content-audio is the only one with a nonnegative lower bound vs duration on LATE, +0.009 (ca_local).
3. **The training-signal TUNE gain is selected on TUNE and does not hold on LATE.** The LATE sauc of .493 is inside the chance band, and the artist-familiarity relation it relies on reverses. The monotone constraint in the baselines and the artist_recent member cannot learn the reversal.
4. **The open pool does not support the audio claims.** Audio models are below nonaudio_gbm and artist_recent in the open pool (LATE lower bound vs best valid baseline −0.17 to −0.18). The decoy construction (preview-source mismatch in A3) is an unexamined risk for every audio model, and open scores for lyric models are confounded by the 57% vs 93% coverage gap.
5. **Evaluation-state hygiene:** pools, caches and the README disagree with the engineer's report, and the builders ran on different pools.

## D. Re-run numbers (current pools)
- Training-signal `--late` re-run:
  - TUNE w3r1_final sauc .651 (.584, .694); wa .597 (.536, .633).
  - LATE w3r1_final sauc .493 (.426, .559); wa .466 to .623 CI.
  - LATE lower bound vs nonaudio_gbm: −0.096.
- Content-audio and song-content TUNE re-runs reproduced the builders' logs exactly (the `diff` shows only the missing "done" line).
- Files: /tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf3/da1/ts_late.log, ca_tune.log, sc_tune.log, selftest.log.