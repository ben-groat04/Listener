## Assessment
RESEARCH LEAD, Workflow 4 round 2. Start 2026-11-21T14:57:44Z, end 14:59:36Z (from `date -u`, recorded in <W4 scratch path, not available>). I touched no sealed data, read nothing under .claude/, used no git history and made no commits.

WHAT I RAN (dev only)
- I read the evalkit v4 code: label definitions in data.py, cap checks, the null band and the verdict in run.py, and describe.py. I also listed .cache/holdout_runs.log. It has 3 lines: the engineer's dummy and the two round-1 finals.
- q1.py (in my scratch folder) checks how stable the label is on TUNE non-holdout tried songs (n=1074, love rate 0.318):
  - Songs loved in their first 90 days have a median of 14 plays in days 90-365; not-loved songs have a median of 0.
  - Spearman between plays90 and days-90-365 plays is 0.73.
  - The 90-day love label predicts long-term keeping (>=6 plays in days 90-365) at AUC 0.85. 289 of the 342 loved songs are kept.
  - exposure_before predicts love at 0.603 and long-term keeping at 0.605.
  - My conclusion: the love label is a stable measure of lasting taste, not mostly 90-day noise. The encounter context (how many new songs came earlier in the same session) is linked to both short- and long-term outcomes, and this context is fixed before the first listen. Part of what decides love is therefore how and why the song was encountered, which no content model can see. For this reason I make the exposure-stratified metric (wx) a co-headline rather than relabelling. That answers the unvetted session-direction idea as far as dev data can: exposure_before is not a consequence of liking, yet it predicts love even among songs not replayed (describe: 0.599). So the context that comes before the listen is at least part of the link.

WHAT I RELY ON WITHOUT RE-RUNNING (reproduced by the devil's advocates)
- Round-1 finals on dev:
  - w4r1_final (whole-listening panel signal on MERT): ALL 0.652 vs ref_audio_final 0.628.
  - final_content (MERT + essentia + duration GBM): ALL 0.645.
- HOLDOUT: ref 0.657, w4r1_final 0.640, newonly 0.652, final_content 0.664, abl_no_dur 0.664.
- The gains over ref are about +0.01 to +0.02, not significant, and inside what TUNE selection produces: neighbouring and random configurations of the same family average around ref.
- The gains sit in known-artist pairs and do not appear for new artists on HOLDOUT. With the candidate's own artist removed from training, w4r1's gain over newonly falls to +0.005.
- Single-head 'property' findings do not survive a cluster-aware 605-way null (p=0.16).
- Random-label refits of both builders' models average about 0.49-0.51 with SD about 0.035-0.043. So the null-control FLAGs mean the harness's song-level band is too narrow for feature-based models. They are not leakage.
- Loopholes: the LATE and HOLDOUT caps hash only the entry file, so a file that imports the main predictor gets an extra look. This happened once on LATE.
- HOLDOUT keeps holdout artists' pre-cutoff history in train, so it tests selection hygiene, not artist-free generalisation.

WHERE THE PROJECT STANDS
- Content-only models plateau at about 0.63-0.66 pooled AUC on every slice. Two very different round-1 ideas each added about +0.015, mostly through known-artist pairs.
- Three problems now matter more than another blend of the same features:
  - (a) Honest selection. Every builder picks from about 80 variants on TUNE, which inflates TUNE by about the size of the gains being claimed.
  - (b) Generalisation to new artists. This is what the eventual candidate search needs, and no model has shown a gain there that holds on HOLDOUT.
  - (c) Representations that are learned rather than averaged. Every model so far is linear on clip means; per-patch essentia embeddings now exist and nothing learned has used them.
- The scoring was re-examined. My reading of the evidence: the label itself is sound (stable, predicts long-term keeping), but pooled sauc mixes in encounter context that no content model can know. The changes:
  - Make wx (pairs within the same exposure_before bucket) a co-headline.
  - Add a long-horizon 'keep' label variant to the label table.
  - Report new-artist sauc as a co-headline.
  - Add a walk-forward selection score that measures a builder's whole selection procedure, not its best pick.
  - The love threshold stays primary. Changing the evaluation label to chase a higher number would not show better taste prediction, but every label variant is reported.

DECISIONS
- Evaluation:
  - Close the cap loopholes with a bundle hash over imported project code.
  - Set a HOLDOUT budget of exactly one run per round-2 builder.
  - Add a pooled DEV+HOLDOUT number in the holdout output.
  - Null control v4: an artist-block permutation band built from the model's own null scores, 5 seeds by default. FLAG only outside that band.
  - Walk-forward selection.
  - Add the round-1 finals as cached references, with a stacking API so builders can use reference scores without reading other agents' folders.
- Shared prep: complete the 188 missing essentia clips; build the dropped time-resolved descriptors (with chroma and key, no HPSS); build one memory-mappable per-patch and clip-level index so builders stop rebuilding compact files. All of it goes in new directories only.
- Builders:
  - A: learned representations over the time-resolved, per-patch features, which tests properly whether learned temporal or nonlinear structure beats clip-mean linear models. This also covers the untested 'parts' hypothesis without prescribing it.
  - B: generalisation to unseen artists and honest selection, the end-goal axis.
  - Both are content-only primaries, must report walk-forward, wx, new-artist and noart results, and get one HOLDOUT run each.

NOT VERIFIED BY ME: how much engineer time the walk-forward and null v4 changes need; whether the workflow lifts FROZEN for a round-2 shared prep (if it does not, shared prep should be skipped and builders use the existing caches).

## Evaluation changes specified
ENGINEER SPEC: evalkit v4.1. Iterate with the fast mode. Do NOT rebuild pools, decoys, universe, previews or labels; dev pools must stay bit-identical (keep the selftest digest check). Never run --sealed or make_sealed. Never run --holdout with a real predictor; to test the --holdout path use a dummy random scorer and a TEMP log file. Your test must not consume a line in the real .cache/holdout_runs.log or .cache/late_runs.log; if the permission system blocks path overrides, add an explicit `--log-dir` option for tests and use it. Write any test lines to the temp location only.

1. CAP LOOPHOLES (bundle hash).
   a. Define bundle_sha256(predictor files): import the predictor in a subprocess and collect every module whose __file__ lies under /home/user/Listener/taste-model/ but NOT under evalkit/. Hash the sorted concatenation of (relative path, file sha256), together with the entry files.
   b. The --late cap (2 per hash) and the --holdout cap (1 per hash) apply to BOTH the entry-file sha256 AND the bundle hash. A run is refused if either has reached its cap. Log both hashes in new lines. Existing lines keep counting by their entry sha256.
   c. Also refuse a --late or --holdout run if any model name in the file's PREDICTORS produces, on the first fold of that slice, a score vector with Spearman >= 0.999 to a model already logged for that slice. Store the first-fold score vector per logged model in a side file `.cache/<late|holdout>_fingerprints.pkl`. Backfill is not required for old lines.
   d. HOLDOUT BUDGET: create `.cache/holdout_budget.json` = {"round": "w4r2", "remaining": 2}. Each successful --holdout run decrements it, and the harness refuses when it is 0. README: one run per round-2 builder, on its pre-declared final file. Devil's advocates never run it.
   e. Selftest: the importing-wrapper case is refused (temp logs), and the fingerprint check refuses a renamed copy.

2. HOLDOUT OUTPUT. In the same --holdout call, also score the main (non-holdout) 14 folds and print a pooled slice DEV+HOLDOUT (ALL ∪ HOLDOUT-ALL, 2450 tried songs), using the global artist bootstrap. Show sauc, wx, wa, macro, new-artist sauc and deltas vs every reference, not graded. Append the DEV+HOLDOUT sauc, wx and new-artist sauc with CIs for each model to the log line.

3. HEADLINES AND LABEL TABLE.
   a. VERDICT: add columns wx (with CI and delta vs best_ref, lo95, P) and new-artist sauc (with delta vs best_ref, lo95, P). Grade sauc, wx and new-artist sauc with the same STRONG / SUGGESTIVE / NONE rules. wa and gc stay as they are.
   b. Label-variant table: add `keep` = >=6 plays in days [90, 365) after the first play. Compute it only for folds whose first-play window plus 365 days ends before DEV_END (all TUNE folds qualify; LATE folds print n/a). Add `strong`, `love_4_2`, `love_10_4` and `keep` sauc columns for each model to a printed LABEL VARIANTS table (TUNE only), with CIs.
   c. Labels for prediction and training are unchanged. Predictors never see `keep`.

4. WALK-FORWARD SELECTION (`--walkforward`, allowed only with --fast, TUNE only).
   a. The family is a file's PREDICTORS dict, or the list `WALKFORWARD_FAMILY` if the file defines it.
   b. For each TUNE fold k, the composite uses the family member with the highest pooled sauc over TUNE folds before k that have at least 10 loved and 10 not-loved rows. Fold 1, or any fold with no eligible earlier fold, uses the first listed member.
   c. Output:
      - the chosen member per fold;
      - the composite's pooled sauc, macro, wx, wa and new-artist sauc with CIs;
      - paired deltas vs every reference row and vs the single best member chosen with hindsight;
      - the 'optimism' = best-hindsight sauc minus composite sauc.
   d. No caching of member choices across runs. Add a selftest that compares against a brute-force recomputation on 3 dummy members.

5. NULL CONTROL v4.
   a. Default `--null-seeds 5`. Keep fresh-process seeds with EVALKIT_NULL_SEED and EVALKIT_NO_FIT_CACHE.
   b. New statistic: rank-normalise each seed's scores within fold, average them per candidate across seeds, and compute sauc and wa of that averaged score.
   c. New cluster-aware band: 300 artist-block label permutations of that same averaged score vector. Within each fold, swap whole artists' label vectors among artists with the same number of tried rows. Artists whose count is unique in the fold are pooled with the nearest count, and their labels are shuffled within the merged block. Report the 2.5-97.5% band.
   d. PASS / FLAG uses the cluster-aware band. Also print the old song-level band and label, marked 'song-level (too narrow for feature models; for comparison)'.
   e. Keep the per-seed numbers, the real-minus-null gap with CI, and the wa and new-artist rows.
   f. Selftest: an artist-constant random scorer must PASS under the cluster-aware band in at least 9 of 10 dummy runs (assert).
   g. README: describe v4 and state which baselines FLAG under the new band, as measured by you.

6. REFERENCES AND STACKING.
   a. Add two cached reference rows:
      - ref_w4r1_listening = PREDICTORS['w4r1_final'] in predictors/w4r1-taste-from-all-listening/predict.py;
      - ref_w4r1_music = PREDICTORS['final_content'] in predictors/w4r1-what-in-the-music/predict.py.
   b. Make sure any cache files they need regenerate automatically from their build scripts if absent (call the builders' build_compact.py etc. from the harness if needed).
   c. Their fit caches must be identity-keyed. Check this, and fix the key only if needed, without changing the scores. If you change their files, record the before and after score equality on fast TUNE.
   d. Cache their scores as for ref_audio_final. best_ref keeps its definition: the highest TUNE point sauc among the references.
   e. New module `evalkit.refs` with `score(name, train, cands, meta)`, for name in {ref_audio_final, ref_w4r1_listening, ref_w4r1_music}. It returns the reference's scores for those candidates by calling the reference code on the given train (train-only fits, identity-keyed caches). Predictors may call it for stacking. Document it in the README. Stacking members inherit the reference's training choices.
   f. Exempt the references from the null control, but a predictor that calls evalkit.refs runs them on the null train like any other code. Verify this with one fast null run of a dummy stacker that returns ref_audio_final via evalkit.refs.

7. MISC.
   a. Print runtime per model in fast runs.
   b. Bump to v4.1. Document comparability: v4 numbers stay comparable on sauc, wa, gc and macro (same rows, same bootstrap); the new columns are additions.
   c. Re-run the selftest. Report fast TUNE numbers for all baselines and the 3 references under v4.1, including wx, new-artist and the label table; the walk-forward output for the round-1 w4r1-taste-from-all-listening PREDICTORS family; and the null v4 PASS / FLAG for the baselines and for the dummy stacker.
   d. State runtimes.

## Shared prep specified
SHARED PREP round 2 (cap 120 min; 4 threads only while no other agent runs). Do this only if the workflow has lifted /home/user/Listener/taste-model/.cache/shared/FROZEN for this step. If FROZEN still exists when you start, build nothing, report that, and stop.
- Add only NEW directories. Never modify or delete existing files under .cache/shared/, except to append new sections to FEATURES.md and to regenerate MANIFEST.txt.
- Everything is per clip or a re-indexing of existing per-clip outputs. No fitted cross-track transform.
- Benchmark each step on 50 clips and write a runtime estimate and go/no-go before each full pass.
- Make every step resumable and put regenerate commands in FEATURES.md. Code goes in the project folder the workflow assigns to shared prep.
- Priority S1 > S2 > S3. Stop starting new work at 105 min. Never publish a cache without its coverage stated.

S1. Complete essentia (new dir `.cache/shared/w4-essentia-extra/`).
- Run the exact P1 code and models (same essentia-tensorflow wheel, same heads, no artist or label embeddings) on the 188 ok-manifest clips missing from w4-essentia (blocks 199, 203, 204, 205).
- Same shard format and array names; list the md5s covered.
- Verify on 4 already-covered clips that a rerun matches w4-essentia (max abs diff), and report it.
- Expected about 2-5 min.

S2. Time-resolved hand-crafted descriptors (new dir `.cache/shared/w4-descriptors/`).
- librosa 1.0.1. Decode each ok-manifest clip once to 22,050 Hz mono, no normalisation. No HPSS.
- Frame-level series aggregated to 0.5 s steps: RMS dB, spectral centroid, bandwidth, rolloff 85%, flatness, contrast (7 bands), zero-crossing rate, onset strength, chroma_stft (12), MFCC (20).
- Clip level:
  - tempo and beat-strength statistics;
  - Krumhansl-Schmuckler key and mode on mean chroma, with the correlation value;
  - loudness range (p95 minus p10 RMS dB);
  - dynamic contrast (max minus median RMS);
  - onset rate;
  - RMS slope;
  - chroma entropy.
- float16 shards keyed by md5, feature names in JSON, step times stored.
- Benchmarked earlier at about 0.44 s/clip without HPSS (chroma will add some). Expected 25-40 min on 4 workers. If the estimate exceeds 70 min, drop MFCC and contrast series (keep clip-level values) and document the drop.

S3. Consolidated, memory-mappable index (new dir `.cache/shared/w4-index/`). Pure re-indexing, no transforms.
- (a) `tracks.parquet`: one row per trackId that appears in train, tried or decoy of the 14 dev folds (main + holdout). Columns: md5 of its preview (via the same trackId-to-preview mapping documented in FEATURES.md), preview source, and has_* flags for MERT, CLAP, essentia (w4-essentia or w4-essentia-extra), descriptors and lyrics.
- (b) `clip_level.npz` with arrays in md5-sorted row order plus an md5 array:
  - MERT clip features in the layout documented in FEATURES.md (all stored windows and layers, unchanged);
  - CLAP vector;
  - essentia head clip mean and max, effnet clip mean and std;
  - descriptor clip-level values (if S2 was built).
- (c) `patches_emb.npy` (float16 memmap, [total_patches, 1280]), `patches_act.npy` ([total_patches, 605]) and `patches_t.npy` (centre times), with `patch_offsets.npy` (start and end row per md5 in the same md5 order), merged from w4-essentia and w4-essentia-extra.
- Report shapes, dtypes, disk size and load time.

FINALLY:
- Append FEATURES.md sections for each new directory: keys, shapes, dtypes, what a row means, time resolution, coverage per slice (TUNE / LATE / ALL, train / tried / decoy, in the existing table format), regenerate commands, measured runtimes and anything dropped. Facts only, no advice on use.
- Regenerate MANIFEST.txt to include the new non-bulk files.
- Recreate FROZEN.