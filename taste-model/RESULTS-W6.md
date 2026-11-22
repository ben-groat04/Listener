# Workflow 6 results: the final model and the sealed test

Every number here comes from the evaluation harness **evalkit v5.3** on the development folds ("TUNE": 10 quarterly folds, 2021-07 to 2023-10). It is the harness's default full run unless a line says "fast". The scores measure how well a model ranks the songs you went on to *love*, meaning played 6 or more times on 3 or more days within 90 days of the first play, above the songs you tried and dropped. 0.5 is chance and 1.0 is perfect.

Decisions use your rule: a difference counts as decided when the lower end of its 80% interval is above zero, with no extra margin. POS means decided better, NEG means decided worse, and UNDECIDED means neither.

## 1. What was assembled, and what it can do toward "what new songs should I listen to?"

**The final model is `avg21_dev`.** It listens to a song's public 30-second preview, turns it into a description of the sound using MERT-v1-95M, a pretrained music-audio model, and scores the song against a taste profile learned from your listening before a given date. It is an equal average of 21 slightly different versions of the earlier best recipe. It uses no artist names, popularity or genre tags. It can score **any** song that has a preview, including songs by artists you have never played, at about 2 seconds of computer time per song.

What it can do:
- **It ranks new songs better than artist familiarity**: 0.659 against 0.619 for a baseline that just favours artists you play a lot. This is decided (POS).
- **The gap is largest on songs by artists you had never played**, which is where discovery happens: 0.668 against 0.498, where artist familiarity has nothing to go on.
- **Catalogue groundwork is in place.** Without any keys, the project can reach Deezer (search, 30 s previews, release dates, genres, related artists, artist top tracks), iTunes (30 s previews), Spotify's public embed page (30 s previews for any Spotify track id), MusicBrainz, ListenBrainz, AcousticBrainz, LRCLIB lyrics, Discogs, Audius and the FMA dataset. The Spotify Web API, Last.fm, Genius, Musixmatch and the Apple Music API all need keys and are not usable.
- In a 60-song sample, at least one preview source covered 98% of songs.
- A Deezer genre-chart and related-artist walk produced 3,699 candidate tracks, 99.6% of them with a preview.
- A pipeline now fetches previews and computes the model's features for any list of tracks. On rebuilt development tracks it reproduced the stored features exactly.

What it cannot do, or has not shown:
- It is **not clearly better than the earlier model** (the "incumbent", `ref_w4r1_listening`, 0.651) on songs by new artists. Its small overall gain sits on artists you already know.
- **No list of suggested songs was made.** That waits for the sealed test and your approval.
- **Previews from other sources lose a little accuracy.** The model was trained mostly on Spotify previews. Scored on a Deezer or iTunes preview of the same song, accuracy drops by about 0.02-0.03, but the interval is wide (roughly -0.05 to +0.04), so the loss is not decided either way. Most of the difference comes from the other source playing a different 30 seconds of the song.
- It has only been tested on songs you chose to try. How it ranks songs you would never have come across yourself is unmeasured, because the comparison set of untried songs ("decoys") does not have comparable audio coverage.

## 2. Final model: development results (harness v5.3, full default run)

| quantity | avg21_dev | incumbent ref_w4r1_listening | artist_recent |
|---|---|---|---|
| overall score (sauc) | 0.659 | 0.651 | 0.619 |
| songs by new artists | 0.668 | 0.667 | 0.498 |
| songs by known artists | 0.643 | 0.632 | n/a |
| first new song of a session (deliberate trials) | 0.617 | 0.615 | 0.569 |

Paired differences with 80% intervals:

| comparison | pooled over folds | folds weighted by precision | two heaviest folds left out |
|---|---|---|---|
| avg21_dev minus artist familiarity | +0.040 [+0.014, +0.085] **POS** | +0.046 POS | +0.045 POS |
| avg21_dev minus incumbent | +0.008 [+0.001, +0.012] **POS** | +0.006 [+0.001, +0.011] POS | +0.004 [-0.004, +0.012] UNDECIDED |

Further checks:
- **Songs by new artists**, minus the incumbent: +0.002 [-0.009, +0.011], UNDECIDED. Minus artist familiarity: +0.171 [+0.122, +0.218], POS.
- **Fold trend.** The gain over the incumbent shrinks over time: -0.006 per year, interval [-0.015, +0.002], UNDECIDED.
- **Per-fold scores** range from 0.455 to 0.690. The two earliest, tiny folds (2021-07 and 2021-10) are at chance for every audio model, including the incumbent.
- **Null control** (the same model trained on scrambled history), quoted verbatim from the harness:
  `NULLCTRL {"version":"v5.3","mode":"v2","seeds":5,"slice":"TUNE","model":"avg21_dev","gated":{"sauc":{"value":0.555,"band":[0.487,0.567],"inside":true},"wa":{"value":0.52,"band":[0.439,0.563],"inside":true},"new":{"value":0.563,"band":[0.429,0.593],"inside":true}},"label":"PASS"}`
  It passed. The null value sits near the top of its band, which is also true of the incumbent.
- **Independence check:** the score of one song does not depend on which other songs are scored with it (median 0.0, p90 0.0). That is what makes it usable on single catalogue songs.

I re-ran the full default run myself and every number above reproduced exactly. Four separate devil's-advocate re-runs (two of `avg21_dev`, two of its duplicate `avg21_fb`) gave the same table and the same null-control line.

**What the devil's advocates found against it:**
- The gain over the incumbent is thin. Its lower bound is +0.001, and it is undecided when the two heaviest folds are left out.
- The 21-version average was picked on these same folds in Workflow 5, after many looks. Across this workflow and the last, more than 25 content variants were scored on the same folds, so some of the +0.008 is selection luck.
- There is no gain on new-artist songs.
- They found no leak or bug that invalidates a score.

## 3. Everything else that was tested (all on development folds; 80% rule)

| idea | result | decision |
|---|---|---|
| Score a second, different 30 s excerpt of each song (from Deezer) and average | -0.002 vs one excerpt | UNDECIDED: no gain |
| Take the strongest window of the clip instead of the average (avg21_dev_max, fast) | +0.010 vs incumbent | POS, but never declared, so not eligible |
| Add a second "music" model built on essentia features (combo_dev_music) | +0.014 vs incumbent | POS, but the score of a song depended on the other songs scored with it. Not usable on single songs, so ineligible |
| Same idea rebuilt correctly (training-only scaling; combo_max_ts / combo_mean_ts, fast) | +0.015 / +0.014 vs incumbent, independence check passed | POS, but **never declared** (the builder stopped early), so not eligible |
| Public catalogue context: release age, related-artist graph, popularity, genre (blend_all_q) | +0.004 vs incumbent | UNDECIDED. Worse on new-artist songs: -0.041 [-0.069, -0.012], NEG. Popularity is measured in 2026, so it looks ahead |
| Catalogue context without popularity (blend_inv_q) | -0.001 vs incumbent | UNDECIDED |
| Label-free corrections for preview source (four kinds) | none reduced the Deezer/iTunes loss | UNDECIDED: no fix shown |
| Mixing Spotify, Deezer and iTunes previews in one list | -0.015 [-0.035, +0.039] (8 folds) | UNDECIDED: usable, slightly worse |

**Reachability groundwork** for finding candidates through Deezer's related-artist lists (development folds; built from songs you actually tried):
- Starting from your 20 top artists before each cutoff, one hop reaches 36% of the new-artist songs you went on to love, against 19% of the new-artist songs you dropped.
- Two hops reach 54% against 49%, at a walk of about 1,500 artists.
- One hop is selective but misses most loved songs. Two hops reach about half but select poorly. There is no control yet for very popular artists that appear in many lists.

## 4. What the evidence supports and does not

Supports:
- The audio of a song's preview carries real information about whether you will come to love it, beyond which artist it is by. This holds on artists you have never heard and has been stable over five workflows.
- The final model beats artist familiarity, decided on every check.
- The final model is a marginal improvement on the earlier model overall (decided, but thin).

Does not support:
- Any gain over the earlier model on new-artist songs.
- Any benefit from public catalogue context, a second excerpt or source corrections.
- A claim that Deezer or iTunes previews score as well as Spotify ones. They are probably slightly worse, and the size is undecided.

Is the score itself the right one for the goal? It was weighed against the goal of finding new songs you will like, not left as a default:
- The love label is itself a listening-frequency measure (songs you kept returning to), so it matches "songs I like" as your plays reveal it.
- The goal is discovery, so the new-artist score is the most relevant secondary. It is pre-declared for the sealed test.
- The main limit is that every test song is one you chose to try. The score cannot show how well the model ranks the open catalogue. Your own judgement of the suggestions is the remaining test.

## 5. State of the held-out data (words only)

- **2024 folds ("LATE")**: seen by agents since Workflow 4, so they serve only as a drift check. One LATE look was allowed per builder. No declared final was vetoed: no LATE interval lay wholly below the incumbent. The final model's identical predecessor had its single look in Workflow 5. A second look was refused by the harness as a duplicate.
- **Artist-disjoint HOLDOUT**: budget 0, unused.
- **Sealed folds (2025-04 to 2026-04)**: untouched. No one ran them, registered a file or read them. They are the only clean test.

## 6. The sealed test (ready, not run)

The package is in `prereg-w6/` (`PREREG.md` and `FILES.sha256` with the hash of every file involved). One file will be registered: `avg21_dev`. It needs only preview audio and MERT features, which the harness pipeline builds for the sealed songs without looking at any labels. The build probably takes about 1-4 hours; a dry run gives the exact estimate. The sealed scoring itself takes about 5 minutes.

Pre-declared questions:
- S1: is it better than chance?
- S2: does it beat artist familiarity?
- S3: is it better than the earlier model?
- S4 (information): how does it do on new-artist songs?

Proposed pass, for you to approve: **S1 and S2 both decided positive.** A decided result on S3 is not expected: a +0.008 gain cannot be resolved on 5 folds. If S3 comes out decided negative, the earlier model makes the first suggestions instead.

## 7. Process problems

- **The round-2 builder for the "correct" music-model ensemble stopped after about 7 minutes of a 60-minute budget.** It thought its first test run was unfinished. In fact the run had finished, showing three candidates POS against the incumbent with the independence check passed. It declared nothing and wrote no report file. Under the rules only declared models can be chosen, so the final is the smaller `avg21_dev` gain, and a probably stronger candidate (+0.014 to +0.015) was lost to this workflow.
- The round-2 preview-source builder declared, as its required final, a file that duplicates `avg21_dev`. So it added no new candidate.
- Two report files were missing: one devil's advocate (catalogue context, "works" direction) and the round-2 ensemble builder. In both cases other agents re-ran the same headlines.
- One devil's advocate put held-out (LATE) numbers in its summary text. It was caught, and they appear nowhere in this file or the sealed package.
- The harness's Deezer lookup helper expects a file name that the shared prep never wrote. The catalogue-context builder read the file directly.
- Deezer matching found only 75% of tried songs, mostly because of a strict 5-second duration rule.
- iTunes lookups covered only 8 of 10 folds (time cap).
- Declarations hash only the thin wrapper file, not the code it imports. No edit after declaration was found.
- Selection on the same development folds accumulates across workflows. The walk-forward check covers only the variants of one builder.

## Next steps (kept separate)

These are recommendations only; none of them has been acted on.
- After your approval, the main session runs the sealed test exactly as in `prereg-w6/PREREG.md`.
- Before or alongside suggestions, the next workflow could declare and evaluate the pool-independent ensembles found here (`combo_max_ts`, `combo_mean_ts`, `avg21_max`). This would happen on development data only, so it would not touch this sealed test. Their essentia input is verified to rebuild exactly on the sealed pipeline and costs about 2.3 s per song.
- For suggestions: generate candidates from a 1-2 hop Deezer related-artist walk plus genre charts. Score them with the final model, preferring Spotify-embed previews and falling back to iTunes or Deezer with the source flagged. Then collect your feedback on specific songs, as you planned.
- Loosen the Deezer duration rule (about 15 s), which a devil's advocate estimated would lift matching from 75% to about 85%. Add a popularity control to the reachability map.
- Try training the model with Deezer and iTunes clips of training songs as extra examples, which is the untested fix for the preview-source gap.
