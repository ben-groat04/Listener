REPORT: w3r2-integrated (builder round 2). Code: /home/user/Listener/taste-model/predictors/w3r2-integrated/predict.py (single file, imports the w3r1-training-signal and w3r1-content-audio code unchanged; usage line in its docstring). No new per-track caches were created; it reuses the shared MERT and CLAP caches. Logs: /tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf3/integrated/ (v1-v3.log, full_tune.log, null.log, late.log). I did not git commit.

## Final model (pre-declared before any --late run)
`w2i_final` = equal-weight blend (1,1,1,1) of four members. Each member is standardised with the mean/std of its OWN scores on TRAINING songs only, so scoring is candidate-independent.
- H: HistGradientBoosting on the nonaudio_gbm feature set. The target is the within-quarter percentile of plays90 (graded, period-normalised). Rows are songs first played in the last 365 d, with a 120 d half-life weight. Only songs whose 90-day horizon is complete before the cutoff are used. Monotone constraints on the artist-familiarity features.
- HA: H plus CLAP similarity features (similarity to loved/dismissed songs of the last 450 d, and to recent listening).
- A: artist-free MERT-95M audio ensemble, local windows, 3 layer groups, trained on the love label. It is the round-1 `ca_ens` code. A song with no audio gets the train-derived neutral value.
- AR: artist_recent, the plain frequency statistic.

Named ablations:
- `w2i_noaudio` = blend of H and AR (1,1): no MERT member and no CLAP features.
- `w2i_nohist` = A alone: no artist or history input of any kind. Its training labels still come from pre-cutoff streams.
- Extra diagnostic (not a model): `w2i_missing_only`, the audio-missingness indicator alone.

## Variant count
11 variants scored on TUNE with --fast. They are listed here.
1. hist_audio (H, HA, 2A)
2. hist_audio_ar (H, HA, 2A, AR)
3. audio only (A)
4. hist only (H, HA)
5. A with meta columns + AR
6. A with a rank target + AR
7. AR weight 2
8. A weight 3 + AR
9. equal weights (this became the final)
10. G, A, AR
11. Ga, A, AR

TUNE sAUC for these ran from 0.643 (hist only) to 0.667. Among variants that contain audio, history and AR it was 0.655-0.667, which is within noise. I picked the equal-weight one as the least tuned, not the TUNE maximum. The 4 final-run entries are separate from the 11 and add nothing new on TUNE; `w2i_nohist` equals variant 3 (0.584) and `w2i_noaudio` is a new combination that was only scored in the full run. Treat the count as 11 + 1 ablation combination = 12. Failed attempts: all variants were entries in one file; the 7 not used were removed from predict.py. There are no other files to delete.

## Results (full harness run, nboot 300; independence p90 = 0.0 for all my models on TUNE and LATE)
TUNE (10 folds). Null-control permutation bands in brackets.

| model | sauc [.459-.537] | wa [.448-.552] | ww | ws | new-artist | gc [.474-.525] | gc_wa [.468-.534] | plift | sp share90 |
|---|---|---|---|---|---|---|---|---|---|
| final | .667 (.602-.707) | .615 (.542-.658) | .650 (.576-.713) | .633 (.49-.729) | .618 (.541-.685) | .622 (.575-.65) | .577 (.518-.609) | 1.51 | .247 |
| noaudio | .645 | .603 | .627 | .614 | .564 | .614 | .574 | 1.50 | .261 |
| nohist | .584 | .568 | .600 | .571 | .566 | .541 | .536 | 1.27 | .019 |

LATE (4 folds, 2024). Bands: sauc .456-.550, wa .451-.565, gc .469-.527, gc_wa .463-.540.

| model | sauc | wa | ww | ws | new-artist | gc | gc_wa | plift | sp share90 |
|---|---|---|---|---|---|---|---|---|---|
| final | .535 (.480-.602) | .583 (.528-.635) | .595 | .624 | .646 (.569-.744) | .541 (.495-.589) | .537 (.487-.59) | 1.07 | .101 |
| noaudio | .478 | .517 | .538 | .559 | .636 | .508 | .511 | 1.03 | .018 |
| nohist | .594 (.543-.641) | .626 (.543-.694) | .596 | .594 | .610 | .558 | .582 | 1.43 | .157 |

ALL (14 folds). Bands: sauc .472-.524, wa and ww not re-quoted here, gc .479-.518.

| model | sauc | wa | ww | ws | new-artist | gc | gc_wa | plift | sp share90 |
|---|---|---|---|---|---|---|---|---|---|
| final | .616 (.558-.660) | .607 (.555-.644) | .629 | .630 | .627 (.570-.679) | .590 (.546-.623) | .565 (.526-.596) | 1.37 | .206 |
| noaudio | .580 | .581 | .593 | .594 | .587 | .573 | .556 | 1.35 | not extracted |
| nohist | .588 | .583 | .599 | .579 | .580 | .547 | .549 | 1.32 | not extracted |

Baselines (ALL sauc / wa):
- nonaudio_gbm .551 / .551
- duration .561 / .588
- meta_gbm .535 / .565
- artist_recent .548 / .499

Missingness-only (preview present or not, no content): TUNE .493, LATE .516, ALL .502 sauc. It is chance-level, so the missing-audio indicator is not what drives the result. Missingness is explicit: the A member uses a neutral value, and HA has an `au_missing` flag.

### Paired deltas of the final vs baselines (P(d>0); lower bounds are 95% for sAUC)
| vs | sAUC TUNE | sAUC LATE | sAUC ALL (lo95) | wa ALL | gc ALL |
|---|---|---|---|---|---|
| nonaudio_gbm | 1.00 | .44 | 1.00 (+.018) | .98 | .997 |
| meta_gbm | 1.00 | .43 | .997 (+.021) | .98 | .997 |
| duration | 1.00 | .27 | .96 (-.003) | .81 | .98 |
| artist_recent | 1.00 | 1.00 | 1.00 (+.041) | 1.00 | 1.00 |
| pool_artist_siblings (diagnostic, uses post-cutoff information) | .98 | .50 | .87 (-.027) | 1.00 | gc P .40 |

Evidence grades vs nonaudio_gbm: sauc NONE under the harness rule (the LATE point delta is negative: -0.005 vs nonaudio_gbm), wa STRONG, gc STRONG. 'dWA vs best meta' on ALL is vs duration: +0.008 (the lo95 is shown only in the log), P(d>0) = 0.81. So within-artist ordering is not clearly beyond duration alone.

### Source ablations: the contribution of each source depends on the slice
- TUNE: removing audio costs .022 sauc (.667 -> .645). Removing history costs .083 (.667 -> .584).
- LATE: removing audio costs .057 (.535 -> .478, below chance for the history-only blend). Removing history GAINS .059 (.535 -> .594).
- ALL: removing audio costs .036 (.616 -> .580). Removing history costs .028 (.616 -> .588).
- The audio-removed blend vs nonaudio_gbm on LATE: dSAUC P(d>0) = 0.20.

### Open pool (sauc, open_wa, p20)
| slice | model | open_sauc | open_wa | p20 |
|---|---|---|---|---|
| TUNE | final | .787 (.717-.831) | .609 | .345 |
| TUNE | artist_recent | .747 | - | .394 |
| TUNE | nonaudio_gbm | .609 | - | .145 |
| LATE | final | .675 (.624-.745) | .608 | .175 |
| LATE | artist_recent | .640 | - | .136 |
| LATE | nonaudio_gbm | .592 | - | .100 |
| ALL | final | .745 (.687-.789) | .609 | .296 |
| ALL | artist_recent | .707 | - | .320 |
| ALL | nonaudio_gbm | .602 | - | .132 |

Open-pool new-artist sauc for the final is .586 on TUNE, .653 on LATE and .608 on ALL, against .47-.57 for nonaudio_gbm. The open-pool sauc of the final is driven largely by known artists (.84 on TUNE), as it is for artist_recent.

### Null control v2 (TUNE, three seeds; band of the 3-seed mean: sauc .475-.519, wa .476-.533, new .454-.536)
| model | sauc s1/s2/s3 -> mean | wa mean | new mean | outcome |
|---|---|---|---|---|
| w2i_final | .509/.497/.539 -> .515 | .518 | .477 | PASS |
| w2i_noaudio | mean .517 | .528 | .487 | PASS |
| w2i_nohist | .505 | .478 | .455 | PASS |
| w2i_missing_only | .487 | .491 | .473 | PASS |

For the final, all three means lie in their bands, so no member needs explaining. Per-seed wa for the final is .523/.529/.503 and new-artist .492/.404/.536. The nohist member is history-free, so its PASS only shows that its label training does not leak.

### Below-chance folds (these are flags from the harness)
- artist_plays, fold 2024-04: AUC .407. The sign of artist familiarity reverses in that fold, as the lead described for the LATE fade.
- popularity, fold 2023-04: AUC .403.
- w2i_missing_only, fold 2022-07: AUC .445.

I did not run a deeper cause analysis on these. For the last one: the diagnostic is constant per audio availability, and this is one small fold with pooled sauc .493. No fold of my final model or either ablation is flagged below chance.

## Did the design react to the LATE fade?
Yes, partly, and this was decided with the lead's fact in view, not from my own LATE look. I gave the plain artist-familiarity member AR weight 1 of 4 (round 1 had 2 of 4) and added a history-free audio member. The only TUNE evidence is that variants with AR weight 2 (.664) and weight 1 (.667) were tied (no preference). I did not measure the fade inside pre-cutoff windows. That justification is therefore missing and I flag it as a weakness.

## What I ran vs what I believe
Ran: the 12 TUNE variants above, one full TUNE+LATE+ALL run (`--late`, one run for all four entries, no model change after seeing LATE), and one null-control run. The full TUNE independence check ran inside the `--late` run (I did not run a separate full TUNE-only pass). Only one --late run was made, so no bug-fix rerun was needed.
Believed, not shown:
- The audio signal is real rather than a proxy for release era or sound-alike artists (the null-control and the missingness-only check support no history leakage, nothing more).
- LATE failure of history features is a time-varying familiarity effect.

## Strongest case against my result
- LATE sauc for the final is .535 (CI .480-.602): not above chance and below nonaudio_gbm's .540, duration's .564 and meta_gbm's .548. The headline ALL .616 is carried by TUNE (.667), where the history members dominate.
- On LATE the history-free audio ablation (.594) beats the final. So the integrated blend is the weaker choice on the held-out slice, and the history inputs hurt there. A history-free audio model is the one with demonstrated stability, but it is only SUGGESTIVE on wa (P .93 on LATE) and gc (P .91), and it does not beat nonaudio_gbm on TUNE sauc (P .71). The audio-vs-duration question is unresolved: duration alone has wa .607 on TUNE.
- The sauc grade is NONE vs nonaudio_gbm, and ALL vs duration has lo95 -.003.
- The blend's equal weights were chosen partly knowing the round-1 result; the 12-variant TUNE search is small but not free.
- LATE is a seen-once-per-design slice; the sealed folds remain the only untouched test.

## Leakage self-audit
- Training labels come from train streams only, and only songs with a complete 90-day horizon are training rows (round-1 `core.build` code).
- Every fitted object (GBM, PCA, standardisers, logistic) is fit on songs in the cutoff's train streams. Member standardisation uses training rows only.
- The shared MERT and CLAP caches are per-track and independent. Harness independence p90 = 0.0.
- I never read sealed data, streams.jsonl, listening_stats.csv or decoy files, and never used exposure context.
- Pretrained audio models may have seen later songs (a known limit stated in the README).
- A caveat: preview availability could correlate with taste. The missingness-only diagnostic shows it does not drive the result.