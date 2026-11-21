# Taste model: results of Workflow 3

Everything here comes from the development ("dev") data: listening up to 2025-04-01, scored as 14 quarterly test points (folds) from 2021-07 to 2024-10. These are split into TUNE (10 folds, 2021-07 to 2023-10), where every design choice was made, and LATE (4 folds, 2024), which was held back to check that the choices generalise. The sealed test folds (2025 onwards) have not been touched. Nothing in this document is a sealed result.

## 1. Short answer

- **The music itself predicts which new songs you come to love.** A model that hears only the 30-second preview audio, with no knowledge of the artist or your history with them, ranks newly tried songs above chance on both TUNE and LATE. It is the only approach that held up on both, and it is the strongest overall result of this workflow (w3r2-audio-taste, `audio_final`).
- **The effect is modest.** Its AUC is about 0.62-0.63, where 0.5 is chance and 1.0 is perfect: if you pick one loved and one not-loved new song, the model ranks the loved one higher about 62% of the time.
- **Artist familiarity is unreliable over time.** "You'll like it because you already play this artist" worked in 2021-2023 and reversed in 2024. Models built mainly on artist history looked best on TUNE and fell to chance on LATE. 
- **Much of what "loved" means is listening behaviour, not the music.** How and when a song was first heard explains a lot of whether it becomes a favourite. That puts a ceiling on how high any music-only model can score with the current label (section 3).
- **Not ready for candidate search.** It does not yet work well enough for that.

## 2. How the evaluation works now, and why it changed

After Workflow 2 the scoring was re-examined. The harness (`evalkit/`, now v3.1) was rebuilt in two steps.

**Problems found in the old scoring**
1. **The label is partly set by how a song was first heard.** A new song that was the only new song in its listening session became loved 48% of the time. One first heard among 9 or more new songs became loved 14% of the time. A score using only "how many new songs were in that session" (no music, no history) beat every legitimate model. Pooled scores therefore mix deliberate picks with casual browsing.
2. **Direction of the session-exposure link.** Both directions are present. New songs heard *before* the candidate in the same session (which cannot be caused by liking it) predict almost as well as those heard *after* it (0.63 vs 0.63). Replaying a song within its first session is very predictive (love rate 17% with one play, 60-98% with two or more). The harness now reports before, after and replay counts separately. It flags that "after" and replays may be consequences of liking the song.
3. **Ties and noise in the old baselines.** Several old baselines tied on most songs and were broken by the same random noise, so their numbers on new artists meant nothing. A single random draw was being used as "chance" and was itself below chance.
4. **Fixed pass marks.** Fixed thresholds were replaced by comparisons.
5. **Leak paths.** `listening_stats.csv` and the play counts in `top_tracks.json` hold lifetime totals that include the sealed period. Both are now forbidden to builders.

**What the harness measures now**
- **Within-group comparisons.** Loved vs not-loved songs by the same artist (`wa`), first heard in the same week (`ww`), or in the same session (`ws`). These remove artist and exposure effects, so they show musical signal more cleanly.
- **New-artist AUC.** Songs by artists you had never played before.
- **A graded score (`gc`).** It measures how well the model orders songs by actual play count. It uses listening frequency directly instead of a yes/no "loved" label.
- **Stronger reference baselines.** Duration alone; a metadata model (`meta_gbm`); and `nonaudio_gbm`, which adds point-in-time artist history to the metadata. `nonaudio_gbm` is the bar any music claim must clear.
- **Chance bands from label shuffling,** instead of one random draw.
- **Diagnostic "oracle" rows.** These use information from after the song was first heard, so they are not usable for prediction. They show how much of the label is behavioural. Plays in the first 7 days alone reach AUC 0.88-0.91.
- **Graded evidence.** Dev results are now graded STRONG / SUGGESTIVE / NONE, with the probability that a model beats a baseline. Previously they were pass/fail on a 95% bound. The sealed run stays the strict final test.
  - STRONG means the 95% lower bound over all 14 folds is above zero and the model is ahead on both TUNE and LATE.
- **A fairer null test.** The old check shuffled song identities but kept each artist's song count, which is real history information. Artist scores therefore "failed" automatically. The new version also relabels artists and uses 3 seeds.
- **Open pool.** Tried songs mixed with "decoy" songs you never played, chosen only from artists known before each cutoff and matched on metadata. It is a rough stand-in for a candidate search.
- **Preview coverage.** Missing previews were filled from iTunes. Coverage is now 94% of tried songs and 99% of decoys.

## 3. Reference points (baselines and diagnostics)

AUC on newly tried songs, "loved" label (at least 6 plays on at least 3 days within 90 days):

| Score | TUNE | LATE | Notes |
|---|---|---|---|
| Chance band | 0.46-0.54 | 0.46-0.55 | 95% range under no signal |
| Popularity | 0.47 | 0.52 | |
| Artist plays / recent artist plays | 0.62 | 0.45 / 0.44 | reverses in 2024 |
| Duration alone | 0.56 | 0.56 | within-artist 0.61 on TUNE |
| Metadata model (`meta_gbm`) | 0.53 | 0.55 | |
| **`nonaudio_gbm`** (metadata + artist history) | 0.56 | 0.54 | the bar to beat |
| How many new songs were in the first session (diagnostic) | 0.66 | 0.62 | not usable for prediction |
| Replays in first session (diagnostic) | 0.69 | 0.74 | not usable for prediction |
| Plays in first 7 days (diagnostic) | 0.88 | 0.91 | not usable for prediction |

One caution runs through every result below: **duration alone gets 0.61 within artists on TUNE.** No model clearly beats it on that measure (section 5).

## 4. What was tried

**Round 1 (three separate approaches)**

**Audio only (`predictors/w3r1-content-audio/`)**
- What it is: pretrained music model (MERT) features from four 5-second moments of each preview, with a simple linear model on top.
- Results: TUNE 0.59, LATE 0.62. Within-artist 0.59 / 0.64. Passed the null test.
- Not shown to beat `nonaudio_gbm`.

**Training signal (`predictors/w3r1-training-signal/`)**
- What it tested: what the model should learn from.
- Graded, volume-normalised targets beat the yes/no "loved" label. The best was a song's play count ranked within its quarter, worth about +0.02 to +0.04 (suggestive, not significant).
- Recent history (last 180-365 days) beat using everything. Old 2020-2022 listening helped only when down-weighted.
- Weighting or dropping songs heard in browsing sessions did not help.
- Its best model reached 0.65 on TUNE and fell to 0.49 (chance) on LATE. It relied on artist familiarity, with the direction forced to "more familiar = more liked", and that relation reversed.

**Song information beyond audio (`predictors/w3r1-song-content-beyond-audio/`)**
- What it used: lyrics from lrclib (84% coverage), as text statistics and embeddings.
- No demonstrable signal. Its within-artist score was matched by duration alone, and the chosen model fell below chance on LATE.
- Other sources were rejected:
  - Deezer: its `rank` field is a crowd statistic, and its bpm/gain are audio-derived.
  - Genius and the Spotify API: unreachable.
  - Last.fm: you declined it.

**Round 2 (two approaches)**

**Integrated (`predictors/w3r2-integrated/`)**
- What it is: an equal blend of a history model, a history model plus audio, the round-1 audio model, and recent artist plays.

**Audio pushed further (`predictors/w3r2-audio-taste/`)**
- What it is: artist-free MERT audio with the graded target, three ridge-regression members averaged, about 38 variants tried on TUNE.

## 5. Best results

AUC with 95% interval. ALL = all 14 folds.

| Model | TUNE | LATE | ALL | Within-artist (ALL) | New-artist (ALL) | Graded `gc` (ALL) |
|---|---|---|---|---|---|---|
| **Audio only, round 2 (`audio_final`)** | 0.621 (0.58-0.65) | **0.633** (0.59-0.68) | **0.626** (0.59-0.65) | 0.606 | 0.621 | 0.575 |
| Audio only, round 1 (`ca_local`) | 0.594 | 0.622 | 0.605 | 0.604 | | 0.561 |
| Integrated blend (`w2i_final`) | **0.667** (0.60-0.71) | 0.535 (0.48-0.60) | 0.616 | 0.607 | 0.627 | 0.590 |
| Integrated without history (audio only) | 0.584 | 0.594 | 0.588 | 0.583 | 0.580 | 0.547 |
| Integrated without audio | 0.645 | 0.478 | 0.580 | 0.581 | 0.587 | 0.573 |
| `nonaudio_gbm` (bar) | 0.559 | 0.540 | 0.551 | 0.551 | 0.532 | 0.544 |

**Audio-only model (`audio_final`) vs `nonaudio_gbm`**
- Overall: +0.074, STRONG (ahead on TUNE +0.06 and LATE +0.09).
- Within-artist: +0.055, STRONG.
- Graded score: +0.031, NONE (probability 0.96 of being ahead, but the 95% bound touches zero).

**Caveats on the audio-only model**
- **Gain over round 1 is small:** about +0.02, mostly on TUNE, after 38 variants. Round 1's simple model already carried most of the effect.
- **Not shown to beat duration within artists.** Duration scores 0.607 vs audio 0.598 on TUNE; across all folds the lower bound is -0.037 (probability 0.80).
- **New-artist gain is uneven.** Across all folds it is 0.621 vs 0.532 for `nonaudio_gbm`. On LATE there is no advantage: 0.641 vs 0.637, and round 1 scored 0.674.
- **Null test failed by a hair.** The 3-seed average was 0.522 against a band edge of 0.519, and it was reported honestly as a FAIL. The builder's check suggests this is a chance outlier: random directions in the same audio space land there about 5% of the time. The devil's advocate did not re-run that check. Under the same null test, 4 of 7 simple baselines also fail, including duration and popularity, which use no history. The test is therefore imperfect in both directions.
- **Release age was ruled out as the explanation.** Release age, which the model never sees, predicts love by itself (0.58). The devil's advocate found the audio score is almost uncorrelated with it, and it keeps 0.628 within release-age groups. That test was coarse: 88% of songs fall in the oldest age bucket.
- **Adding metadata did not help.** It cost 0.004-0.006.
- **Missing audio does not drive the result.** A "no audio" flag alone scores 0.51. A clean "audio songs only vs all songs" split was not produced in round 2. Round 1 did produce one: 0.601 vs 0.594.
- **The open pool flatters audio models.** Audio models score 0.70 there, but a missing-preview flag alone gets 0.53, so the decoys carry a shortcut. In the top 20 picks it is worse than recent artist plays (0.16 vs 0.32 precision).
- **"Specific parts of the music"**. The only test available compared four fixed 5-second moments against the whole 30-second clip. Modelling the moments separately added 0.00-0.01, in both rounds. This neither supports nor rules out the idea: four windows of a preview is a weak test.

**Integrated blend**
- Best on TUNE, and the null test passed after the devil's advocate fixed a caching bug that had made the 3 seeds identical.
- On LATE it is at chance (0.535) and below its own audio-only version (0.594). History members that helped on TUNE hurt in 2024.
- Its "beats nonaudio_gbm" grade is NONE overall (LATE is -0.005), and STRONG on within-artist and graded scores.
- The devil's advocate swapped in the stronger round-2 audio model and got 0.672 on TUNE, which is within noise of 0.667.

## 6. What the evidence supports and what it does not

**Supported**
- Preview audio carries real, artist-independent information about which new songs you will love. It is stable across 2021-2024 and beats a metadata-plus-artist-history model.
- Artist familiarity is not a stable predictor of your taste: positive in 2021-2023, reversed in 2024.
- Training on how much you played a song, ranked within its period, works better than a yes/no threshold. Recent history matters more than old.
- A large part of "loved" reflects listening behaviour and exposure, not only the music.

**Not supported (yet)**
- That audio beats song length within the same artist.
- That specific moments of a song matter more than its overall sound. This was not properly testable with 30-second previews.
- That lyrics add anything.
- That any model is good enough for candidate search. In the open pool, audio's top-20 picks are weaker than "artists you play recently".
- That any combination of history and audio generalises better than audio alone.

**Integrity notes**
- The LATE slice is no longer fully unseen. Round-1 LATE results were shared with round-2 builders, and the artist-flip fact came from LATE. Auditors and the engineer ran extra LATE runs, all logged in `.cache/late_runs.log`.
- Only the sealed folds are a clean test. No one ran them.
- Folder names differ from the briefs. Code is in `predictors/w3r1-*` and `predictors/w3r2-*`.
- The obsolete Workflow 2 folders (`A-*`, `B-*`, `C-*`) and their old-pool caches were removed in the post-workflow cleanup (nothing current imported them).

