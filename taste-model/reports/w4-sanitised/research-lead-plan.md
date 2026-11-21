## Assessment
RESEARCH LEAD, Workflow 4 round 1. Start 2026-11-21T10:47:55Z, end 10:53:04Z, both from `date -u` and recorded in <W4 scratch path, not available> I did not touch sealed data, did not read .claude/, used no git history and made no commits.

WHAT I RAN (dev only; scripts q1.py and q2.py are in my scratch folder)
- q1: loaded dev streams through evalkit's loader. Result: 106,188 streams from 2020-06 to 2025-03. Every stream has playedMs >= 30 s, so skips are not in the data and cannot be used as a signal. About 90% of first plays run more than 80% of the track.
- q2: candidate counts per quarterly fold from 2020-10 to 2024-10. Dev has about 2,450 tried songs in total. The 2023-01 and 2023-10 folds hold about 68% of the TUNE loved x not-loved pairs. Folds from 2021-07 to 2022-10 have 40-120 songs from few artists (2022-10: 89 songs, 10 artists). Adding 2020-10 to 2021-04 would add only 46 songs, so it is not worth doing.
- Network checks: essentia.upf.edu models (200), api.deezer.com, huggingface, zenodo, lrclib and pypi are reachable. essentia-tensorflow 2.1b6.dev1389 has a cp313 manylinux wheel (the container runs Python 3.13). discogs-effnet .pb and .onnx files and the genre_discogs400 head download fine.
- Container: 32 GB disk free, 15 GB RAM, 4 cores. librosa 1.0.1, torch 2.15 cpu, onnxruntime, lightgbm and sklearn are installed.

WHAT I RELY ON WITHOUT RE-RUNNING
- The reviewers' verified findings: the null-control fit-cache bug in w3r1-content-audio (also imported by w3r2-integrated); preview-source and lyrics-record asymmetries in the open pool (has-lyrics flag AUC 0.706); two folds dominating pooled TUNE; nonaudio_gbm (0.559) losing to artist_recent and artist_plays (0.619) on TUNE; LATE used at least 17 times.
- audio_final 0.621 on TUNE, reproduced by the results reviewer.

WHERE THE PROJECT STANDS
- One result holds up on dev: an artist-free MERT audio model, AUC about 0.62-0.63 on TUNE and LATE. It equals single-number familiarity baselines on TUNE and does not beat duration within artist (0.607 vs 0.598).
- Workflow 3 tried 38 variants of ridge, GBM and SVR on MERT, with CLAP and four 5-s windows. All sat at 0.59-0.62, so the MERT-plus-new-song-outcome approach looks saturated.
- Two inputs have not been tried:
  - Training signal: the models learned only from new songs' 90-day outcomes. They never learned from the whole pre-cutoff listening record, which shows what the user plays heavily at each time and what they tried and dropped. It is a much larger signal than about 1,000 matured new songs.
  - Representation: nothing musically interpretable or time-resolved exists. There are no style/genre/mood/instrument activations and no frame-level loudness, timbre or harmony curves. The only test of "parts" used four fixed windows of a MERT mean.
- Evaluation integrity is the most urgent problem. LATE is partly used up and TUNE has been tuned heavily, so a new untouched dev slice is needed before more iteration. A random time slice is impossible (dev ends at 2025-04 and the later data is sealed), so I choose an artist-disjoint HOLDOUT: about 25% of primary artists, chosen by salted hash, across all 14 folds. No new iteration can score it, and it is run once per final predictor. LATE stays as the time-drift check (minus HOLDOUT artists, at most 2 runs per hash). TUNE loses about 25% of its rows. I accept that cost.
- Pooled sauc stays the primary number. Next to it come macro-over-folds, per-fold results and a subgroup breakdown, which addresses the "one score hides differences" idea. The artist bootstrap becomes global across folds, so intervals get wider and more honest. The VERDICT compares against a reference set: nonaudio_gbm, artist_recent, duration, meta_gbm and the Workflow-3 audio_final, which the harness now scores as a cached reference. Beating nonaudio_gbm alone stops being enough.
- Null control: in v2 a predictor's fit cache can make the 3 seeds identical, and a fixed feature prior pushes content models (and duration and popularity) outside a band built for a random score. Fix: one fresh process per seed, a cache-disable environment variable, and an optional seed count. A FAIL becomes a flag that the devil's advocate must explain. It no longer silently disqualifies or certifies.

UNVETTED IDEAS (decisions)
1. Session direction: tested with a descriptive table (love rate by exposure_before x exposure_after x first-session replays) and a within-exposure_before stratified AUC. The labels are not changed until the evidence is in.
2. Evidence standard: graded evidence on dev and strict on sealed is kept. The new HOLDOUT gives a cleaner single look, which lowers the cost of accepting noise in dev.
3. One score hides differences: the breakdown table is added.

OTHER DECISIONS
- The love label, the 90-day horizon and the candidate definition stay as primary. gc (graded concordance) is kept. The label-variant table and the oracle rows remain the record of label subjectivity. Re-defining the label is not in this round's builder scope because the descriptive tables come first.
- Open pool: its primary metrics move to the subset of songs (tried and decoy) that have a Spotify-CDN preview, which removes the source and missing-preview shortcuts. The full open pool stays secondary, with shortcut baselines. Lyrics lookups are completed for decoys, so the lyrics shortcut goes away.
- discogs artist/label embeddings are excluded on purpose. They are trained to recognise artists (an artist-identity shortcut).

BUILDERS (2)
- A: learn current taste from the whole pre-cutoff listening record, content-only inputs.
- B: which musical properties, and which moments of a clip, carry the signal, using new interpretable and time-resolved descriptors.
- Both have content-only primary predictors. Artist history may appear only as a separately reported secondary variant, because history reversed in 2024. Both must report new-artist and within-artist results, a same-artist-excluded check, the gap to ref_audio_final, and HOLDOUT once.

Not done or not verified by me: essentia install and speed on this container (the shared-prep agent must benchmark it); the lrclib rate; whether the HOLDOUT bucket hits about 25% of songs in each fold.

## Evaluation changes specified
ENGINEER SPEC: evalkit v4. Use the fast mode for your own iteration. Do NOT rebuild pools, decoys, the universe, previews or labels: every change below only alters which rows are scored, how they are summarised, and the null/reference machinery. The dev pools must stay bit-identical to the current cached pools; assert this in the selftest by comparing the row sets against the current cache before and after. Never run --sealed or make_sealed. You may extend the sealed code path only so that it would accept the new reporting; do not execute it.

1. NEW HELD-OUT SLICE "HOLDOUT" (artist-disjoint).
   a. Define holdout artists in data.py by salted hash: holdout iff int(sha256("w4-holdout|" + str(primary_artist_raw_id)).hexdigest(), 16) % 100 < 25, using the raw stats.fm primary artist id before anonymisation. Treat songs with artist -1 as non-holdout.
   b. Report in the selftest the HOLDOUT share of tried songs and of loved songs per fold and overall. If the overall share of tried songs is outside 18-32%, change the salt suffix once (w4-holdout-2) and document it. Do not iterate further.
   c. HOLDOUT rows are the tried songs of holdout artists in all 14 dev folds, together with the decoys of holdout artists (open pool).
   d. In every non-holdout run (--fast, default, --late, --null-control), remove HOLDOUT rows from cands and from the pools BEFORE calling predictors. Train streams are unchanged: pre-cutoff history of holdout artists stays in train.
   e. TUNE = the 10 early folds minus HOLDOUT. LATE = the 4 late folds minus HOLDOUT. ALL = TUNE + LATE.
   f. New flag `--holdout` scores only HOLDOUT rows. It prints a VERDICT with three slices: HOLDOUT-ALL (14 folds), HOLDOUT-early (the 10 TUNE-era folds) and HOLDOUT-late (the 4 LATE-era folds).
   g. Cap: one --holdout run per predictor file sha256. The harness refuses a second run of the same hash, and refuses --holdout combined with --fast or --null-control.
   h. Each --holdout run appends a JSON line to `.cache/holdout_runs.log`: UTC time, file paths, sha256, model names, and the HOLDOUT-ALL sauc / wa / gc / new-artist sauc with CI for each model. Devil's advocates can then read the results without re-running.
   i. README: HOLDOUT is run once, by a builder, on its final pre-declared predictor, after writing the declaration in its report. Devil's advocates never run --holdout.
   j. Baselines and reference rows are scored on HOLDOUT in the same call.

2. LATE. Keep the cap of 2 --late runs per predictor hash. Add a selftest check that the cap logic refuses a third run (use a temp log). De-duplicate nothing in the existing log; append only.

3. BOOTSTRAP. Change the artist-cluster bootstrap so that a cluster is the primary artist GLOBALLY: all rows of an artist in every fold of the slice are drawn together. Keep pair weights as products of draw counts, and keep shared resamples across models so deltas stay paired. Update the metrics brute-force selftest.

4. SUMMARIES.
   a. Next to pooled sauc, print `macro_sauc`: the mean of per-fold AUC over folds that have at least 10 loved and at least 10 not-loved rows in the slice, with a CI from the same resamples.
   b. Print a per-fold AUC table for every model by default.
   c. Add `wx_sauc`: pairs sharing fold AND exposure_before bucket (0, 1-2, 3-8, 9+). It is computed from harness diagnostics and never shown to predictors. Treat it like ws: CI, permutation band, paired deltas.
   d. Add a BREAKDOWN table, printed in fast and full runs. For each model it shows sauc with CI by: fold; new vs known artist; exposure_before bucket; the tercile of the user's total plays in the song's own 90-day window, with tercile edges fixed over the dev tried songs; release-age bucket; and preview present vs absent.

5. REFERENCES AND VERDICT.
   a. Add `ref_audio_final` as a harness reference row. It is Workflow 3's audio_final, from predictors/w3r2-audio-taste/predict.py (MERT cache only). Fix its cache key as needed so that it is deterministic and identity-safe.
   b. Score it once per (code hash, cutoff, slice) and cache its scores in .cache/shared next to the baseline-score cache, so builders do not pay for it on every run. Exempt it from the null-control gate printout.
   c. The VERDICT shows deltas, with lower bound, P(d>0) and 80% interval, for sauc, wa, gc and macro_sauc against EACH of: nonaudio_gbm, artist_recent, duration, meta_gbm, ref_audio_final.
   d. Add a column `best_ref` = the reference with the highest TUNE point sauc, fixed from TUNE and applied to every slice. Base the evidence grade on best_ref instead of nonaudio_gbm. Keep the STRONG / SUGGESTIVE / NONE definitions, computed on TUNE / LATE / ALL with HOLDOUT excluded.
   e. HOLDOUT is reported with deltas and P, not graded.

6. NULL CONTROL v3.
   a. Run each null seed in a FRESH Python process (multiprocessing spawn, or subprocess), importing the predictor anew, so in-memory caches cannot carry over.
   b. Set the environment variables EVALKIT_NULL_SEED=<seed> and EVALKIT_NO_FIT_CACHE=1 in that process. Document in the README that predictors must either key any disk cache on a hash of train identities (trackId, song, artistIds) or skip disk caches when EVALKIT_NO_FIT_CACHE is set.
   c. Add `--null-seeds N` (default 3). The band is that of an N-seed mean. Cache bands per N.
   d. Selftest: a dummy predictor with an identity-blind module-level cache must give different scores across seeds. Assert this; do not just print it.
   e. Print: per-seed and mean sauc, wa and new-artist sauc; the real-minus-null gap with a bootstrap CI; and a PASS / FLAG label. FLAG means the mean is outside the band. A FLAG is not an automatic fail. The README must state that a FLAG on a content model has to be explained by the builder or devil's advocate, e.g. with random-label refits in the predictor's own feature space, and that 4 of 7 baselines currently FLAG.
   f. Fix the cache key in predictors/w3r1-content-audio/predict.py: add an identity hash of train trackId and song. Delete the broken predictors/w3r1-song-content-beyond-audio/null_seeds.py.

7. OPEN POOL.
   a. Primary open metrics (open_sauc all / new / known, open_wa, p20) are computed on the subset where BOTH tried songs and decoys have a previewUrl from the Spotify CDN, using the source column of previews/manifest.csv == spotify.
   b. The full open pool stays as a secondary table.
   c. Add two open-pool shortcut baselines: `has_preview` and `preview_source_itunes` (1 if the preview is iTunes-sourced). Score them in both open tables.
   d. Report counts of tried songs and decoys per fold in the subset.

8. LABEL DESCRIPTIVES (tests the unvetted session-direction idea).
   a. New module `python3 -m evalkit.describe`, TUNE non-holdout only. It prints:
      - love rate and n by exposure_before bucket x exposure_after bucket;
      - the same table split by replays_first_session (1 vs 2 or more);
      - AUC of exposure_before restricted to songs with replays_first_session == 1;
      - love rate by contextId present vs absent.
   b. Facts only, no recommendation.

9. HYGIENE.
   a. Fix or delete ablate.py. If kept, the window must filter training songs by first-play time, not truncate streams.
   b. Delete data.decoy_presample and fix the README text about presampling and about preview presence meaning the same thing.
   c. Include itunes_fallback.csv, decoy_raw and album_release.json CONTENT, not just size, in _pool_hash only if this does not change the current pool hash's cached content. If it would force a rebuild, instead add a selftest check that compares content hashes against a recorded value.
   d. Include run.py in _code_hash.
   e. Warn loudly, with "SUSPECT CONSTANT SCORES" in the output, when more than 50% of a model's scores in any fold are tied.
   f. Replace datetime.utcnow.
   g. README: "95% lower bound" means the 2.5th percentile of a two-sided interval.
   h. Bump to v4. Document comparability: no v3 number is comparable, because rows changed (HOLDOUT removed) and the bootstrap changed.
   i. Re-run the selftest. Report fast-run TUNE baseline and ref_audio_final numbers under v4.
   j. State the runtime of a fast run and of a full run.

## Shared prep specified
SHARED PREP (cap 120 min, 4 threads only while no other agent runs; everything per clip and independent of other tracks; no fitted cross-track transform). Inputs: every ok row of .cache/shared/previews/manifest.csv (10,288 clips, keyed by md5 of previewUrl). Put the build code in the project folder at the location the workflow assigns to shared prep. Make it resumable, and write a regenerate command into FEATURES.md. Benchmark each step on 50 clips first, and write a runtime estimate with a go/no-go before each full pass. Priority order: P1 > P2 > P3. P3 runs concurrently, since it is network-bound, using at most 1 thread. Drop lower-priority parts, never partially publish a cache without its coverage stated, and stop starting new work at 105 min.

P1. Essentia pretrained music models (directory `.cache/shared/w4-essentia/`).
- Install: `pip install essentia-tensorflow==2.1b6.dev1389`, the cp313 wheel.
- Fallback if it fails within 20 minutes: the plain `essentia` package for the mel front end plus onnxruntime running discogs-effnet-bsdynamic-1.onnx. Use the exact essentia front end (TensorflowInputMusiCNN-style, 16 kHz mono, as in essentia's model docs). If both fail, skip P1 and document.
- Models, downloaded from https://essentia.upf.edu/models/: discogs-effnet-bs64-1 (the embedding model) and these classification heads on discogs-effnet embeddings:
  - genre_discogs400 (400 styles)
  - mtg_jamendo_moodtheme
  - mtg_jamendo_instrument
  - mtg_jamendo_genre
  - danceability
  - voice_instrumental
  - mood_aggressive, mood_happy, mood_party, mood_relaxed, mood_sad, mood_acoustic, mood_electronic
  - tonal_atonal
  - approachability_regression and engagement_regression, if available for effnet.
- Add arousal/valence: emomusic or deam heads on msd-musicnn-1 embeddings, only if the benchmark shows the total P1 cost fits.
- Do NOT compute discogs artist or label embeddings: they are trained to identify artists, which is the shortcut to avoid.
- Decode each clip once to 16 kHz mono.
- Store, in float16 shards keyed by md5:
  (a) per-patch (time-resolved) head activations with patch centre times in seconds;
  (b) clip-level mean and max of each head;
  (c) clip-level mean and std of the 1280-d effnet embedding;
  (d) per-patch effnet embeddings, only if the total disk for P1 stays under 2 GB, otherwise omitted and documented.
- Record the label names of every head in a JSON file next to the shards.
- Expected cost: well under 1 s per clip; confirm by benchmark. Use up to 3 worker processes with 1 thread each.

P2. Hand-crafted time-resolved descriptors with librosa 1.0.1 (directory `.cache/shared/w4-descriptors/`).
- Decode once to 22,050 Hz mono, without z-scoring.
- Frame-level series at about 0.5 s resolution (aggregate from the native hop): RMS (dB), spectral centroid, bandwidth, rolloff (85%), flatness, contrast (7 bands), zero-crossing rate, onset strength, chroma_stft (12), MFCC (20), and harmonic share from HPSS. Drop HPSS if the benchmark shows it more than doubles the cost.
- Clip-level values: tempo and beat-strength statistics, the estimated key and mode (Krumhansl-Schmuckler on mean chroma, plus the correlation value), loudness range (95th minus 10th percentile of RMS dB), dynamic contrast (max minus median RMS), onset rate, and the slope of RMS over the clip.
- Store as float16 shards keyed by md5, with the feature names in JSON.
- Expected cost: about 0.5-1 s per clip per process. Use up to 3 processes, sharing the CPU budget with P1. If P1 and P2 together would exceed about 90 min, cut P2 to clip-level values plus RMS, onset and chroma series.

P3. Complete the lyrics lookups so tried songs and decoys are comparable (directory `.cache/shared/w4-lyrics/`).
- Copy every existing record from .cache/shared/w3r1-song-content-beyond-audio-lyrics/lyrics.jsonl. Do not modify the old directory.
- Look up, with the same lrclib query and acceptance rules as predictors/w3r1-song-content-beyond-audio/fetch_lyrics.py, every train, tried and decoy track of the 14 dev folds (opaque trackId keys) that has no record.
- Polite rate. Resumable. Time box 75 min.
- Then build feats.pkl and emb.pkl for the new records with the same code and model as Workflow 3, into the new directory.
- Report record and found rates for tried vs decoy, in the same table format as FEATURES.md.

FINALLY: append sections for w4-essentia, w4-descriptors and w4-lyrics to .cache/shared/FEATURES.md. For each give keys, array shapes and dtypes, what one row means, time resolution, coverage per slice and group (in the existing format), the exact regenerate command, the measured runtime of each pass, and anything dropped. Facts only, no recommendation about use. Then create .cache/shared/FROZEN.