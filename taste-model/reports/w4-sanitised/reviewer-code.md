CODE REVIEW (reviewer-code). Start 2026-11-21T10:42:14Z, end 2026-11-21T10:47:03Z (from `date -u`, in <W4 scratch path, not available>). No job ran over 10 minutes. No sealed data touched; no git history used; no commits made; nothing under .claude/ read. Reports read: only RESULTS.md (a few passages).

## A. What I actually ran (dev-only; scripts in my scratch folder)
1. `python3 -m evalkit.selftest`: passed ("selftest OK", 35 s wall, 2 threads). The metrics engine matches brute force, including gc and gc_wa. Independence gate, point-in-time artist features and the permutation band all passed. Tried-vs-decoy shortcut AUC was 0.570 (public metadata) and 0.587 (with release-age bucket).
2. `python3 -W ignore -m evalkit.run --fast` (baselines only, cached, 8 s). No "BELOW CHANCE" flag was printed. Single cells below 0.5 do exist, e.g. duration 0.427 in 2021-07 and popularity at ~0.40-0.46 in several folds.
3. Preview source by pool (tried vs decoy, all 14 dev folds), from `src.py`.
4. Null-control cache check: the fit-cache key of w3r1-content-audio is identical for 3 null seeds and the real train (`nk.py`). Scoring `ca_whole` under null seeds 0 and 1 gives identical scores (`nk2.py`).
5. Lyrics-cache coverage and the open-pool AUC of a has-lyrics flag (`lyr.py`).
6. Pair weight per fold (`w.py`), the 4% of candidates dropped for missing meta (`drop.py`), the identity merge through post-cutoff links (`ident.py`), preview/MERT/CLAP cache coverage (`cov.py`), and decoy_raw cache vs needed artists (`seeds.py`).
7. `py_compile` on all predictor scripts: all compile. Network check: stats.fm, iTunes, lrclib and PyPI return 200; huggingface returns 307. These hosts are reachable.
I did NOT run: any predictor through `evalkit.run`, the full (slow) run, `--late`, `--null-control`, `make_decoys`, `fetch_itunes`, `fetch_previews`, the MERT/CLAP builders, or any of the analysis, ablation and variants scripts. Statements about those are from reading only.

## B. Findings, most important first

**B1. [Verified] The null-control cache bug still exists on disk in `predictors/w3r1-content-audio/predict.py`.**
- The `_fit` cache key there is `(cutoff, len(train), sum of timestamps, cfg)` and contains no identity hash.
- The null control keeps timestamps and shuffles identities, so all 3 seeds, and the real run, share one key. For `ca_whole`, seed 1 scores are bit-identical to seed 0.
- `predictors/w3r2-audio-taste/ref_ca_local.py` documents this and works around it for one wrapper. The root file was never fixed.
- `predictors/w3r2-integrated/predict.py` imports that file as `CA` and uses `CA.make_ens` for its audio member. Unless the devil's advocate patched it elsewhere, `w2i_final` and `w2i_nohist` null runs are single-seed repeated three times. RESULTS.md says the devil's advocate "fixed a caching bug that had made the 3 seeds identical", but the fix is not in the code on disk (I believe it was done in a throwaway copy; unverified).
- Round-1 "Passed the null test" for w3r1-content-audio rests on 1 effective seed compared against the band for a 3-seed mean. That is a mismatch, not necessarily wrong.
- Worse case: a process that ran a normal evaluation before the null control would reuse the REAL fit under the null train. That produces a spurious FAIL or an invalid PASS.
- Fix: put a hash of trackId and song in the key, as `w3r2-audio-taste` and `core._tkey` do. A harness-level fix would be better: clear or invalidate predictor state per null seed, or have `score_predictor` pass `train` objects with a nonce.
- `null_seeds.py` (beyond-audio) calls `run._null_control(train, rng)`, missing the `cands` argument, so it would raise TypeError. It is broken; it says "harness uses one fixed shuffle" but the harness now uses 3 seeds.

**B2. [Verified] Open-pool shortcuts in the preview and lyrics caches. These are shortcuts for any audio, lyrics or missingness predictor on the open pool.**
- Preview source share (tried vs decoy; shares computed from my crosstab):

  | Source | Tried | Decoy |
  |---|---|---|
  | Spotify | 67.6% | 86.3% |
  | iTunes meta | 13.8% | 11.5% |
  | iTunes fallback | 12.4% | 1.4% |
  | None | 6.1% | 0.9% |

  Counts: tried 2450 (1657/339/304/150), decoys 12250 (10566/1404/166/114).
- A binary "iTunes-sourced" flag therefore has open-pool AUC of about 0.57 by arithmetic, before codec or loudness differences that an embedding model can pick up. The README's "presence carries the same meaning in both" is not true in practice.
- Cause: `fetch_itunes.targets()` looks up every preview-less tried song, but only a random 250 preview-less decoys drawn from the whole universe (`N_DECOY_LOOKUPS=250`).
- Pool eligibility (`data._open_parts`) keeps a preview-less decoy only if it was looked up, so decoys are conditioned on having a Spotify preview and tried songs are not.
- `data.decoy_presample` was meant to supply the lookup targets. It is dead code, and the README and the `PRESAMPLE` comment describe behaviour that does not exist.
- Lyrics cache: a lookup record exists for 100% of tried and train tracks but only 57.8% of decoys. Found-lyrics rate is 94.2% (tried) vs 53.1% (decoys).
- The has-lyrics flag has open-pool AUC 0.706 (computed from `feats.pkl`).
- Within tried songs, found vs not found has the same love rate (0.278 vs 0.277), so this is purely a pool artefact.
- `fetch_lyrics.py` iterates the whole current universe, so rerunning it (lrclib is reachable) would remove the gap. The stale cache predates the 2021-07 and 2021-10 pool rebuild, but that rebuild alone cannot explain a 42% gap (those folds hold only about 8% of decoys). The cause is not established.
- The tried-pool metrics are not affected by any of this, because both groups come from the user's own songs.

**B3. [Verified] The TUNE headline sauc is dominated by two folds.**
- Pair weights (n_loved x n_notloved) share of TUNE: 2023-01 = 32.8%, 2023-10 = 35.5%, together 68%. The five folds from 2021-07 to 2022-04 together carry 3.2%.
- Fold 2022-10 has 89 tried songs from only 10 distinct artists.
- ALL: 2023-01 and 2023-10 give 42%; the four LATE folds give 38%.
- The artist-cluster bootstrap resamples (fold, artist) clusters independently per fold, so it ignores same-artist correlation across folds. CIs are somewhat too narrow.
- "TUNE" is effectively about 4 well-populated folds. Per-fold AUC of ±0.1 in tiny folds is noise.
- A macro-average over folds, or per-fold reporting next to the pooled value, would be more honest.

**B4. [Verified] The "reference to beat" is weaker than a one-line baseline on TUNE.**
- Fast-run TUNE sauc: nonaudio_gbm 0.559, artist_recent 0.619, artist_plays 0.619, artist_love_rate 0.550, duration 0.559.
- The README calls nonaudio_gbm "THE reference any music/content claim must beat". It loses to a frequency statistic. The VERDICT's `best_valid` column compensates only partly.
- Cause (README comment in baselines.py): training rows are confounded with calendar time, so the GBM needs monotone constraints and recency weights. I did not re-derive this.
- "Beats nonaudio_gbm" evidence grades therefore flatter. Evidence against `artist_recent` and `duration` should be shown by default.
- Within-artist, artist baselines are exactly 0.500 by construction, so only duration (0.607) and meta/nonaudio GBMs carry information there.

**B5. [Believed from reading, not run] `ablate.py --window` damages labels.**
- It truncates `train` to the last 365 or 730 days, then predictors call `song_table(train)`. Every old favourite played in the window then looks "first played at window start", and its plays in the next 90 days look like a fresh love.
- The training labels are contaminated. Window ablation results (365 vs sub365) are suspect. `core.py` and the `w3r2-audio-taste` window options filter by first-play time instead, which is fine.

**B6. [Verified, minor] Transductive identity.**
- Train `song` ids are canonicalised using the full history (`_load_all`), including links to later named streams.
- Measured at cutoffs 2022-10 / 2023-10 / 2024-10: 2.1% / 2.0% / 1.3% of train streams belong to songs (2, 4 and 5 songs respectively) that would stay separate under cutoff-truncated identity.
- Effect is tiny. Candidates are protected (selftest asserts no train/candidate overlap).
- `make_folds` also drops candidates with no usable meta or identity, calling this "label-independent". 107 of 2557 candidate songs (4.2%) were dropped overall, with love rate about 0.1 vs 0.27. In 2023-2024 folds the dropped songs have a lower love rate (e.g. 0.04 in 2024-01, though only 22 of 24 are 'unknown'). The claim is slightly untrue, but the effect is tiny.

**B7. [Verified] Silent failure modes in predictors.**
- The `_store()` functions in the audio predictors and `_cache()` in the lyrics predictor swallow a missing or empty cache and return all-missing or empty features. The predictor then outputs constant or neutral scores with no error. A broken or absent cache would yield a plausible-looking chance-level score.
- Suggestion: assert a non-trivial coverage fraction, or raise.
- `ca_whole` mode contains dead code (`... if False else ...`).

**B8. [Verified] Cache and regeneration hygiene.**
- `_pool_hash` includes `.cache/itunes_fallback.complete` only by file size, not `itunes_fallback.csv` content. It also ignores `decoy_raw` and `album_release.json` content (size only). Rerunning `fetch_itunes` or changing related-artist lists would NOT invalidate cached pools.
- The streams file is hashed by size only.
- `_code_hash` for baseline-score caches excludes `run.py`, although `prepare_folds` (public-view shuffle seed) lives there.
- Pool regeneration calls the live stats.fm API (`album_release`). `popularity` and release dates are "2026 measurements", so a rebuild on another date can differ.
- Regenerating everything is long: iTunes at about 15-20 requests/min, MERT at 1.8 s per clip (about 7 h in W3), CLAP at 2.4 clips/s. This matches the stated container constraints.
- `decoy_raw` holds 1325 artist files; only 1142 are needed by the dev folds (183 are leftovers, probably the sealed seeds). The universe filters by `source_artists`, so this is harmless clutter.
- The MERT cache holds 2528 unused rows and CLAP holds 3543 (FEATURES.md already notes this).
- All 10,288 manifest URLs have MERT and CLAP rows; none are missing.

**B9. [Verified] Documentation and code mismatches.**
- README says "95% lower bound". The code uses the 2.5th percentile of the paired bootstrap, which is a two-sided 95% CI lower end, i.e. a 97.5% one-sided bound. Harmless, but the wording is loose.
- `data.py` `ok` comment says "label-independent" (see B6).
- Several analysis scripts hard-code stale constants. `calib_randdir.py` hard-codes the harness null band "(0.475,0.519)"; the current permutation band is (0.462, 0.539) in the selftest's 60-perm run.
- `datetime.utcnow()` (deprecated) in the sealed log.
- The selftest tolerances are loose: random AUC within ±0.05, and the permutation-band check allows ±0.05. The null-control part of the selftest is printed, not asserted.
- `late_runs.log` has duplicate lines (10:20:25 and 10:20:26 for the same files). The audit trail is not de-duplicated.
- `.cache/late_runs.log` has 17 lines. I confirm that count; the README's "09:00-09:05" statement I did not check.

**B10. [Verified, design caveat] Sealed-data guard is a convention.**
- `data._load_all()` is a public function that returns the full streams including the sealed era. Only `load_streams` guards. Anything calling `_load_all` (including `prepare_folds`, the pool builder and `make_open_folds`) is by policy only.
- `prepare_folds` returns the raw `pool` dict with labels in the same process, so predictor code could import them. The "harness refuses" language in the README applies only to `load_streams`.
- Predictors never receive post-cutoff rows through the public view; selftest asserts this.

## C. Things I checked that are fine
- Point-in-time artist features in `baselines._Hist` (selftest compares against truncated-log recomputation).
- `evalkit/metrics.py` weighted AUC, gc and gc_wa and the bootstrap. The selftest brute-force match is genuine; I read the code and found no off-by-one.
- Fold seeds depend on pre-cutoff streams only (asserted by selftest).
- No predictor fits a scaler, PCA, vocabulary or normaliser on pool or decoy tracks. All fits (w3r1-content-audio, w3r2-audio-taste, lyrics, core.py) use `song_table(train)` songs only. The stated risk of transductive transforms on decoys is not present in current code (by reading, not by a run).
- `feats.py` features for training songs use only streams before the song's own first play and matured songs only (the leakage self-audit script's logic looks right; I did not run it).
- Dev label horizons end before DEV_END (selftest asserts it).
- The singleton independence check restricts meta to train plus that candidate, which is a sound design.
- Opaque id hashing: 13 hex digits is below 2^53, so float conversion is exact. Titles and artist names remain visible in `trackName` and `meta.artistNames`, so pretrained-model knowledge of the real songs can be used. That is a design decision, not a bug.

## D. Dead, unused or leftover code (not deleted; reviewers do not edit)
- `data.decoy_presample` (never called; see B2).
- `predictors/w3r1-song-content-beyond-audio/null_seeds.py` (broken; see B1).
- `predictors/w3r2-audio-taste/ref_ca_local.py` (only a workaround for B1).
- `predictors/w3r1-training-signal/variants_*.py` (9 files), `audit.py`, `diag_flip.py`, `predictors/w3r1-content-audio/{ablations,analyze_missing,investigate}.py`, `predictors/w3r1-song-content-beyond-audio/analysis.py`: scripts behind reported analyses. They compile; I did not run them. If no reported score depends on them they could be removed.
- `__pycache__` directories inside predictors (git-ignored).

