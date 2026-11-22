# Inventory: Workflow 4 round-1 predictors (w4r1-*)

Area: /home/user/Listener/taste-model/predictors/w4r1-taste-from-all-listening/ (TAFL) and /home/user/Listener/taste-model/predictors/w4r1-what-in-the-music/ (WITM). Files read: every .py in both folders (build_compact.py, predict.py, predict_secondary.py; build_compact.py, build_desc.py, predict.py, analyze_*.py, artist_*.py, taste_drift.py), builder/DA reports for both models and shared-prep-r1 and w3 RESULTS in the sanitised folders, evalkit/data.py constants. Nothing was run; no experiments. (Only `grep` on evalkit/data.py and README for HORIZON_DAYS and the love definition.)

Abbreviations. "Feeds" = whether the choice feeds the final reported scores directly (Y = the predictor scores; N = diagnostic/analysis script only; Y(var) = only the named variant). Paths: TAFL = predictors/w4r1-taste-from-all-listening, WITM = predictors/w4r1-what-in-the-music. Report names: B-T = builder-r1-taste-from-all-listening.md, B-W = builder-r1-what-in-the-music.md, DA-T-w / DA-T-d = devils-advocate-r1-taste-from-all-listening works/dismissed, DA-W-w / DA-W-d = devils-advocate-r1-what-in-the-music works/dismissed, W3 = w3-sanitised/RESULTS.md. "Fast TUNE" numbers are pooled AUC on the TUNE slice (dev, not held-out) as reported there. No held-out (LATE/HOLDOUT) numbers are quoted in this inventory.

Notes on what was not covered: the Workflow 3 file predictors/w3r2-audio-taste/predict.py (WITM's MERT member, `audio_final`, loaded at WITM/predict.py:126) and the shared caches' own construction (MERT extraction, essentia models, previews) are outside this area, so only the point where the w4r1 code consumes them is listed. Gaps in evidence are marked "none found".

## Table

| id | file:line | what | value | kind | reason / evidence found | variation or test found | feeds final |
|---|---|---|---|---|---|---|---|
| T01 | TAFL/build_compact.py:9 | MERT layers kept and combined | layers 4-8 (slice 4:9) averaged, per window | number | none found in code or reports (shared cache holds all layers; choice not justified) | B-T "other MERT layer groups (.618-.643)" fast TUNE, no per-group numbers; DA-T-d did not vary layers | Y (all TAFL members) |
| T02 | TAFL/build_compact.py:9 | Use of 4 time windows per clip | 4 windows (shape [N,4,768]) | assumption | inherited from the frozen W3 MERT cache (W3: "four 5-second moments of each preview"); no reason for 4 given | B-T mode local (4 rows) vs whole (window mean) both used as members; W3 "modelling the moments separately added 0.00-0.01"; no other window count possible | Y |
| T03 | TAFL/build_compact.py:9 | Layer aggregation is an unweighted mean, done in float32 then stored float16 | mean, f16 | assumption | none found | none found | Y |
| T04 | TAFL/build_compact.py:18 | Storage precision for all blocks | float16 | assumption | size (compact.npz 160 MB per B-T) | none found | Y (rounding) |
| T05 | TAFL/build_compact.py:16,18 | Missing clips filled with zeros plus has_* mask | zeros + mask | assumption | none found | none found | Y |
| T06 | TAFL/build_compact.py:9,11,13 | Which feature blocks are stored (MERT, CLAP, essentia act, essentia emb); only MERT is used by predict.py | 4 blocks, 1 used | assumption | B-T: CLAP/essentia/lyrics tried only as plain additions | B-T "extra CLAP/essentia/lyrics blocks .611-.648"; DA-T-d per-block scale g .5/1 on CLAP and essentia: .596-.627, time-resolved essentia .628/.629 (all vs MERT panel .627) | Y (excluded) |
| T07 | TAFL/predict.py:27 | CFG default ncomp (PCA components) | 64 | number | none found for 64 specifically; B-T lists 32, 64, 128, 256 tried | B-T panel: 128 comps .651, 256 .642-.644, 32 .632 (fast TUNE, full ensemble); sec_cap varies by n | Y |
| T08 | TAFL/predict.py:27 | CFG default ridge alpha | 300.0 | number | none found | B-T alpha tried inside the ~20 panel settings (values not itemised); DA-T-w sens.py alpha x2/x0.5 neighbours .633-.652 (config-level, not per alpha) | Y |
| T09 | TAFL/predict.py:27 | Default signal type | "panel" | assumption | B-T: whole-record idea is the workflow question | newonly vs panelonly vs final ablations (B-T): newonly .630, panelonly .627, final .651; joint signal in one ridge .645 | Y |
| T10 | TAFL/predict.py:27,52 | Panel K: number of 91-day periods | 2 | number | B-T: "K=2 with min plays 2 is a TUNE selection (optimism)" | B-T ~20 panel settings; DA-T-d: K1 .620, K2 .627, K4 .610, K8 .601, P45K4 .639, P60K2 .620, P30K6 .618, full-ensemble fin_p45k4 .658, fin_p60k3 .650 vs control .651; DA-T-w sens.py neighbours .633-.652, random configs .623-.649 | Y |
| T11 | TAFL/predict.py:27,53 | Panel period length P | 91 days (about one quarter) | number | none found beyond convention (aligns with quarter rank of W3 recipe); B-T lists P among tuned settings | DA-T-d: P182 .588, P45, P60, P30 as above | Y |
| T12 | TAFL/predict.py:27,58 | Recency half-life for panel weight | 180 days | number | W3: "recent history (last 180-365 days) beat using everything" | B-T lists half-life among ~20 panel settings (no numbers); DA-T-w sens.py varied half-life (grouped result .633-.652) | Y |
| T13 | TAFL/predict.py:27,63 | newhl (half-life for "new" signal) | None (off) | number | none found | B-T / DA-T-w ens.py recency-weighted new variant .625 vs .629 unweighted | Y (off) |
| T14 | TAFL/predict.py:27,56 | minplays threshold for panel songs | 2 | number | B-T: "K=2 with min plays 2 is a TUNE selection" | DA-T-d: min_plays 1/5 -> .607/.577 | Y |
| T15 | TAFL/predict.py:27 | mode default | "whole" (window mean) | assumption | none found | members use both whole and local (E); no comparison of the modes alone found | Y |
| T16 | TAFL/predict.py:27,112 | member wt default | 1.0 (equal member weights) | number | none found | none found | Y |
| T17 | TAFL/predict.py:27 | noart default | False | assumption | design: noart is a diagnostic variant | final vs final_noart reported (.651 vs .617 TUNE) | N (diagnostic variants) |
| T18 | TAFL/predict.py:41,73,75 | Whole mode: mean of 4 windows before PCA | window mean | assumption | none found | local vs whole members | Y |
| T19 | TAFL/predict.py:73-75 | Standardisation of features: per-dimension mean/std with epsilon | sd + 1e-6 | assumption/number | none found | none found | Y |
| T20 | TAFL/predict.py:75 | PCA whitened | whiten=True | assumption | none found | none found (DA-W/B-W tested PCA64-whitened for essentia only: .558 vs .604 at alpha 300) | Y |
| T21 | TAFL/predict.py:75 | PCA seed | random_state=0 | number | convention | none found | Y |
| T22 | TAFL/predict.py:75 | PCA fit population: all train-stream songs with audio in meta (not just rows with a signal) | all audio songs | assumption | B-T: "PCA fit on train-stream songs only"; reviewer-code found no pool/decoy fits | none found | Y |
| T23 | TAFL/predict.py:75 | PCA components capped at has.sum()-1 | min(ncomp, n-1) | assumption | numerical guard | sec_cap varies component count by n (T58) | Y |
| T24 | TAFL/predict.py:73 | Local mode: PCA fit on all windows pooled (rows = windows) | pooled windows | assumption | none found | none found | Y (E members) |
| T25 | TAFL/predict.py:70 | Songs restricted to those with trackId in meta | filter | assumption | needed for preview lookup | none found | Y |
| T26 | TAFL/predict.py:32 | Preview identity key: md5 of previewUrl | md5(url) | assumption | matches shared cache keys | none found | Y |
| T27 | TAFL/predict.py:33 | Songs with non-finite or missing MERT get has=False, features zeroed | zero block | assumption | none found | none found | Y |
| T28 | TAFL/predict.py:77 | Training rows kept: has audio and W>0 | keep mask | assumption | none found | "unplayed active songs as zero rows" tried, .584 (B-T) | Y |
| T29 | TAFL/predict.py:61 | "new" signal: maturity cutoff for first play | 90 days before cutoff (also HORIZON_DAYS=90 in evalkit/data.py:15) | number | W3 recipe; harness label horizon 90 d | none found in TAFL; WITM varies nothing either (see W07) | Y |
| T30 | TAFL/predict.py:61-62 | "new" target: percentile rank of plays90 within quarter of first play, per-quarter groups | pct rank by calendar quarter (to_period("Q")) | assumption | W3: graded targets beat yes/no; "play count ranked within its quarter" best (+0.02 to +0.04, suggestive) | log-count target .598 (B-T); love label .570 / share90 .576 in WITM (B-W); no other grouping window than quarter found | Y |
| T31 | TAFL/predict.py:64 | pandas rank(pct=True) tie handling (average) and 0 target for unselected rows (masked by W) | average ties | assumption | none found | none found | Y |
| T32 | TAFL/predict.py:57 | Panel: skip a period if fewer than 20 songs qualify | 20 | number | none found | none found | Y |
| T33 | TAFL/predict.py:53 | Panel periods are consecutive non-overlapping blocks ending at the cutoff | e=cutoff-P*k | assumption | none found | DA-T-w stale.py shifted panel back 180/365 d: .593/.595 vs .630 newonly | Y |
| T34 | TAFL/predict.py:57-58 | Panel target: percentile rank of play counts among songs with >=minplays in the period; play counts (not distinct days or time spent) | count-based | assumption | W3 target choice | log-count target .598; retention signal .589; none for distinct-days | Y |
| T35 | TAFL/predict.py:58 | Panel weight: 0.5**(P*(k+0.5)/hl), mid-period age | exponent mid-point | assumption | none found | hl varied (T12) | Y |
| T36 | TAFL/predict.py:58,59 | Songs of all ages (old or new) pooled in panel; Y summed over periods and weights normalised | additive | assumption | B-T design | joint signal .645 | Y |
| T37 | TAFL/predict.py:78 | Row weights normalised to mean 1 | ws = W*len/sum | assumption | convention | none found | Y |
| T38 | TAFL/predict.py:80 | Ridge penalty identity, intercept effectively unpenalised | reg[-1,-1]=1e-6 | number | convention | none found | Y |
| T39 | TAFL/predict.py:80 | Ridge solved with uniform alpha on whitened PCs (alpha scaled to weights summing to n rows) | alpha as in members | assumption | none found | alpha varied as T08 | Y |
| T40 | TAFL/predict.py:86 | Score standardisation by mean/std of member's own training-row scores | mean, std+1e-9 | assumption/number | design | none found | Y |
| T41 | TAFL/predict.py:105 | Missing audio -> neutral score 0 | 0.0 | assumption | B-T: "ties in the middle"; preview-absent row AUC 0.500 by construction | none found; DA-T-w "restricted to preview-present rows" final .663 vs ref .640 | Y |
| T42 | TAFL/predict.py:112 | Ensemble: weighted mean of member scores, equal weights | wt 1.0 each | assumption | none found | DA-T-w ens.py: 4-member new-signal-only ensemble .629 | Y |
| T43 | TAFL/predict.py:115 | Member E (local mode) alpha | 1200.0 | number | none found; "W3-style" | none found for 1200 specifically | Y |
| T44 | TAFL/predict.py:115 | Member W32 ncomp and alpha | ncomp 32, alpha 150.0 | number | none found; "W3-style" | none found for this member alone | Y |
| T45 | TAFL/predict.py:116 | NEW members: E-new (local, alpha 1200, ncomp 64) and W32-new (whole, 32, 150) | 2 members | assumption | B-T: W3 recipe re-implemented gave .630 | w3like_new .630/.615/.600 vs newonly .630 | Y |
| T46 | TAFL/predict.py:117 | PAN members: local ncomp 128 alpha 2400 and whole ncomp 64 alpha 300 | 128/2400, 64/300 | number | B-T: "Panel with 128 components .651 / .629 / .667 (chosen)" | 32/128/256 comps; DA-T-d neighbours; DA-T-w 10 neighbours + 7 random configs: .633-.652 and .623-.649, declared .651 top | Y |
| T47 | TAFL/predict.py:120 | Final composition: 2 NEW + 2 PAN members, equal weights | 4 members | assumption | declared before first --late run (DECLARATION 13:33:08Z per DA-T-d) | newonly/panelonly/final ablations | Y |
| T48 | TAFL/predict.py:84-85,104 | noart: exact leave-own-artist-out via sufficient statistics, PCA not refit, primary artist only | design | assumption | diagnostic; DA-T-w confirmed it removes only own primary artist id | n/a | N (final_noart variants) |
| T49 | TAFL/predict.py:92-94 | Fit cache key and EVALKIT_NO_FIT_CACHE bypass | key (cutoff, hashes) | assumption | fix for the W3 cache bug (W4 results section 2) | DA-T-w verified nulls vary across seeds | N (does not alter scores if key is right) |
| T50 | TAFL/predict.py:106 | Candidate score standardised then averaged over 4 windows in local mode (window scores mean before standardising) | mean of windows | assumption | none found | none found | Y |
| T51 | TAFL/predict_secondary.py:12-15,32 | History term window | 180 days | number | W3: "recent history (last 180-365 days) beat using everything" | only 180 tried; DA-T-d own probe with learned slope instead of hand weight | N (secondary, not primary) |
| T52 | TAFL/predict_secondary.py:15 | History transform log1p of artist plays | log1p | assumption | none found | none found | N (secondary) |
| T53 | TAFL/predict_secondary.py:33 | History weight w | 0.3 and 1.0 | number | none found ("two fixed hand weights" per DA-T-d) | both reported; DA-T-d notes no other weights or time-varying use | N (secondary) |
| T54 | TAFL/predict_secondary.py:21 | History term added to unit-scale content score unnormalised ("h / 1.0") | raw h, divisor 1.0 | assumption | comment says "unit-ish scale"; h not z-scored although `_z` is defined (unused, line 9) | none found | N (secondary) |
| T55 | TAFL/predict_secondary.py:9-10 | Helper `_z` defined, not used | 1e-9 epsilon | assumption | none | n/a | N |
| T56 | TAFL/predict_secondary.py:29 | sec_cap: PAN[0] components = min(128, max(16, n//6)) | divisor 6, floor 16 | number | B-T: "a fix for the sparse early folds that hurt the declared model"; chosen after TUNE and HOLDOUT seen (post-hoc) | one test: no improvement (.651/.652 vs final .651/.652) | N (secondary) |
| T57 | TAFL/predict_secondary.py:29 | sec_cap: PAN[1] components = min(64, max(16, n//12)) | divisor 12, floor 16 | number | as T56 | as T56 | N (secondary) |
| T58 | TAFL/predict_secondary.py:28 | n = number of songs in train (song_table size), not number of panel songs | n=len(song_table) | assumption | comment says "n = songs in train streams" though the docstring says "number of panel songs" | none found | N (secondary) |
| W01 | WITM/build_compact.py:10 | Segment length for time-resolved features | 5.0 s | number | none found (matches 5-s moments of W3 MERT windows by convention) | per-segment results in B-W; no other length tried | Y (SL member) |
| W02 | WITM/build_compact.py:10 | Number of segments, last one absorbs overflow | min(int(t/5),5) -> 6 segments | number | 30-s preview / 5 s | none found | Y |
| W03 | WITM/build_compact.py:10 | Patch to segment assignment by patch centre time | uses patch_t | assumption | none found | none found | Y |
| W04 | WITM/build_compact.py:14,16 | Empty segment -> NaN, storage float16 | NaN, f16 | assumption | none found | none found | Y |
| W05 | WITM/build_compact.py:8 | Clip statistics kept: act_mean, act_max, emb_mean, emb_std from shard (computed upstream in shared prep) | 4 blocks | assumption | none found | act_max tried (.564), emb std (.567-.595) in B-W | Y (act_mean only in final) |
| W06 | WITM/predict.py:9,16 | COMPACT cache path and auto-regeneration | path | assumption | housekeeping | n/a | N |
| W07 | WITM/predict.py:10 (cfg "mature") | Maturity cutoff for training songs | 90 days | number | = HORIZON_DAYS 90 | none found | Y |
| W08 | WITM/predict.py:10 | Default feat | "act" (essentia head activations, 605 columns) | assumption | B-W question | feat variants (emb, seg, actmax, embstd, meta, desc) tested | Y |
| W09 | WITM/predict.py:10,32 | Activation transform logit with clip | logit, clip 1e-4..1-1e-4 | number | none found | B-W: raw instead of logit .561 vs .578 (alpha 300) | Y |
| W10 | WITM/predict.py:10 | Default alpha | 300.0 (overridden to 1e4 in final) | number | n/a | alpha 100/300/1e3/3e3/1e4/3e4 = .571/.578/.590/.604/.611/.606 (B-W, fast TUNE) | Y (via override) |
| W11 | WITM/predict.py:139 | Final alpha for essentia ridge members A and SL | 1e4 | number | B-W: "Clearly better with strong regularisation (alpha 1e4 is what I picked and declared)" (peak of grid) | grid in W10 | Y |
| W12 | WITM/predict.py:10,87 | Target default | rank_plays (pct-rank of plays90 within quarter of first play) | assumption | W3 (graded, volume-normalised target) | love .570, share90 .576 (alpha 300) vs .578 | Y |
| W13 | WITM/predict.py:84,87 | Quarter grouping | calendar quarter | assumption | W3 | none found | Y |
| W14 | WITM/predict.py:10,90 | hl default None (no recency weight) | None | number | none found | B-W: half-lives 730/365 d .607/.601 vs .611 (flat) | Y (off) |
| W15 | WITM/predict.py:89 | Uniform sample weights | 1 | assumption | none found | hl (W14) | Y |
| W16 | WITM/predict.py:10,78-79 | ncomp default 0 (no PCA) | 0 | number | none found | PCA64 whitened .558, PCA8 + ridge .612, GBM on PCA40 .589 (B-W) | Y (off) |
| W17 | WITM/predict.py:78 | Standardiser sd epsilon | 1e-6 | number | convention | none found | Y |
| W18 | WITM/predict.py:91 | Min mature songs to fit | >20 | number | guard | none found | Y |
| W19 | WITM/predict.py:94 | Logistic regression for love target: C = 1/alpha, max_iter 300 | 1/alpha, 300 | number | none found | love target .570 (B-W) | N (love-target variant only) |
| W20 | WITM/predict.py:98 | GBM hyperparameters | max_iter 80, lr 0.05, depth 3, min_samples_leaf 30, l2 5.0, seed 0 | number | none found | none found (B-W: "tuning was only coarse: alpha, a handful of blend weights, one segment subset"); GBM on PCA40 .589 for another feature set | Y (DUR member) |
| W21 | WITM/predict.py:138 | DUR member: meta features only, GBM learner | feat meta | assumption | duration within-artist signal (harness duration baseline wa .645 on TUNE) | DA-W: duration does not transfer to HOLDOUT; abl_no_dur .639 vs .646 TUNE | Y |
| W22 | WITM/predict.py:58 | Meta columns: log1p(duration s), explicit, popularity/100, popularity==0 flag; NaN filled with 0 | 4 columns | assumption | none found | none found; "descriptors+metadata GBM .596 / duration GBM alone .559" (B-W) | Y |
| W23 | WITM/predict.py:63,82 | Meta standardisation only used when cfg meta True (never in final) | n/a | assumption | n/a | n/a | N |
| W24 | WITM/predict.py:54,53 | seg features: NaN segment filled with the row's mean of other segments, else 0 | nanmean fill | assumption | none found | none found | Y (SL) |
| W25 | WITM/predict.py:52 | Rows with non-finite features considered "ok" for seg regardless | ok &= isfinite or seg | assumption | none found | none found | Y (SL) |
| W26 | WITM/predict.py:140 | SL segments used | (3,4,5) = 15-30 s of clip | number | B-W per-segment fast TUNE: seg0 .576, seg1 .567, seg2 .578, seg3 .611, seg4 .605, seg5 .593; first half .578 vs second .612 (P .93, lo -0.005) | those tests; chosen after seeing them on TUNE ("one segment subset" tried), all in-sample | Y |
| W27 | WITM/predict.py:140,99 | SL fit: one row per segment, target repeated; score = mean over segments (agg "mean") | rows x3 | assumption | B-W | max agg .599, six-segment mean .602, clip mean .611 | Y |
| W28 | WITM/predict.py:10 | agg default | "mean" | assumption | none found | max over segments .599 | Y |
| W29 | WITM/predict.py:101 | Score standardisation by mean/std over train songs with audio; neutral = median training score | mean, std, median | assumption | docstring: "No audio -> train-median score" | none found | Y |
| W30 | WITM/predict.py:116 | No-audio candidates get neutral (median) score | median | assumption | docstring | B-W: preview absent AUC .594 (n=79) | Y |
| W31 | WITM/predict.py:37 | Preview identity key md5(previewUrl) | md5 | assumption | matches shared cache | none found | Y |
| W32 | WITM/predict.py:143 | Final members and weights: A, SL, DUR with weights 1, 1, 1.5 (weighted mean) | 1/1/1.5 | number | B-W: "weights 1/1.5/2 all within 0.642-0.646", chosen 1.5 | that sweep (heads+MERT, +DUR) | Y |
| W33 | WITM/predict.py:135,143 | MERT audio_final weight relative to essentia total | wm = 1.0 | number | B-W "Chosen: heads, late-segments, DUR (1.5) and MERT at 1.0 = 0.646" | B-W blends "weights 1/1.5/2 all within 0.642-0.646" | Y |
| W34 | WITM/predict.py:132-134 | Blend = (weighted mean of essentia member z-scores) + wm * W3 MERT z-score, i.e. MERT given half the total weight | additive | assumption | none found | none found | Y |
| W35 | WITM/predict.py:126 | MERT member = Workflow 3 audio_final loaded from the W3 file (all its constants are outside this area) | import | assumption | B-W: "heads+MERT 0.621-0.639" blends | blends tested; ablation abl_no_mert .623 | Y |
| W36 | WITM/predict.py:144-147 | Ablation set (no_mert, no_dur, no_essentia, act_only) | 4 ablations | assumption | declared pre --late (B-W) | n/a | Y(var) |
| W37 | WITM/predict.py:142 | final_content composition (3 essentia-side members + MERT) | design | assumption | declared 13:51:52Z before --late | ablations | Y |
| W38 | WITM/predict.py:48 | embstd/emb alternatives (effnet embedding) not in final | alpha 3000/10000/30000 = .573/.587/.594 | number | B-W | those values | N |
| D01 | WITM/build_desc.py:6 | Descriptor decode sample rate | 16000 Hz | number | "cost" per docstring | B-W: earlier 22 kHz/chroma/key/HPSS version replaced before shards kept; no alternative scored | N (descriptors not in final) |
| D02 | WITM/build_desc.py:6,13 | Hop length and n_fft | 512, 1024 | number | convention (librosa defaults 512, 2048 for n_fft changed to 1024) | none found | N |
| D03 | WITM/build_desc.py:9 | Mono downmix via ffmpeg | -ac 1 | assumption | none found | none found | N |
| D04 | WITM/build_desc.py:11 | Skip clips shorter than 5 s | SR*5 samples | number | none found | none found | N |
| D05 | WITM/build_desc.py:12 | dB conversion epsilon | 1e-6 | number | convention | none found | N |
| D06 | WITM/build_desc.py:15 | Onset strength from dB-scaled magnitude spectrogram | design | assumption | none found | none found | N |
| D07 | WITM/build_desc.py:19-21 | 6 segments of 5 s; per-segment 7 stats + dB std; clip stats incl. dynamic range = p95 - p10 dB | 5 s, p95-p10 | number | none found for percentiles | none found | N |
| D08 | WITM/build_desc.py:22-23 | Tempo = librosa.feature.tempo from onset envelope; floor 30 bpm; log2(/120) | 30, 120 | number | none found | tempo showed no signal (AUC 0.501) in B-W | N |
| D09 | WITM/build_desc.py:5-24 | Choice of descriptors (loudness, centroid, rolloff, flatness, bandwidth, onset, zero crossing; chroma/key/HPSS dropped for cost) | 10 clip-level | assumption | docstring: dropped for cost | none found | N |
| D10 | WITM/build_desc.py:37 | Checkpoint interval | 400 clips | number | housekeeping | n/a | N |
| D11 | WITM/build_desc.py:27 | Only manifest rows with ok==True | filter | assumption | none found | none found | N |
| A01 | WITM/analyze_duration.py:12 | Duration bucket edges | 0,90,150,180,210,240,270,300,360,1e5 s | number | none found | none found | N |
| A02 | WITM/analyze_duration.py:13-14 | Title regexes (live, remix/mix)/edit, remaster, feat./with, acoustic, interlude/intro/outro/skit, version) | 7 regexes | assumption | none found | "interlude/edit" flags too rare to test (B-W) | N |
| A03 | WITM/analyze_duration.py:22,24 | Comparison transforms: |log(dur/180)|, duration relative to artist median in fold | 180 s | number | none found | none found | N |
| A04 | WITM/analyze_duration.py:25-26 | Mixed-label artist groups with more than 1 song | len>1 | assumption | none found | none found | N |
| A05 | WITM/analyze_desc.py:6,18 | Sign of each descriptor learned per fold from Spearman against training rank target; OOS signed AUC | sign | assumption | design | none found | N |
| A06 | WITM/analyze_desc.py:29 | Bootstrap resamples (artist-cluster) | 60 | number | cost | none found | N |
| A07 | WITM/analyze_desc.py:31,33 and analyze_heads.py:66 | CI levels | 2.5/97.5 (95%) | number | convention | none found | N |
| A08 | WITM/analyze_desc.py:16 | Maturity 90 d, quarter rank as in the predictor | 90 d | number | same as W07 | none found | N |
| A09 | WITM/analyze_heads.py:17-23 | Head sign learned from Spearman against quarter-rank plays90 on mature train songs | sign | assumption | design | per-fold stability reported ("stable in all 10 folds") | N |
| A10 | WITM/analyze_heads.py:62 | Artist-cluster bootstrap resamples | 60 | number | cost | none found | N |
| A11 | WITM/analyze_heads.py:69-73 | Permutation null: 30 permutations of labels within fold, max over 605 heads; p95 reported | 30 | number | cost | none found | N |
| A12 | WITM/analyze_heads.py:48 | Chunk size 50 positive rows | 50 | number | memory | n/a | N |
| A13 | WITM/analyze_heads.py:55 | RNG seed | 0 | number | convention | none found | N |
| A14 | WITM/analyze_heads.py:45 | Fold-stratified and within-artist pair AUC definitions (artist x fold key) | design | assumption | none found | none found | N |
| A15 | WITM/artist_proxy.py:10 | Alphas for proxy refits | A 1e4, SL 1e4, emb 3e4 | number | A, SL from final; emb 3e4 = best of B-W emb grid | emb grid .573/.587/.594 | N |
| A16 | WITM/artist_proxy.py:41,49 | Bootstrap resamples | 60 (called with nb 60; default 200) | number | cost (B-W: "CI (60)") | none found | N |
| A17 | WITM/artist_proxy.py:19,26 | Refit excluding all of an artist's train songs (leave-artist-out), not refitting standardiser per exclusion | design | assumption | none found | differs from artist_excluded_cv by 4-bucket design (-0.004 vs -0.03 unresolved, B-W) | N |
| A18 | WITM/artist_proxy.py:12 | Restricted to rows with audio (974 songs) | filter | assumption | B-W | n/a | N |
| A19 | WITM/artist_excluded_cv.py:14 | Number of random artist buckets | 4 | number | none found | none found | N |
| A20 | WITM/artist_excluded_cv.py:14 | Bucket RNG seed = cutoff date as integer | YYYYMMDD | number | none found | none found | N |
| A21 | WITM/artist_excluded_cv.py:33-36 | Bootstrap resamples and seed | 100, seed 0 | number | cost | none found | N |
| A22 | WITM/taste_drift.py:9 | Ridge alpha for drift analysis | 1e4 | number | final A alpha | none found | N |
| A23 | WITM/taste_drift.py:23 | Number of top heads listed | 15 | number | none found | n/a | N |
| A24 | WITM/taste_drift.py:19 | Cosine between ridge coefficient vectors as drift measure | design | assumption | none found | none found | N |

## Counts and counting rules

- Rows: 131 (T01-T58 TAFL, W01-W38 WITM predictor, D01-D11 build_desc, A01-A24 analysis scripts).
- Reason or evidence found: 44. Counted only when a report, README or docstring gives a stated reason or evidence (e.g. a grid, a W3 finding, a declaration). Rows whose reason cell says only convention, cost, memory, numerical guard, housekeeping or "design" count as not found.
- Variation or test found: 59. Counted when a report cites any score for another value or design of the same item (fast TUNE numbers, DA probes, ablations). Rows starting "none found" count as none, even if a related test is mentioned.
- Items in rows marked "N" under feeds do not enter the final model scores (diagnostics, descriptors not used by final, secondary models, noart variants).

## Facts worth noting (no recommendation)

- Almost every number in TAFL predict.py (K, P, half-life, minplays, ncomp, alphas) was chosen among about 85 fast-TUNE variants (B-T), and DA-T-d found the declared K=2/P=91 not to be a tuned optimum, with surrounding settings scoring .577-.658 against .651.
- The 4 windows and layers 4-8 come from frozen shared inputs; the layer choice has no stated reason or numbers beyond "other MERT layer groups .618-.643".
- Alphas 1200 and 150 of the NEW members have no documented origin in this area.
- WITM alpha 1e4 sits at the peak of the grid tried (alpha 3e4 scored lower), segments (3,4,5) were chosen after a per-segment scan on TUNE.
- The folds themselves (TUNE_CUTOFFS 2021-07..2023-10, quarterly) are harness constants and not part of this area.
- Both predictors' held-out numbers are not reproduced here.
