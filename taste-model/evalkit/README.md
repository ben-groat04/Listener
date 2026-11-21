# evalkit v4: does a method predict which NEW songs the user comes to love?

**v4 (this version)**: (1) a new artist-disjoint HOLDOUT slice (25% of the artists by salted hash), removed from every normal run and scored once per predictor hash with `--holdout`; (2) artist-cluster bootstrap with
GLOBAL artist clusters; (3) `macro_sauc`, `wx_sauc`, a per-fold AUC table and a BREAKDOWN table; (4) references `ref_audio_final` (Workflow 3's audio_final) and `best_ref` (evidence grade is vs best_ref, deltas vs five references);
(5) null control v3 (every seed in a fresh process, `--null-seeds`, real-minus-null gap, PASS / FLAG); (6) open-pool primary metrics on Spotify-CDN previews only, shortcut baselines `has_preview` / `preview_source_itunes`;
(7) `--late` capped at 2 runs per predictor hash with a read-only table; (8) `python3 -m evalkit.describe` label descriptives; (9) hygiene (see "Comparability" and the end of this file).

**Comparability: NO v3 / v3.1 number is comparable to a v4 number.** Rows changed (HOLDOUT rows are removed from TUNE / LATE / ALL, so the tried-song counts and every score change) and the bootstrap changed (global artist
clusters instead of (fold, artist) clusters: CIs, P(d>0) and lower bounds are different; wa / gc_wa bootstrap pair weights are now products of draw counts). The dev POOLS themselves are bit-identical to v3.1 (selftest asserts it against digests recorded
before the change: `evalkit/pool_reference.json`); only which rows are scored and how they are summarised changed.

v3.1 changes, relative to v3: (1) null control v2 (artist/album relabelling, 3 seeds, gated) with the old identity-only shuffle kept as `--null-control-identity` (diagnostic);
(2) graded metric `gc` / `gc_wa` (concordance with plays90); (3) graded evidence (P(delta>0), 80% intervals, STRONG / SUGGESTIVE / NONE) in the VERDICT; (4) within-artist reference
'dWA vs best meta'; (5) diagnostics `exposure_before` / `exposure_after` / `replays_first_session` next to `exposure_session`; (6) housekeeping (iTunes fill text, LATE audit note).

v3 replaces the v2.1 success bar and fixed thresholds by an evidence table (VERDICT) and changes folds, baselines, metrics and the open pool. Scores of v2.x
are NOT comparable (different folds, different decoys, different baselines, different CIs); see "Comparability".

## Protocol (code: data.py)
* Song = connected component of (normalised title + primary artist) and trackId links, so remasters/live/deluxe versions,
  one trackId under several artist ids, and 'unknown track name' plays are the same song.
* Cutoff C: a song is a candidate if it was never played before C and is first played in [C, C+3 months) ("tried" songs).
* Label `love` = >=6 plays on >=3 distinct days in 90 days after first play (binary primary target). `strong` = >=15 plays / 5 days; `love_4_2`, `love_10_4`
  (neighbouring definitions) and the continuous `days90`, `plays90`, `share90` are reported next to it. `share90` = plays90 / ALL the user's plays in that song's own
  90-day window [first, first+90 d): normalises for listening volume over time.
* Folds (dev): 14 quarterly cutoffs 2021-07-01 .. 2024-10-01. **HOLDOUT** (v4): a song is a HOLDOUT song iff its RAW stats.fm primary artist id `a` satisfies `int(sha256("w4-holdout|" + str(a)).hexdigest(), 16) % 100 < 25` (data.is_holdout; artist -1 is
  never holdout). HOLDOUT rows = the tried songs of holdout artists in all 14 folds plus the decoys of holdout artists (open pool). Tried-song share 30.2% overall (loved 25.6%; per fold in the selftest output; the salt was not changed), so the
  split is artist-disjoint, not label-driven. **In every non-holdout run (--fast, default, --late, --null-control) HOLDOUT rows are removed from `cands` and from the pools BEFORE predictors are called** (their `meta` rows too, unless the track is in train); train streams are
  unchanged (pre-cutoff history of holdout artists stays in train). **TUNE** = the 10 early folds (2021-07..2023-10) minus HOLDOUT: all iteration happens here. **LATE** = the 4 late folds (2024-01..2024-10) minus HOLDOUT: only scored with `--late`, capped at
  2 runs per predictor file hash (run.py refuses a third, with a message), each run appends one JSON line (UTC time, predictor paths, sha256) to `.cache/late_runs.log` AND writes its full output table to the read-only file `.cache/late_tables/<sha256>.txt` (`<sha256>_run2.txt`
  for a second run; mode 444), so devil's advocates verify LATE claims by READING it instead of re-running --late. ALL = TUNE + LATE. Streams >= 2025-04-01 are refused by `load_streams`; dev label horizons end exactly there.
  `--holdout` scores only HOLDOUT rows (all 14 folds) and prints the VERDICT for three slices: HOLDOUT-ALL (14 folds), HOLDOUT-early (the 10 TUNE-era folds) and HOLDOUT-late (the 4 LATE-era folds). Baselines, shortcut rows and the reference rows are scored on HOLDOUT in the same call.
  One `--holdout` run per predictor file sha256 (the harness refuses a second run and refuses --holdout together with --fast, --null-control, --late or --sealed); each run appends a JSON line to `.cache/holdout_runs.log` (UTC time, file paths, sha256, model names, and HOLDOUT-ALL
  sauc / wa / gc / new-artist sauc with 95% CI for every model), so devil's advocates read the result from the log. **HOLDOUT is run once, by a builder, on its final pre-declared predictor, after writing the declaration in its report. Devil's advocates never run --holdout.**
  HOLDOUT is reported with deltas and P(d>0) and is NOT graded. Sealed cutoffs (2025-04 .. 2026-04) are unchanged (the sealed path scores all rows, no HOLDOUT split; it was extended only to accept the new reporting and was not run); their labels/manifest must be regenerated by the main session.
* Two pools per fold, scored in ONE predictor call:
  * tried pool (primary): loved vs tried-but-not-loved songs.
  * open pool (end-goal proxy): tried songs + 5x as many decoys: real songs the user NEVER played (checked against the FULL history, incl. later years, inside the harness) by
    seed artists of that fold, already released by the end of the fold window. Decoy = "not tried", NOT "would hate".
* Open-pool construction v3 (data.make_open_folds, make_decoys.py): seeds are chosen PER FOLD from PRE-CUTOFF information only (top-300 artists by plays in streams before the
  cutoff + up to 6 stats.fm related artists of each of the top 150; selftest asserts that truncating the history at the cutoff does not change the seeds). The universe is
  fetched from api.stats.fm (raw cache `.cache/decoy_raw`, max 200 tracks per artist) once for all folds; each fold selects the tracks of its own seed artists.
  Decoys are covariate-matched in two stages (stage 1: draw 8x |tried| candidate decoys with weights from a per-fold logistic model, before the slow iTunes preview lookups, which therefore only
  had to be done for these stage-1 decoys; stage 2: re-fit with the iTunes-filled preview information and draw the final 5x |tried| decoys from the stage-1 draw). The v3 helper `data.decoy_presample` was removed in v4 (unused). Matching covariates: metadata shape
  (missing fields, preview/spotifyId presence, title==album, duration, explicit, #artists, title length, popularity decile) x new-artist flag + **release-age bucket**
  relative to the cutoff (<3 months incl. not yet released, 3-12 months, 1-3 y, >3 y, unknown). Tried songs' release date = earliest known stats.fm album date over the
  albums listed for the track (cache `.cache/album_release.json`); decoys' = earliest album date. Decoys always have a date, so 'unknown' occurs for tried songs only (rate reported by
  selftest). Release age is a matching covariate only; it is not given to predictors.
* What a predictor sees: `train` (streams < C), `cands` (song, trackId, albumId, artistIds, artist, trackName), `meta` indexed by trackId (name, durationMs, explicit,
  popularity, spotifyId, previewUrl, albumName, artistNames). Rows are shuffled, all ids are opaque hashes (equality joins only), no labels/flags/timing. meta covers only tracks
  in train or the pool. **previewUrl**: where stats.fm (Spotify / Apple) has none, the iTunes Search fallback (ACTIVE: `.cache/itunes_fallback.complete` exists, so the fill applies to all folds; built by `python3 -m evalkit.fetch_itunes`, resumable, ~6-15 lookups/min
  from this container: lookup by primary artist + title, accepted only if normalised title and primary artist match and |duration difference| <= 5 s) fills it, for user tracks and decoys alike. **Preview presence does NOT mean the same thing for tried songs and decoys**:
  a decoy is eligible only if it has a preview or was looked up at all (iTunes lookups are rate limited), whereas every tried song is kept whether or not a preview was found. Selftest coverage (non-HOLDOUT rows of the 14 dev folds): preview present for 93.5% of tried songs and
  99.0% of decoys, so an ABSENT preview identifies a tried song (a missing-preview flag alone scored ~0.53 on TUNE in v3), and the share of iTunes-sourced previews differs between tried songs and decoys. The tried-vs-decoy shortcut AUC from public metadata is 0.603 (0.615 with the non-public
  release-age bucket). v4 therefore reports the open pool in two tables (see Metrics: primary = Spotify-CDN previews only, secondary = full pool) and adds the shortcut baselines `has_preview` and `preview_source_itunes`. Tracks still without preview have previewUrl NaN: handle this explicitly and report it.
* Independence: the score of a candidate must not depend on the other candidates. The harness re-scores random candidates alone (meta restricted to train + that candidate) and
  reports the 90th percentile relative change (`independence` p90; NaN = not checked = fail). Fix random seeds; cache fitted models by cutoff.

## Metrics (tried pool unless stated; all with artist-cluster bootstrap CIs; resamples are shared by all models => paired deltas)
**Bootstrap (v4)**: a cluster is the primary artist GLOBALLY: one multinomial draw over all artists of the slice gives each artist a draw count, and ALL rows of that artist in every fold of the slice get that count (before v4 an artist was resampled separately within each fold). Pair weights
are products of the two rows' draw counts (for sauc, wa, ww, ws, wx, gc, gc_wa alike); resamples are shared by all models of a slice, so deltas are paired. "95% lower bound" everywhere means the 2.5th percentile of the two-sided 95% interval.
`macro_sauc` (v4): the mean of the per-fold AUC over the folds that have at least 10 loved and at least 10 not-loved tried rows in the slice (the set of folds is fixed from the unweighted counts, so it is the same in every resample), with a CI from the same resamples; printed next to pooled sauc, with a permutation band and paired deltas (dMACRO).
`wx_sauc` (v4): pairs sharing fold AND exposure_before bucket (0, 1-2, 3-8, 9+ other new songs earlier in the same session). Computed from harness diagnostics, never shown to predictors; like ws it has a CI, a permutation band and paired deltas (dWX). The per-fold AUC table (with CIs) is printed for every model in every run.
**BREAKDOWN tables (v4, printed in fast and full runs)**: for every model, sauc with 95% CI (pairs within fold, inside the group) by fold; new vs known artist; exposure_before bucket; tercile of the user's total plays in the song's own 90-day window (= plays90 / share90; tercile edges fixed over all dev tried songs, computed from the cached pools); release-age bucket
(of the tried song, relative to the cutoff); preview present vs absent. The first row of each table is the number of loved / tried songs in the group.
**Open pool (v4)**: the PRIMARY open metrics (open_sauc all / new / known, open_wa, p20, open_dSAUC...) are computed on the subset in which BOTH tried songs and decoys have a previewUrl from the Spotify CDN (source column of `previews/manifest.csv` == spotify); the full open pool is printed as the secondary table `open_love_full`;
`open_subset_counts_per_fold` lists the tried songs and decoys per fold in the subset. Shortcut baselines `has_preview` (1 if a previewUrl exists) and `preview_source_itunes` (1 if the preview is iTunes-sourced) are scored in both tables.
* `sauc` stratified AUC = AUC over all within-fold (loved, not-loved) pairs (all / new-artist / known-artist songs). Macro AUC, AP/lift, p10, p20, r20 and `plift`
  (pooled top-10% hits / hits expected at each fold's base rate) are reported; ties are averaged over random tie-breaks (exact expectation for the bootstrap, 20 seeds for AP/lift/r20/macro).
* `gc` graded concordance (C-index) of the score with `plays90` over tried songs: all pairs in the same fold whose plays90 differ (ties in plays90 excluded; score ties count 0.5), pooled with pair
  weights (pair weight = product of the two rows' artist-cluster draw counts in the bootstrap). `gc_wa`: the same over pairs sharing fold AND primary artist. Both have artist-cluster bootstrap CIs, a permutation null band
  (plays90 permuted within fold / within fold x artist of a fixed random score, 200 permutations), paired deltas vs every model and VERDICT columns. It uses all the information in plays90 (not only the binary love cut), is
  therefore less sensitive to the arbitrary love threshold, and answers "does the score order songs by how much they were played?". The Spearmans below are kept.
* `wa_sauc` within-artist: AUC over loved/not-loved pairs sharing fold AND primary artist. `ww_sauc` within-week: pairs sharing fold and ISO week of first play.
  `ws_sauc` within-session (exposure-matched): pairs sharing fold and the listening session (gap > 30 min between plays) of the first play. All pooled with pair weights.
* Spearman (within fold, tried pool) of the score with `days90`, `log1p(plays90)` and `share90`.
* Paired deltas (shared resamples) of sauc, macro_sauc, wa_sauc, wx_sauc, gc, gc_wa and the open-pool variants versus every other model. For EVERY paired delta three tables are printed: `<d>_lower_bound` (95% lower bound = 2.5th percentile of the two-sided interval),
  `<d>_P_gt0` (P(delta>0) = share of the shared bootstrap resamples with delta>0) and `<d>_80ci` (80% interval = 10th..90th percentile). Tables: dSAUC, dMACRO, dWA, dWX, dGC, dGCWA, open_dSAUC (+ _new, _known), open_dP20, open_dWA.
* PERMUTATION NULL BAND: 200 label permutations within fold (within group for wa/ww/ws/wx) of a fixed random score give the 95% band of sauc, macro_sauc, wa, ww, ws, wx and new-artist sauc under
  no signal. Predictor independent, cached in `.cache/shared/evalkit-nullband-*.pkl`.
* Per-fold AUC with CI; any model x fold whose CI upper bound is below 0.5 is flagged `BELOW CHANCE - investigate`.
* Open pool: `open_sauc` (all / new / known), `open_wa_sauc` (pairs of a loved tried song and a decoy sharing fold and primary artist), p20, each with CI and paired deltas.
* VERDICT table per non-baseline model and slice (for a baseline-only run: the baselines, shortcuts and the reference): sauc + CI + permutation band, macro_sauc + CI + band, wa CI, gc / gc_wa + CI + band, ww / ws / wx / new-artist CIs, plift, Spearman share90, open (primary table) sauc / open_wa / p20,
  independence p90, label-variant consistency (love_4_2, love_10_4, strong each >= love - 0.03; reported, not gated), `best_ref` and the evidence columns. The table `VERDICT_DELTAS` lists, for every model and EACH of the five references (nonaudio_gbm, artist_recent, duration, meta_gbm, ref_audio_final), the paired delta of
  sauc, wa, gc and macro_sauc: point delta, 95% lower bound, P(d>0), 80% interval ('*' marks best_ref). The DIAGNOSTIC reference rows are printed at the top of each slice. There are no fixed thresholds.
  **best_ref** = the reference (of the five above) with the highest TUNE point sauc (non-HOLDOUT rows), computed once from TUNE and applied to every slice, including HOLDOUT. **Evidence columns** (vs best_ref, per metric sauc / wa / gc): point delta `d_<m>_vs_best_ref`, `P_<m>_gt0`, `ci80_<m>` and the grade `evidence_<m>`:
  STRONG = ALL-slice (14 folds minus HOLDOUT) 95% lower bound > 0 AND point delta > 0 on both TUNE and LATE; SUGGESTIVE = P(delta>0) >= 0.8 on both TUNE and LATE; NONE otherwise. With `--late` the grade is written in the ALL-slice VERDICT
  (which also carries the ALL-slice deltas, 95% lower bound, P and 80% interval, plus TUNE_/LATE_ point deltas and P); the TUNE and LATE VERDICTs say 'see ALL'. Without `--late` only TUNE exists: the column says 'TUNE only (P=..)'. HOLDOUT VERDICTs report deltas and P and are not graded.
  **Why graded, not "lower bound > 0"**: dev evidence uses this graded scale on purpose, because the sealed run is the strict final test. Reason: strict lower-bound gating on dev was judged possibly too strong a filter for a subjective target, so the harness reports graded evidence in dev and keeps the strict gate for the sealed run. A SUGGESTIVE grade is a reason to keep a direction alive in dev, not a claim.
  **dWA vs best meta**: columns `dWA vs best meta` (name of the model), `dWA vs best meta lo95` and `dWA vs best meta P(d>0)`: wa_sauc delta of the model vs the best of (duration, meta_gbm, nonaudio_gbm), the best chosen by the slice's POINT wa_sauc.
* `SUSPECT CONSTANT SCORES` is printed (top of the output) when more than 50% of a model's scores in a fold fall in one tie block (shortcut rows are exempt). The artist_plays / artist_recent / artist_love_rate baselines trigger it by design in folds where most pool songs are by unknown artists (score 0).
* One summary number hides that tests can be good to different degrees at different times / listening frequencies: read the per-fold table, macro_sauc, wx_sauc and the BREAKDOWN tables, not only pooled sauc.

## Null control v3 (`--null-control [--null-seeds N]`, run.py `run_null_worker`, `null_report`)
Train is modified, candidates are not: (1) song-identity shuffle (every train song takes another train song's ids/title/artist, keeping its own timestamps); (2) a random bijection over ALL artist ids appearing in train U cands is applied to train only (`artistIds`, `artist`, and the artist part of the song key,
consistently per song), and one over all album ids of train U cands to `albumId`; meta of the train tracks (`artistNames`, `albumName`) follows the relabelling. A candidate's artist therefore maps to a random OTHER artist's (or no) history, and per-artist song counts no longer line up with candidate artists.
**Every seed runs in a FRESH python process** (subprocess `python -m evalkit.run --_null-worker ...`, seed = cutoff yyyymmdd + k, k = 0..N-1) that imports the predictor anew, with the environment variables `EVALKIT_NULL_SEED=<k>` and `EVALKIT_NO_FIT_CACHE=1`, so no in-memory cache can carry over between seeds.
**Predictors must either key any disk cache on a hash of the train identities (trackId, song, artistIds) or skip disk caches when `EVALKIT_NO_FIT_CACHE` is set** (and a fit cache must include the seed / the identities of any relabelled or shuffled labels in its key). The harness baselines do both (`baselines._train_key`: null seed + position-weighted hashes of trackId / song / artist / timestamps; cache bypass with EVALKIT_NO_FIT_CACHE).
`--null-seeds N` (default 3): the band is that of an N-seed mean (mean of N independent label permutations of a fixed random score, 200 times; cached per N). Printed per slice (TUNE, and LATE / ALL with --late) and model (baselines + your predictors; shortcut rows and `ref_audio_final` are exempt): real, per-seed and mean sauc, wa_sauc and new-artist sauc;
the real-minus-null gap with an artist-cluster bootstrap CI; and a label: **PASS** iff the N-seed mean of sauc, wa_sauc and new-artist sauc each lie inside the band, otherwise **FLAG**. **A FLAG is not an automatic fail**: a FLAG on a content model has to be EXPLAINED by the builder or devil's advocate, e.g. with random-label refits in the predictor's own feature space
(do the same features, fitted to random labels, reach the same score?). Currently 4 of the 7 baselines FLAG (the null score of a predictor with a fixed, label-independent skew, e.g. through duration or popularity, does not average to 0.5), so a FLAG alone does not show leakage. `--null-control-identity` keeps the old identity-only shuffle (one seed = cutoff) as a DIAGNOSTIC (not gated): it preserves
per-artist song counts, which is real history information. A null run replaces the normal tables (no VERDICT, no independence check) and is slow (N seeds x folds x models, one process start per seed). The selftest asserts that an identity-blind module-level cache gives identical scores in one process but different scores across fresh-process seeds, and that the harness' own null seeds differ.

## Baselines (always scored together with your predictor; all pool independent and gate-checked)
`popularity`, `artist_plays`, `artist_recent` (180-d half-life), `artist_love_rate`, and the HistGradientBoosting baselines (fixed params, random_state=0, 2 threads; training rows = train songs first played
before cutoff-90 d, labels from song_table(train)):
`duration` (durationMs alone), `meta_gbm` (duration, explicit, popularity, preview present, #artists, title length, album==title, title keyword flags), `nonaudio_gbm` (meta_gbm + point-in-time artist
history: artist plays all-time and 180-d half-life, smoothed love rate of matured songs, #earlier songs, days since last played, featured artist known, new-artist flag; training songs use only
streams before their own first play). **nonaudio_gbm is the reference any music/content claim must beat.** No noise is added to baseline scores (ties stay ties). `random` is no longer a scored model: chance = 0.5
(plus the permutation band). 
DIAGNOSTICS (computed inside the harness from raw pool data; they use post-cutoff information, are not valid predictors, are exempt from independence checks, reported as references):
`pool_artist_siblings`, `pool_album_siblings`, `exposure_before` (minus the number of distinct songs first played EARLIER in the same session than the candidate's first play), `exposure_after` (minus the number first played LATER in that session),
`exposure_session` (minus the total = before + after + 1; unchanged from v3), `replays_first_session` (plays of the candidate within its first session), all with decoys below every tried song (replays: 0),
`oracle_day1` (plays on the first-listen day), `oracle_7d` (plays in the first 7 days; decoys 0). The oracles show how much of the label is behavioural, not musical.
PLAINLY: `exposure_after` and `replays_first_session` can be CONSEQUENCES of liking the song (a liked song is replayed and the listener keeps going, so more new songs follow it in the session), whereas `exposure_before` cannot be: it is fixed before the song is first heard.

## Rules for builders
* Never run `--sealed`, never read `.sealed/`, never import `decoy_universe` / `make_decoys`, never read raw streams (use `evalkit.data` loaders).
* Do NOT read `spotify-liked-songs/listening_stats.csv` at all (lifetime aggregates incl. the sealed era).
* Do NOT read `top_tracks.json` except through `evalkit.data.load_meta` (it holds lifetime play counts). `playlist_names.json` may be read.
* Any fitted transform (scaler, PCA, clustering, vocabulary, normaliser, embedding post-processing, model) must be fit only on tracks that appear in the train streams for that cutoff,
  never on pool, decoy or later tracks. A cache of per-track features is fine only if each track's features are computed independently of other tracks.
* Missing-preview handling must be explicit and reported.
* `--null-control` (null v2, below; TUNE slice) must be run on the final predictor and must PASS.
* Registration + hash logging (`register.py`, `late_runs.log`, sealed `runs.log`) is an audit trail, not a cryptographic lock.

## Commands (run from /home/user/Listener/taste-model)
    python3 -m evalkit.selftest                          # leakage/sanity checks
    python3 -W ignore -m evalkit.run --fast [pred.py ...]  # iteration: TUNE slice, nboot 100, no independence check, no LATE output
    python3 -W ignore -m evalkit.run [pred.py ...]         # TUNE slice, nboot 300, independence check on  (baselines are always included)
        --late          also score the LATE slice; tables printed separately for TUNE, LATE and ALL (logged in .cache/late_runs.log)
        --null-control            null control v2 (3 seeds, gated); with --late also scores LATE and ALL
        --null-control-identity   old identity-only shuffle, diagnostic only (can be combined with --null-control)
        --nboot N  --indep-n N  --window all|730|365|sub365
    python3 -m evalkit.register pred.py name             # MAIN SESSION ONLY: pre-register final model(s)
    python3 -W ignore -m evalkit.run --sealed pred.py    # MAIN SESSION ONLY: one look per registered file, logged with its hash
    python3 -m evalkit.make_sealed [--write-manifest]    # MAIN SESSION: regenerate .sealed/labels.csv, verify against sealed_manifest.json
    python3 -m evalkit.make_decoys [--sealed]            # build-time: fetch artists (stats.fm) and write the decoy universe (--sealed adds the sealed folds' seeds)
    python3 -m evalkit.fetch_itunes                      # build-time, rate limited (~20 requests/min): iTunes preview fallback lookups (resumable)
    python3 -m evalkit.fetch_previews [--report]         # shared preview-audio cache, see below
Predictor: `predict(train, cands, meta, cutoff) -> one finite score per candidate row` or a dict `PREDICTORS = {name: fn}`.
Caches (all git-ignored, regenerable from code; changing data.py / metrics.py / baselines.py changes the hashes and rebuilds them): pools `.cache/shared/evalkit-pools-<hash>.pkl`, baseline scores `evalkit-baseline-scores-<hash>.pkl`, permutation bands, `.cache/album_release.json`,
`.cache/itunes_fallback.csv`, `.cache/decoy_raw`, `.cache/decoy_universe.csv.gz`. The Workflow-2 predictors and their feature caches were removed in the Workflow-3 cleanup (they covered the old pools only); current per-track caches are listed in `.cache/shared/FEATURES.md`.

## Shared preview-audio cache (`.cache/shared/previews/`, built by `evalkit/fetch_previews.py`)
Every distinct previewUrl (incl. iTunes fallbacks) in the meta of any DEV fold (train tracks + tried and decoy pool tracks of all 14 dev cutoffs): `audio/<md5(previewUrl)>.<ext>` = the original
downloaded bytes (mp3/m4a), unchanged; `manifest.csv` columns md5, previewUrl, ext, bytes, duration_s (ffprobe), source (spotify / itunes_meta / itunes_fallback), ok, error. Previews are keyed
by the RAW url; look a track's file up through `meta.previewUrl` (md5 of the url string). The manifest lists exactly the urls needed by the current dev pools (10288 ok rows; v3.1 rebuilt it after the 2021-07 / 2021-10 pools were regenerated).
Per-track feature caches built from these previews (round 1) are documented in `.cache/shared/FEATURES.md` (read-only shared inputs).

## History-length / drift ablation (ablate.py)
`--window 730|365|sub365` trains on the last 2y / 1y / a random subsample of ALL history with the same number of streams as the last year. Compare 365 vs sub365 per fold. Dev only.

## Late slice (seen-once-per-design) and the sealed folds
`.cache/late_runs.log` holds one line per `--late` run. Its lines timestamped 09:00-09:05 UTC on 2026-11-21 are devil's-advocate audit looks at the round-1 predictors (the lead's brief counts 3 looks; the log has 4 lines in that window, 2 for the same file), and the round-1 LATE results are public. LATE is therefore a 'seen-once-per-design' slice, not an untouched one;
the sealed folds are the only untouched test.

## Comparability
v3.1 vs v3: folds, labels, decoy draws (for 8 of the 10 TUNE folds bit-identical; the 2021-07 and 2021-10 pools were rebuilt and ~20-27% of their decoys differ from the cached pools of round 1, see the report) and the baselines' scores are unchanged, so v3 sauc / wa / p20 are comparable
(except those two small folds). New in v3.1: gc, gc_wa, evidence grades, null v2 (v3 null-control results are NOT comparable: use `--null-control-identity` for the old shuffle), exposure_before / exposure_after / replays_first_session.
v2.x scores (8 dev folds 2023-01..2024-10, old decoys seeded by lifetime artist plays, old baselines with noise, thresholded bar) are not comparable to v3 numbers. For a like-for-like check use
the per-fold AUC table: folds 2023-01..2024-10 exist in both, but the decoy pools, preview fill and (for baselines) tie handling changed.

## Known limitations
* Pools are shaped by the user's choices; decoys are an approximation of an open catalogue (stats.fm tracks of seed artists, <=200 per artist, spotifyPopularity measured in 2026).
* spotifyPopularity is measured in 2026 (mild look-ahead; public prior). 27% of user tracks have popularity 0 (missing).
* Pretrained audio models may have seen sealed-era songs (unavoidable). Preview availability may correlate with taste (untested); iTunes lookups are rate limited (~20/min).
* Early folds are tiny (2021-07: ~50 tried songs, love rate ~65%), their AUC is very noisy; sauc pools pairs across folds.
