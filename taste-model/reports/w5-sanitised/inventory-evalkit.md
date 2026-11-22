# Inventory: evalkit v4.1 assumptions and chosen numbers

Scope: /home/user/Listener/taste-model/evalkit/ (README.md, data.py, baselines.py, metrics.py, run.py, refs.py, bundle.py, ablate.py, describe.py, fetch_itunes.py, fetch_previews.py, make_decoys.py, make_sealed.py, register.py, selftest.py, pool_reference.json, sealed_manifest.json). Evidence sources: README, code comments, /home/user/Listener/taste-model/reports/w3-sanitised/ and w4-sanitised/ (abbreviated W3 / W4 below). Facts only; no judgement.

What I actually ran: `date`, file reads, greps. No evalkit run, no experiments, nothing touching sealed data or raw streams. What I only believe is marked "(read only)".

Column key. R = reason/evidence found (Y: text / N: none found). V = any variation or test of the value found (Y: where / N: none found). Feeds = does the choice feed the final scores directly (Y direct / N no / P partly or indirectly; "open" = only open-pool tables; "grade" = the evidence grade / verdict).

Note on the 80% decision threshold: the harness prints both 95% two-sided intervals (headline CIs, "lower bound" = 2.5th percentile) and 80% intervals (10th-90th percentile) plus P(d>0). The graded rule uses P>=0.8 (SUGGESTIVE) and a 95% lower bound (STRONG). See rows E96-E99.

## A. Data, identity, labels, folds (data.py)

| id | file:line | what | value | kind | R | V | Feeds |
|---|---|---|---|---|---|---|---|
| E01 | data.py:57 | Exact duplicate plays dropped: rows with same (trackId, endTime) treated as re-imported duplicates | drop_duplicates(trackId, t) | assumption | Y: inline comment "exact re-imported duplicate plays" | N: none found | Y (every count) |
| E02 | data.py:68, 102 | Every stream row counts as one play regardless of playedMs; playedMs is loaded into the frame but used nowhere in evalkit (grep) | no minimum play length, no skip filter | assumption | N: none found | N: none found | Y (plays90, days90, all labels, exposure, share90) |
| E03 | data.py:53 | Timestamps: endTime used as the play time, timezone dropped (tz_localize(None)); "distinct days" are calendar days of that naive time | endTime, tz stripped, normalize() for days | assumption | N: none found | N: none found | Y (days90 in love definition, day1) |
| E04 | data.py:56 | Primary artist = first element of artistIds (-1 if empty); used for clusters, within-artist metrics, new_artist flag, HOLDOUT, decoy dedupe | artistIds[0] | assumption | N: none found | N: none found | Y (bootstrap clusters, wa, new-artist, HOLDOUT) |
| E05 | data.py:40-45 | song_key title normalisation: remove bracketed text, remove " - ..." suffix, lowercase, non-word to space; merges remasters/live/deluxe | regexes | assumption | Y: docstring (merge versions of same song) | N: none found (W4 reviewer-code checked identity merge through post-cutoff links, read only; no alternative tried) | Y (what a "song" and a "new song" is) |
| E06 | data.py:58-67 | 'unknown track name' / empty titles keyed by trackId; song = connected component of (title+artist) and trackId links; canonical key = earliest named stream | graph merge | assumption | Y: docstring (3% of plays, same trackId under different artist ids) | N: none found | Y |
| E07 | data.py:111 | love label | plays90 >= 6 AND days90 >= 3 | both | Y: README "primary binary target"; W3 plan "Keep love"; no derivation of 6/3 found. W4 RESULTS: love predicts keep (>=6 plays days 90-365) AUC 0.85, 289 of 342 loved TUNE songs kept | Y: label variants love_4_2, love_10_4, strong, keep reported for every model (README; W3 builder-r1-training-signal.md:200: scores .650/.657/.640/.641; W4 RESULTS: moved by at most 0.02). Graded/continuous alternative gc (plays90) and a graded training target explored by W3 builder | Y (every binary metric) |
| E08 | data.py:16, 101 | Label horizon (watch window after first play) | HORIZON_DAYS = 90 | number | Y: comment "how long after first listen we watch a song" | P: keep label looks at days 90-365 (long-term check); horizon itself never varied | Y |
| E09 | data.py:112 | strong label | plays90 >= 15 and days90 >= 5 | number | Y: comment "a clear favourite" | Y: reported as a label variant | N (secondary table) |
| E10 | data.py:114-115 | love_4_2 and love_10_4 neighbouring definitions | 4/2 and 10/4 | number | Y: comment "neighbouring definitions for sensitivity" | Y: they are the variation | N |
| E11 | data.py:119 | share90 = plays90 / all plays by the user in the song's own [first, first+90d) window; denominator floor 1 | formula | assumption | Y: comment "normalises for listening volume over time" | N: none found as a headline; used in BREAKDOWN terciles and Spearman | N for sauc; Y for sp_share90 column and tercile BREAKDOWN |
| E12 | data.py:19 | Fold cutoff spacing | quarterly (freq "QS") | number | Y: W3 plan item 1 states "quarterly" (stated, not argued). W4 reviewer-code B3: pair weights make 2 of 10 TUNE folds 68% of pooled TUNE sauc | N: no other spacing tried (only macro_sauc and per-fold tables report the fold structure) | Y |
| E13 | data.py:19 | First cutoff | 2021-07-01 | number | N: none found for this date (README only says early folds are tiny, 2021-07 ~50 tried songs) | N: none found | Y |
| E14 | data.py:19, 24 | Last cutoff | 2024-10-01 (14 folds total) | number | P: selftest asserts first+90d <= DEV_END, and 2024-10 + 3 months + 90 d reaches 2025-04-01 exactly, so it is the last quarter that fits DEV_END | N | Y |
| E15 | data.py:160, 155 | Candidate window width: songs first played in [C, C+3 months) | 3 months (DateOffset) | number | N: none found (equal to the fold spacing) | N | Y |
| E16 | data.py:155-163 | Candidate definition: song never played before C and first played in the window ("tried" songs); songs first played earlier but "loved later" are not candidates; new_artist = primary artist unseen before C | definition | assumption | Y: README protocol | N | Y |
| E17 | data.py:20-21 | TUNE = first 10 folds, LATE = last 4 folds | 10 / 4 | number | Y: W3 plan item 1 (stated); LATE as a time-held-out slice | N: none found | Y (which folds the grade uses) |
| E18 | data.py:22-23 | HOLDOUT = artists with sha256(salt+id) % 100 < 25; artist -1 never | salt "w4-holdout|", 25 | number | Y: W4 plan "about 25%" (stated); selftest asserts overall tried share in 18-32%; realised 30.2% (W4 engineer-r1.md:27-28), salt not changed | N: one salt only | Y (removes ~30% of rows from TUNE/LATE) |
| E19 | data.py:24 | DEV_END; no dev stream/label on or after it | 2025-04-01 | number | Y: fixed by project rules (earlier design) | N | Y |
| E20 | data.py:25 | Sealed cutoffs | 5 quarterly cutoffs 2025-04..2026-04 | number | N: none found (mirrors the dev spacing) | N | N (sealed only) |
| E21 | data.py:147-151, 168 | Candidates need trackId in meta with name and popularity not null and not an "unknown" song; others dropped as "label-independent" | filter | assumption | Y: inline comment. W4 reviewer-code: dropped 107 of 2557 candidates (4.2%) with love rate about 0.1 vs 0.27, so "label-independent" is "slightly untrue" (read only) | N | Y (which songs are scored) |
| E22 | data.py:127-144 | Session = new session after gap > 30 min between consecutive plays (any song) | SESSION_GAP_MIN = 30 | number | Y: W3 plan (stated, no argument) | N: none found | Y (exposure_before drives wx, a co-headline graded metric; also ws, diagnostics, BREAKDOWN) |
| E23 | data.py:137-139 | exposure_before = count of distinct songs first played earlier in the same session; exposure_after = later; replays_s1; day1 (calendar day); d7 = plays in first 7 days | definitions; 7 days | both | Y: docstring; README plainly states exposure_after / replays can be consequences of liking | N: 7 days only | Y (wx metric, BREAKDOWN, diagnostic rows) |
| E24 | data.py:136 | week = ISO year*100 + ISO week of first play (within-week metric ww) | ISO week | assumption | N: none found | N | N (ww not graded) |
| E25 | data.py:81-93 | Meta record per track: first album as albumName, previewUrl = Spotify preview else Apple preview, durationMs etc. from top_tracks.json | choices of fields | assumption | N: none found | N | P (meta used by baselines/predictors) |
| E26 | data.py:83 | spotifyPopularity is a 2026 snapshot (look-ahead); missing treated as 0 in baselines and matching | fillna(0) | assumption | Y: README Known limitations ("mild look-ahead; 27% of user tracks have popularity 0") | N: none found | Y (popularity, meta_gbm, nonaudio_gbm) |
| E27 | data.py:12, 174-178 | Opaque id hash: sha1 of ID_SALT + id, first 13 hex digits | "evalkit-v2" | number | Y: comment (kept so per-track feature caches stay valid) | N | N |
| E28 | data.py:11 | DECOY_RATIO (decoys per tried song in open pool) | 5 | number | Y: comment "~20x the loved songs at a ~25% love rate" (stated) | N: none found | open only |
| E29 | data.py:201 | Decoy seed artists per fold: top-300 pre-cutoff artists by plays (all artistIds incl. featured), plus up to 6 stats.fm related artists of each of the top 150 | N_SEED 300, N_REL_SEEDS 150, N_REL 6 | number | Y: W3 plan states these numbers; selftest asserts seeds use pre-cutoff data only. No argument for the values | N | open only (and shapes who the decoys are) |
| E30 | data.py:202 | Stage-1 decoy pre-sample size | PRESAMPLE = 8 (x tried) | number | Y: comment (limits slow iTunes lookups) | N | open only |
| E31 | data.py:308-316 | Decoy eligibility: not played by user EVER (full history incl. sealed era), released before fold window end, a source artist in the fold's seed set, and (if fallback active) preview present or looked up | rule | assumption | Y: docstring; README says "Decoy = not tried, NOT would hate". W4 reviewer-code: preview presence differs between tried and decoys (read only) | N | open only |
| E32 | data.py:229 | Valid release timestamp window | 0 < ms < 4.1e12 | number | Y: comment "drop junk dates" | N | open only (release bucket) |
| E33 | data.py:259-263 | Tried-song release date = earliest known date over listed albums + stream album | rule | assumption | Y: docstring | N | open only (matching) |
| E34 | data.py:265-268 | Release-age bucket edges: <91 d, <365 d, <1096 d, else; unknown=4 | 91 / 365 / 1096 days | number | Y: W3 plan lists "<3 months, 3-12 months, 1-3 y, >3 y, unknown" (stated) | N | open only; BREAKDOWN |
| E35 | data.py:270-283 | Covariates for decoy matching: metadata shape, duration centred 240000 ms /60000, popularity/100, pairwise interactions, squares, release bucket crossings, popularity decile one-hot | feature list and constants | both | Y: docstring "v2.0 audit: classifier on metadata shape reached 0.73"; selftest shortcut AUC < .62 asserted (W3/W4: 0.570-0.603) | N: no alternative feature set | open only |
| E36 | data.py:297 | Matching logistic model | C=5.0, max_iter 3000, class_weight balanced | number | N: none found | N | open only |
| E37 | data.py:298-300 | Decoy draw weights = odds p/(1-p) of that model, p clipped to [1e-4, 1-1e-4], weights capped at the 99.5% quantile; Efraimidis-Spirakis sampling; seed = cutoff yyyymmdd (+1 for stage 2) | numbers | both | Y: docstring (re-weight universe to tried songs' feature distribution) | N | open only |
| E38 | data.py:334 | Decoys get love=0 ("not tried") in the open pool; all-decoy rows have is_decoy=1 | label 0 | assumption | Y: README / docstring | N | open only |
| E39 | data.py:345-355 | Preview fill: iTunes fallback applied to user tracks and decoys alike only if the fill is complete | rule | assumption | Y: README | N | open only |
| E40 | data.py:361-372 | Public view: rows shuffled with seed = cutoff yyyymmdd; meta.name overwritten with candidate title | seed rule | assumption | Y: comment (v2.0 name identified tried songs) | N | N |
| E41 | data.py:239-246 | Album-date fetch retries 4, timeout 40 s, 4 threads | numbers | number | N: none found | N | N |

## B. Baselines and references (baselines.py, refs.py)

| id | file:line | what | value | kind | R | V | Feeds |
|---|---|---|---|---|---|---|---|
| E42 | baselines.py:8, 36 | Recency half-life of artist plays (artist_recent, and nonaudio_gbm feature) | HL = 180 days | number | Y: W3 plan item 2 states "180-day half-life"; comment "crude taste-drift handling" | P: W3 builder-r1-training-signal.md:78-90 varies half-life (none .525, 180 d .557 ...) for that builder's own predictor, not the harness baseline | Y (artist_recent is a reference and best_ref candidate; nonaudio_gbm too) |
| E43 | baselines.py:9, 44 | Smoothing pseudo-count of artist love rate (K_SMOOTH and a separate literal k = 2.0 in artist_love_rate); prior = mean love of matured songs | 2.0 | number | N: none found | N | Y (baseline row; nonaudio_gbm feature) |
| E44 | baselines.py:41-42, 83, 136 | Maturity rule: only songs whose first play is before cutoff-90 d have labels | tied to horizon 90 | assumption | Y: comment | N | Y |
| E45 | baselines.py:22-28 | Artist plays count all artistIds incl. featured; track score = max over its artists | rule | assumption | N: none found | N | Y |
| E46 | baselines.py:47 | artist_love_rate tie-break term | 1e-3 * log1p(artist plays) | number | Y: comment "deterministic secondary key, not noise" | N | Y (baseline row) |
| E47 | baselines.py:92-94 | Title keyword flags | 13 keywords (live, remix, acoustic, remaster, version, edit, feat, intro, interlude, skit, instrumental, demo, mix), word-boundary regex on lowercased title | both | Y: W3 plan item 2 lists them (stated) | N | Y (meta_gbm, nonaudio_gbm) |
| E48 | baselines.py:96-102 | meta_gbm feature set: duration, explicit, popularity, preview present, #artists, title length, album==title, keyword flags | feature list | assumption | Y: W3 plan item 2(b) | N | Y |
| E49 | baselines.py:82-90 | nonaudio_gbm artist-history features: plays all-time, half-life plays, smoothed love rate (matured), #earlier songs, days since last play, featured-known, new-artist | feature list | assumption | Y: W3 plan item 2(c); called "THE reference that any music/content claim must beat" | N | Y |
| E50 | baselines.py:105 | GBM hyperparameters | max_iter 150, learning_rate 0.05, max_leaf_nodes 8, min_samples_leaf 40, l2 1.0, no early stopping, random_state 0 | number | N: none found for the specific values (W3 plan says "fixed params") | P: W3 builder-r1-training-signal.md:108 reports 60 iterations .636, 4 leaves .633, min_samples_leaf 80 .626, for that builder's own predictor, not the baseline | Y (4 reference/baseline rows) |
| E51 | baselines.py:106-109 | Monotone constraints on familiarity features (ap_all, ap_hl, love_rate, n_songs, feat_known +1; days_since, new_artist -1) | sign map | assumption | Y: comment: unconstrained GBM learned the reversed direction (TUNE sauc 0.46, below chance); W3 engineer-r1.md:36 | Y: the unconstrained version was the trial that was rejected (value 0.46 as stated in comment; not re-run by me) | Y |
| E52 | baselines.py:110, 141 | Training-row recency weight 0.5**(age/180 d) | WEIGHT_HL = 180 | number | Y: comment (confounding of counts with calendar time, same as artist_recent) | N: none found (None option exists in code) | Y |
| E53 | baselines.py:136-138, 144, 146 | GBM training rows: matured train songs with meta; prior fallback 0.25 when no matured songs; constant base-rate fallback when one class only | 0.25 | number | N: none found | N | Y (early folds) |
| E54 | baselines.py:17-19 | popularity baseline: popularity with missing as 0 | fillna(0) | assumption | N | N | Y |
| E55 | baselines.py:171-182 | Shortcut rows has_preview and preview_source_itunes | definitions | assumption | Y: README (carry no taste information; tried vs decoy preview asymmetry) | N | open only |
| E56 | baselines.py:181 | The seven VERDICT references: nonaudio_gbm, artist_recent, duration, meta_gbm, ref_audio_final, ref_w4r1_listening, ref_w4r1_music | list | assumption | Y: README v4/v4.1 text (earlier workflows' finals added as references) | N | Y (grade is relative to best_ref) |
| E57 | baselines.py:182 | DIAGNOSTIC rows (siblings, exposure_*, replays, oracle_day1, oracle_7d) | list | assumption | Y: README | N | N (not graded) |
| E58 | refs.py:18-22 | Which earlier predictors are references and which PREDICTORS key: audio_final, w4r1_final, final_content | mapping | assumption | Y: README v4.1 item 6 | N | Y (best_ref and deltas) |
| E59 | refs.py:64-69 | Cutoff inference when not given: first dev or sealed cutoff after last train stream | rule | assumption | Y: docstring | N | N |

## C. Metrics and bootstrap (metrics.py)

| id | file:line | what | value | kind | R | V | Feeds |
|---|---|---|---|---|---|---|---|
| E60 | metrics.py:8-12 | AUC with ties counted half (average ranks) | convention | assumption | Y: docstring | N | Y |
| E61 | metrics.py:17-28 | fold_metrics: top fraction for p10/hits 10%, r20 20%, p20 top 20 songs, nseeds=20 random tie-breaks, folds with n<10 dropped | .1, .2, 20, 20 | number | Y: W3 plan "average over 20 random tie-break seeds"; selftest compares to the weighted engine | N | N (secondary: AP, lift, r20, p10, p20; p20 is in open tables) |
| E62 | metrics.py:57-59 | exposure_before bucket edges for wx_sauc and BREAKDOWN | 0 / 1-2 / 3-8 / 9+ | number | Y: W4 plan item states them; W4 engineer-r1.md:80 reports love rate falls 0.43/0.32/0.20/0.11 across them. Edges not derived | N: none found | Y (wx is a graded co-headline) |
| E63 | metrics.py:65-72 | macro_sauc includes folds with at least 10 loved and 10 not-loved (unweighted counts) | min_each = 10 | number | Y: W4 plan item 3a states it | N | Y (macro reported, not graded) |
| E64 | metrics.py:38-55, 61-63 | Headline sauc pools all within-fold (loved, not-loved) pairs; each fold weighs by n1*n0 | pooling rule | assumption | Y: README; W4 reviewer-code B3 notes 2 of 10 TUNE folds carry 68% of pair weight and five early folds 3.2% (read only) | P: macro_sauc, per-fold AUC table and BREAKDOWN by fold are alternatives printed alongside | Y |
| E65 | metrics.py:111, run.py:755 | Bootstrap unit and size: resample primary artists globally (one multinomial draw over all artists of a slice, shared by all rows and folds), pair weight = product of draw counts; nboot 100 (fast) / 300 (full); seeds 1000*(slice index+1), +1 for open pool | cluster = primary artist; 100/300 | both | Y: README v4 (global clusters replace (fold, artist) clusters); W4 reviewer-code B3 says the old per-fold clusters were somewhat too narrow | P: v3 (fold, artist) vs v4 global is a change, not a tested sensitivity; nboot 100 vs 300 never compared in docs I read | Y (all CIs, P(d>0), grades) |
| E66 | metrics.py:108-110 | Within-group metrics: wa = same fold and primary artist; ww = same fold and ISO week; ws = same fold and session; wx = same fold and exposure bucket | groupings | assumption | Y: README | N | Y (wa, wx graded; ww/ws not) |
| E67 | metrics.py:137-163 | gc / gc_wa: all within-group pairs with differing plays90 (ties excluded, score ties 0.5) | definition | assumption | Y: README ("uses all the information in plays90, less sensitive to the love threshold") | N | Y (gc graded) |
| E68 | metrics.py:164-172, run.py:365 | Per-fold CI alpha .05; BELOW CHANCE flag when upper bound < 0.5 | 0.05, 0.5 | number | N: none found | N | N |
| E69 | metrics.py:180 | permutation band: 200 permutations, seed 0, fixed uniform random score, 2.5-97.5 percentiles, rounded 3 | 200, 95% | number | Y: W3 engineer-r1.md:43 / engineer-r2.md:15 (stated). W4 reviewer-code: the selftest checks tolerance +-0.05 | N: selftest uses 60-permutation run | N (band printed; PASS/FLAG uses cluster_band) |
| E70 | metrics.py:218-237 | artist_blocks rule: within a fold artists with equal numbers of tried rows are swapped as blocks; unique counts merged with the nearest count (smaller on tie), chains allowed, merged blocks shuffled at row level | rule | assumption | Y: W4 research-lead-review.md:86; selftest: artist-constant random scorer passes cluster band 10/10 vs 1/10 song-level | N | Y (null control label) |
| E71 | metrics.py:245 | cluster_band: 300 block permutations, seed 0, 2.5-97.5 percentiles | 300, 95% | number | Y: W4 review (stated) | N | Y (PASS/FLAG) |

## D. Run harness, grading, null control, caps (run.py)

| id | file:line | what | value | kind | R | V | Feeds |
|---|---|---|---|---|---|---|---|
| E72 | run.py:108 | keep label: plays in days [90, 365) after first play >= 6 | 6 / 90 / 365 | number | Y: README ("keep"); W4 RESULTS: love predicts keep, AUC 0.85 | N: keep thresholds not varied | N (variant table only) |
| E73 | run.py:110-112 | keep computed only where window end + 365 d < DEV_END | rule | assumption | Y: docstring | N | N |
| E74 | run.py:101-106 | Tercile edges of total plays in the 90-day window (plays90/share90), over all tried songs of 14 dev folds incl. HOLDOUT | quantiles 1/3, 2/3 | number | Y: docstring | N | N (BREAKDOWN) |
| E75 | run.py:147 | Preview source rule: spotify iff manifest source == spotify else itunes; defines the open-pool PRIMARY subset | rule | assumption | Y: README (preview presence differs for tried songs and decoys) | N | open only (primary open metrics) |
| E76 | run.py:171-206, 755 | Independence check: indep_n = 8 random candidates re-scored alone (0 in fast mode), rng seed 7, statistic = p90 of |change|/std | 8, seed 7, p90 | number | N: none found for 8; selftest requires p90 < .01 for baselines | N | N (gate) |
| E77 | run.py:231 | Interval level: two-sided 95% (2.5-97.5 percentiles), alpha = 0.05 / n_looks (n_looks 1 in dev) | 95% | number | Y: README. W4 reviewer-code notes the "95% lower bound" wording is a 97.5% one-sided bound | N | Y (STRONG grade, lower-bound columns) |
| E78 | run.py:256-264 | Paired delta statistics: P(d>0) = share of finite resamples with d>0; 80% interval = 10th-90th percentile | 80% | number | Y: README ("80% interval"; W3 RESULTS graded evidence) | N | Y (SUGGESTIVE grade uses P) |
| E79 | run.py:441-462 | Evidence grade rule: STRONG = ALL-slice 95% lower bound > 0 and point delta > 0 on both TUNE and LATE; SUGGESTIVE = P(d>0) >= 0.8 on both TUNE and LATE; else NONE | 0.95 / 0.8 | number | Y: README ("strict lower-bound gating judged possibly too strong for a subjective target"; sealed run keeps strict gate) | N: none found | Y (grade) |
| E80 | run.py:26 | Graded metrics list: sauc, wx, new-artist sauc, wa, gc (not macro, ww, ws, open metrics) | list | assumption | Y: README v4.1 item 3 | N | Y |
| E81 | run.py:487-494 | best_ref = reference with highest TUNE point sauc (non-HOLDOUT), fixed once and applied to every slice | rule | assumption | Y: README | N | Y (all evidence deltas) |
| E82 | run.py:397 | best_meta for "dWA vs best meta" chosen by slice point wa among duration, meta_gbm, nonaudio_gbm | rule | assumption | Y: README | N | N (extra column) |
| E83 | run.py:417 | label_consistency tolerance: love_4_2, love_10_4, strong each >= love - 0.03 | 0.03 | number | Y: W3 plan item ("reported, not gated") | N | N |
| E84 | run.py:249-251 | SUSPECT CONSTANT SCORES when more than 50% of a fold's scores tie | 0.5 | number | N: none found | N | N |
| E85 | run.py:281-282 | Open-pool primary subset (Spotify-sourced previews for tried and decoys) and within-artist open metric | rule | assumption | Y: README | N | open only |
| E86 | run.py:20-21, 534 | Caps: --late 2 runs per hash; --holdout 1 run per hash; holdout budget file initial 2 (now 0) | 2 / 1 / 2 | number | Y: README (design of seen-once slices) | N | N (access control) |
| E87 | run.py:545 | Fingerprint refusal threshold Spearman >= 0.999 on first fold | 0.999 | number | N: none found | N | N |
| E88 | run.py:584, 601-606 (see also 756) | Null control: default 5 seeds (v3 used 3), seed = cutoff yyyymmdd + k, each seed in a fresh process; null nboot = min(nboot,100) | 5, 100 | number | Y: W4 research-lead-review.md:44 (stated); W3 plan used 3 seeds | P: 3-seed (v3) vs 5-seed (v4.1); labels not comparable (README) | N for scores; Y for PASS/FLAG |
| E89 | run.py:35-54 | Null construction: song identity shuffle across train songs keeping timestamps, plus random bijection over all artist ids and album ids of train U cands applied to train only | design | assumption | Y: docstring; README | Y: identity-only version kept as --null-control-identity diagnostic | N for scores; Y for PASS/FLAG |
| E90 | run.py:608-622 | Null statistic: per-seed within-fold rank / fold size, averaged across seeds, sauc / wa / new-artist sauc inside 2.5-97.5 cluster band; PASS only if all three inside | rule, 95% | both | Y: README (cluster-aware band, old song-level band too narrow for feature models) | Y: old song-level label printed alongside (4 of 7 baselines FLAGged vs 1 under new band, README); selftest 10-dummy-run check | N for scores; Y for PASS/FLAG |
| E91 | run.py:697 | Walk-forward eligibility: earlier folds with >= 10 loved and >= 10 not-loved; selects highest pooled sauc; ties/fold 1 use the first listed member | 10 | number | Y: W4 research-lead-review.md:75 | N | N (composite reported) |
| E92 | run.py:28 | LABEL_VARIANTS list | love, strong, love_4_2, love_10_4, keep | assumption | Y: README | N | N |
| E93 | run.py:344-346 | Spearman summaries: days90, log1p(plays90), share90, mean of per-fold Spearman | choices | assumption | Y: README | N | N |
| E94 | run.py:90-93 | pool digest columns used by selftest | list | assumption | Y: comment | N | N |
| E95 | run.py:23, 26 | REF = ref_audio_final as default reference name | name | assumption | Y: README | N | N |
| E96 | run.py (grading text in README:102) | Dev threshold rule: dev decisions graded on P(d>0) >= 0.8 and 95% lower bound, strict gate kept for sealed | see E79 | assumption | Y: README | N | Y |
| E97 | run.py:769-771 | Slice composition: TUNE alone unless --late/--holdout; LATE and ALL printed separately; DEV+HOLDOUT pooled | rule | assumption | Y: README | N | Y (which folds a grade sees) |
| E98 | run.py:164-166, 827-829 | Reference scores cached per (code hash, bundle, cutoff, slice part): references scored once, not re-fitted per run | cache | assumption | Y: README | N | N |
| E99 | run.py:853 | Bootstrap seeds per slice 1000*(index+1); Block seed+1 for open pool | seeds | number | N | N | N (resample draws) |

## E. Other modules (ablate, describe, fetch_*, make_*, bundle, selftest)

| id | file:line | what | value | kind | R | V | Feeds |
|---|---|---|---|---|---|---|---|
| E100 | ablate.py:20 | History windows | 730 d, 365 d, random subsample "sub365" matched to streams of last-365-day songs | number | Y: docstring (sample-size control) | Y: the ablation is itself a variation tool; not exercised by selftest (README); W4 reviewer-code B5 (pre-v4 truncation flaw, read only) | Y only if --window used |
| E101 | describe.py:12, 37 | Wilson z = 1.96; bootstrap 300; "replays 1 vs 2+" split | numbers | number | N | N | N |
| E102 | fetch_itunes.py:34 | Preview-less decoys looked up | N_DECOY_LOOKUPS = 250, rng seed 0, seeded sample | number | Y: comment (rate limit ~15/min); W4 reviewer-code: causes tried/decoy preview asymmetry (read only) | N | open only |
| E103 | fetch_itunes.py:23-32, 61 | iTunes acceptance: normalised title match, primary artist match (parts split on & , feat x and with), |duration diff| <= 5000 ms, query without bracket text, limit 10 results | 5 s, 10 | number | Y: README states the 5 s rule; no justification of 5 s | N | open only (preview values; also user tracks) |
| E104 | fetch_itunes.py:55-77 | Rate-limit handling: delay start 3.0 s, +0.5 on 403, cap 12, floor 2.2, retries 12, sleep 20 s | numbers | number | Y: comment (403 after ~20 requests/min) | N | N |
| E105 | fetch_previews.py:18-19, 45-46, 60 | Source classification scdn.co = spotify else itunes; ok iff >= 1000 bytes and ffprobe duration > 1 s; retries 3; threads <= 6 | numbers | both | N for thresholds | N | open only (primary subset) |
| E106 | make_decoys.py:36, 17, 31 | stats.fm /tracks limit 200 per artist; only tracks with a dated album and artists kept; 4 tries, sleep 0.1 | 200 | number | Y: README ("at most 200 tracks per artist" API cap) | N | open only (decoy universe) |
| E107 | make_decoys.py:63 | Decoy albumId = first listed album | rule | assumption | N | N | N |
| E108 | bundle.py:13, 64 | Bundle hash path regexes, probe timeout 600 s | numbers | number | Y: docstring | N | N |
| E109 | selftest.py (assert lines 79, 106, 115, 124, 154) | Tolerances: HOLDOUT tried share 18-32%; random AUC within 0.5+-0.05; 7-day oracle > 0.85; baseline independence p90 < 0.01; tried-vs-decoy shortcut AUC < 0.62 | numbers | number | Y: stated in asserts (v2.0 shortcut was 0.73) | N | N |
| E110 | pool_reference.json, sealed_manifest.json | Digests of 14 dev pools and sealed labels | hashes | assumption | Y: README | N | N |

## F. Structural assumptions not tied to one line

| id | file:line | what | value | kind | R | V | Feeds |
|---|---|---|---|---|---|---|---|
| E111 | README Protocol; run.py prepare_folds | Primary target is love versus tried-but-not-loved among songs the user chose to try (tried pool); the open pool with decoys is secondary | design | assumption | Y: README | P: open-pool tables printed alongside | Y |
| E112 | data.py:42; run.py:141-143 | HOLDOUT rows removed from cands/pools/meta of normal runs but their pre-cutoff history stays in train; HOLDOUT is artist-disjoint, not time-disjoint | design | assumption | Y: README Known limitations | N | Y |
| E113 | README Metrics | Primary headline = pooled stratified AUC (sauc) with global artist bootstrap; wx, new-artist sauc, wa, gc as co-grades; macro not graded | choice of headlines | assumption | Y: README v4/v4.1; W4 RESULTS lists scores | N | Y |
| E114 | README, data.py:163 | new_artist defined by primary artist only (featured artists ignored) | rule | assumption | N | N | Y (new-artist sauc is graded) |
| E115 | data.py:96-110 | Train for a cutoff = all streams before C, so train-song labels near C come from truncated horizons (baselines filter, other code may not) | rule | assumption | Y: comment in artist_love_rate | N | P |
| E116 | README Folds, W4 RESULTS | The fold set as a whole (14 quarterly cutoffs, 10/4 split, pooled pair weighting) is the sampling frame; follow-up question "is the set of folds arbitrary": the docs I read state the spacing and dates without derivation (E12-E15, E17); the only documented look at fold structure is macro_sauc / per-fold tables and W4 reviewer-code B3 weights | structure | assumption | N | P: macro_sauc, per-fold AUC, BREAKDOWN by fold | Y |

## Summary notes (facts)
- Rows with a documented reason are mostly "stated in the plan/README" rather than argued from data.
- Variations found are: label definitions (E07-E10, E72), unconstrained vs constrained GBM (E51, comment), null-control seed count and band type (E88-E90), bootstrap clustering change (E65), baseline-hyperparameter-like variants only inside builders' own predictors (E42, E50).
- Nothing found varying: fold spacing/start/end/window width, HOLDOUT salt and percentage, session gap, exposure bucket edges, HORIZON_DAYS, DECOY_RATIO and seed counts, iTunes 5 s rule, grade thresholds 0.8 / 95%, nboot.
