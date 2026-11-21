# Workflow 4 results

Written by the final research lead from the reports of every agent in this workflow. I re-ran nothing. Every number below comes from a builder report and was checked by at least one devil's advocate (DA), unless it is marked otherwise. Candidate-song search was not part of this workflow, and nothing here says it is ready.

## 1. The short answer

- **The best content-only models predict which new songs you will love at a pooled AUC of about 0.63-0.66 on every slice of the data.** AUC is the chance that a loved song is ranked above a dropped one, so 0.5 is chance and 1.0 is perfect.
- **None of the four new models clearly beats the best earlier model.** Each was tuned on the TUNE folds and gained about +0.01 to +0.02 there. That is about the size of the gain you get just by picking the best of many tries on the same data. On HOLDOUT, a slice no builder had tuned on, every gain shrank to within noise (at most +0.007) or reversed.
- **A realistic estimate of what this approach does on songs it has not been tuned on is about 0.61-0.64.** The walk-forward score (sections 3-4) puts honest selection at 0.613-0.625. The reference models score 0.626-0.643 on DEV+HOLDOUT.
- **Songs by artists you have never played score about the same as everything else (about 0.62-0.66).** No model has a new-artist advantage that holds on HOLDOUT.
- **Much of what decides "loved" cannot be seen in the audio.** How a song was first encountered (how many other new songs came before it in the same listening session) predicts love about as well as the audio models do. This context is fixed before the song is heard.

## 2. What the project review found (before any new work)

Two reviewers checked the Workflow 3 code and results.

**Bugs and shortcuts**
- **Null-control cache bug.** The null control is the test that checks a model scores near chance on shuffled data. A cache in the Workflow 3 audio predictor was keyed without song identities, so all three shuffled "seeds" were really one seed repeated. The integrated predictor imported the same code, so its null results were affected too. The bug had not been fixed on disk.
- **Open-pool shortcuts.** The open pool mixes songs you tried with "decoy" songs you never played. Tried songs and decoys had different preview sources, and decoys were far more often missing lyrics lookups. A has-lyrics flag alone scored 0.706 on that test.
- **A window-ablation script damaged its labels.**

**Problems with the scoring**
- Two folds carried 68% of the weight in the pooled TUNE score.
- The "reference to beat" (nonaudio_gbm, 0.559) was weaker than a one-number artist-plays baseline (0.619).
- The confidence intervals were too narrow.

**What held up**
- Workflow 3's audio-only MERT model (MERT is a pretrained music-audio model) reproduced at 0.621 on TUNE.
- On TUNE it only equalled simple artist-familiarity baselines.
- It did not beat song duration at ranking songs by the same artist.

**On your question "is the score calculation good?"**
- The love label (6 or more plays on 3 or more days within 90 days of the first play) holds up. It predicts long-term keeping (6 or more plays in days 90-365) at AUC 0.85, and 289 of the 342 loved TUNE songs were kept. It measures lasting taste, not short-term noise.
- What the label cannot separate out is encounter context. So "within the same encounter context" (wx) was added as a headline score next to pooled AUC, and new-artist AUC became a headline too.
- Every model was also scored on four other label definitions, including the long-term "keep" label. Scores moved by 0.02 at most, so no result depends on the exact love threshold.

## 3. Direction chosen and why

**Fix the scoring first.** The review showed the scoring could not separate real gains from noise. The changes (evalkit v4, then v4.1):
- **HOLDOUT, a new untouched slice.** About 25% of artists were set aside, chosen by a fixed hash. A dev slice split by time was impossible because the data after the dev period is sealed. Only a model's declared final could be scored on HOLDOUT, and only once.
- **Honest confidence intervals.** The bootstrap now resamples whole artists across all folds.
- **More reporting.** Per-fold results, a macro average over folds, and a breakdown by subgroup, which addresses the idea that "one score hides differences".
- **A set of reference models.** A new model now has to beat the best of them, not just one weak model.
- **Walk-forward score.** It scores a builder's whole selection procedure instead of its hindsight pick.
- **New null control.** It runs each seed in a fresh process and judges the result against a band that accounts for songs by the same artist being similar.
- **Loopholes closed.** A wrapper file that imports an already-tested predictor no longer gets an extra look at LATE or HOLDOUT.

**Then two pairs of builders. Each primary model had to use song content only:** audio, lyrics and metadata. Listening history could be used to build training targets, but never as an input describing a candidate song. This rule follows your warning about artist shortcuts, and it was reinforced when artist familiarity reversed in 2024.

- **Round 1**
  - Learn current taste from the whole listening record, not just from new songs' 90-day outcomes. This follows your point that listening frequency is the most reliable taste signal.
  - Find which musical properties, and which moments in a clip, carry the signal. New interpretable audio features (essentia style, mood and instrument tags, measured over time) were built for this.
- **Round 2**
  - Learned, nonlinear and time-resolved models (small neural nets, attention over clip segments).
  - Models aimed at artists you have never played, with honest selection.

## 4. Results

Pooled AUC on tried songs. TUNE = 2021-07 to 2023-10, LATE = 2024, DEV+HOLDOUT = all 2,450 tried songs pooled.

| Model | TUNE | LATE | HOLDOUT | DEV+HOLDOUT | New-artist (TUNE / HOLDOUT) |
|---|---|---|---|---|---|
| ref_audio_final (Workflow 3 MERT ridge) | 0.632 | 0.621 | 0.657 | 0.626 | 0.614 / 0.637 |
| R1 whole listening record (ref_w4r1_listening) | 0.651 | 0.653 | 0.640 | 0.643 | 0.667 / 0.621 |
| R1 MERT + essentia + duration (ref_w4r1_music) | 0.646 | 0.642 | 0.664 | 0.642 | 0.613 / 0.624 |
| R2 learned nets ensemble | 0.638 | 0.615 | 0.657 | 0.627 | 0.627 / n/a |
| R2 unseen-artist ridge ensemble | 0.645 | 0.639 | 0.653 | 0.639 | 0.640 / 0.657 |
| Best simple baselines (artist plays / duration) | 0.619 / 0.577 | 0.440 / 0.566 | 0.521 / 0.510 | | ~0.50 |

**Caveats that apply to every row**
- **Selection.** Each builder scored 30-95 variants on TUNE. Walk-forward scores: 0.651 for the R1 listening family (no optimism), 0.625 for the R2 nets family (optimism +0.013), 0.613 for the R2 unseen family (optimism +0.032). A family's typical member scored about the reference level. With song labels shuffled (random-label refits), scores scatter with a standard deviation of about 0.04, so TUNE differences of 0.02 are noise.
- **Small HOLDOUT.** HOLDOUT has 740 tried songs, of which 148 are by new artists. The new-artist interval there runs from about 0.46 to 0.81.
- **HOLDOUT is not an artist-free test.** Holdout artists' earlier listening stays in training. Only the scored rows are artist-disjoint, so HOLDOUT checks selection hygiene, not generalisation to unseen artists.

**What the devil's advocates found, model by model**
- **R1 whole listening record**
  - Its TUNE score was the best of 17 nearby and random configurations.
  - With the candidate's own artist removed from its training songs, its gain over the new-songs-only recipe fell from +0.021 to +0.005.
  - It lost to the simpler new-songs-only version on HOLDOUT (0.640 vs 0.652).
  - Strongest point in its favour: new-artist songs on TUNE (+0.052 over the reference, lower bound +0.015) and on LATE. This did not replicate on HOLDOUT.
- **R1 music properties**
  - Its gain splits into essentia (+0.007, not significant) and a duration member that adds nothing on HOLDOUT.
  - All of its advantage is on songs by artists you already knew. It has no edge on new artists in any slice.
  - Its single-property findings did not survive a multiple-comparison test that accounts for songs by the same artist being similar (p = 0.16). They are hypotheses, not findings.
- **R2 learned nets**
  - **Bug:** the "panel weight 0.5" setting was never used in the code, so every panel run used weight 1.0. The DA fixed this in a scratch copy: weights 0.5 to 2.0 gave 0.631-0.638.
  - The nets add nothing over the linear part on LATE (0.615 vs 0.640) or HOLDOUT.
  - Max-pooling over the four MERT windows was coded but never tried. A DA's quick test matched the full ensemble on TUNE (0.638, new-artist up to 0.655). That number is TUNE-only and unproven.
- **R2 unseen-artist ridge ensemble**
  - Its headline 0.645 is a hindsight pick. The honest figure is 0.613 (walk-forward) or 0.629 (hyperparameters chosen inside training).
  - It does not beat the best reference on any slice with an interval that excludes zero.
  - A DA tested pooling over the best moments of a clip on essentia patch embeddings. It gave about +0.02 on that feature block (borderline significant) and nothing once added to the final model.

**Null control:** no leakage was found in any model. Round-1 models were FLAGged under the old band, but random-label refits in each model's own feature space average 0.46-0.51. So the old band was too narrow for feature models. Under the v4.1 band both round-2 finals PASS. That band is wide (about 0.08), so a PASS has limited power.

**Within-artist ranking.** Song duration alone still ranks songs by the same artist about as well as or better than every content model on TUNE (0.645). It falls to chance on HOLDOUT (0.498).

## 5. What the evidence supports and what it does not

**Supported**
- There is real, modest content signal (about 0.62-0.65 AUC), well above shuffled-label nulls and above duration and metadata models.
- It works about as well for new artists as for known ones.
- MERT carries most of it. Essentia tags and embeddings are weaker (0.56-0.61), and CLAP and lyrics alone are near chance.
- Artist familiarity is unreliable over time: it helped in 2021-2023 and reversed in 2024.
- Descriptive only: on TUNE, loved songs lean dark, heavy, aggressive, synth- or industrial-driven, vocal and loud. Dropped songs lean acoustic, vintage, calm and instrumental. Some tendencies flipped between early and late training sets, which mixes real taste drift with small-sample noise.
- Encounter context matters. The order effect holds even among songs that were not replayed in their first session (AUC 0.60). So at least part of the session link is not a consequence of liking the song. That is the relevant unvetted idea, tested as far as dev data allows; the reverse direction is not ruled out.

**Not supported**
- Any model beating the Workflow 3 reference by a real margin.
- Learned or temporal models adding anything over clip averages.
- "Specific parts of songs" as a usable signal. The tests found at most a small, unreplicated edge (the late half of the clip, peak-patch pooling). Previews are fixed 30-second excerpts from an unknown position in the song, so whole-song structure was never testable. The hypothesis is neither confirmed nor ruled out.
- Readiness for candidate search. The open-pool test still mostly measures ranking within familiar artists, and artist_recent matches the content models there.

## 6. Process problems found

- The R2 nets panel weight was not implemented (above).
- Duration checks by the DAs, as reported:
  - Every DA's recorded duration took the shorter of its self-reported and file-timestamp spans.
  - One R1 DA (taste-from-all-listening, works) had a 62.5-minute file-timestamp span against 20.6 minutes self-reported; its work ran as two attempts.
  - The R2 unseen-artist dismissed DA ran about 45 minutes over two attempts.
  - No cap was breached.
- Frozen shared folder:
  - All feature inputs match the manifest.
  - One harness score cache (evalkit-baseline-scores-df0f...pkl) changed at 14:52, after the freeze.
  - Two more harness caches were written there at 15:07, during the round-2 engineer's work, although the engineer reported writing nothing there.
  - MANIFEST.txt is stale for that file.
  - None of these are model inputs.
- Round-2 shared prep built nothing because FROZEN was never lifted. Not built:
  - the hand-crafted time-resolved descriptors (round 1 had also dropped them);
  - the 188 missing essentia clips;
  - the fast-loading consolidated index.
- Reproducibility:
  - The R2 nets builder overwrote most of its exploration configs, so most of its variant numbers cannot be regenerated from the folder.
  - Neural-net training varies by about 0.004 between runs.
- The round-2 engineer's tightened cap rule now refuses a --late run of the R1 music predictor, because it imports the Workflow 3 file that already has 3 LATE lines. Future models should stack it through `evalkit.refs.score` instead of importing it.
- `.cache/holdout_budget.json` lives in a git-ignored folder and cannot be regenerated from code. It reads remaining 0.

## 7. State of the held-out slices

- **LATE:** `.cache/late_runs.log` now has 23 lines (17 before this workflow). LATE results were seen by every later agent. Treat it as a weak drift check, not a holdout.
- **HOLDOUT:** 5 log lines: 1 engineer test with a random scorer and 4 real finals. Its numbers and the DEV+HOLDOUT pooled numbers were seen by the round-2 builders and DAs. HOLDOUT is now partly used up in the same way as LATE. A fresh untouched check needs a new idea: a new artist-hash slice would overlap with tuned data.
- **Sealed data:** untouched. It remains the only clean test.

## 8. What I would do next

1. **Accept the plateau as the current state.** Clip-level MERT gives about 0.63-0.65, and four very different attempts did not move it.
2. **Encounter context.** Most of the missing signal is plausibly about listening behaviour, not the audio. If the goal is predicting which songs will be loved, model encounter context explicitly, as a separate, clearly labelled non-content component. For candidate search, where no context exists, accept that the ceiling is lower.
3. **Unexplored content leads, each worth one honest test.** Each needs its hyperparameters chosen inside training, a walk-forward score, and no TUNE hand-picking:
   - max or peak pooling over finer segments (MERT per patch rather than 4 windows);
   - the panel weight with the bug fixed;
   - the hand-crafted time-resolved descriptors, which have never been built;
   - longer audio, if full-length audio or previews from other positions in the song can be obtained (only 30-second excerpts exist now).
4. **Before more tuning, decide how future claims will be checked.**
   - Sealed data stays the only clean test. It is run only by the main session after you approve.
   - Count new artists and new songs separately. 148 new-artist HOLDOUT songs cannot resolve differences under about 0.08.
5. **Housekeeping.**
   - Lift FROZEN for any shared-prep step that is meant to build something.
   - Regenerate MANIFEST.txt.
   - Move the holdout budget into regenerable code.
   - Remove dead code: the unused panel-weight setting and the non-regenerable variant lists.
6. **Timing for the next workflow.**
   - Agents finished well inside their caps: builders 42-64 of 90-120 minutes, DAs about 20 minutes. Several builders stopped early by choice, and DAs flagged this as insufficient effort.
   - The slow jobs were:

     | Job | Time |
     |---|---|
     | essentia extraction | 99 min |
     | null control | 7-14 min (5 seeds) |
     | --late or --holdout run | 2.5-8 min |
     | full TUNE run | 3-5 min |
     | fast run | 0.5-3 min |

   - Shared prep is the bottleneck; budget about 2 hours for any new audio extraction.
   - The workflow's start and finish (10:42 to about 17:25 UTC) spanned about 6.7 hours.
