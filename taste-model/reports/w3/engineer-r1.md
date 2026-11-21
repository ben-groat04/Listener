ENGINEER REPORT: evalkit v3 is implemented in /home/user/Listener/taste-model/evalkit/. The iTunes preview fallback (item 6) is built but NOT active; everything else in the spec is done.

Nothing is committed. I did not run --sealed, make_sealed, or any sealed cutoff. I did not read PLAN.md, .sealed/ or earlier logs, and I did not open streams.jsonl directly; all stream access went through evalkit's loader.

## 1. The item that did not complete: iTunes preview fallback
**What happened**
- The iTunes Search API rate-limits this container to roughly 6-15 lookups per minute. The original 2355 lookups would have taken hours. I saw 403 responses, and a second concurrent client made the 403s worse. The main session also flagged the projected duration, so I cut the scope.
- Scope now: preview-less user tracks that are tried songs in a dev fold, plus a seeded sample of 250 preview-less decoys. Other preview-less train-only user tracks are not looked up. This deviates from the spec's "every user track".
- Even this reduced scope did not finish. At the time I stopped it, `.cache/itunes_fallback.csv` held about 270 rows (it grew a little after the final run because a stray process kept appending; I killed it).
- `fetch_itunes.py` is resumable and writes `.cache/itunes_fallback.complete` once all its targets are resolved. `data.load_meta_all` fills previews, and decoy eligibility changes, only when that marker exists. A partial fill would make "preview present" mean different things for tried songs and decoys.

**Consequence**
- previewUrl is currently exactly what stats.fm provides. Coverage is about 82% of tried songs and 87% of decoys.
- Missing previews stay NaN and must be handled explicitly by predictors.

**Selftest numbers**
- The selftest's metadata-shape shortcut classifier gets AUC 0.587 (AUC 0.595 when the release-age bucket is added), both under the 0.62 limit.
- The release-age bucket is available for all tried songs (0% unknown).

**To finish it:** run `python3 -m evalkit.fetch_itunes` repeatedly (about 15 per minute at best), then rebuild pools and rerun the selftest. The preview audio cache would then need a resumable `fetch_previews` top-up.

## 2. What changed (all in evalkit/; README.md rewritten, selftest.py updated, passing)
- **Folds.**
  - 14 quarterly dev cutoffs, 2021-07 to 2024-10.
  - TUNE is 10 folds, LATE is 4 folds, ALL is both.
  - `--fast` is TUNE only, nboot 100, no independence check, no LATE.
  - The default run is TUNE, nboot 300, with the independence check.
  - `--late` prints separate TUNE, LATE and ALL tables and appends a JSON line to `.cache/late_runs.log`: UTC time, predictor paths, sha256 of each file, plus whether the run was `--null-control` and the `--window` setting.
  - The log currently holds one line, from my final baseline-only `--late` run. I deleted the earlier test lines.
- **Labels.** `share90` is added. Spearman of the score against days90, log1p(plays90) and share90 is reported.
- **Baselines.**
  - Kept: popularity, artist_plays, artist_recent, artist_love_rate.
  - Added: `duration` (a one-feature gradient-boosting model), `meta_gbm` and `nonaudio_gbm`.
  - `random` is removed as a scored model. Tie noise is removed everywhere.
  - Point-in-time artist features are verified by a selftest that recomputes them from truncated history.
  - Design choice to review: an unconstrained `nonaudio_gbm` learned the reversed direction on TUNE (sauc 0.46) because artist-history counts are confounded with calendar time. I added monotone constraints on the familiarity features and a 180-day recency weight on training songs, for all GBM baselines. I chose the 180-day half-life to match artist_recent and tested only a handful of variants, on TUNE only. They are constants at the top of `baselines.py`.
- **Diagnostics.**
  - They are computed inside the harness from pool columns, not through the predictor interface: pool_artist_siblings, pool_album_siblings, exposure_session, oracle_day1, oracle_7d.
  - For exposure_session, decoys are scored below every tried song.
  - Oracles are 0 for decoys.
- **Metrics (rewritten in metrics.py).**
  - Everything runs on one weighted engine: bootstrap weights come from artist-cluster resampling. The selftest checks it against brute force.
  - Reported: sauc for all, new-artist and known-artist songs; wa_sauc, ww_sauc and ws_sauc; plift; p20; AP lift; CIs; paired lower-bound tables against every other model for sauc and wa (open-pool variants too, plus p20); permutation null band (200 permutations, cached); per-fold AUC with CI; the BELOW CHANCE flag.
  - Tie-averaging for p10/p20/r20/hits is the exact expectation over random tie-breaks, which is the limit of the 20-seed average. The 20-seed average is used for AP, lift, r20 and macro AUC.
- **Open pool.**
  - Seeds are chosen per fold from pre-cutoff plays only (top 300 artists plus up to 6 related artists of each of the top 150). A selftest asserts that truncating history at the cutoff leaves the seeds unchanged.
  - The decoy universe is now one file with `source_artists` per track. It has 84,875 tracks, built with `make_decoys.py` from the existing raw cache plus newly fetched artists.
  - Exclusion of any song the user ever played stays as before, and is documented in the README.
  - Draws are covariate-matched in two stages (draw 8 times the tried count, then 5 times).
  - Release-age buckets use stats.fm album dates, cached in `.cache/album_release.json`, and are included in both the matching model and the selftest classifier.
  - `open_wa_sauc` is implemented: loved tried songs against decoys by the same primary artist.
- **VERDICT table.**
  - It has no fixed thresholds. The diagnostic reference rows are printed at the top of each slice.
  - Null control is PASS only if tried sauc and wa_sauc both lie inside the 95% permutation band.
  - Label-variant consistency is reported, not gated.
  - When a predictor file has no `PREDICTORS` dict, its model name is now the file stem instead of the full path.
- **Cache hashes.** Pool and baseline cache hashes no longer depend on the partial iTunes csv; they depend only on its completion marker.
- **Stale caches.** Deleted old pools, baseline pickles and null bands. Current ones are in `.cache/shared/` (one pools, one baseline-scores, one nullband file). The Workflow 2 feature caches (`clap-preview-emb`, `hand-audio-feat-v1`, `C-textemb-v1`) are untouched and are noted in the README as covering the old pools only. No failed-attempt code was left in the project.

## 3. Shared artefact: preview audio cache
- Location: `/home/user/Listener/taste-model/.cache/shared/previews/`
- Contents: `audio/<md5(previewUrl)>.<ext>` holds the original downloaded bytes, unchanged. `manifest.csv` has columns md5, previewUrl, ext, bytes, duration_s, source, ok, error.
- Size and status: 9220 distinct previewUrls, all 9220 ok, about 4 GB. All 14 dev cutoffs are included; no sealed cutoffs.
- Script: `evalkit/fetch_previews.py` (resumable, at most 6 threads; `--report` prints coverage).
- Coverage by fold, fraction of tried songs / decoys with ok audio:

| Fold | Tried | Decoys |
|---|---|---|
| 2021-07 | 0.727 | 0.850 |
| 2021-10 | 0.612 | 0.743 |
| 2022-01 | 0.673 | 0.840 |
| 2022-04 | 0.750 | 0.885 |
| 2022-07 | 0.717 | 0.808 |
| 2022-10 | 0.775 | 0.872 |
| 2023-01 | 0.796 | 0.849 |
| 2023-04 | 0.841 | 0.874 |
| 2023-07 | 0.755 | 0.827 |
| 2023-10 | 0.823 | 0.849 |
| 2024-01 | 0.879 | 0.894 |
| 2024-04 | 0.846 | 0.895 |
| 2024-07 | 0.871 | 0.939 |
| 2024-10 | 0.868 | 0.891 |

- These URLs come from the pools before I made the iTunes fill inactive. The pools did not change (the fill was already inactive when they were built), so the scope still matches.
- If the iTunes fill is later completed, the scope grows and `fetch_previews` needs a top-up run.

## 4. Dev baseline scores (full run, `--late`, baselines only)
Full output is in `/tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf3/final_run_baselines.log`.

Selftest passes, with the same results as the final-state log in section 1. Chance is 0.5; the permutation band for TUNE sauc is (0.459, 0.537).

**Tried pool, love label, all songs (sauc with 95% CI)**

| Model | TUNE sauc | LATE sauc |
|---|---|---|
| popularity | 0.471 (0.435, 0.507) | 0.521 |
| artist_plays | 0.619 (0.558, 0.652) | 0.454 |
| artist_recent | 0.619 (0.550, 0.653) | 0.436 |
| artist_love_rate | 0.550 (0.469, 0.630) | 0.493 |
| duration | 0.559 (0.506, 0.606) | 0.564 |
| meta_gbm | 0.524 (0.482, 0.570) | 0.558 |
| nonaudio_gbm | 0.557 (0.512, 0.604) | 0.534 |
| pool_artist_siblings (diag) | 0.630 | 0.546 |
| exposure_session (diag) | 0.658 | 0.619 |
| oracle_day1 (diag) | 0.766 | 0.821 |
| oracle_7d (diag) | 0.880 | 0.906 |

- The artist-based baselines are above chance on TUNE and not above it on LATE. artist_plays also trips the BELOW CHANCE flag on fold 2024-04.
- Within-artist (`wa_sauc`) is 0.50 for all artist-only scores. This is by construction: same artist, same score.
- On TUNE, nonaudio_gbm's `wa_sauc` is 0.540 and duration's is 0.607.

**Open pool, TUNE (open sauc)**

| Model | Open sauc |
|---|---|
| artist_recent | 0.749 |
| artist_plays | 0.728 |
| nonaudio_gbm | 0.600 |
| popularity | 0.511 |

- For exposure_session and the oracles, the open-pool numbers are high by construction: decoys sit below every tried song and the oracles give them 0.

**Null control check**
- `--null-control` run on a mock predictor (artist_recent plus popularity) returned FAIL (sauc 0.60 on TUNE, outside the band).
- The identity shuffle preserves the number of songs per artist, which is itself a familiarity signal, so the check is strict for artist-based scores.
- I did not run null control on the real baselines.

## 5. Comparability and usage
- **Comparability.** Earlier scores are not comparable. The folds, decoys (re-seeded per fold), baselines (tie noise removed, GBMs added), CIs and bar all changed. The README says so.
- **Sealed cutoffs.** The code paths exist but I did not run them. Before any sealed run the main session must:
  1. run `python3 -m evalkit.make_decoys --sealed` (fetches the extra seed artists);
  2. optionally run `python3 -m evalkit.fetch_itunes --sealed` and finish the dev lookups;
  3. run `make_sealed --write-manifest`.
- **Early folds.** The first folds are tiny (2021-07 has 44 tried songs, a love rate near 65%) and noisy.
- **Environment.** About 2 threads were used throughout. The early `fetch_itunes` process briefly exceeded that while building its decoy target list, before I applied thread limits.