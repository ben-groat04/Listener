# Devil's advocate r2 (direction: works) - signal-fresh-and-averaging

## Per-claim verification (all from code and output files; my fast TUNE re-run of predict.py reproduced the builder's output byte-for-byte except timings and the dump path)
| # | Verdict | Evidence |
|---|---|---|
| 1 | holds | Re-ran `evalkit.run --fast --best-ref ref_w4r1_listening --dump-scores ... predict.py` (195 s). FILE_DELTAS80 row default-minus-f_m0s_q is d=-0.006 [-0.010,+0.001] (sign flipped: +0.006 [-0.001,+0.010]), UNDECIDED. Note report text is inconsistent: its declaration header says [-0.000,+0.011] (that is the dump bootstrap), section 0 says [-0.001,+0.010]. |
| 2 | holds | All 20 deltas positive (+0.0016..+0.0111, mean +0.0063); every FILE_DELTAS80 row UNDECIDED (best lo80 is +0.003, f_m60s_q). |
| 3 | holds, interpretation soft | calib_boot.py re-run on my dump: P(null best>=obs)=0.167; family mean P=0.02; count-positive P=0.025. calib_results.jsonl: 5 of 10 null seeds above +0.0111. BUT the refit null uses near-noise models (sauc 0.47-0.57, delta sd 0.015) so it overstates chance; the bootstrap P=0.17 is below 0.2, i.e. by a plain 80% rule the best-of-20 is NOT clearly "within chance"; the two calibrations disagree. |
| 4 | holds | My LOFO on my dump: drop 2023-01 gives +0.0018 [-0.0054,+0.0080]; fold_meta IV +0.0017, I2 0. Also NEW: the declared final avg21 shows the same dependence (LOFO drop 2023-01 +0.0037 [-0.0015,+0.0091], vs +0.0079 all folds); the report gives LOFO for the primary only. |
| 5 | holds | FIXED COMPARATOR tables in results/altsets_primary_and_avgs.txt: f_m0s_q POS only on tune_h (+0.011 [0.005,0.015]) and tune_y (+0.011 [0.006,0.015]); UNDECIDED on tune, tune_q1, tune_q2, tune_m. |
| 6 | holds, wording flawed | Means over cells: 60 +0.0067, 30 +0.0052, 0 +0.0075, 90 +0.0048 (the 90 mean is over only 2 cells). The parenthetical "roll91 and all groupings only" is wrong for 60/30/0 (those are over all 6 cells incl. quarter). Like-for-like (r91/all only): 60 +0.0073, 30 +0.0057, 0 +0.0091, 90 +0.0048 - still not monotone, differences of 0.001-0.004 vs SE ~0.005, i.e. no information either way. |
| 7 | holds | FILE_DELTAS80: avg21 +0.008 [+0.001,+0.012]; avg_mat +0.005; avg_grp +0.005; avg_fresh2 +0.003; nested +0.004; none POS. |
| 8 | holds, low power | Re-ran `--null-control final.py`: PASS (cluster band), seed-mean sauc 0.555 in (0.487,0.567) - near the upper edge; real-null gap +0.134 [0.094,0.174]; identical to builder. results/null_procs.txt: all 7 other procedures PASS. "No spurious gain" rests on 10 refit seeds with per-seed delta sd ~0.01, so it cannot exclude a +0.003 inflation. |
| 9 | holds (as a signal split) | default-minus-stale rows: stale_pan90 +0.031, stale_new90 +0.007, stale_all90 +0.040 (cost of staleness). Caveat: shifting the panel window back 90 d also changes which period the panel represents (composition), so "freshness" is confounded with window position; panel and new-song targets have different effective sizes. |
| 10 | holds | predict.py: features are MERT PCA (audio only); listening streams enter only through _newsig/_pansig targets. No listening features exist. |
| 11 | holds for sauc, selectively framed | full_run_final.txt VERDICT_DELTAS: vs default +0.008 [+0.001,+0.012] UNDECIDED; vs artist_recent +0.040 [+0.014,+0.083] (lo95 -0.005); siblings diagnostic from report. But in the same table macro_sauc vs artist_recent is -0.005 [-0.031,+0.044], gc -0.004; pool_artist_siblings alone (a non-audio structural diagnostic) has sauc 0.644 vs final 0.659. Across alternative fold sets the primary vs artist_recent is +0.040 (tune), +0.009, +0.029, +0.026, +0.026 (tune_h), +0.003 (tune_y) with 80% intervals containing 0 in 5 of 6 sets. |
| 12 | holds | I recomputed per-fold AUC and artist-bootstrap 80% intervals from my dump: 2021-07 0.494 [0.33,0.68] (27 artists), 2021-10 0.492 [0.37,0.61] (24 artists); scores not constant. Consistent with chance; weak test, as stated. |
| 13 | holds | run_late_final.txt (read-only) matches the numbers in report section 8; none are in the structured result. LATE is partly used; direction agrees with TUNE, size roughly half (what selection inflation would predict), UNDECIDED. |

## Items beyond the claims
- TIMING: builder 22:12:21 -> 23:13:23 (61 min); file mtimes (22:13 first run ... 22:58 late, 23:12 results copy) agree; no job beyond cap. Report says the final was declared at 22:56 "before any --late" while PREREG.md/final.py are dated 22:19-22:21 and the declaration text in PREREG says 22:21: harmless inconsistency, final.py was fixed before late (22:58).
- Final is an equal average of the default and 20 near-copies: sharing a 0.5-weight panel half with default, so deltas are diluted and strongly correlated (not 20 confirmations). Family comes from round-1 choice on the same TUNE songs.
- FOLD_META for avg21 vs default: IV +0.006 [+0.001,+0.011], Q 4.4/9, trend -0.006/yr [-0.015,+0.002]; the largest recent fold (2023-10, n=235) shows +0.003; gain is carried by 2023-01 (n=283).
- Engineer v5.1 vs spec: VERSION v5.1; FILE_DELTAS80 nboot 1000 fixed seed with decision80; --best-ref with FIXED COMPARATOR; FOLD_META printed; dump has first_play_date (checked); holdout budget file still {w5r1, 0}. I did not run selftest or any --late/--holdout run.

## What I ran
Fast TUNE re-run (run_da_main.txt, dump_da.pkl, 195 s), harness --null-control on final.py (run_null_da.txt), calib_boot.py/analyze_calib.py, my own fold_meta/LOFO/per-fold AUC analyses (inline python). Not run: full run, alt-set runs (read from builder's saved outputs), selftest, late/holdout.
## Shared inputs
shared-w5r1 has DONE; all 7 files match MANIFEST sha256. Builder did not use it (reads .cache/w4r1/compact.npz).
