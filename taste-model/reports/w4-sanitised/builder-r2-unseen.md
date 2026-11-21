Builder r2, task unseen-artist-generalisation. Start 2026-11-21T15:35:14Z, end 2026-11-21T16:20:10Z (45 min). Nothing was committed. No --sealed, make_sealed, decoy files, raw streams, PLAN.md or .claude/ were touched.

SUMMARY
- A content-only ridge ensemble (4 members: MERT layer-group blocks plus essentia head and embedding blocks) reaches TUNE sauc 0.645, wx 0.632, new-artist sauc 0.640 [0.552, 0.707], wa 0.634.
- It does not beat the best reference. Against ref_w4r1_listening on TUNE: d_sauc -0.007 (P 0.22, lo -0.030), d_wx -0.011, d_new -0.027 (P 0.07). On HOLDOUT-ALL its new-artist sauc is 0.657 [0.458, 0.812] against 0.621 for ref_w4r1_listening, but n=148 and the CI is far too wide to separate them.
- Walk-forward selection over the 36-member family I chose from gives sauc 0.613, so the selection optimism is +0.032. Honest answer: the advantage over the references is not shown. The content-only signal sits on a plateau of about 0.62-0.65 sauc.
- New-artist sauc (0.640) holds up against the reference audio models, but the paired deltas against ref_audio_final and ref_w4r1_music have CIs spanning zero. It is not distinguishable from the best reference.
- Content-only model whose new-artist score is the same by construction (artist rows can not matter for an unseen artist): the ridge scores of unseen artists are identical in full and noart variants (0.640 / 0.640).

WHAT I BUILT AND WHY
- Files: /home/user/Listener/taste-model/predictors/w4r2-unseen-artist-generalisation/{predict.py, final.py, build_compact.py, build_compact2.py}. final.py is the declared entry file; it loads predict.py by path.
- Inputs: per-clip MERT layer-group means (layers 0-3 / 4-8 / 9-11, averaged over 4 windows), CLAP, essentia act_mean, emb_mean, act_max, emb_std, MERT window std and delta, lyric embedding. The listening record is used only for training targets and weights (rule 1). Nothing at candidate level uses artist or history in the primary models.
- Targets ("signal"): panel (percentile of plays inside each of the last K 91-day periods, recency weight) + new (percentile of first-90-day plays within the quarter of first play, for songs first played at least 90 d before the cutoff). "both" = the two summed with weights. These are the user's listening-frequency statistics.
- Artist handling in training: adem (de-mean target by shrunk leave-one-out artist mean) and apow (weight 1/n_artist_rows^p).
- Model: whitened PCA per block (fit on train-stream songs) plus weighted ridge with unpenalised intercept. alpha is chosen by artist-grouped 5-fold CV inside train, never on TUNE. combine=concat (one ridge) or trust (one ridge per block, weight = squared positive artist-grouped CV correlation). Optional RBF kernel ridge. Fit caches are keyed on a hash of train (trackId, song, artist) plus timestamps. noart=True removes each candidate's own primary-artist rows exactly (sufficient-statistics subtraction).
- Cached features (built from frozen shared caches into .cache/w4r2-unseen/): compact.npz (build_compact.py, actual 2m23s, 1 thread) and compact2.npz (time-resolved summaries, actual ~2 s).
- Declared final (written before any --late run, declaration file in my scratch): w4r2_unseen_final = f1_ens_ridge = standardised mean of 4 ridge members, all signal "both":
  (a) mert_mid, 64 comps, hl 90;
  (b) mert_lo+mid+hi concat, 32 comps each, hl 90;
  (c) trust over mert lo/mid/hi + essentia act + emb, hl 90;
  (d) mert_mid, 64 comps, panel P=60 K=3, hl 120.
  Ablations in the same file: w4r2_unseen_final_noart (f2, own-artist rows removed) and w4r2_unseen_auto (g2: top 3 of a 16-config grid, chosen by artist-grouped CV inside train).
- The declared final was chosen after I had seen TUNE results of its members and of f1-f4. It is therefore selected on TUNE. The walk-forward block quantifies that.

VARIANTS SCORED ON TUNE (all fast mode; counted = 60 predictors + 3 full runs of the final file). sauc / wx / new-artist sauc [95% CI]. Reference rows for orientation: ref_audio_final .632/.629/.614, ref_w4r1_listening .651/.643/.667, ref_w4r1_music .646/.647/.613.
- v01 mert_mid, panel, nc48: .618/.610/.620
- v02 mert_mid, new signal: .619/.608/.591
- v03 mert_mid, both: .633/.621/.615
- v04 panel+adem1: .604/.591/.602
- v05 panel+apow0.5: .607/.595/.599
- v06 panel+apow1: .593/.588/.573
- v07 panel noart: .599/.597/.620
- v08 clap: .520/.522/.560
- v09 eact: .576/.587/.599
- v10 eemb: .582/.584/.591
- v11 lyr: .499/.496/.515
- v12 mert_lo: .569/.561/.541
- v13 mert_hi: .576/.583/.632
- v14 trust all 7 blocks (panel): .616/.612/.618
- v15 same + adem1: .586/.590/.588
- v16 concat mert3+clap nc32: .591/.584/.632
- v17 both, trust all: .632/.622/.618
- v18 both, mid+eact nc32: .616/.613/.602
- v19 both nc96: .622/.617/.608
- v20 both nc24: .595/.589/.586
- v21 both K3: .619/.608/.599
- v22 both hl90: .634/.620/.616
- v23 both mert_hi: .571/.571/.606
- v24 both mert3 nc32: .629/.621/.620
- v25 both trust mert3+eact+eemb: .633/.625/.615
- v26 both apow0.25: .630/.615/.624
- v27 both noart: .613/.609/.615
- v28 both P182: .605/.597/.608
- v29 both P60 K3 hl120: .632/.623/.624
- v30 both nc128: .610/.609/.625
- v31 both krr: .637/.627/.637
- v32 both krr mert3: .618/.613/.652
- v33 both hl90 nc64: .639/.627/.646
- v34 mstd (MERT window std): .496/.508/.524
- v35 mdelta: .524/.528/.494
- v36 eactmax: .583/.584/.591
- v37 estd: .574/.575/.544
- v38 mid+mstd nc32: .626/.619/.622
- v39 trust time (mid, mstd, eactmax, estd): .629/.617/.597
- f1 ens ridge (declared final): .645/.632/.640
- f2 noart: .621/.612/.640
- f3 ridge + krr: .644/.631/.647
- f4 f1 stacked with ref_audio_final + ref_w4r1_music via evalkit.refs.score (secondary): .652/.643/.646
- f5 f1 + 0.25*z(log duration) (metadata, secondary): .653/.643/.654
- g1 auto top1: .618/.607/.594
- g2 auto top3: .629/.625/.645
- 14 analysis variants a_<block>_{full,noart} (table below).
- Every individual variant sits at or below 0.64. The differences among most of them are far below the CI width (about ±0.03).
- Failed or dropped ideas: de-meaning by artist, down-weighting artist rows, CLAP alone, lyrics alone, MERT window std/delta, P182. All are kept in predict.py as counted variants; no code was deleted.

WALK-FORWARD (fast, 36-member family = v01-v39 + f1, f2, f3, ran 3m53s)
- Chosen member per fold: v01 for the first two folds, then v09_eact, v18, v11_lyr (2022-07), v30 (2022-10 and 2023-01), f1 from 2023-04.
- Composite sauc 0.613 [0.571, 0.646], macro 0.555, wx 0.604, wa 0.613, new-artist 0.633 [0.528, 0.699].
- Best member with hindsight f1 0.645; optimism = +0.032.
- Composite vs ref_audio_final d -0.019 (P 0.16); vs ref_w4r1_listening d -0.039 (lo -0.064, P 0.00); vs ref_w4r1_music d -0.034 (P 0.03).
- Reading: picking the variant by early-fold sauc chooses noise (it picked lyrics-only at one fold). f1 itself is a hindsight pick, so its 0.645 is optimistic. The honest-procedure number is 0.613 on sauc and 0.633 on new-artist.
- Inside-train artist-grouped CV selection (g2) gives .629 / .625 / .645, which is more honest, with the new-artist number on the same level as f1.

WHICH INPUTS TRANSFER TO UNSEEN ARTISTS (TUNE fast; "new" = songs by artists absent from train, n=377; "known" n=697; full = own-artist rows kept in training, noart = removed)
- mert_mid: sauc .634 / .614; new .616; known .630 / .608. Best single block; about 0.02 of its known-artist gain is artist fingerprint.
- mert_hi: new .598; known .545 / .538. Transfers at roughly the same level as mid, but weaker on known artists.
- mert_lo: new .561; known .567 / .544. Weak.
- clap: new .588; known .517 / .502. Weak.
- essentia act: new .574; known .569 / .556.
- essentia emb: new .558; known .583 / .552. Loses most of its gain without own-artist rows, so it behaves as an artist fingerprint.
- lyric emb: new .493; known .536 / .557. Chance.
- MERT window std / delta: chance (.49-.52).
- Training choices: de-meaning and artist down-weighting reduced sauc and did not raise new-artist sauc (v04-v06). "both" signal and shorter half-life (hl 90) were the most consistent gains, about +0.015 within noise.
- Own-artist training rows: on TUNE the artist-history component adds about +0.02-0.03 sauc (final .645 vs noart .621). On LATE the sign reverses (noart .648 vs full .639), consistent with artist familiarity reversing in 2024. On new-artist songs the two are identical by construction.
- Evidence level: single TUNE run per variant, CIs about ±0.03; I only believe the ordering where the differences exceed that (hi/mid vs clap/lyrics, mert_mid vs chance features).

FINAL RESULTS (final = w4r2_unseen_final; sauc / wx / wa / new-artist sauc; CI in brackets)
- TUNE full run (nboot 300, independence p90 0.0; runtime 3m00s): sauc .645 [.588, .678], macro .575, wx .632 [.590, .665], wa .634 (wa CI .557-.652 on the verdict table), new-artist .640 [.552, .707], known .632; gc .585. Open pool: open_sauc_all .738 [.657, .777], new .731 [.654, .799], known .737, open_wa .576, open p20 .155 (best_open_p20 .26 is another model). noart: .621 / .612 / .616 / .640, open .709, open new .731, p20 .125. auto: .629 / .625 / .624 / .645, open .736, new .721, p20 .145.
- LATE (2024, 4 folds; --late run 1 of 2 used, 7m46s): final sauc .639 [.582, .684], wx .632, wa .657, new .649 [.479, .733]. noart .648 / .637 / .653 / .649. auto .626 / .625 / .651 / .613. Refs on LATE: audio_final .621, listening .653, music .642. final minus ref_w4r1_listening: d -0.015 (lo -0.040, P 0.09).
- ALL (14 dev folds from the same run): final .642 [.594, .680], wx .632, wa .639, new .643 [.559, .700]; noart .631 / .621 / .624 / .643; refs listening .652, music .645, audio_final .628.
- HOLDOUT-ALL (run once; 14 folds; n 740 tried, 148 new-artist): final sauc .653 [.579, .722], macro .659, wx .649 [.568, .732], wa .553, new-artist .657 [.458, .812], known .634. noart .639 / .637 / .548 / .657. auto .650 / .645 / .533 / .624. Refs: audio_final .657, listening .640, music .664 (their new .637/.621/.624). Open: final .764 [.700, .818], new .710, p20 .142. Final minus ref_w4r1_listening: sauc +0.013 (P 0.93, lo -0.002), wx +0.015, new +0.036 (P 0.81, lo -0.042); vs ref_audio_final sauc -0.003, new +0.020; vs ref_w4r1_music sauc -0.010, new +0.033.
- DEV+HOLDOUT (pooled, 2450 tried, 713 new-artist; not graded): final sauc .639 [.607, .668], wx .630, wa .616, new .653 [.586, .709], known .627. noart .626 / .619 / .604 / .653. Refs: listening .643 (new .671), music .642 (new .622), audio_final .626 (new .621). Final minus listening: sauc -0.005 (lo -0.019, P 0.20), wx -0.008, new -0.018 (P 0.09); vs audio_final: sauc +0.013 (P 0.87), new +0.032 (P 0.96, lo -0.004); vs music: sauc -0.003, new +0.031 (P 0.95, lo -0.007).
- I did not change the predictor after HOLDOUT. The holdout run was done on final.py (3 models) and used 1 of the 2 shared budget. Full HOLDOUT output: <W4 scratch path, not available> (HOLDOUT-ALL VERDICT at line 5282, DEV+HOLDOUT at 5372). TUNE: full_tune.txt, LATE/ALL: late.txt, null: null.txt in the same folder. I did not paste the verbatim tables here; the rows above are copied from those files.

PAIRED DELTAS vs REFERENCES (TUNE full run; point d, lo95, P(d>0))
- vs ref_audio_final: sauc +0.013 (lo -0.024, P .73); wx +0.003 (lo -0.028, P .59); new +0.025 (lo -0.029, P .81).
- vs ref_w4r1_listening (best_ref): sauc -0.007 (lo -0.030, P .22); wx -0.011 (P .13); new -0.027 (lo -0.070, P .07).
- vs ref_w4r1_music: sauc -0.002 (lo -0.048, P .45); wx -0.014 (P .26); new +0.027 (lo -0.026, P .80).
- wa vs duration (TUNE): .634 vs .645 (d -0.011, lo -0.084, P .32). HOLDOUT wa .553 vs duration .498 (duration wa not significant either; d +0.055, lo -0.134).
- vs baselines (TUNE lower bounds of d_sauc / P): artist_recent -0.017 (P .92; point d +0.026); artist_plays -0.016 (P .87); duration +0.038 (P .99); meta_gbm +0.006 (P .98); nonaudio_gbm +0.120 (P 1.0); has_preview +0.107; preview_source_itunes -0.024; popularity -0.019; artist_love_rate +0.004. Diagnostics (post-cutoff info, not valid predictors): pool_artist_siblings -0.002 lower bound (P .97; point .645 vs .644); pool_album_siblings -0.038. New-artist lower bounds vs artist_recent and artist_plays +0.053 (P 1.0), vs pool_artist_siblings +0.025 (P .99), vs nonaudio_gbm +0.090.
- Evidence grades: sauc, wx and new-artist evidence vs best_ref = "TUNE only (P=0.22)" style, i.e. no advantage over best_ref.

BREAKDOWN and LABEL VARIANTS (TUNE full run, sauc [95% CI])
- new_vs_known: final new .640 [.55,.71], known .632 [.54,.67]; noart new .640, known .603 [.52,.66]; auto new .645, known .611. ref_w4r1_listening new .667, known .632; ref_audio_final .614/.625; ref_w4r1_music .613/.650.
- By exposure_before (0, 1-2, 3-8, 9+): final .617 / .653 / .619 / .735; noart .592 / .624 / .622 / .694; ref_w4r1_listening .615 / .672 / .641 / .782.
- By plays tercile of the 90d window (low, mid, high): final .541 / .688 / .647; noart .506 / .655 / .646; ref_w4r1_listening .567 / .672 / .671. The final is weakest on the low-plays tercile (about 0.54, noart 0.51).
- By preview: preview present .657 [.60,.69]; missing preview exactly 0.500 for all content models (no content, neutral score).
- By release age: old releases .648 [.58,.69] (n 987); small release-age buckets are too small (n 18-50) to read.
- LABEL VARIANTS sauc (love / strong / love_4_2 / love_10_4 / keep): final .645 / .638 / .627 / .638 / .627; noart .621 / .623 / .607 / .619 / .617; auto .629 / .628 / .623 / .625 / .614; refs: audio_final .632/.632/.616/.626/.635; listening .651/.649/.636/.645/.633; music .646/.647/.642/.640/.648. All within 0.02 of love.
- Open pool (TUNE): see TUNE results above; HOLDOUT-ALL open_sauc .764, open new .710, p20 .142; DEV+HOLDOUT open .751, new .748, p20 .189 (listening: .751 / .743 / .186; music: .752 / .727 / .154). The open pool carries the missing-preview shortcut and decoy-selection caveats (decoys come from artists known before each cutoff), so I give it no weight beyond the tried-pool numbers.

ARTIST CHECKS
- "noart" (own primary-artist training rows removed): TUNE .645 to .621 (known .632 to .603); LATE .639 to .648 (known-artist gain disappears/reverses); HOLDOUT .653 to .639; DEV+HOLDOUT .639 to .626. New-artist numbers identical (the candidate's artist is absent from train by definition).
- New-artist sauc of the final is 0.640 TUNE / 0.649 LATE / 0.657 HOLDOUT / 0.653 DEV+HOLDOUT, so the content signal does not depend on artist rows; about 0.02 of the known-artist number does (fingerprint share).
- Compared with the references on new-artist songs, the final is +0.02-0.03 above ref_audio_final and ref_w4r1_music (P .80-.96 pooled, lower bounds around zero), and 0.018-0.027 below ref_w4r1_listening on dev (P .07-.09), but 0.036 above it on HOLDOUT (P .81). No consistent ranking.

BELOW-CHANCE FOLDS (investigated)
- The harness flagged meta_gbm fold 2022-04 and preview_source_itunes fold 2023-10; none of my models.
- My final's per-fold AUC: 2021-07 .553, 2021-10 .447, 2022-01 .562, 2022-04 .478, 2022-07 .536, 2022-10 .568, 2023-01 .682, 2023-04 .604, 2023-07 .652, 2023-10 .645. Two early folds are below 0.5 (n 39 and 31 tried, CIs [.28,.62] and [.26,.72], so compatible with chance). All references show the same early weakness (ref_audio_final .374 in 2021-07, .524 in 2021-10).
- Reading: gains are concentrated in the later folds with more training songs and more tried songs. The early folds are too small to say anything. I believe (not tested) that small train sets limit the ridge, but I did not test this.

STRONGEST CASE AGAINST MY RESULT
1. Nothing beats the references: on TUNE the final is -0.007 sauc below ref_w4r1_listening and +0.013 above ref_audio_final, both within noise; the walk-forward composite is 0.613.
2. The declared final was picked after about 40 TUNE looks, and the hindsight best member of the family looks 0.032 better than the procedure. Neighbouring variants (v01-v33) average about 0.62, i.e. about the ref_audio_final level.
3. The new-artist subset is small (377 TUNE, 148 HOLDOUT) and its CIs span ±0.08-0.18; the HOLDOUT new-artist 0.657 vs 0.621 is not a finding.
4. HOLDOUT wa is only 0.553 (below its TUNE 0.634) and not above duration; the within-artist content signal did not hold on HOLDOUT.
5. On the low-plays tercile the final is 0.54; the signal sits mostly in songs that already have high play counts.
6. wx removes only the session-novelty confound; I did not test the reverse-causation idea beyond the wx column, and I did not test the LATE-vs-TUNE difference between full and noart for significance (LATE .648 vs .639 is well within CI).
7. Stacking the two references with my ensemble (f4, TUNE .652) does not beat ref_w4r1_listening alone (.651).

WHAT I ACTUALLY RAN (runtimes: estimate / actual)
- build_compact.py (estimate ~3 min, go): 2m23s. build_compact2.py: ~2 s.
- Fast runs: 5 batches of 4-16 variants each, 82-92 s each; walk-forward 3m53s (estimate 5 min, go).
- Full TUNE run: 3m00s (estimate 8 min, went).
- Null control v4 (5 seeds, 3 models; estimate 6 min, actual 9m39s, exceeded estimate but within cap, wait-and-see decision).
- --late (1 run): 7m46s (estimate 5 min).
- --holdout (1 run): 6m18s (estimate 10 min).
- 2 threads max; no other job concurrent except the 1-thread build_compact2.

WHAT I ONLY BELIEVE (not tested)
- The early-fold weakness comes from small training sets.
- The 0.02 own-artist share on known songs is a fingerprint/familiarity effect rather than a content effect (supported only by the noart ablation, not a separate test).
- Neighbouring configurations differ by noise, not by a real hyperparameter effect.

Files kept: predict.py (all counted variants, ensembles, auto, dur-stack), final.py, build_compact.py, build_compact2.py. __pycache__ removed. Caches in /home/user/Listener/taste-model/.cache/w4r2-unseen/ (git-ignored, regenerable from the two build scripts). Scratch: <W4 scratch path, not available> (fast1-8.txt, wf.txt, full_tune.txt, null.txt, late.txt, holdout.txt, summ.py, TIMING.txt, DECLARATION.txt).

## null_control_result
PASS (null control v4.1, TUNE, 5 seeds, cluster-aware band) for the declared final w4r2_unseen_final: avg_sauc 0.544 (band 0.481-0.564), avg_wa 0.505 (0.433-0.565), avg_new 0.548 (0.424-0.594), all inside. Real-vs-null sauc gap +0.125 (CI 0.074-0.169; real 0.645, seed mean 0.520). final_noart and auto also PASS. Under the old song-level band the same three FLAG (sauc OUT); the harness marks that band too narrow for feature models. Among the baselines in the same run, duration FLAGs on the cluster band (sauc and wa OUT); the rest PASS.