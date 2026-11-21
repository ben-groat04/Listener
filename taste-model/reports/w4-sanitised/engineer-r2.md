ENGINEER r2 REPORT: evalkit v4.1 (all seven spec items plus the hygiene items implemented).
Start 2026-11-21T15:01:22Z, end 2026-11-21T15:34:31Z (TIMING.txt in /tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf4/engineer-r2/). Nothing was committed. No --sealed, make_sealed, decoy or raw-stream access. No real predictor was run with --holdout or --late.

## WHAT I CHANGED (files in /home/user/Listener/taste-model/evalkit/)
New files: bundle.py (bundle hash), refs.py (evalkit.refs). Edited: run.py, metrics.py, baselines.py (REFERENCES now has 7 names), selftest.py, README.md. data.py and make_decoys.py are untouched, so the pool hash is unchanged and the pools are bit-identical (selftest asserts the digests).
1. Cap loopholes
 - a/b. bundle.py imports the entry file in a subprocess and collects the modules under taste-model/ outside evalkit/. It also records importlib spec loads made at import time. It adds files named by a path literal in code (docstrings and comments ignored, via ast) and files imported by name from the same folder, so lazy loads at call time are found. The bundle hash is the sha256 of the sorted (relative path, file sha) pairs plus the entry files' sha. Both the entry sha and the bundle hash are checked against the cap (late 2, holdout 1) and logged in new lines as bundle_sha256 and member_sha256. Old lines count by entry sha.
 - DEVIATION (my addition): a bundle hash that includes the wrapper file can never equal the hash of the wrapped predictor. So I also refuse a run if any imported or loaded project file was itself logged as a predictor entry file `cap` times. A project file that was never submitted as an entry (a shared helper) does not count.
 - Side effect: the existing w4r1-what-in-the-music/predict.py imports w3r2-audio-taste/predict.py, which already has 3 LATE log lines. Its --late is therefore now refused. Builders must stack via evalkit.refs.score instead of importing it.
 - c. Fingerprints are stored in `<log-dir>/late_fingerprints.pkl` and `holdout_fingerprints.pkl`. The check refuses a model whose first-fold scores have Spearman >= 0.999 to a model logged by a DIFFERENT file; re-running the same file is not compared with itself. It uses the first LATE fold (main rows) for late and the first dev fold (holdout rows) for holdout. There is no backfill.
 - d. I created .cache/holdout_budget.json = {"round":"w4r2","remaining":2}. Each --holdout run decrements it after the log line is written and before any output is printed. The harness refuses at 0 or if the file is missing. That file lives in git-ignored .cache and is not regenerable from code, so the main session must recreate it if it is lost.
 - Tests use `--log-dir DIR` (new option). Logs, fingerprints, budget file and late tables go to DIR. The real logs and budget were verified unchanged by md5 before and after my tests.
2. --holdout also scores the main 14 folds with the same predictors (independence check only on the holdout part) and prints the pooled slice DEV+HOLDOUT. That slice is not graded and has deltas vs every reference. holdout_runs.log lines gain `dev_plus_holdout` (sauc, wx and new-artist sauc with CIs per model).
 - Tested with a dummy random scorer and a temp log dir. Result: 5m22s, budget 2 to 1 in the temp dir, the second run refused by the hash cap, a renamed copy refused by the fingerprint (Spearman 1.0000).
 - Caveat: DEV+HOLDOUT pools the main LATE folds with everything else, so a holdout run exposes the pooled dev result.
 - Bug fixed in passing: the HOLDOUT slices used the main-slice null-band cache key, so the printed band was wrong. The key now includes the part.
3. Headlines and label table
 - VERDICT has wx (CI, band, dWX_lo_vs_best_ref, d, P, ci80) and new_artist_sauc (same). evidence_sauc, evidence_wx and evidence_new_artist are graded STRONG/SUGGESTIVE/NONE by the same rules. wa and gc are unchanged. VERDICT_DELTAS has wx and new_artist_sauc columns.
 - New "LABEL VARIANTS" table (TUNE only, sauc [CI]) with love, strong, love_4_2, love_10_4, keep. keep is a harness-only pool column, computed only where c + 3 months + 365 days < DEV_END. That is all 10 TUNE folds; LATE folds print n/a.
 - The selftest checks keep against raw streams for 40 songs, checks LATE = NaN, and checks keep is not public.
4. --walkforward is allowed only with --fast. Family = PREDICTORS or WALKFORWARD_FAMILY. The composite is added as the model `walkforward[<folder>]`. The block prints the chosen member per fold, composite sauc/macro/wx/wa/new with CIs, paired deltas vs every reference and vs the hindsight best member, and the optimism. Nothing is cached across runs. The selftest compares against a brute force on 3 dummy members over 7 folds, with two folds too small to be eligible.
5. Null v4
 - Default --null-seeds is 5. Each seed's scores are rank-normalised within fold and averaged. sauc, wa and new-artist sauc of the average are compared with a cluster-aware band: 300 artist-block label permutations of the same averaged vector (artists with equal count swap whole label vectors within a fold; unique counts are merged into the nearest count and row-shuffled).
 - PASS/FLAG uses the cluster-aware band. The old song-level band and label are printed, marked 'song-level (too narrow for feature models; for comparison)'. Per-seed numbers, gaps with CIs and the wa and new-artist rows are kept.
 - The selftest asserts an artist-constant random scorer PASSes in >= 9 of 10 dummy runs: measured 10/10 (the song-level band passed 1/10).
6. References and stacking
 - ref_w4r1_listening (w4r1_final) and ref_w4r1_music (final_content) are added as cached rows. Caches are in `.cache/evalkit-cache/evalkit-ref-<name>-<bundle>-<code hash>.pkl`. best_ref keeps its definition and is now ref_w4r1_listening (0.651).
 - `evalkit.refs.score(name, train, cands, meta, cutoff=None)` calls the reference code on the given train. The cutoff is inferred from train if omitted. It is documented in the README.
 - Missing compact caches regenerate from build_compact.py (builder scripts run as subprocesses). I verified both real caches by moving them aside and regenerating: 2s and 4s, arrays identical.
 - Identity keys, checked empirically on a train with identity columns permuted among rows:
   - The w3r2 audio_final and w4r1-music keys are sums of row hashes (blind to a row permutation; the keys also lack albumId).
   - The w4r1-listening key is order-sensitive and fine.
   - I did NOT edit their files, so their scores, entry hashes and caps are unchanged. Instead refs.py keeps one strong key per reference (order-sensitive hashes of trackId, song, artist, albumId, timestamps, null seed, cutoff) and clears the reference's own fit caches whenever it changes. Selftest-asserted.
   - Harness reference rows go through the same guard. Because no files were edited, no before/after score check was needed. The w4r1_final scores in the old v4 harness run (0.651 TUNE sauc) equal ref_w4r1_listening in v4.1.
 - Null exemption: the reference rows are exempt. A dummy stacker returning ref_audio_final via evalkit.refs.score ran the reference on the null train. Its per-seed null sauc was 0.501/0.526/0.551/0.564/0.474 against 0.632 real, and it PASSed.
7. Misc: runtime per model is printed. Version string is v4.1; the README has a v4.1 section with comparability. Harness caches moved to `.cache/evalkit-cache/` because `.cache/shared/` is frozen; the pools are still read from `.cache/shared/` and nothing was written there.

## COMPARABILITY
I diffed the v4 and v4.1 fast TUNE `tried_within_group` tables as text (point values and CIs, 18 rows: baselines, shortcuts, ref_audio_final, diagnostics). All identical. So v4 sauc, wa, gc and macro stay comparable; wx, new-artist, the label table, the two new reference rows and the DEV+HOLDOUT slice are additions. v4 null PASS/FLAG labels are not comparable with v4.1 (new statistic, band and seeds). best_ref moved from ref_audio_final to ref_w4r1_listening, so evidence grades vs best_ref are harder than in v4.

## FAST TUNE v4.1 (non-holdout rows, 1074 tried songs, 342 loved), sauc / wx / new-artist sauc / macro / wa
popularity .476/.475/.500/.500/.459; artist_plays .619/.600/.498/.611/.500; artist_recent .619/.602/.498/.606/.500; artist_love_rate .543/.552/.498/.597/.503; duration .577/.580/.515/.562/.645; meta_gbm .539/.542/.493/.498/.593; nonaudio_gbm .555/.557/.479/.530/.557; has_preview .476/.481/.446/.480/.492; preview_source_itunes .482/.483/.461/.497/.520
ref_audio_final .632/.629/.614/.609/.614; ref_w4r1_listening .651/.643/.667/.597/.629; ref_w4r1_music .646/.647/.613/.618/.620.
Full CIs and the VERDICT and VERDICT_DELTAS tables with wx and new-artist deltas: .../engineer-r2/v41_baseline_fast_final.txt.

LABEL VARIANTS (sauc: love / strong / love_4_2 / love_10_4 / keep; loved counts 342/315/396/324/355 of 1074): popularity .476/.460/.477/.467/.476; artist_plays .619/.611/.627/.610/.634; artist_recent .619/.610/.625/.609/.632; artist_love_rate .543/.527/.538/.528/.515; duration .577/.575/.565/.575/.556; meta_gbm .539/.531/.528/.542/.552; nonaudio_gbm .555/.542/.557/.551/.577; has_preview .476/.471/.482/.474/.465; preview_source_itunes .482/.474/.499/.478/.473; ref_audio_final .632/.632/.616/.626/.635; ref_w4r1_listening .651/.649/.636/.645/.633; ref_w4r1_music .646/.647/.642/.640/.648. CIs are in the file.

WALK-FORWARD on the w4r1-taste-from-all-listening PREDICTORS family (6 members; file: walkforward_listening.txt):
 - Chosen members per fold: w4r1_final, w4r1_final, then w4r1_newonly for 2022-01 to 2022-10 (4 folds), then w4r1_final for 2023-01 to 2023-10 (4 folds).
 - Composite sauc .651 [.608,.681], macro .601, wx .643, wa .624, new-artist .668 [.573,.734].
 - Best member with hindsight is w4r1_final at .651, so optimism is +0.000.
 - Composite minus ref_w4r1_listening is d=-0.000 on sauc (P .48).

NULL v4, TUNE, 5 seeds, cluster-aware band (null_v41.txt): 6 of the 7 baselines PASS (popularity, artist_plays, artist_recent, artist_love_rate, meta_gbm, nonaudio_gbm). `duration` FLAGs (avg_sauc .543 vs upper .541; avg_wa .567 vs upper .558). Under the old song-level band 4 of 7 FLAG (popularity, artist_plays, artist_recent, duration). The dummy stacker PASSes (song-level: FLAG). The random-scorer dummy PASSes.

## RUNTIMES (what I ran, 2 threads)
Cold full v4.1 fast baselines run, all caches rebuilt: 73s (refs 12/13/19s each). Same run warm: about 13s. Full selftest: 1m49s (v4.1 part only: 29s). Null v4 on 8 models plus a random scorer: 3m56s. Walk-forward fast on the 6-member family: 52s. Dummy --holdout: 5m22s. Dummy --late with temp logs: 2m44s. For comparison, the old-harness fast run of the listening file took 68s. No job exceeded 10 minutes.

## NOT DONE / CAVEATS
 - Nothing in the spec was skipped.
 - The fingerprint check only covers runs from v4.1 on (no backfill, as specified).
 - Bundle probing needs the predictor file to be importable in a fresh subprocess; otherwise the run errors.
 - README also states the member-cap deviation.

Files: /home/user/Listener/taste-model/evalkit/{run.py,metrics.py,bundle.py,refs.py,baselines.py,selftest.py,README.md}; test inputs and outputs are in /tmp/claude-0/-home-user-Listener/22c975e6-58fa-522d-b17b-f92c7924f862/scratchpad/wf4/engineer-r2/.