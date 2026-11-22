# Sealed-test pre-registration, Workflow 6

Written by the Workflow 6 final research lead on 2026-11-22, before any sealed scoring. Nothing here has been run on sealed data. Nobody has run `--sealed`, registered a file or read `.sealed/`. **Only the main session runs the steps below, and only after the owner has seen the dev results and approved.**

Harness: evalkit **v5.3** (sha256 of every evalkit file in `FILES.sha256`). `make_sealed.py`, `sealed_manifest.json` and `register.py` are byte-identical to the hashes the engineers recorded at the start of this workflow.

## 1. What will be registered

Exactly **one** file:

| registered name | file | model inside | declared on dev |
|---|---|---|---|
| `avg21_dev` | `predictors/w6r1-content-ranker-final/final_avg21_dev.py` | `avg21_dev` (one model) | `w6r1_avg21_dev`, 2026-11-22T12:06:20Z, sha256 `d2ce1c31b35842e3b84b20ba61b23e4a3515c830f4abf4e3ed64f79981fa898d` |

Bundle: the registered file is a thin wrapper. It loads `predict.py` in the same folder, which imports `grid.py` in that folder and `evalkit.features`. All three predictor files, every evalkit file, the MERT extractor and the incumbent's code are hashed in `FILES.sha256`. Run `sha256sum -c prereg-w6/FILES.sha256` from `taste-model/` before registering. If any line fails, stop and report it. The registry and the declaration hash only the thin wrapper, so `FILES.sha256` is the only guard on `predict.py` and `grid.py`. It covers every code file the registered model executes: the wrapper, `predict.py`, `grid.py`, `evalkit/features.py`, `evalkit/data.py`, `evalkit/refs.py` (imported by `predict.py` for the reference members), the whole of evalkit, the incumbent reference code, and also the dev feature caches the model reads (dev MERT shards `.cache/shared/w3r1-mert-v1/shard_*.npz` and `.cache/w4r1/compact.npz`). There is no threshold or constant outside these files; the only clip rule is that a song with no clip scores 0, which is in `predict.py`. The optional second-excerpt cache of `predict.py` (`.cache/shared-w6r1/`) is not read by `avg21_dev` and is not hashed.

What the model is: an equal average of 21 training-signal configurations of the Workflow 4/5 listening recipe. Input is MERT-v1-95M features of 4 windows of 5 s from the song's 30 s preview (layers 4-8, mean over windows). The model applies whitened PCA and weighted ridge, trained only on per-song targets from the owner's pre-cutoff listening. It takes no artist, popularity or catalogue input. A song with no preview clip gets the neutral score 0. `FEATURES = ("mert",)`.

**Why only one file (mechanical rule of the evaluation design, applied on dev):**
- `avg21_dev` is the only declared candidate in this workflow that meets every eligibility condition and is POS against the incumbent: +0.008, 80% [+0.001, +0.012].
- `w6r2_avg21_fb` gives identical scores to `avg21_dev` (the harness treats it as the same predictor), so it is the same candidate.
- `combo_two_music` and `combo_dev_music` fail the independence condition: a song's score depends on the other candidates. `combo_two_music` also needs a second preview excerpt that the sealed pipeline does not produce.
- `blend_all_q` and `blend_inv_q` are not POS against the incumbent. They also need Deezer album, artist and related-artist fields, which the sealed pipeline does not produce.
- The round-2 content-ensemble builder declared nothing.
- No eligible candidate from another builder remains, so there is no secondary final.

## 2. Comparators and baselines

Fixed comparators (`run.COMPARATORS`, unchanged):
1. `artist_recent`: the artist-familiarity baseline.
2. `ref_w4r1_listening`: the incumbent model, computed by the harness as a reference with train-only fits. It needs no registration.

All other baselines and references (popularity, artist_plays, duration, ref_audio_final, ref_w4r1_music, ...) are printed for information only.

## 3. Steps, in order (main session only)

1. `cd /home/user/Listener/taste-model && sha256sum -c prereg-w6/FILES.sha256`. Every line must say OK.
2. Sealed labels: as the evalkit README requires, the main session regenerates and verifies `.sealed/labels.csv` with `python3 -m evalkit.make_sealed`. The run must agree with `sealed_manifest.json`. (Nobody in this workflow checked whether this was already done.)
3. Dry run: `python3 -m evalkit.sealed_prep --main-session --count`. It prints track counts, missing clips per group and a runtime estimate. It uses no network and no model.
4. Feature build: `python3 -m evalkit.sealed_prep --main-session --threads 2`. Use the default stages only (fetch, mert, compact).
   - **Do not pass `--essentia` or `--deezer`.** The final does not use them.
   - The command is resumable. If clips failed, run it once more with `--retry`.
   - It prints counts, runtimes and per-fold coverage only, never labels.
5. Coverage gate. Decided **before** any sealed score is seen, from the per-fold table that `sealed_prep` prints (columns `fold`, `group`, `tracks`, `has_key`, `mert`). The column that counts is **`mert`** (share of tracks with a MERT row); `has_key` is only the share with a clip. Read it for the groups `tried` and `train`.
   - Reason for the two levels: the harness decides on the **pooled** tried-song coverage (track-weighted over the 5 folds; STOP if below 90%), while this gate also looks at single folds. On dev the pooled tried-song MERT coverage was 0.926 but fold 2021-10-01 was below 90%, so a weak single fold is a real possibility.
   - **Pooled rule (the harness wins; no override).** Compute the pooled `tried` `mert` share. If it is below 90% after one `--retry`, report the per-fold table to the owner and stop. If the owner still wants the run, the harness will print `COVERAGE ... -> STOP` and `INTERPRETATION STOPPED`: S1, S2 and S3 are then **not evaluated**, there is no PASS or FAIL, and the printed numbers are information only, labelled "coverage-limited". The owner's go-ahead cannot lift the harness STOP, and this package does not change evalkit.
   - **Single-fold rule.** If the pooled share is at least 90% but a fold's `tried` `mert` share is below 90% (after one `--retry`), report the table to the owner before continuing. If the owner says go on, the harness interprets the pooled numbers, S1/S2/S3 are decided by the rules in section 4 and a PASS is possible, but every sealed number is labelled "coverage-limited (fold list)", and the per-fold AUC of the weak fold is flagged.
   - **Train-song coverage** (`group` = `train`) is checked and reported per fold from the same table. It is not a gate (the harness has no STOP for it); a fold with a `train` `mert` share below 90% is labelled "train coverage-limited". Songs without a clip get the neutral score 0, so low coverage lowers a model's score rather than inflating it.
   - After the run, the harness's own `COVERAGE avg21_dev` line (pooled tried-song `mert=`) must agree with the pre-run table. If it says STOP, apply the pooled rule above.
6. `python3 -m evalkit.register predictors/w6r1-content-ranker-final/final_avg21_dev.py avg21_dev`.
7. `python3 -W ignore -m evalkit.run --sealed predictors/w6r1-content-ranker-final/final_avg21_dev.py > <save path>.out 2> <save path>.err`. No `--nboot` option is passed, so the run uses the default of 300 resamples (see section 4). This is one look, logged with its hash. Do not run it a second time.
   - **Crash recovery.** The harness appends the look to `.sealed/runs.log` after scoring and before it prints any table. (a) If the run fails **before** that line is written (the file hash is absent from `runs.log`; e.g. a missing feature or a data error), nothing was looked at: fix the cause without touching the predictor files or evalkit, re-verify step 1, and run step 7 once more unchanged. (b) If the run fails **after** the line was written, the harness refuses a second run of this file ("already evaluated on sealed"). Do not work around it by editing, renaming or wrapping the file or by re-registering a copy: that would be a second look. Report to the owner the saved `.out` and `.err` files, verbatim, and which blocks were printed; quantities in blocks that were not printed stay unanswered, and the owner decides what to do. Whether the line was written is checked by the main session by hash only, without reading the contents of `.sealed/`.
8. Report every pre-declared quantity below to the owner, quoting the harness lines verbatim.

Note on the harness banner: the sealed output prints `INTERPRETATION STOPPED` if **any** model's pooled tried-song coverage is below 90%, and that includes the information-only reference `ref_w4r1_music`. Without `--essentia`, `ref_w4r1_music` will show essentia=0.000 and trigger the banner. Pre-declared handling:
- If the only COVERAGE lines that say STOP belong to `ref_w4r1_music`, the banner does not apply to `avg21_dev`, `ref_w4r1_listening` or `artist_recent`. Their numbers are interpreted.
- `ref_w4r1_music`'s numbers are not interpreted.
- If the COVERAGE line of `avg21_dev` or `ref_w4r1_listening` says STOP, nothing is interpreted. Report the coverage only.

## 4. Evaluation design, exactly as applied

- Slice: the 5 sealed folds, quarterly cutoffs 2025-04-01 .. 2026-04-01, fixed in `make_sealed.py` and `sealed_manifest.json`. The tried pool is all tried songs of each fold, with no HOLDOUT split on the sealed path.
- Label: `love`, meaning at least 6 plays on at least 3 distinct days within 90 days of first play.
- Primary measure: pooled within-fold AUC (sauc) of loved versus tried-but-not-loved songs.
  - Resamples: the paired differences of S2 and S3 (`COMPARATOR_SET`) use **1000** artist-cluster resamples at the harness's fixed seed (`FD_NBOOT`, `FD_SEED`), whatever `--nboot` is. The interval of a single model's sauc (S1, `SAUC80` line) uses the run's `--nboot`, which is the **default 300** because the registered command passes none. S1 is therefore decided on 300 resamples and S2/S3 on 1000; this is fixed here, not chosen after the fact.
  - **The raw (unrounded) value decides, never the 3-decimal print.** The harness prints the intervals rounded to 3 decimals and does not save raw bounds, but it computes the decision from the raw bounds. So the decisions are read from the harness's own decision output: for S1 the `lo80 > 0.5: YES/NO` text of the `SAUC80 avg21_dev` line (computed from the raw lower bound); for S2 and S3 the **`decision80`** column of `COMPARATOR_SET` (plain rule `lo80 > 0` on the raw bounds, computed in `cmpset.plain80`). A printed `lo80` of +0.000 or +0.001 is not used to decide; if the printed lower bound and the harness's decision look inconsistent (rounding), the harness's decision stands. Nothing in evalkit is changed to expose raw values; if the owner wants them they can be recomputed only by a later, separately approved step.
  - Only the `decision80` column and the pooled interval decide. The `decision80_iv`, `decision80_heaviest_out` and `decision80_margin005` columns are information only.
- **Decision rule (the owner's):** a difference is decided when the lower end of its 80% interval is above zero, with no extra margin.
  - POS if lo80 > 0; NEG if hi80 < 0; otherwise UNDECIDED.
  - For a single model's sauc, "better than chance" means lo80 > 0.5.
  - 95% intervals and the `decision80_margin005` column are information only.

### Pre-declared primary questions
- **S1.** `avg21_dev` sauc: is lo80 > 0.5? Source: the `SAUC80 avg21_dev` line, `lo80 > 0.5: YES/NO`.
- **S2.** `avg21_dev` minus `artist_recent`, pooled: is lo80 > 0? Source: COMPARATOR_SET.
- **S3.** `avg21_dev` minus `ref_w4r1_listening`, pooled: POS, UNDECIDED or NEG? Source: COMPARATOR_SET.

### Pre-declared secondary quantities (information only; none can overturn S1-S3)
- **S4** (the one closest to the end goal of new songs): `new_artist_sauc` difference of `avg21_dev` minus `artist_recent` and minus `ref_w4r1_listening`. Source: FILE_DELTAS80 comparator rows. Also the new-artist and known-artist sauc of each model, from the tried_love table.
- The inverse-variance-weighted and heaviest-folds-left-out columns of COMPARATOR_SET.
- wa (within-artist), gc, strong-label AUC and love_4_2 / love_10_4 from LABEL VARIANTS.
- sauc in the exposure_before = 0 bucket (BREAKDOWN).
- The per-fold AUC table and any BELOW CHANCE line.
- Top-decile lift and p20.
- Clip-source mix: share of sealed tried clips by source (stored / Spotify embed / iTunes / Deezer), counted from `previews/manifest.csv` without labels. Round 2 measured an undecided loss of about 0.02-0.03 sauc when a song's clip comes from Deezer or iTunes instead of the dev clip. Flag threshold: if more than 10% of the sealed clips fetched by `sealed_prep` come from iTunes or Deezer, the sealed result is labelled "fallback-clip heavy"; this is a label for the owner only and changes no decision.
- Open pool: not part of this test, because decoy feature coverage differs from tried-song coverage by construction. Report it only if decoy MERT coverage is at least 90%, and read it separately for new and known artists.

## 5. Proposed pass criterion (for the owner to approve; nobody applies it before approval)

**Proposed: the sealed test PASSES if S1 = YES and S2 = POS.** In plain words, the model ranks the songs the owner later loved above the songs tried and dropped better than chance, and better than artist familiarity, on data nobody has looked at.

**Outcome cells** (pooled `decision80` decides each of S2 and S3; the heaviest-folds-out and IV columns never overturn it):

| S1 | S2 (pooled) | result |
|---|---|---|
| YES | POS | PASS |
| YES | UNDECIDED or NEG | not passed; the owner decides with every number in front of them |
| NO | POS | not passed (the model is not shown to be better than chance, even though it is decided above artist familiarity); nothing is suggested before a discussion; reported as such, not as a partial pass |
| NO | UNDECIDED or NEG | not passed; nothing is suggested before a discussion |
| harness STOP (coverage) | any | not evaluated (section 3, step 5) |

If S2 or S3 is POS on the pooled column but UNDECIDED on the heaviest-folds-out or IV column (this is the dev pattern of S3: pooled POS, heaviest-out UNDECIDED), it is reported as POS with that fact stated beside it. S3 NEG on the pooled column makes the incumbent the first-suggestion model; S3 POS or UNDECIDED keeps `avg21_dev`.

S3 is not part of the pass. Its dev gain over the incumbent (+0.008) is too small to expect a decided result on 5 folds. S3 only chooses which model makes the first suggestions:
- The model used for the first suggestions is `avg21_dev`, unless S3 is NEG. If S3 is NEG, it is the incumbent `ref_w4r1_listening`.
- If S1 is not met, nothing is suggested before a discussion with the owner.
- If S1 is met but S2 is not POS, the owner decides, with every number in front of them.

There is no numeric success bar beyond this. The owner judges all numbers.

## 6. Inputs needed on the sealed folds and how each is produced (no sealed label or result is read)

| input | produced by | cost |
|---|---|---|
| Preview clip of every train, tried and decoy track of the sealed folds | `sealed_prep` fetch stage. Order: stored previewUrl, then Spotify embed by spotifyId, then iTunes, then Deezer. The source of each clip is recorded. | stored URL about 0.1 s per clip; Spotify embed gap 1 s; iTunes gap 3.5 s |
| MERT-v1-95M rows (4 x 5 s windows, 24 kHz, 12 layers) | `sealed_prep` mert stage into `.cache/evalkit-cache/sealed-feats-v1/mert-v1/`. Exactly the dev extractor: hide-and-rebuild tests in engineer-r1 and shared-w6r2 were bit-identical. | 2.1-2.2 s per clip on 2 threads |
| Compact MERT store of the incumbent (`compact/w4r1`) | `sealed_prep` compact stage | seconds |
| Owner's pre-cutoff listening (training targets) | `evalkit.data.load_streams` inside the harness's sealed path, train streams before each sealed cutoff only | n/a |
| Essentia, Deezer records, second excerpt | **not needed** by the final | none |

Labels are computed only inside `evalkit.run --sealed`. sealed_prep prints counts, runtimes and coverage only.

## 7. Expected runtime

- The number of clips that need fetching and MERT is unknown until `--count` runs. The dry run on one dev fold found 3723 tracks, of which 143 lacked MERT.
- Sealed-era tracks are mostly new to the caches. As a rough guide, 2,000-6,000 clips at about 2.2 s each is about 1.2-3.7 h of MERT, plus fetch time. Use the `--count` estimate. Tried and train clips are built first and decoys last, so a decoy-only shortfall does not block the primary questions.
- The `--sealed` run itself: about 3-8 min, comparable to a `--late` run.

## 8. What the sealed run will and will not tell the owner

It will tell:
- whether the content model, trained only on listening history and preview audio, still ranks the songs the owner went on to love above the songs tried and dropped, on the 5 sealed quarterly folds (cutoffs 2025-04-01 .. 2026-04-01), which nobody has looked at;
- whether it beats artist familiarity there;
- whether it is better than, equal to or worse than the incumbent;
- how it does on songs by artists the owner had never played (S4).

It will not tell:
- how good its suggestions of catalogue songs the owner has never tried will be. Every sealed song is one the owner chose to play, so the test ranks songs within the owner's own discovery stream, not the open catalogue;
- anything about Deezer- or iTunes-sourced previews beyond the fallback clips the pipeline happens to use;
- whether the owner will like the suggestions. That is the owner's own judgement, through the feedback planned for the next phase.

A difference of about +0.008 between the final and the incumbent is very unlikely to be decided on 5 folds. An UNDECIDED S3 is the expected outcome and does not count against the model.
