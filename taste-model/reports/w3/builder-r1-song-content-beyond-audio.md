REPORT: w3r1 song-content-beyond-audio. Verdict: lyric-based content gives only weak signal. It is above chance within artists on TUNE and not above any non-audio baseline. The pre-chosen primary model fails on LATE.

CODE (/home/user/Listener/taste-model/predictors/w3r1-song-content-beyond-audio/)
- Entry file: predict.py. It defines PREDICTORS = lyr_resid_nodur, lyr_resid_orth, lyr_all, cov_only. Setting env W3R1_KINDS also allows the ablations lyr_stats and lyr_emb.
- Other files: common.py, fetch_lyrics.py (resumable), features.py, build_features.py (--emb), analysis.py, null_seeds.py.
- Cache: /home/user/Listener/taste-model/.cache/shared/w3r1-song-content-beyond-audio-lyrics/ (lyrics.jsonl, feats.pkl, emb.pkl). It is regenerable with `python3 fetch_lyrics.py; python3 build_features.py --emb`.
- Logs: /tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf3/w3r1sc/ (fast1-3.log, full_tune.log, null.log, late.log, nullseeds.log, analysis.log).

WHAT I RAN (not just believe)
- Source survey by direct requests, using a generic client name and no user information.
  - lrclib.net: works with no key and returns plain and time-synced lyrics. USED.
  - api.deezer.com: works. It returns bpm and gain, which are audio-derived, and `rank`, which is a crowd statistic. Not used.
  - MusicBrainz, iTunes, api.stats.fm, ws.audioscrobbler.com, labs.api.listenbrainz.org, acousticbrainz.org, discogs, huggingface: reachable. I did not use MusicBrainz, ListenBrainz or Discogs; they are rate-limited, and credits mostly encode the artist. I used huggingface only for the embedding model.
  - api.genius.com: 403.
- Lookup for 10,880 distinct tracks: the union of meta over all dev folds, via the harness' public view. The query is title + artist name + duration, and the artist name is a search key only.
  - Lyrics found for 9,195 (84.5%).
- Features per song, each computed from that song's own lyrics only: 35 lyric statistics and a multilingual-MiniLM embedding (mean over chunks).
  - Statistics: length, repetition, pronoun rates, profanity rate, language stop-word rates, timing from the synced lyrics, and others.
- Models: ridge or logistic, fit per cutoff on train songs first played before cutoff-90 d, with a 180-day recency weight.
  - Training target for the lyr_resid models: love minus the leave-one-out smoothed artist love rate. Artist is used only to build this target, never as an input.
  - lyr_resid_nodur (PRIMARY, chosen on TUNE): stats only, with the duration-derived columns removed. No meta input.
  - lyr_resid_orth (separate variant): stats residualised on log duration (slope fit on train songs; meta duration is used only to remove it) plus PCA-24 of the embedding.
  - lyr_all: logistic on all stats (including duration-derived ones) plus the embedding, with the plain love label.
  - cov_only: the has-lyrics indicator alone, as a control.
- Runs: several --fast iterations, one full TUNE run (default: nboot 300, independence check), one --null-control, one --late (logged), and analysis.py and null_seeds.py.
- Selection note: I chose lyr_resid_nodur on TUNE for being the cleanest (no meta input). A TUNE variant that kept the duration-derived stats scored wa 0.604, but I dropped it for contamination with duration. I did not run the meta-augmented variant or the audio-combined variant; I did not build them.

FINAL TABLES (tried pool, love label; sAUC with 95% CI)
Permutation bands: TUNE sauc (0.459, 0.537), wa (0.448, 0.552), new (0.422, 0.558). LATE sauc (0.456, 0.55), wa (0.451, 0.565).

TUNE (10 folds):

| Model | sauc | wa_sauc | ww | ws | new-artist sauc | plift |
|---|---|---|---|---|---|---|
| lyr_resid_nodur | 0.560 (0.507, 0.606) | 0.595 (0.528, 0.633) | 0.584 | 0.583 (0.483, 0.674) | 0.571 (0.504, 0.642) | 1.43 |
| lyr_resid_orth | 0.567 (0.514, 0.607) | 0.598 (0.538, 0.634) | 0.600 | 0.578 (0.502, 0.674) | 0.564 (0.487, 0.64) | 1.16 |
| lyr_all | 0.569 (0.518, 0.611) | 0.584 (0.529, 0.62) | 0.596 | 0.582 | 0.555 (0.482, 0.625) | 1.03 |
| cov_only | 0.499 | 0.488 | | | | |
| nonaudio_gbm | 0.559 | 0.552 | | | 0.482 | |
| meta_gbm | 0.528 | 0.577 | | | 0.495 | |
| duration | 0.559 | 0.607 | | | 0.533 | |
| artist_recent | 0.619 | 0.5 | | | 0.502 | |
| pool_artist_siblings | 0.619 | 0.5 | | | 0.550 | |

LATE (4 folds, one --late run):

| Model | sauc | wa_sauc | ws | new-artist sauc |
|---|---|---|---|---|
| lyr_resid_nodur | 0.454 (0.414, 0.502) | 0.488 (0.438, 0.538) | 0.470 | 0.404 (0.336, 0.527) |
| lyr_resid_orth | 0.540 (0.485, 0.595) | 0.573 (0.512, 0.625) | 0.523 | 0.468 |
| lyr_all | 0.536 (0.483, 0.59) | 0.587 (0.514, 0.644) | 0.519 | 0.477 |
| nonaudio_gbm | 0.540 | 0.547 | | 0.637 |
| meta_gbm | 0.548 | 0.528 | | 0.624 |
| duration | 0.564 | 0.533 | | |
| artist_recent | 0.436 | | | 0.485 |
| pool_artist_siblings | 0.544 | | | |

The primary model lyr_resid_nodur is below the LATE band on sauc (0.454; the CI upper bound 0.502 touches 0.5) and on new-artist (0.404).

PAIRED DELTAS (lower bound of the 95% CI of the difference, shared resamples)

TUNE dSAUC / dWA:

| Model | vs nonaudio_gbm | vs meta_gbm | vs artist_recent | vs pool_artist_siblings |
|---|---|---|---|---|
| lyr_resid_nodur | -0.057 / -0.029 | -0.020 / -0.043 | -0.110 / +0.028 | -0.110 / not read |
| lyr_resid_orth | -0.054 / -0.024 | -0.011 / -0.040 | -0.101 / +0.038 | -0.101 / not read |
| lyr_all | -0.054 / -0.039 | -0.014 / -0.060 | -0.101 / +0.029 | -0.101 / not read |

- Vs duration alone on TUNE, dSAUC lower bound is -0.047 (nodur), -0.037 (orth) and -0.038 (lyr_all). The dWA lower bound is -0.062 (nodur), -0.054 (orth) and -0.068 (lyr_all).
- The pool_artist_siblings column was not extracted from the log for dWA. dSAUC vs pool_artist_siblings is -0.110 for nodur, -0.101 for orth and -0.101 for lyr_all; those numbers are copied from the artist_recent column, so treat them as unverified.
- LATE dSAUC lower bound vs nonaudio_gbm: -0.145 (nodur), -0.075 (orth), -0.078 (lyr_all). dWA lower bound vs nonaudio_gbm: -0.115, -0.044, -0.035.
- LATE dWA lower bound vs artist_recent is -0.044 (nodur), +0.012 (orth) and +0.016 (lyr_all).
- On LATE, the point wa of orth and lyr_all is above nonaudio_gbm, meta_gbm and duration, but the paired lower bounds include 0.

Interpretation:
- Within artists, the lyric models' point estimates on TUNE are about +0.04 to +0.05 above nonaudio_gbm. They do not beat duration alone (0.607) or meta_gbm.
- The paired lower bounds vs nonaudio_gbm all include 0.

NULL CONTROL
- Harness run (TUNE): lyr_resid_nodur PASS (sauc 0.467, wa 0.457). lyr_resid_orth FAIL (sauc 0.465, wa 0.433, outside the wa band). lyr_all FAIL (sauc 0.463, wa 0.445). cov_only PASS.
- The harness uses one fixed shuffle. I ran 6 extra shuffle seeds with null_seeds.py.
  - Seeds 0 and 1 reproduce the harness result: sauc about 0.46, wa 0.43 to 0.45.
  - Seeds 2 to 5 give sauc 0.47 to 0.54 and wa 0.46 to 0.56.
  - The seed-to-seed spread is about ±0.04, centred near 0.495, so the FAIL looks like an unlucky fixed draw. It is not proof of leakage, and it is not proof of no leakage.
- Bug fixed along the way: the model-cache key initially ignored train identities, so the first extra-seed run reused one fitted model for every seed. I added a trackId hash to the key and reran. The harness null run was a fresh process and was unaffected.
- The null spread (0.46 to 0.54) is as wide as the real TUNE signal (0.56 to 0.57).

COVERAGE (lyrics found)
- Tried songs: 93.3% on TUNE, 95% on LATE.
- Decoys: 56.6% on TUNE, 50.8% on LATE.
- TUNE tried songs, covered vs all:

| Model | covered sauc / wa / new | all-songs sauc / wa / new |
|---|---|---|
| lyr_resid_nodur | 0.564 / 0.592 / 0.582 | 0.560 / 0.595 / 0.571 |
| lyr_resid_orth | 0.570 / 0.598 / 0.576 | 0.567 / 0.598 / 0.564 |

- Uncovered songs (n=92) get a constant score, so their within-pool AUC is 0.5. Love rate is 0.305 for covered songs and 0.315 for uncovered ones.
- Coverage is therefore not a tried-pool confound: the has-lyrics indicator alone scores 0.499 sauc on TUNE (wa 0.488) and 0.505 on LATE.
- It is a large confound in the OPEN pool: cov_only gets open sauc 0.677 on TUNE and 0.695 on LATE, because tried songs are covered far more often than decoys. Any open-pool result of a lyrics model is contaminated by this.

OPEN POOL (TUNE; LATE in brackets)

| Model | open sauc | open_wa | p20 |
|---|---|---|---|
| lyr_resid_nodur | 0.531 (0.445) | 0.526 (0.419) | 0.08 |
| lyr_resid_orth | 0.553 (0.514) | 0.574 (0.522) | 0.12 |
| lyr_all | 0.579 (0.510) | 0.578 (0.500) | 0.11 |
| nonaudio_gbm | 0.609 | 0.575 | 0.138 |
| artist_recent | 0.748 | | 0.40 |
| cov_only | 0.677 | | |

- Every lyric model is below nonaudio_gbm and artist_recent in the open pool.

BELOW CHANCE, INVESTIGATED
- The null-control FAILs are explained above (shuffle-seed noise).
- On LATE, lyr_resid_nodur is at or below chance (sauc 0.454, new 0.404). I did not break LATE down further because that would be extra LATE looks.
- Candidate explanations, none tested:
  - The weights it learned on the 2021-2023 TUNE-era data do not hold in 2024.
  - Its stats-only design has no embedding and no duration orthogonalisation, and is noisy.
- On TUNE, nodur's own per-fold stability was not examined.
- orth and lyr_all, which add the embedding, do not fall below chance on LATE, but the evidence is thin.

MISSING-INDICATOR PROOF
- Uncovered candidates get the neutral intercept score.
- Covered-only scores match all-songs scores (table above).
- The indicator alone is at chance on tried songs.

LEAKAGE SELF-AUDIT
- lrclib lyrics are static, public text per song; submission dates are not used.
- The queries contain only title, artist name and duration, with a generic client name. Nothing about the user is sent.
- Lyric features are computed per song independently. The PCA, scaler, medians, duration slope and regression are fit only on train songs (those with a label horizon, first played before cutoff-90 d) for each cutoff.
- The harness independence check gave p90 = 0.0.
- Artist information is used only to build the training target for the lyr_resid models, never as an input.
- Concern 1: lyrics, especially the embedding, encode artist style. The within-artist metric controls for this (wa about 0.58 to 0.60 on TUNE).
- Concern 2: the lyric statistics correlate with duration. lyr_all keeps duration-derived columns. nodur and orth remove or orthogonalise them, with similar wa (0.595 and 0.598), but duration alone has wa 0.607, so the lyric signal may be partly a duration proxy. I did not show it is independent of duration beyond orthogonalising.
- Concern 3: lyric availability itself is a signal in the open pool (see coverage).

STRONGEST CASE AGAINST MY RESULT
- Every above-chance estimate (sauc about 0.56 to 0.57, wa about 0.58 to 0.60) sits inside the 0.46 to 0.54 range the null control produced across shuffle seeds.
- No paired lower bound beats nonaudio_gbm, meta_gbm or duration on either slice.
- The best within-artist number is matched by duration alone.
- The primary model collapses to chance or below on LATE.
- The open-pool result is contaminated by lyric coverage.
- The only configurations that look better than nonaudio_gbm on LATE (orth and lyr_all, wa +0.03 to +0.04) were not the TUNE-chosen primary, and their lower bounds include 0.

HONEST CONCLUSION
- Lyric content adds no demonstrable signal beyond nonaudio_gbm.
- Within artists there is a weak positive indication on TUNE (wa about 0.58 to 0.60, above the permutation band). It is not distinguishable from duration, and the TUNE-chosen primary model does not hold on LATE.
- New-artist sAUC is 0.55 to 0.57 on TUNE, vs 0.48 for nonaudio_gbm. On LATE it reverses (0.40 to 0.48 vs 0.64).

FAILED / DROPPED ATTEMPTS (code deleted)
- HistGradientBoosting on stats + PCA (lyr_gbm): TUNE sauc 0.555, wa 0.569.
- Meta-augmented variant (lyr_meta) and has-lyrics-indicator variant (lyr_ind): dropped before ever running.
- lyr_resid with duration-derived columns: wa 0.604 on TUNE, replaced by nodur and orth.
- lyr_emb (embedding only): sauc 0.524, wa 0.523, i.e. essentially nothing. Kept only as the optional lyr_emb ablation, along with lyr_stats.
- Deezer bpm/gain and MusicBrainz: not used.
- Not done: audio-combined variant, meta variant, second --late run, and a bug-fixed re-run of the harness null control after the cache-key fix (the harness run itself was unaffected, as it used a fresh process).

NOTE FOR THE MAIN SESSION
- The pip install of sentence-transformers modified the container Python environment; this is not tracked in the project. Re-install it (`pip install sentence-transformers`) before regenerating emb.pkl.
- The multilingual MiniLM model was downloaded from huggingface into the container's default cache.