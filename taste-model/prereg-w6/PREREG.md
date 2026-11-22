# Sealed-test pre-registration, Workflow 6

Written by the Workflow 6 final research lead on 2026-11-22, before any sealed scoring. Nothing here has been run on sealed data. Nobody has run `--sealed`, registered a file or read `.sealed/`. **Only the main session runs the steps below, and only after the owner has seen the dev results and approved.**

Harness: evalkit **v5.3** (sha256 of every evalkit file in `FILES.sha256`). `make_sealed.py`, `sealed_manifest.json` and `register.py` are byte-identical to the hashes the engineers recorded at the start of this workflow.

## 1. What will be registered

Exactly **one** file:

| registered name | file | model inside | declared on dev |
|---|---|---|---|
| `avg21_dev` | `predictors/w6r1-content-ranker-final/final_avg21_dev.py` | `avg21_dev` (one model) | `w6r1_avg21_dev`, 2026-11-22T12:06:20Z, sha256 `d2ce1c31b35842e3b84b20ba61b23e4a3515c830f4abf4e3ed64f79981fa898d` |

Bundle: the registered file is a thin wrapper. It loads `predict.py` in the same folder, which imports `grid.py` in that folder and `evalkit.features`. All three predictor files, every evalkit file, the MERT extractor and the incumbent's code are hashed in `FILES.sha256`. Run `sha256sum -c prereg-w6/FILES.sha256` from `taste-model/` before registering. If any line fails, stop and report it.

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
5. Coverage gate. This is decided **before** any sealed score is seen:
   - Read the per-fold tried-song coverage that sealed_prep prints.
   - If every sealed fold has MERT features for at least 90% of its tried songs, continue.
   - If any fold is below 90% after one `--retry`, report the per-fold coverage to the owner and stop. The owner decides whether to go on. If the owner says go on, every sealed number is labelled "coverage-limited".
6. `python3 -m evalkit.register predictors/w6r1-content-ranker-final/final_avg21_dev.py avg21_dev`.
7. `python3 -W ignore -m evalkit.run --sealed predictors/w6r1-content-ranker-final/final_avg21_dev.py > <save path>`. This is one look, logged with its hash. Do not run it a second time.
8. Report every pre-declared quantity below to the owner, quoting the harness lines verbatim.

Note on the harness banner: the sealed output prints `INTERPRETATION STOPPED` if **any** model's pooled tried-song coverage is below 90%, and that includes the information-only reference `ref_w4r1_music`. Without `--essentia`, `ref_w4r1_music` will show essentia=0.000 and trigger the banner. Pre-declared handling:
- If the only COVERAGE lines that say STOP belong to `ref_w4r1_music`, the banner does not apply to `avg21_dev`, `ref_w4r1_listening` or `artist_recent`. Their numbers are interpreted.
- `ref_w4r1_music`'s numbers are not interpreted.
- If the COVERAGE line of `avg21_dev` or `ref_w4r1_listening` says STOP, nothing is interpreted. Report the coverage only.

## 4. Evaluation design, exactly as applied

- Slice: the 5 sealed folds, quarterly cutoffs 2025-04-01 .. 2026-04-01, fixed in `make_sealed.py` and `sealed_manifest.json`. The tried pool is all tried songs of each fold, with no HOLDOUT split on the sealed path.
- Label: `love`, meaning at least 6 plays on at least 3 distinct days within 90 days of first play.
- Primary measure: pooled within-fold AUC (sauc) of loved versus tried-but-not-loved songs, with paired differences from 1000 artist-cluster bootstrap resamples at the harness's fixed seed. Read from the sealed `COMPARATOR_SET` table, `pooled` column, and from the `SAUC80` line.
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
- Clip-source mix: share of sealed tried clips by source (stored / Spotify embed / iTunes / Deezer), counted from `previews/manifest.csv` without labels. Round 2 measured an undecided loss of about 0.02-0.03 sauc when a song's clip comes from Deezer or iTunes instead of the dev clip. A fold with many fallback clips is flagged for that reason.
- Open pool: not part of this test, because decoy feature coverage differs from tried-song coverage by construction. Report it only if decoy MERT coverage is at least 90%, and read it separately for new and known artists.

## 5. Proposed pass criterion (for the owner to approve; nobody applies it before approval)

**Proposed: the sealed test PASSES if S1 = YES and S2 = POS.** In plain words, the model ranks the songs the owner later loved above the songs tried and dropped better than chance, and better than artist familiarity, on data nobody has looked at.

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
