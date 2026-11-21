DEVIL'S ADVOCATE ROUND 1, direction DISMISSED. Verdict: the reported scores re-run correctly. The main weakness is in what was dismissed or never tried, not in the numbers.

## What I ran (not just believed)
- Full `--late` runs (TUNE nboot 300, independence check, LATE, ALL) of all three builders' predict.py on the CURRENT pools (hash 282fcbd…). These appended 3 lines to /home/user/Listener/taste-model/.cache/late_runs.log, at 09:01, 09:03 and 09:05. The log now has extra audit lines, and training-signal's two `--late` runs now show up in it. Logs are in /tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf3/da1/ (`w3r1-*.late.log`).
- `--null-control` for all three builders (`*.null.log`).
- Four scratch predictors (blends, a rank target with recency weighting, MERT and training-signal's learned-only member) via `--fast`, TUNE only: `da1/x/da_pred.py`, `fast.log`, `fast2.log`.
- Song-content ablations `lyr_stats` and `lyr_emb` via `--fast` (`sc_abl.log`).
- Checked report claims against code and logs: extraction wall-clock times, the late_runs.log chronology, the stage tables in all_summary.txt.
- Not run: any `--sealed` run; any look at LATE with my own variants.
- No project code changed. I only wrote scratch files and deleted nothing.

## Claim table
| Claim | What I ran | Result | Verdict |
|---|---|---|---|
| content-audio TUNE: ca_local sAUC .594, wa .593, ww .600, ws .577; ca_whole .590 | full `--late` re-run | identical to 3 decimals, including every CI | holds |
| content-audio LATE: ca_local .622, wa .637, ca_whole .612 | same re-run | identical | holds |
| content-audio paired lower bounds vs nonaudio_gbm (TUNE -0.029, LATE +0.010) | read from re-run logs | consistent. On ALL 14 folds the lower bound is +0.005 (ca_local) and -0.003 (ca_whole). wa vs nonaudio on ALL is -0.002 | holds. "Not established" is fair |
| content-audio null control: all PASS, sauc .491-.509, wa .467-.482 | `--null-control` re-run | identical | holds |
| content-audio independence p90 = 0 | re-run | 0.0 | holds |
| content-audio "no BELOW CHANCE flag on any ca_* model" | grep of re-run | none flagged. Per-fold AUC is 0.38-0.52 for the first 5 folds and 0.57-0.64 from 2023-01 on. The report puts this down to noise from small folds and no investigation was done | holds, but the early-fold weakness is only explained, not tested |
| content-audio "metadata adds nothing" (-0.002 TUNE, -0.009 LATE) | read from table | confirmed from the re-run point estimates | holds (point estimates only, as the report says) |
| content-audio hl ablation: audio-only recency weighting does not help | my TUNE test: `ca.make(mode="local", target="rank", hl=120)`, a combination the builder never tried | sAUC .591, wa .556, vs ca_local .594 and .593 | holds |
| content-audio extraction times (15,838 s and 9,793 s) | build_mert*.log, shard mtimes, timestamps | consistent: first run ends 05:58, second 08:51. Cannot be checked further | holds |
| content-audio "all numbers are on the CURRENT pools" | marker file mtime 03:38, pool pickle `282fcbd…` at 03:47 | true. The engineer's report says the iTunes fill was NOT active, but the marker exists now, so the fill was completed after that report | holds. The engineer's report is stale |
| training-signal final TUNE: sauc .650, wa .594, ww .633, ws .627, new .588 | `--late` re-run on the current pool | sauc .651, wa .597, ww .637, ws .633, new .595 | holds within ≤0.007. The builder's run (logged 03:02) used the OLD pools (`a3e8…`). The pools were rebuilt at 03:47 |
| training-signal LATE: sauc .491, wa .539, ww .549, new .592; vs nonaudio -0.096 | same re-run | sauc .493, wa .545, ww .553, new .602; vs nonaudio -0.096. wa vs nonaudio is -0.068 (reported -0.076) | holds. LATE failure is real |
| training-signal lower bounds on TUNE: sauc vs nonaudio +0.042, vs artist_recent +0.011; wa vs nonaudio -0.011 | re-run | +0.039, +0.012; wa -0.015 | holds |
| training-signal null control: final FAIL (.575), learned_only PASS (.504), noaudio .573, lovetarget .557 | `--null-control` re-run | .576, .506, .574, .558. wa: final .520, learned_only .520 | holds. The harness null control is structurally strict for any artist-statistic score, which fits the builder's explanation |
| training-signal "audio adds about +0.01 sauc" | re-run: w3r1_final vs w3r1_noaudio | sauc +.006 on TUNE, lower bound -0.023 on wa. LATE shows audio helping (.493 vs .478) | holds as "within noise" |
| training-signal stage tables (targets, exposure, window) | cross-checked against all_summary.txt | numbers match the report. I did not re-run the variants | holds as transcribed, unverified as re-runs |
| training-signal "about 300 variants" | counted result lines in all_summary.txt | about 181 result lines | unverified. Not contradicted |
| training-signal "exposure handling doesn't help" | stage tables | all methods within ±0.02, all tested only with HGB on about 600 rows and weighting or dropping of history rows | holds weakly. A weak test, not a strong negative |
| song-content TUNE: nodur .560 / wa .595, orth .567 / .598, lyr_all .569 / .584 | re-run | identical, all CIs too | holds |
| song-content LATE: nodur sauc .454, new .404; orth .540; lyr_all .536 | re-run | identical (nodur sauc .454, wa .488, ww .447) | holds |
| song-content null: nodur PASS, orth FAIL (wa .433), lyr_all FAIL | re-run | identical | holds |
| song-content seed-noise explanation (null spread 0.46-0.54) | not re-run (null_seeds.py) | none | unverified. The "FAIL is just an unlucky draw" reading is therefore unverified |
| song-content ablations: lyr_emb sauc .524 / wa .523 | `--fast` | .524 / .523 | holds |
| song-content: stats with duration-derived columns scored wa .604 and was dropped | `lyr_stats` `--fast` (`lyr_all` minus embedding, includes duration-derived columns) | sauc .561, wa .581, new .580 | partly holds. wa .604 from the earlier variant is unverified, because that variant's code was deleted |
| song-content "nodur's own per-fold stability was not examined" | grep of BELOW CHANCE in re-run | the harness flags lyr_resid_nodur fold 2022-07 on ALL (AUC .422, CI upper .485). The report does not mention it | doesn't hold as written. The below-chance fold exists in the harness output and was not investigated |
| song-content has-lyrics indicator: 0.499 TUNE, 0.505 LATE | re-run | identical | holds |
| Engineer v3 numbers (artist baselines above chance on TUNE, not on LATE) | read from re-run logs | .619 / .619 on TUNE; .454 / .436 on LATE; artist_plays 2024-04 flagged | holds |

## What was dismissed or never tried (the main attacks)
1. **Audio was never combined with artist-history models properly.**
   - content-audio was barred from artist and history inputs. training-signal used only 5 CLAP similarity features and never used MERT.
   - My first-attempt test (TUNE `--fast`, fixed, not tuned) averaged z-scores of ca_local and training-signal's `w3r1_learned_only`:
     - sAUC .666 (.615, .708), wa .633 (.581, .676), ww .657, ws .624, new-artist .604.
     - Paired lower bounds vs nonaudio_gbm: sAUC +0.051, wa +0.020. It is the first wa lower bound above 0 in this project.
     - vs artist_recent: sAUC +0.011. vs w3r1_learned_only alone: sAUC -0.006, wa +0.012.
   - Reading: the audio adds at most a small amount to the strong learned model. Combining it was never tested by any builder.
   - Caveats:
     - TUNE only. LATE was not run, and it would be a logged extra look.
     - The blend z-scores over the candidate set, so it would fail the independence check. A train-fitted standardiser is needed (training-signal already does this).
     - Only about 4 variants were tried.
2. **The audio models' LATE gain is mostly weak baselines, not strong audio.** artist_recent is at .436 on LATE. Audio beats nonaudio_gbm on LATE by only +0.010 (lower bound). ca_local's ALL-slice lower bound vs nonaudio_gbm is +0.005.
3. **Within-artist (wa) is not clean.** A one-feature duration baseline gets wa .607 on TUNE, higher than every audio or lyric model (.584-.598) and higher than meta_gbm .577. Every "within-artist signal" claim is statistically indistinguishable from duration. Paired lower bounds vs duration on TUNE are negative for all models: audio -0.067 on wa, lyrics -0.054 to -0.068.
4. **Training-signal's LATE collapse comes from a design choice, not from the target.**
   - Monotone familiarity constraints and the artist_recent member (weight 2) cannot learn the sign flip. On LATE, learned_only (no artist_recent) is .535 vs nonaudio .540, and the final is .493.
   - On ALL 14 folds, learned_only has sAUC .604 with lower bound +0.013 vs nonaudio_gbm, but ALL includes the TUNE it was selected on.
   - A free-sign or recency-only familiarity variant was proposed by the builder and never run.
5. **Song-content never ran the combined audio+lyrics variant or the metadata variant.** The primary model was chosen for "cleanliness" before it was known to fail on LATE.
6. **Comparability.** Training-signal ran on the old pools, the other two on the new ones. The engineer's report says the iTunes fill was not active, but the marker and the new pools now exist (marker mtime 03:38). The numbers I re-ran move by ≤0.007, so this does not change any conclusion.
7. **Null control.** The identity shuffle keeps per-artist song counts, so any artist-statistic score "fails" (artist_recent scores .602). A label-only permutation would be a stricter test of artist-free models. That is an evaluation design flaw, not a predictor flaw.

## Effort claims checked against files
- content-audio's wall-clock figures match logs and shard timestamps.
- Its ablation tables are reproducible only by `ablations.py`, which I did not re-run.
- Training-signal's chronology is consistent. The null2 run finished 03:02:17, the `--late` run was logged 03:02:24, and the stage logs end before that.
- The "about 300 variants" count is unverified (181 result lines).
- None of the above used the sealed data.

## Files
- /tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf3/da1/ (logs and `x/da_pred.py`)
- /home/user/Listener/taste-model/.cache/late_runs.log (3 audit lines added)