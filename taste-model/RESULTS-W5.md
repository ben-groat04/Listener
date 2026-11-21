# Workflow 5 results: arbitrary numbers, tuning, and the fold set

All scores are TUNE-era development numbers (10 quarterly folds 2021-07 to 2023-10, 1074 tried songs, 342 loved) unless stated otherwise. They come from evalkit v5.0 (round 1) and v5.1 (round 2). With no new flags, both versions give exactly the same output as v4.1; the selftest checks this.

The main score is "sauc": the chance that a loved song is ranked above a tried-but-not-loved song from the same fold. 0.5 is chance.

Decisions use 80% intervals of paired differences, which is the owner's risk preference. Results are called:
- **decided**: the 80% interval is clear of zero;
- **undecided**: the interval's lower end is within 0.005 of zero. Such bounds flip with the bootstrap seed.

Held-out (LATE, HOLDOUT) numbers are not in this file. They are in the research lead's final report, section 6, and are described here only in words.

## 1. What the inventories found

Six agents listed every assumption and chosen number in the harness, the Workflow 3 and 4 predictors, and the feature preparation. Five wrote inventories; the sixth checked them for gaps.
- **552 rows** across the five inventories, plus **15 items** the gap checker found missing (567 in all). Some items appear in more than one inventory, such as the label and the folds, so the count of distinct items is somewhat lower.
- **A reason was found for 306 rows.** Most reasons are "stated in an earlier plan or README", not an argument from data.
- **A variation or test was found for 190 rows. None was found for 362**, nor for the 15 extra items. Where tests existed, they were mostly one-value-at-a-time comparisons on the same TUNE folds that the defaults had been chosen on.
- Never varied before this workflow:
  - the fold set (start date, spacing, window length, the 10/4 TUNE/LATE split);
  - the 90-day label horizon;
  - the HOLDOUT share;
  - the decoy ratio;
  - the 30-minute session gap;
  - the exposure buckets;
  - the grading thresholds.
- Notable facts:
  - Every dev stream is at least 30 s long, so skips are not in the data.
  - Two quarters (2023-Q1 and 2023-Q4) carry 69% of the pooled TUNE score's weight.
  - The "newest quarter stub" in the training target was found to hold 0-1 songs per fold, so it has no practical effect.

## 2. Does tuning the numbers help?

**Answer: no, not at the 80% level, in any of the three model areas tested.** Choosing numbers honestly, separately at each fold using only that fold's own past data (nested "inner" folds), was neutral or harmful every time.

| Area (base recipe) | Variants scored | Best single change vs default | Honest per-fold tuning vs default |
|---|---|---|---|
| Audio-content numbers (W3 audio_final: layers, windows, PCA, alpha, member weights, missing-audio fill) | 91 | +0.002 (alpha x0.1, 80% lower end +0.0002); it does not hold on other fold sets | 5 procedures: -0.006 to -0.033; four are decidedly worse |
| Listening-history and time numbers (W4 listening recipe) | 102 in round 1 + 35 in round 2 | about +0.007 to +0.011, which is the size chance alone gives when picking the best of the family | 10 procedures in round 1, 1 shrunk procedure in round 2: -0.015 to +0.008; none decided better |
| Music-recipe numbers (W4 music recipe: essentia clip and alpha, segments, GBM, member and MERT weights) | 82 | +0.003 | 4 procedures: -0.006 to +0.0003 |

Selection, accounted for honestly:
- Every default had already been chosen on these same TUNE folds by earlier workflows. "Every neighbour is worse" is therefore partly regression to the mean. It shows that tuning on TUNE cannot find more. It does not show that the defaults are good on new songs.
- Inner folds rank configurations only weakly the way the real test fold does (mean Spearman 0.25 for the audio recipe). That explains why per-fold selection fails.

One weak lead was tested with a pre-registered design in round 2. It concerns how the newest listening enters training: no 90-day wait, scaled partial counts for young songs, and coarser grouping of the target.
- The pre-registered primary comparison: +0.006, 80% [-0.001, +0.010]. **Undecided.**
- All 20 members of the family were slightly positive.
- An equal-weight average of the 21 configurations (final_avg21): +0.008, 80% [+0.001, +0.012]. Undecided under the harness's 0.005 margin, but above zero under a plain 80% rule. One devil's advocate stresses this point.
- The gain leans on one heavy fold (2023-01). Without it, the primary falls to +0.002 and the average to +0.004.
- Fair reading: a possible small real effect of about +0.004 to +0.008, inflated by selection and not confirmed. It is far below the smallest difference this data can resolve (section 3).

The averaging test itself:
- Averaging over plausible values never created spurious gains under null labels.
- For the listening recipe, averaging was mildly positive. For the music recipe, it tied the default. A post-hoc average of audio-content recipes lost.

Two other findings:
- **Freshness of the listening record matters a lot.** Cutting the record back by 30, 90 or 180 days costs 0.010, 0.040 or 0.079 sauc. Most of the cost sits in the recent-listening signal, not the new-song signal. By contrast, down-weighting old listening (half-lives, windows) never helped. Older listening is useful as long as the newest listening is also included.
- **Missing audio.** Songs without a preview clip are loved more often, and ranking them high gains about +0.01 to +0.02 on the tried songs. The gain does not hold within artist. It probably reflects the catalogue, not taste, and should not be used in a search for new songs. Caveat: the builder's evidence that open-pool candidates all have audio was wrong, because that table filters on previews by construction. So the question is unresolved, not settled.

Not tested: the W4 music recipe's MERT member numbers (PCA sizes, alphas, layers), the essentia blocks of the W3 recipe, other learner families, and the learned-representation and unseen-artist recipes of Workflow 4.

## 3. Is the set of folds arbitrary, and does it matter?

**Partly. Most fold choices are harmless. A few change conclusions.**

Harmless at 80%. Model rankings stay stable, with Kendall tau 0.76-0.91 over 12 models:
- shifting fold boundaries by 1-2 months;
- monthly versus quarterly retraining (paired differences inside noise);
- pairing songs by fold or by calendar quarter;
- session gap 5-120 minutes, and most exposure-bucket edges;
- the artist-history baseline's half-life (30-730 days) and the GBM baseline settings;
- dropping the first 1-4 quarters (pooled numbers move by 0.005 or less).

Over the five models that matter, ranking stability is weaker: tau 0.8 for shifted quarters and 0.4 for half-year folds.

Choices that change conclusions:
- **Training staleness of 6-12 months** (yearly folds) costs content and listening models 0.04-0.07 sauc. It costs the artist-history baseline almost nothing. On yearly folds the content models' lead disappears.
- **Label horizon.** With 180- or 365-day labels, the content models' lead over artist_recent is no longer decided, because songs by familiar artists keep being played. The 90-day label tracks the long-term outcome well (AUC 0.87 against keeping a song for a year). Changing its thresholds makes little difference.
- **Choosing the "best reference" on the fold set being scored** changes which reference wins (listening, music, or even artist_recent on yearly folds). Use a fixed comparator.
- **Weighting.** Weighting periods equally flips the sign of the content-versus-artist_recent difference. Round 2 found this is mostly noise:
  - Equal weight gives the four tiny 2021-22 folds (31-45 songs, near chance for every content model) the same influence as 283-song folds.
  - Per-fold differences are consistent with one common difference. The heterogeneity test has only about 27% power, so this is "not detected", not "shown absent".
  - Pooled pairs stay the primary score. Inverse-variance weighting and "drop the two heaviest folds" are recommended as required secondary checks.
- **A time trend.** The lead of content and listening models over artist history grows by about +0.10 per year (80% interval about +0.05 to +0.15).
  - It is not explained by a growing training history: models trained on only the last 12 months show the same trend.
  - It is largely a contrast between the four noisy early folds and the later ones. Without the first four folds, the lower end touches zero.
  - The love rate of newly tried songs fell from about 0.7 to 0.23 over the same period, so part of the trend may be a change in era.

The score itself:
- Pooled sauc on the love label is as reproducible as any of 14 candidate scores. Top-of-list scores, equal-weight macro, graded and 365-day scores were clearly noisier.
- This test is partly circular: the reference models were tuned on pooled sauc on this same data. "Not beaten" is shown; "best" is not.
- Resolution: the 80% half-width of a paired difference is about 0.025 between references and 0.04 against artist_recent. **Improvements smaller than about 0.02 cannot be established on this data.**
- The open-pool score (tried songs versus never-played decoys) disagrees with sauc about references versus artist_recent. It mostly measures what the user tries, and depends on how the decoys were built.
- Random variation in play counts is small, but this was tested only under a simple Poisson model. The real limit appears to be how much can be predicted before listening, but that is a belief, not a measurement.

## 4. Best results (TUNE, full runs)

The devil's advocates reproduced every headline number below exactly. The research lead re-ran five of the six finals in fast mode and got the same point scores; the sixth (w5_tuned_margin) was re-run by the round-2 lead plan.

| Model (harness) | sauc | vs artist_recent (80%) | vs best single reference (80%) | Devil's advocate notes |
|---|---|---|---|---|
| pair_z: listening ref/0.70 + music ref/1.27 (v5.1) | 0.661 | +0.042 [+0.013, +0.090] decided | vs listening +0.009 [-0.001, +0.022]; vs music +0.014 [+0.001, +0.027]; both undecided | The two references were picked knowing their TUNE scores. Null control passes, but its gated value 0.569 is close to the band top 0.580. |
| final_avg21: average of 21 listening configurations (v5.1) | 0.659 | +0.040 [+0.014, +0.083] | vs listening +0.008 [+0.001, +0.012] undecided | Leans on fold 2023-01. No advantage over artist_recent on macro or gc. |
| w5_final_mat0s: listening + no-wait partial targets (v5.0) | 0.657 | +0.038 [+0.014, +0.082] | +0.006 [-0.001, +0.011] undecided | Chosen after 87+ looks. Wins only 4 of 10 folds. Other configurations pass the same sign rule. |
| w5r1_stack3: rank average of 3 references (v5.0) | 0.653 | +0.034 [+0.004, +0.084] | +0.002 [-0.010, +0.016] | Fails the harness independence check by construction. Clearly worse than the listening reference on new-artist songs. |
| final_avg81: average of 81 music configurations (v5.1) | 0.646 | +0.027 [-0.006, +0.079] | vs music -0.001 [-0.003, +0.002]: a tie | Tie is near-automatic (0.99 correlation with the default). |
| w5_tuned_margin: inner-tuned audio recipe (v5.0) | 0.625 | +0.006 [-0.026, +0.055] | vs audio_final -0.006 [-0.021, +0.001] | A slightly worse copy of the default. |

Reference rows: ref_w4r1_listening 0.651, ref_w4r1_music 0.646, ref_audio_final 0.632, artist_recent 0.619.

All six finals pass the null control on the cluster-aware band. They all fail the older song-level band, which the harness README calls too narrow for feature models.

**No Workflow 5 model beats the Workflow 4 listening reference at the decision level.** None beats the diagnostic pool_artist_siblings either (0.644; it uses information from after the cutoff and is not a valid predictor). Gains over artist_recent hold on pooled sauc but vary across fold sets and labels.

Devil's advocate verdicts:
- Each builder's claims were checked by two devil's advocates: 190 checks in total. 170 hold, 17 do not hold and 3 were left unverified.
- The claims that did not hold were wording or inference errors, not wrong numbers. They include:
  - a trend described as "positive from 2022-Q4", when the heaviest quarter is negative;
  - a bar study that omitted yearly folds;
  - "nboot fixes seed noise";
  - a chance benchmark inflated by wild configurations;
  - "the quarter stub is real", when it holds 0-1 songs;
  - "the margin rule removes the damage", which is true for one inner-fold design only;
  - "no maturity dose-response", which compared unlike cells;
  - "best-of-20 within chance", when the bootstrap check gives P 0.17;
  - a NEG count of 7+1, when all 8 are low-fill variants;
  - "open-pool decoys all have audio".
- The three unverified claims were weighed as follows:
  - Tuner drift: verified by the other devil's advocate.
  - Music walk-forward: read but not re-run by either devil's advocate. It is a low-power side result.
  - "Label noise is not the limit": kept as a belief.

## 5. State of the held-out slices

- **LATE (2024 folds)**: 29 logged runs, 6 of them in this workflow (one per builder). It has been seen by every agent since Workflow 4, so it is only a drift check. In direction it agreed with TUNE:
  - no final was clearly better than the best reference;
  - the small listening-family gain reappeared at about half its TUNE size, undecided;
  - the artist-history baseline is much weaker on LATE, so every model's lead over it grows.
- **HOLDOUT (artist-disjoint)**: three new single-use runs were allowed in round 1, one per builder, and all were used. The budget is now 0 and was kept closed in round 2. Nothing on HOLDOUT contradicted TUNE.
- **Sealed data**: untouched.

## 6. What the evidence does and does not support

Supported:
- Tuning the existing recipes' numbers on TUNE, or choosing them per fold, does not improve them.
- Averaging over plausible values is at least as safe as choosing one value.
- Fresh listening data matters, not old-data down-weighting.
- 1-3-month fold choices and pairing are harmless; staleness, label horizon and comparator choice are not.
- Pooled sauc is a reasonable primary score that resolves only differences of about 0.02 or more.

Not supported:
- That the default numbers are good in absolute terms.
- That any Workflow 5 model beats the best Workflow 4 reference.
- That the newest-listening gain is real.
- That the missing-audio effect is taste.
- That the upward trend will continue after the dev period.
- That pooled sauc predicts success in a real search among unheard songs.
- Anything about the untested recipes or model families.

The project's standing position is unchanged: a real but modest content signal (sauc about 0.65). This workflow found that the arbitrary numbers are not what holds it back.

## 7. Process problems

- **Timing.** About 6 hours in total (lead plan at 18:11 UTC, this report about 00:10 UTC; the inventories ran before that). Builders used 35, 99, 44 / 61, 47 and 23 minutes of 120 / 90-minute caps. Devil's advocates noted under-use: unrun items that cost minutes, and a calibration stopped at 10 of 12 seeds with time to spare. No job broke its cap.
- **Reproducibility is good.** Every builder's headline numbers were regenerated bit-for-bit from the project folders. Gaps:
  - some scratch-only dumps and null-refit pickles are regenerable only by re-running;
  - one analysis output file (score-calculation a5_trend_abs.txt) is all NaN; the real numbers are in a "_tail" file;
  - one analysis silently dropped a fold.
- **Pre-registration is only partly verifiable.** Several grid and pre-registration files were last modified after their first scored runs, because declarations were appended to them. Re-runs show the scored parts were not changed. One round-1 report left out four scored post-hoc combinations.
- **Reporting slips.** These were caught by devil's advocates:
  - the null-control statistic was misquoted (per-seed mean instead of the gated value) in three reports;
  - interval wording was inconsistent;
  - the round-1 audio null calibration used one shared permutation per seed, which is about two effective draws.
- **Harness gaps.**
  - The 0.005 "undecided" margin is stricter than the owner's plain 80% rule. Two round-2 results fall between the two.
  - FILE_DELTAS80 prints nothing for single-model files.
  - The engineer never ran --late or --holdout live; the builders' runs worked.
  - The round-1 stack fails the independence check.
- **Housekeeping.** `__pycache__` folders remain in the six w5 predictor folders, for the cleanup agent.

## Next steps (kept separate)

These are recommendations only. Nothing below has been run.

1. **Stop tuning the existing recipes' numbers.** The evidence says further gains there are below what this data can resolve. Effort is better spent on new information, such as listening-context features for the new song or features that separate model staleness from feature staleness, or on recipes not yet tested here.
2. **Adopt a pre-registered decision rule:**
   - primary score: pooled sauc on love, quarterly TUNE folds;
   - required secondary checks: inverse-variance per-fold delta and the delta without the two heaviest folds, all with the same sign;
   - fixed comparators: artist_recent and ref_w4r1_listening;
   - 80% artist-cluster interval with at least 1000 resamples;
   - an explicit choice between "lower end > 0" and "lower end > 0.005", made once by the owner's rule and recorded;
   - secondary checks: strong and love_10_4 must not flip a sign; report within-artist, new-artist and per-half-year results.
3. **Retrain monthly where cheap**, never on 6-12-month-stale models. Report a monthly-fold run beside the quarterly one.
4. **Plan the next clean test now.** HOLDOUT is spent and LATE is worn out, so the next unbiased evidence is the sealed slice. Gather enough dev evidence first: no single change found here, including averaging and freshness, is large enough to be worth spending it on.
5. **If the missing-audio question matters for search,** test it with a fill learned from training data and with an audio-present-only evaluation, not with fixed constants.
