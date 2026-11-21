ENGINEER REPORT: evalkit v3.1 and shared caches. Everything in "Changes" and "Ran" below was run in this session unless it is under "Beliefs / gaps". No --sealed, make_sealed, .sealed/ or raw streams were touched.

## Changes (all in /home/user/Listener/taste-model/evalkit/)

**1. Null control v2**
- `run._null_control(train, cands, rng, relabel)` keeps the song-identity shuffle. With relabel=True it also applies a random bijection over all artist ids of train ∪ cands, and one over all album ids, to train only. This covers artistIds, artist, albumId and the artist part of the song key, so each song stays consistent.
- I also made the meta of the shuffled train tracks follow the relabelling (`artistNames`, `albumName`). The spec did not ask for this. Without it a predictor reading meta names would still see true artists.
- Seeds are cutoff yyyymmdd + k, for k = 0, 1, 2.
- `--null-control` now runs `run.null_report` INSTEAD of the normal tables. It prints per-seed and 3-seed-mean sauc, wa_sauc and new-artist sauc per model, baselines included, plus the band. The gate is PASS iff all three means lie in the 95% band of a 3-seed mean (200 repeats of the mean of 3 independent label permutations of a fixed random score; cached with `_band(..., nmean=3)`).
- `--null-control-identity` keeps the old identity-only shuffle, one seed, diagnostic only, not gated. The README explains it preserves per-artist song counts, which is real history information. The two flags can be combined.
- With `--late`, the null report also covers the LATE and ALL slices.

**2. Graded metric**
- `gc` and `gc_wa` are in `metrics.Block.stats`. Pairs with differing plays90 inside a fold (or fold × primary artist) are pooled with weights, and score ties count 0.5.
- Both have artist-cluster bootstrap CIs, a permutation band (plays90 permuted within the group, 200 permutations), paired-delta tables and VERDICT columns (`gc`, `gc_ci`, `gc_band`, `gc_wa*`, `dGC_lo_vs_nonaudio_gbm`). The Spearmans are kept.
- The selftest checks both against brute force, including a bootstrap replicate.

**3. Evidence grades**
- Every paired delta now has `<d>_lower_bound`, `<d>_P_gt0` and `<d>_80ci` tables. Deltas covered: dSAUC, dWA, dGC, dGCWA, open_dSAUC (all, new, known), open_dP20, open_dWA.
- VERDICT columns per metric (sauc, wa, gc) versus nonaudio_gbm: `d_<m>_vs_nonaudio_gbm`, `P_<m>_gt0`, `ci80_<m>`, `evidence_<m>`.
- Grading follows your definitions exactly (`run.finish_verdicts`).
  - STRONG: ALL-slice 95% lower bound > 0, and point Δ > 0 on both TUNE and LATE.
  - SUGGESTIVE: P ≥ 0.8 on both TUNE and LATE.
  - NONE: otherwise.
- With `--late`, the grade and the ALL-slice deltas (lower bound, P, 80% interval) are in the ALL VERDICT, together with TUNE_ and LATE_ point deltas and P. The TUNE and LATE VERDICTs say 'see ALL'.
- Without `--late`, the column reads 'TUNE only (P=..)'.
- The README states the graded scale is on purpose, because the sealed run is the strict final test, and quotes the user's two sentences verbatim.
- A baseline-only run now prints VERDICT rows for the baselines. Before, it printed none.

**4. Within-artist reference**
- VERDICT columns `dWA vs best meta` (the model name), `dWA vs best meta lo95` and `dWA vs best meta P(d>0)`.
- The best of (duration, meta_gbm, nonaudio_gbm) is chosen by the slice's point wa_sauc. Baselines in that set get NaN.

**5. Diagnostics**
- `exposure_before`, `exposure_after`, `exposure_session` (kept; same ordering as before, defined as minus (before + after + 1)) and `replays_first_session`.
- Pool columns are `exp_before`, `exp_after`, `replays_s1`. Decoys sit below every tried song, or at 0 for replays. DIAGNOSTIC in baselines.py is updated.
- The README says plainly that 'after' and the replay count can be consequences of liking the song, while 'before' cannot.

**6. Housekeeping**
- README rewritten for v3.1: iTunes fill text (now active, with current coverage), the null v2 section, a late-slice note and a comparability note.
- The late_runs.log note: the lines timestamped 09:00-09:05 UTC are devil's-advocate audit looks. The log has 4 lines in that window (2 for the same training-signal file), not the 3 in the brief. LATE is a "seen-once-per-design" slice, and the sealed folds are the only untouched test.
- Deleted stale caches: pools a3e8db819279fcc7, nullband a3e8db819279fcc7, baseline-scores 2be464b7a6373185, baseline-scores 025a9e55dd444c85 (obsolete after the code change), pools 282fcbd3606cc4e0 and nullband 282fcbd3606cc4e0 (superseded). Round-1 feature caches kept.
- Current caches: `evalkit-pools-d4147e4b5cf5972f.pkl`, `evalkit-nullband-d4147e4b5cf5972f.pkl`, `evalkit-baseline-scores-9aaf2da010bb63de.pkl`.
- Failed attempts: none to delete.

**New toy-predictor check.** I ran one predictor through `--fast` to check the non-baseline VERDICT path. It worked, and it was a scratch file outside the project.

## Ran
- `python3 -m evalkit.selftest`: OK (about 1.5 min). The null v2 result on 3 TUNE folds is printed, not asserted. The band is sauc (0.444, 0.562), wa (0.333, 0.657), new (0.429, 0.571).

  | model | sauc 3-seed mean | wa_sauc mean | new-artist sauc mean | outcome |
  |---|---|---|---|---|
  | artist_recent | 0.511 | 0.514 | 0.523 | PASS |
  | nonaudio_gbm | 0.507 | 0.495 | 0.461 | PASS |

- `--late` full baseline run (nboot 300, independence on). It appended 2 lines with `files: []` to late_runs.log, because I ran the summary twice (09:28 and 09:34 UTC).
- `--null-control --null-control-identity` for the baselines on TUNE (10 folds).
- `--fast` baselines and a toy predictor run (scratch).

## Current dev baselines
Columns: sauc, wa_sauc, gc, gc_wa, open p20 (open-pool precision at top 20).

TUNE (10 folds, 95% bands: sauc 0.459-0.537, wa 0.448-0.552, gc 0.474-0.525, gc_wa 0.468-0.534)

| model | sauc | wa | gc | gc_wa | open p20 |
|---|---|---|---|---|---|
| popularity | .471 | .447 | .482 | .474 | .094 |
| artist_plays | .619 | .500 | .591 | .500 | .371 |
| artist_recent | .619 | .500 | .596 | .500 | .394 |
| artist_love_rate | .550 | .502 | .540 | .500 | .179 |
| duration | .559 | .607 | .539 | .566 | .073 |
| meta_gbm | .528 | .577 | .534 | .547 | .065 |
| nonaudio_gbm | .559 | .552 | .557 | .534 | .145 |

LATE (4 folds, bands: sauc 0.456-0.550, wa 0.451-0.565, gc 0.469-0.527, gc_wa 0.463-0.540)

| model | sauc | wa | gc | gc_wa | open p20 |
|---|---|---|---|---|---|
| popularity | .521 | .476 | .535 | .496 | .037 |
| artist_plays | .454 | .496 | .498 | .499 | .121 |
| artist_recent | .436 | .496 | .490 | .499 | .136 |
| artist_love_rate | .493 | .499 | .505 | .507 | .037 |
| duration | .564 | .533 | .539 | .512 | .099 |
| meta_gbm | .548 | .528 | .530 | .516 | .050 |
| nonaudio_gbm | .540 | .547 | .523 | .527 | .100 |

ALL (14 folds): nonaudio_gbm sauc .551, wa .551, gc .544, gc_wa .532, open p20 .132. Full tables are in the scratchpad logs.

The LATE artist_plays fold 2024-04 and the ALL popularity fold 2023-04 are flagged BELOW CHANCE.

Baseline VERDICT rows versus nonaudio_gbm (the dSAUC_lo_vs_nonaudio_gbm column; TUNE and LATE rows):

| model | TUNE | LATE |
|---|---|---|
| artist_plays | 0.001 | -0.148 |
| artist_recent | -0.005 | -0.154 |
| duration | -0.058 | -0.046 |
| meta_gbm | -0.067 | -0.032 |

The ALL-slice grades for all baselines are NONE on sauc, wa and gc. Example P(Δ>0) values (TUNE | LATE):
- artist_plays: sauc .98 | .02
- duration: wa .84 | .41
- meta_gbm: wa .92 | .19

DIAGNOSTIC references (TUNE | LATE sauc):
- exposure_before .623 | .583
- exposure_after .625 | .600
- exposure_session .658 | .619
- replays_first_session .694 | .743
- oracle_7d .880 | .906

## Null v2 baseline results (TUNE, 3-seed mean sauc / wa_sauc / new-artist sauc; band of the mean: sauc 0.475-0.519, wa 0.476-0.533, new 0.454-0.536)

| model | sauc | wa_sauc | new | outcome |
|---|---|---|---|---|
| popularity | .471 | .447 | .507 | FAIL (sauc, wa out) |
| artist_plays | .523 | .502 | .507 | FAIL (sauc out) |
| artist_recent | .525 | .502 | .503 | FAIL (sauc out) |
| artist_love_rate | .503 | .501 | .511 | PASS |
| duration | .520 | .524 | .501 | FAIL (sauc out) |
| meta_gbm | .510 | .517 | .473 | PASS |
| nonaudio_gbm | .518 | .518 | .493 | PASS |

Two points, both from this session's checks:
- popularity, duration and meta_gbm use no history, so the null cannot remove their real metadata signal. FAIL is expected for them, and PASS only says no history leakage.
- For artist_plays and artist_recent the specified band is probably too narrow. Their score is constant within an artist. A random artist-constant score against the real labels, with a 3-seed mean, ranges 0.459-0.541, versus 0.475-0.519 for the specified band. Their means (0.523 and 0.525) lie inside that wider range. This is my own quick check against the real labels, not part of the harness. I did not change the band, since the spec fixed it.

Identity-only shuffle, diagnostic (TUNE sauc):
- artist_plays .595
- artist_recent .602
- nonaudio_gbm .518

The history-count models keep signal under it, which is the reason for v2.

## Comparability
- Folds, labels, baseline code and decoy rules are unchanged.
- Pools for 8 of the 10 TUNE folds are bit-identical to the cached pools used before. Baseline scores for those 8 folds are identical (max diff 0).
- The 2021-07 and 2021-10 pools came out different when rebuilt. 49 of 220 decoys (2021-07) and 66 of 245 decoys (2021-10) differ from the old cached pickle. The rebuild is deterministic (two separate processes gave identical output). Earlier scores for those 2 small folds, and TUNE pooled numbers by a small amount, are therefore not exactly comparable.
- I could not identify why the old pickle differed. Possible causes are a stale cache or a different data.py when it was built.
- The 4 LATE folds (2024) were not compared against old pools.
- v3 null-control results are not comparable to v2. Use `--null-control-identity` for the old shuffle.
- If any round-1 predictor consumed old LATE-fold pools, preview coverage in the 2021 folds changed slightly (see the manifest below).

## Shared artefacts (location and format only)

**Previews.** The manifest at `.cache/shared/previews/manifest.csv` was extended by `fetch_previews` to the current pools. It has 10288 ok rows and exactly matches the urls the current pools need. The earlier manifest had 10297 rows, 9 of them no longer needed, and a backup is in the scratchpad. Audio files are kept.

**MERT.** `.cache/shared/w3r1-mert-v1/` has 131 shards (shard_00130 added). The coverage check showed 29 urls missing because of the regenerated pools. I topped them up with `build_mert.py` in about 1 min. It now covers every ok manifest row.

**CLAP.** The spec said 9220 of 10297 covered. Actually only 5713 of the manifest md5s were covered. The other 3507 cached keys were not in the manifest, and 4584 manifest rows (plus 45 new urls) were missing. I ran `build_clap.py` twice, about 33 min in total at 1 thread (the spec estimated 10 min). It appends to the same file `.cache/shared/w3r1-clap/emb.npz`, which now has 13831 keys covering every manifest row. 3507+ of those keys are unused leftovers.

**Lyrics.** Unchanged. Coverage gap: every train and tried track has a lookup record, but only 57.8% of decoys do (found 53.1%, embedding 50.7%). That asymmetry means a missing lyrics record is more likely for a decoy. I did not fix it.

**FEATURES.md.** Written at `.cache/shared/FEATURES.md`. It covers keys, shapes, dtypes, one-row meaning, regenerate commands, the per-track-independent statement, and coverage per slice (TUNE, LATE, ALL) for train, tried and decoy.

Audio coverage (all caches identical):

| group | TUNE | LATE | ALL |
|---|---|---|---|
| train | 0.892 | 0.895 | 0.894 |
| tried | 0.928 | 0.956 | 0.939 |
| decoy | 0.990 | 0.991 | 0.991 |

The shortfall is tracks with no previewUrl.

## Not done / caveats
- The spec's CLAP figures (9220 of 10297, about 10 min) were wrong, as above.
- The spec says 3 audit looks; the log shows 4 lines. The README states this.
- Under `--null-control`, no independence check runs.
- The selftest "shortcut AUC" with the release-age bucket varies run to run: 0.585 in the first run, 0.593 in the final one.
- The scratchpad folder already held other agents' files (final_run.log, gbmexp.py, and others). I did not read or delete them.