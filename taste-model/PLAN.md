# Taste model plan

Status: nothing has been built yet. Both researchers measured data availability and speed, but nobody has trained a predictor, so there are no accuracy numbers for any method. The only models scored so far are simple baselines (below).

## 1. How success will be measured

**The test.** The model only sees your listening before a cutoff date. It then scores songs from the following 3 months. A song counts as "loved" if you played it at least 6 times, on at least 3 different days, within 90 days of first hearing it. There are 8 development rounds (cutoffs up to Oct 2024). There are 5 sealed rounds (1,664 songs, 2025-26) that nobody has tuned on, and each look at them is logged.

**Two pools.**
- *Tried pool (primary):* songs you started playing in the window, and the question is "which of the songs I try will I love". Base rate of loved is about 23%.
- *Open pool (closer to the end goal):* the same songs plus 5x as many real songs you never played, matched on popularity. "Never played" does not mean "would hate", so this is a weaker, separate metric.

**Headline metric:** stratified AUC (0.5 = coin flip, 1.0 = perfect). Confidence intervals resample by artist, so they are honest but wide (about +/-0.05 on dev, +/-0.07 for the new-artist subset).

**Baselines (all measured, sealed tried pool):**

| Baseline | Tried pool AUC | Open pool AUC |
|---|---|---|
| random | 0.495 | 0.491 |
| Spotify popularity | 0.526 | 0.519 |
| how much you played the artist | 0.449 | 0.495 |
| recent artist plays | 0.453 | 0.553 |
| artist's past love rate | 0.519 | 0.498 |
| "other pool songs by same artist" (shortcut) | 0.515 | 0.549 |
| "other pool songs on same album" (shortcut) | 0.552 | 0.539 |

Plain reading: on songs you try, artist and popularity information is at chance or worse. On dev, artist-based baselines looked a bit better (up to 0.58 tried, 0.69 open) but that mostly vanished on sealed data. On the open pool, recent-artist plays reach about 0.55 (0.68 on dev). Any model has to beat all of these.

**Proposed "works VERY WELL" bar (all must pass on sealed, after passing on dev):**
- Tried pool: AUC lower confidence bound >= 0.65 (point estimate about 0.70-0.72); new-artist songs lower bound >= 0.60; beats every baseline above with a paired interval above zero; top-10% of ranked songs holds at least 1.8x the base rate (about 45% loved); results hold for stricter/looser definitions of "loved" and correlate with days played.
- Open pool: AUC lower bound >= 0.75; new-artist >= 0.65; beats every baseline; top-20 precision >= 0.40 (about 10x chance) and >= 1.3x the best baseline.
- Controls: scoring a song alone gives the same score as within the pool (independence), and a run with scrambled song identities in the training history falls to chance (AUC <= 0.56).

These thresholds are judgement, not derived from a power analysis. A true new-artist AUC near 0.68 would only pass about half the time. Passing proves ranking power on songs you tried and on a decoy pool; it does not yet prove discovery from a truly open catalogue.

## 2. Approaches to build first (ranked)

Step 0, before any modelling: build the data layer (song table, download previews, lyrics, caches in `.cache/`) and validate the embedding model. Audio is cheap to fetch (about 3-10 minutes for roughly 4.5k previews; Spotify has about 69%, plus Apple gives 84%, Deezer search fills most of the rest) but the Deezer match rate is only a 30-sample estimate and can return the wrong version.

**1. Audio embeddings plus a simple per-user model.**
- *What:* turn each 30 s preview into a vector with a pretrained music model, then score a song by similarity to songs you loved vs. songs you tried and dropped (kNN, logistic regression, per-cluster prototypes). Training negatives are your own once-played-and-abandoned songs.
- *Evidence:* it is the only approach that can judge a song with no history, and your artist history is at chance, so the signal must come from the music. But no one has shown it beats chance on your data; this is literature belief only. The risk is that it just learns genre.
- *Data:* previews are obtainable (shown: 500/500 downloaded). CLAP loads and runs on CPU, but the timing estimates differ 5x (30 min vs 3 h) and one researcher found transformers 5.x may return the wrong (unprojected) vectors. Must be sanity-checked first (same-artist retrieval, zero-shot text match) and timed. MERT was blocked (needs remote code); AST and MusiCNN via onnx were not tried, so a second embedding family has no feasibility evidence yet.
- *Guards:* no artist or popularity features (evidence says they are useless here); report AUC separately for new artists and for known artists, within-artist, and with the candidate's artist removed from training; run null control and permuted-label control; report results by preview availability.

**2. Behavioural / co-listening embeddings from your own history (item2vec on sessions, playlist and album sequence), then map audio onto that space.**
- *What:* learn which songs you play near each other, and regress audio onto those positions so unseen songs get a position.
- *Evidence:* untested by anyone. It uses structure the other methods ignore (147k plays, 13% consecutive same-album plays, 14% of plays have playlist context), and the devil's advocate objected to dismissing it without testing. Weak prior, cheap to try.
- *Data:* already in hand.
- *Guards:* the independence and shuffled-ID tests; must beat the sibling shortcuts, since album/sequence structure is also what makes the shortcut work.

**3. Multi-window / segment-level audio model (for "I like songs for specific parts").**
- *What:* embed several 5-10 s windows per preview and score by best-matching or top-k windows.
- *Evidence and limit:* only worth doing once approach 1 shows real signal. Be honest: there is no part-level supervision, a preview is one fixed 30 s slice, and full-length audio is not available here (YouTube downloads returned 403). So this can only test "does windowing help", not "it understands the parts you like". It costs about 3x the compute.
- *Guards:* same as approach 1; gains are attributed to windowing only through a matched ablation.

**4. Lyrics and metadata blocks as additive features.**
- *What:* lyric text embeddings (lrclib has about 83-90% coverage, 30-sample checks), language/explicitness, artist genres.
- *Evidence:* cheap, but your top plays are often instrumental/cinematic, and genres are artist-level, which is the shallow signal you warned against. Add only if dev scores improve.
- *Guards:* popularity excluded from the primary model (it is measured in 2026), compare with and without it.

**Deferred, not built now:** end-to-end audio fine-tuning (no GPU, about 2k positives), sequence transformers, external collaborative filtering, LLM song-knowledge features.

**Old data question.** Run the harness's history ablation (all history, last 2 years, last 1 year, same-size random subsample) on dev so recency is separated from sample size. 2020-22 is only about 640 distinct tracks but about a third of all plays.

## 3. Must-pass tests (from the devil's advocate)

1. Pool-sibling baselines (same artist / same album in pool) must be beaten by a paired interval. Built in.
2. Single-candidate independence: scoring a candidate alone must not change its score (median change < 1%). Built in.
3. Shuffled rows and hashed IDs: same result. Built in.
4. Artist-disjoint check: report within-known-artist AUC and a run excluding the candidate's artist from training, to show audio is not just identifying the artist. Builders must add this.
5. Embedding sanity before modelling: zero-shot text-audio check and same-artist retrieval vs. random; time a full run.
6. Open pool with decoys and top-k precision. Built in (decoys are artist-seeded, so only a rough proxy).
7. Label sensitivity (4/2, 6/3, 10/4 plays/days, strong, days played Spearman). Built in.
8. Drift ablation with matched sample size. Built in.
9. Permuted-label / null control: pipeline falls to chance, so cached features cannot leak. Null control is built in; permuted-label check is for builders to add.
10. Preview-coverage bias: love rate and AUC by Spotify / Deezer-matched / no preview, plus Deezer version-match rate on 2025-26 songs. NOT built in; builders must report it.

Sealed data: only the main session can run it, only on pre-registered, hashed predictor files, with widened intervals per look.

## 4. Open questions for you

1. Is the bar above strict enough, or too strict? (It is calibrated so a lucky model rarely passes, but a real 0.68 new-artist model passes only half the time.)
2. Is "loved = 6+ plays on 3+ days within 90 days" how you would define it? Playlist inclusion, album binges and crowded quarters can inflate or hide it.
3. Do you want the open-catalogue test (hit rate in the top 20 from about 100k unheard songs) built before the end goal? The current decoys are only a rough stand-in.
4. Is it OK to allow trust_remote_code for MERT? It was blocked, and without it only CLAP, AST and onnx-based models are available.
5. Anything you know about which parts you like (drops, vocals, bridges, production)? Previews may not contain them, and you can tell us whether a spot check on a few songs would be useful.
6. Are playlists you made (e.g. "Best Songs") a clean signal of what you love? They could be used as an extra, explicit positive label.
