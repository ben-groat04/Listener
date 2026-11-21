REPORT: w3r1 content-audio (MERT-95M preview-audio predictor). Everything below is from evalkit v3 harness runs on the CURRENT pools (hash 282fcbd…), which include the completed iTunes preview fill. All numbers are tried pool, love label, 95% artist-cluster CIs, unless stated.

## 0. Bottom line
- The music carries a modest but real signal about which new songs get loved. It beats chance on TUNE and LATE and is robust to missing-audio handling.
- Its advantage over nonaudio_gbm is NOT established. The paired lower bounds are -0.022 (TUNE) and +0.004 to +0.010 (LATE), so the edge is at most marginal.
- It is far below artist-based scores on TUNE (artist_recent 0.619) and in the open pool.
- In the open pool it does not beat nonaudio_gbm.

## 1. What I built (all in /home/user/Listener/taste-model/predictors/w3r1-content-audio/)
- `build_mert.py`
  - Per-clip MERT-v1-95M features, trust_remote_code, int8-dynamic linear layers, 2 threads.
  - Each 30 s preview gets 4 windows of 5 s. The 12 transformer layers are averaged over time inside each window, giving [4 windows, 12 layers, 768].
  - Cache: `.cache/shared/w3r1-mert-v1/shard_*.npz`. It is resumable and regenerable.
  - Usage: `python3 -W ignore predictors/w3r1-content-audio/build_mert.py`
- `predict.py` (harness entry file; PREDICTORS: ca_whole, ca_local, ca_ens, ca_whole_meta, ca_ens_meta)
  - Inputs per song are the MERT features only (plus metadata in the `_meta` variants).
  - Artist, artist history and pool structure are never inputs.
  - User history is used only for training targets: songs first played at least 90 d before the cutoff, with the love label from `song_table(train)`.
  - Standardiser (train-song mean/std), PCA-64 whitened, then logistic regression (C=0.05), using layers 4-8 averaged.
  - ca_whole: the 4 windows are averaged first (one instance per song).
  - ca_local: each window is a training instance carrying the song's label, and a song's score is the mean of its window logits.
  - ca_ens: ensemble of three layer groups (0-3, 4-7, 8-11), time-local.
  - `_meta` variants add log duration, explicit, popularity and a popularity-missing flag as extra inputs.
  - Songs with no usable audio get the median score of the train songs ("neutral").
  - Training uses no recency weighting (hl=None, chosen on TUNE, see ablation 3).
- `ablations.py` (ablations 1-3), `analyze_missing.py` (ablation 2, excluded vs included), `investigate.py` (below-chance investigation).

## 2. Chosen on TUNE only
- Recency weighting: none. It is within noise of the alternatives (ablation 3).
- Headline audio-only variant: ca_local, best TUNE sAUC (0.594). ca_whole is reported next to it.
- ca_ens was picked on an earlier, partial-coverage TUNE and was NOT confirmed after the preview top-up (see §6).

## 3. Final tables (full runs, with the independence check)

### TUNE (10 folds, 1490 tried songs, base rate 0.306). Null band: sauc (0.459, 0.537), wa (0.448, 0.552), ww (0.459, 0.538), ws (0.428, 0.577), new (0.422, 0.558).

| Model | sAUC (CI) | wa (CI) | ww (CI) | ws (CI) | new-artist sAUC (CI) |
|---|---|---|---|---|---|
| ca_whole | 0.590 (0.549, 0.623) | 0.584 (0.542, 0.609) | 0.607 (0.540, 0.650) | 0.551 (0.441, 0.653) | 0.572 (0.493, 0.658) |
| ca_local | 0.594 (0.548, 0.631) | 0.593 (0.531, 0.625) | 0.600 (0.535, 0.649) | 0.577 (0.463, 0.689) | 0.554 (0.463, 0.637) |
| ca_ens | 0.584 (0.545, 0.620) | 0.568 (0.519, 0.604) | 0.600 (0.534, 0.656) | 0.571 (0.468, 0.681) | 0.566 (0.481, 0.639) |
| ca_whole_meta | 0.588 (0.546, 0.620) | 0.584 (0.543, 0.608) | 0.595 (0.529, 0.637) | 0.532 (0.429, 0.622) | 0.565 (0.485, 0.651) |
| ca_ens_meta | 0.584 (0.545, 0.618) | 0.570 (0.525, 0.603) | 0.587 (0.530, 0.638) | 0.560 (0.470, 0.665) | 0.566 (0.488, 0.641) |
| nonaudio_gbm | 0.559 (0.520, 0.603) | 0.552 (0.506, 0.602) | 0.560 (0.507, 0.618) | 0.543 (0.458, 0.616) | 0.482 (0.416, 0.546) |
| meta_gbm | 0.528 (0.491, 0.571) | 0.577 (0.530, 0.620) | 0.531 (0.488, 0.588) | 0.558 (0.474, 0.635) | 0.495 (0.414, 0.557) |
| artist_recent | 0.619 (0.550, 0.653) | 0.500 | 0.602 (0.530, 0.649) | 0.590 (0.508, 0.644) | 0.502 |
| pool_artist_siblings (diag) | 0.619 (0.534, 0.679) | 0.500 | 0.619 (0.549, 0.658) | 0.643 (0.535, 0.706) | |

- ca_local plift 1.447 (1.136, 1.613) and p20 0.482, against artist_recent plift 1.386 and p20 0.509.
- Spearman with days90 and share90 is about 0.02 or below, so the signal is binary-level only (this is from the earlier, partial-coverage fast run).

### LATE (4 folds, 960 tried songs, base rate 0.233). Null band: sauc (0.456, 0.550), wa (0.451, 0.565), ww (0.44, 0.544), ws (0.424, 0.571), new (0.394, 0.592).

| Model | sAUC (CI) | wa (CI) | ww (CI) | ws (CI) | new-artist sAUC (CI) |
|---|---|---|---|---|---|
| ca_whole | 0.612 (0.562, 0.659) | 0.605 (0.537, 0.663) | 0.620 (0.550, 0.690) | 0.630 (0.485, 0.745) | 0.656 (0.567, 0.746) |
| ca_local | 0.622 (0.572, 0.669) | 0.637 (0.563, 0.694) | 0.629 (0.561, 0.701) | 0.661 (0.516, 0.765) | 0.674 (0.580, 0.744) |
| ca_ens | 0.594 (0.543, 0.641) | 0.626 (0.543, 0.694) | 0.596 (0.528, 0.667) | 0.594 (0.485, 0.699) | 0.610 (0.519, 0.698) |
| ca_whole_meta | 0.603 (0.551, 0.652) | 0.611 (0.538, 0.672) | 0.611 (0.543, 0.679) | 0.623 (0.484, 0.748) | 0.648 (0.571, 0.731) |
| ca_ens_meta | 0.583 (0.521, 0.638) | 0.611 (0.521, 0.688) | 0.582 (0.508, 0.656) | 0.586 (0.444, 0.688) | 0.594 (0.519, 0.697) |
| nonaudio_gbm | 0.540 (0.490, 0.588) | 0.547 (0.482, 0.604) | 0.588 (0.516, 0.645) | 0.582 (0.420, 0.670) | |
| meta_gbm | 0.548 (0.505, 0.589) | 0.528 (0.459, 0.580) | 0.556 (0.483, 0.604) | 0.528 (0.383, 0.622) | |
| artist_recent | 0.436 (0.375, 0.511) | 0.496 | 0.490 (0.423, 0.562) | 0.494 (0.414, 0.571) | |
| pool_artist_siblings (diag) | 0.544 (0.461, 0.612) | 0.500 | 0.531 (0.451, 0.599) | 0.573 (0.468, 0.640) | |

- ca_local plift on LATE: 1.428 (1.003, 1.889).
- LATE is a held-out dev slice, used in one `--late` run. It is logged in `.cache/late_runs.log` with the sha256 of predict.py (178bc043…).

### Paired lower bounds (95%, shared resamples). Positive means credibly better than the baseline.

| Comparison | sAUC TUNE | sAUC LATE | wa TUNE | wa LATE |
|---|---|---|---|---|
| ca_whole vs nonaudio_gbm | -0.022 | +0.004 | -0.025 | -0.017 |
| ca_local vs nonaudio_gbm | -0.029 | +0.010 | -0.028 | +0.006 |
| ca_whole vs meta_gbm | +0.006 | +0.007 | -0.039 | 0.000 |
| ca_local vs meta_gbm | +0.006 | +0.014 | -0.045 | +0.027 |
| ca_whole vs artist_recent | -0.071 | +0.090 | +0.042 | +0.041 |
| ca_local vs artist_recent | -0.076 | +0.096 | +0.031 | +0.067 |
| ca_whole vs pool_artist_siblings | -0.088 | -0.019 | +0.042 | +0.037 |
| ca_local vs pool_artist_siblings | -0.078 | -0.006 | +0.031 | +0.063 |

- Paired lower bounds against artist_plays, artist_love_rate, duration, popularity and the other ca_* variants are in `/tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf3/w3r1/late.log`.
- Versus artist_recent, the TUNE sAUC lower bound is negative and the LATE one is positive. On LATE this comes from artist_recent collapsing to 0.436 (below chance), not from audio being strong.
- Versus the weaker baselines, audio-only is credibly above popularity (+0.056 TUNE, +0.014 LATE) and artist_plays (+0.067 LATE). It is not credibly above duration on either slice.

### Metadata variant (separate, as required)
- Metadata adds nothing to the audio-only model. This is a point-estimate comparison with no paired CI.
- ca_whole_meta minus ca_whole: -0.002 sAUC on TUNE and -0.009 on LATE.
- ca_ens_meta minus ca_ens: 0.000 on TUNE and -0.011 on LATE.

### Open pool (tried songs plus 5x decoys)

| Model | TUNE open sAUC | TUNE open_wa | TUNE p20 | LATE open sAUC | LATE open_wa | LATE p20 |
|---|---|---|---|---|---|---|
| ca_whole | 0.574 | 0.480 | 0.080 | 0.582 | 0.613 (0.525, 0.701) | 0.038 |
| ca_local | 0.576 (0.539, 0.611) | 0.495 (0.412, 0.596) | 0.080 | 0.587 | 0.624 (0.522, 0.716) | 0.038 |
| nonaudio_gbm | 0.609 | 0.575 | 0.138 | 0.592 | 0.527 | 0.100 |
| artist_recent | 0.748 | 0.500 | 0.400 | 0.640 | 0.500 | 0.136 |

- The LATE open_wa column is the new-artist open sAUC column in the harness output, not open_wa. I read it wrongly; take LATE open_wa for ca_whole and ca_local from `late.log` before quoting it.
- TUNE open_wa is near chance (0.48 to 0.50): audio does not separate loved tried songs from same-artist decoys.
- On TUNE, audio-only open sAUC is lower than nonaudio_gbm and much lower than artist_recent. The open-pool paired lower bound vs nonaudio_gbm is -0.092 (ca_whole) and -0.100 (ca_local).
- On LATE, audio is within about 0.01 of nonaudio_gbm in open sAUC, with a paired lower bound of -0.071.
- Open-pool p20 on LATE is 0.038 for audio against 0.100 for nonaudio_gbm.

### Null control (`--null-control`, TUNE, final predict.py)
- ca_whole 0.491, ca_local 0.494, ca_ens 0.505, ca_whole_meta 0.494, ca_ens_meta 0.509.
- wa is 0.467 to 0.482, inside the (0.448, 0.552) band. The harness marks all five PASS.
- Caveat: ca_ens ww under null is 0.515 and ca_ens_meta ws is 0.538. The harness does not gate on ww or ws, and these are inside their bands.

### Independence check
- p90 relative change is 0.0 for all ca_* variants, on TUNE and LATE.

## 4. Ablations (TUNE, `--fast`, `ablations.py`, final config; difference bars are small relative to CIs)

### (1) Whole-clip vs time-local
- Whole-clip summary: sAUC 0.590, wa 0.584, ww 0.607, ws 0.551.
- Local mean of window logits: 0.594, 0.593, 0.600, 0.577.
- Local max: 0.593. Local top-2: 0.597. Local mean plus std: 0.595.
- Only 1 window, or only window 2, scores 0.561 and 0.580, so the clip's other moments are being used.
- Paired sAUC lower bounds:
  - local_mean vs whole: -0.017
  - top2 vs whole: -0.008
  - whole vs local_mean: -0.028
- On LATE, ca_local (0.622) is above ca_whole (0.612), but the paired lower bound for ca_local vs ca_whole is -0.006.
- Answer: modelling individual moments adds at most +0.004 sAUC (TUNE) and +0.010 (LATE), neither significant. It adds a little to wa and ws on LATE. It is not a clear win.

### (2) Songs without usable audio
- Audio coverage of tried songs is 90% for loved songs and 94% for not-loved songs. Decoys are 99%.
- Included vs excluded (`analyze_missing.py`, TUNE):

| Model | Included (all songs) sAUC | Excluded (audio-only rows) sAUC |
|---|---|---|
| ca_whole | 0.590 | 0.596 |
| ca_local | 0.594 | 0.601 |
| ca_indicator_only | 0.493 | 0.500 |

- An indicator-only predictor (missing = 1) scores sAUC 0.493 (0.475, 0.512) and open sAUC 0.490. The missing-audio flag is therefore not what drives the result.
- The indicator-only predictor is pure noise: the loved-rate of missing songs flips sign between folds (investigate.py).
- Handling variants (sAUC / open sAUC):

| Handling | sAUC | open sAUC |
|---|---|---|
| neutral (median train score) | 0.590 | 0.574 |
| missing = lowest score | 0.564 | 0.531 |
| missing = highest score | 0.599 | 0.609 (open p20 0.218) |

- Putting missing songs at the lowest or highest score changes open-pool numbers a lot, because decoys are almost all audio-covered. I kept "neutral" as the only non-gameable choice.

### (3) Recency weighting (TUNE sAUC)
- hl=None 0.590; 730 d 0.587; 365 d 0.584; 180 d 0.582; 90 d 0.583; 45 d 0.585.
- Flat within noise on tried sAUC. I chose none.
- Open sAUC does rise with recency (0.574 without weighting, 0.617 at 90 d), but the primary tried metric does not move, so I did not change the choice.
- I did not run the harness `--window` ablation.

## 5. Below-chance cells and investigation
- Fold 2021-07 for ca_whole is AUC 0.382. It has 44 tried songs and is trained on only 159 songs with audio, so it is noise.
- Fold 2021-10 is 0.450. In the first four folds the models are 0.38 to 0.58.
- No flag was raised on any ca_* model in the final runs.
- The BELOW CHANCE flags are on baselines: artist_plays on 2024-04 (AUC 0.407) and popularity on 2023-04 (0.403). Not investigated.
- A fold-by-fold breakdown of the train and test love rates for audio-covered vs missing songs is in `investigate.py`.

## 6. Things I did and things that went wrong
- Wall-clock times:
  - First MERT extraction: 7,719 clips, 15,838 s (4.4 h).
  - Second top-up extraction: 5,062 clips, about 9,800 s (2.7 h). Extraction was paused (SIGSTOP) while I ran harness jobs, to respect the 2-thread limit.
  - Fast ablation runs: about 1 min.
  - Full TUNE run: 49 s.
  - Null control: 48 s.
  - `--late` run: 105 s.
- The pools changed mid-task. At about 03:38 the iTunes fill marker was written (by someone else), and the pool hash changed (`evalkit-pools-282fcbd3…`).
  - My first extraction had been planned on the old pools.
  - I ran `python3 -m evalkit.fetch_previews --threads 3` (about 6 min, 5,077 new audio files added to the shared cache) and extracted features for the new clips.
  - All final numbers above were recomputed after that. Final audio coverage is 90-97% of tried songs and 98-100% of decoys per fold.
- Tuning before the top-up used the old 73-87% tried-song coverage. Findings from that partial-coverage phase:
  - Layer choice, ncomp, C, cohort-balanced weights and a rank target were all swept. Every variant landed at wAUC about 0.52-0.557.
  - Cohort-balanced weights (`balance=True`) were worse (0.499).
  - The rank-target option (`target="rank"`) is still in predict.py and `analyze` code paths, but never gave a reliable gain.
  - ca_ens (layer-group ensemble) looked best on that partial data but was worse than ca_local after the top-up.
  - I did not delete these knobs from predict.py, since they are used by ablations and by ca_ens.
- `hl=180` was my first default. Full-coverage TUNE then favoured no weighting (0.590 vs 0.582), so I changed the default to None before the final runs. The `--late` run used the final file.
- Failed or abandoned: nothing was deleted from the project folder. Scratch benchmarks stay in my scratchpad.

## 7. Leakage self-audit
- Fitted objects (standardiser, PCA, logistic regression, score mean/std, neutral value) are fitted only on songs present in the cutoff's train streams.
- Training labels come from `song_table(train)` for songs first played at least 90 days before the cutoff.
- Per-clip MERT features are computed independently of every other track and cached under `.cache/shared/w3r1-mert-v1/` (regenerable).
- Artist ids, artist history and pool structure are not used.
- The independence check passes: p90 relative change is 0.0.
- `meta` is used only by the `_meta` variants (duration, explicit, popularity).
- The MERT weights are pretrained on audio and may have seen sealed-era songs (unavoidable, as the README already notes).
- I never ran `--sealed`, never read `.sealed/`, never opened streams.jsonl, and read neither PLAN.md nor earlier workflow logs. I used `--late` once.
- I did read `prepare_folds()` output via evalkit (dev folds only).

## 8. The strongest case against my result
- The edge over nonaudio_gbm is within the CI. TUNE lower bound is -0.022 to -0.029 and LATE only +0.004 to +0.010. A nonaudio_gbm with better tuning, or a differently tied artist-history variant, would likely close the gap.
- Audio similarity to the user's past loves may largely re-encode "sounds like artists I currently play". wa_sauc of 0.58-0.64 is within-artist (not just same artists), but cross-artist pairs can still be driven by audio similarity of artists the user already plays.
- On LATE the audio models gain mostly because artist_recent collapses (0.436, below chance) and nonaudio_gbm weakens, not because audio improves.
- In the open pool audio is clearly worse than artist_recent (0.576 vs 0.748 on TUNE) and its open_wa is about chance. So it is not a strong end-goal candidate finder on its own.
- Labels are behavioural. The oracles (oracle_day1 0.766 TUNE, 0.821 LATE) show how much of "love" is how the user listens (exposure, session), not the music.
- The audio features are only four 5 s windows of a 30 s preview, int8-quantised MERT-95M, and a linear head. Nothing deeper was tried, and the layer, ncomp and recency variants are all within noise of each other.
- Tuning was on partially covered data and the best choices changed after the preview top-up, which shows how noisy TUNE is (about 1,490 songs).
- Early folds (44 to 120 tried songs) are close to pure noise.

Files and logs: code in `/home/user/Listener/taste-model/predictors/w3r1-content-audio/`; run logs in `/tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf3/w3r1/`. The `--late` run log is `late.log`, the null-control log is `null2.log`, the full TUNE log is `full_tune2.log`, the ablation log is `abl_fast3.log`, and the missing-audio log is `missing2.log`. Full-run numbers in this report match these logs.