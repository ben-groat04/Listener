REPORT: builder r2, learned-representations (cap 90 min, used 64 min wall clock, 15:35:13 to 16:39:15 UTC)

HEADLINE
- Learned or time-resolved structure does NOT beat clip-mean linear models on dev.
- The declared final, `final_ens`, is a 4-member mix: two linear members, two learned (MLP, attention) members. It scores TUNE sauc .638, equal to ref_audio_final .632 (d +.007, P .67, lo -.015) and below ref_w4r1_listening .651.
- The linear-only ablation of it is as good or better on LATE and HOLDOUT, so the nets add nothing.
- The only consistent gain I found came from the training signal (panel rows, +0.01 to +0.03 on TUNE). It is not significant, and its HOLDOUT effect is about zero.

WHAT I BUILT AND WHY
- Folder: /home/user/Listener/taste-model/predictors/w4r2-learned-representations/
  - predict.py: core code and the PREDICTORS dict (10 models).
  - final.py: lean entry file with the final plus 3 ablations. All full, null, LATE and HOLDOUT runs used this file.
  - excl_check.py: artist-exclusion diagnostic (fast TUNE only).
  - variants.py: the exploration variants, as configs (code behind the numbers below; not re-run as a file, see "what I only believe").
  - build_patches.py: builds the dense patch store `.cache/w4r2-lr/` (about 5 s, git-ignored, regenerable). It stores essentia patch embeddings (1280-d) and head activations (605), at most 29 patches per clip, from the frozen shared shards.
- Inputs: only the song's own clip.
  - essentia per-patch effnet embeddings or 605 head activations;
  - MERT windows (4 windows, layers 4-8 mean).
  - No artist or history feature enters any candidate score.
- Training:
  - Target is rank_plays: percentile of 90-day plays within the quarter of first play, for songs mature for 90 days.
  - "Panel" signal (optional): extra rows for songs with at least 2 plays in each of the last two 91-day periods before the cutoff. Target = percentile of plays in the last period. Weight 0.5. The listening record is used for targets only.
  - Fitting: standardiser, PCA and nets are fitted on train songs only. The fit cache is keyed on train identities (trackId, song, artist, timestamps) and honours EVALKIT_NO_FIT_CACHE.
  - Hyperparameters were fixed by prior, then compared on TUNE (counted below). I did NOT do artist-grouped CV inside train, so some hyperparameter choice came from looking at TUNE.
- Learned models:
  - `mlp`: MLP on the clip mean.
  - `attn`: per-patch encoder plus attention pooling, with random patch dropout.
  - `conv`: temporal conv over neighbouring patches plus attention.
  - Training details: 5-seed ensembles of nets, AdamW, MSE (one pairwise rank-loss variant).
- Linear models:
  - ridge on the clip mean;
  - "patchridge": ridge with every patch or window as a row, scored as the mean over patches. This is the time-local linear control.

VARIANTS SCORED ON TUNE (fast, 1074 tried / 342 loved)
Every variant is counted (32 distinct configs including controls, about 30 over six fast runs). Columns: sauc / new-artist sauc. wx for the final and its ablations is in the full-run table below. wx was not extracted for the exploration variants and is not claimed for them.

- Essentia effnet embedding, clip mean, ridge: .559 / .543.
- Essentia embedding patch-ridge: .570 / .549.
- Essentia embedding MLP: .553 / .579.
- Essentia embedding attention: .550 / .572.
- Essentia embedding attention + panel: .574 / .572.
- Essentia embedding conv + panel: .560 / .559.
- Essentia embedding patch-ridge + panel: .574 / .552.
- Essentia head activations, ridge on the mean: .582 / .590.
- Essentia head activations attention: .565 / .560.
- Essentia head activations attention + panel: .581 / .592.
- Essentia head activations conv + panel: .578 / .567.
- Essentia head activations ridge + panel: .577 / .568.
- MERT clip mean ridge: .615 / .593.
- MERT patch-ridge (4 windows as rows): .624 / .603.
- MERT patch-ridge + panel: .635 / .619.
- MERT MLP: .592 / .630.
- MERT MLP, regularised (h16, wd .1, dropout .5): .612 / .611.
- MERT MLP + panel: .619 / .637 (a panel weight of 1.0 gave an identical result; see the note below).
- MERT attention: .591 / .628.
- MERT attention, regularised + panel: .617 / .631.
- MERT attention with pairwise rank loss: .589 / .628.
- MERT attention over 12 layer-by-window tokens: .576 / .586.
- Linear ensemble of MERT patch-ridge + heads ridge + embedding patch-ridge: .615.
- The same plus nets: .622.
- `ens_lin2`: .628 / .618.
- Final candidates with panel: ens_mert3 (patch-ridge, MLP, attention) .632 / .627; ens_mert_act (final) .635 / .628; ens_lin_panel .633 / .619.
- Walk-forward family (final file, fast; re-run values differ by about .003-.004 from the first runs, because net training is not exactly reproducible):
  - final_ens .638 / .627
  - abl_linear_only .633 / .619
  - abl_nets_only .622 / .626
  - abl_no_panel .630 / .626
  - ctl_clipmean_mert .615 / .593
  - ctl_clipmean_act .582 / .590
  - m_mlp_mert_panel .623
  - m_attn_mert_panel .622
  - m_patchridge_mert_panel .635
  - m_ridge_act_panel .577

Reference TUNE sauc / new-artist sauc: ref_audio_final .632 / .614; ref_w4r1_listening .651 / .667; ref_w4r1_music .646 / .613.
Note: the identical result for panel weight 1.0 versus 0.5 on the MERT MLP is suspicious. I did not investigate it, so treat that variant row as unverified.

WALK-FORWARD (fast, on predict.py PREDICTORS, 10 members, 2m46s)
- Composite sauc .625 [.586,.644], macro .589, wa .585, wx .621, new-artist .627.
- The best member with hindsight is final_ens at .638, so the optimism is +.013.
- Composite minus ref_audio_final is about -.007 (sauc .625 against .632).
- The selection procedure itself therefore does no better than the references, and the final's TUNE score is slightly optimistic.

FINAL (declared before LATE; DECLARATION.txt in the scratch folder)
- Definition: `final_ens` in final.py.
- Members, averaged after each is standardised by its own train-song score mean and std:
  1. MERT patch-ridge (nc64, alpha 1200)
  2. MERT MLP (nc32, h16)
  3. MERT attention over the 4 windows
  4. essentia-heads ridge on the clip mean
- All four use panel rows (weight 0.5).
- Songs without audio get the train-median score.
- Ablations in the same file:
  - abl_linear_only: members 1 and 4;
  - abl_no_panel: all four members, no panel rows;
  - ctl_clipmean_mert: MERT clip-mean ridge.

FULL TUNE RUN (nboot 300, independence on; independence p90 = 0.0 for all my models; runtime 4m19s against an 8 min estimate)
Columns: sauc [95% CI] / macro / wa / wx / new-artist sauc.
- final_ens: .638 [.594,.667] / .588 / .608 / .628 / .627 [.54,.69]
- abl_linear_only: .633 / .595 / .610 / .624 / .619
- abl_no_panel: .630 / .597 / .607 / .625 / .626
- ctl_clipmean_mert: .615 / .572 / .575 / .611 / .593

Paired deltas for final_ens (d; lo95; P):
- vs ref_audio_final:
  - sauc +.007 (lo -.015, P .67)
  - wx -.001 (lo -.024, P .47)
  - new-artist +.013 (lo -.035, P .71)
  - wa -.006
- vs ref_w4r1_listening (best_ref):
  - sauc -.013 (lo -.035, P .14)
  - wx -.015 (lo -.044, P .09)
  - new-artist -.040 (lo -.095, P .08)
- vs ref_w4r1_music:
  - sauc -.008 (P .29)
  - wx -.019 (P .15)
  - new-artist +.014 (P .79)
- wa vs duration: -.037 (lo -.120, P .24). Duration has wa .645 on TUNE; the final's wa is .608.
- vs the harness baselines:
  - nonaudio_gbm: +.083 (lo +.001, P .98)
  - artist_recent: +.019 (lo -.025, P .83); wa +.108 (lo +.049)
  - artist_plays: P .83 (lower bound -.025)
  - duration: +.061 (lo +.011)
  - meta_gbm: +.099 (lo +.032)
  - pool_artist_siblings: P(d>0) = .947 (lower-bound table value -.005)
  - pool_album_siblings: P .84
  - exposure_session: P .007 (it is higher, +.12 or so; that is a harness diagnostic, not a valid predictor)
- Evidence grade vs best_ref: not significant on sauc, wx or new-artist.

BREAKDOWN by new_vs_known_artist (sauc [95% CI]):
- final_ens: new .627 [.54,.69]; known .627 [.57,.66]
- abl_linear_only: .619 / .622
- abl_no_panel: .626 / .621
- ctl_clipmean_mert: .593 / .610
- ref_w4r1_listening: .667 / .632
- ref_audio_final: .614 / .625

LABEL VARIANTS (sauc; love / strong / love_4_2 / love_10_4 / keep):
- final_ens: .638 / .639 / .627 / .630 / .638
- abl_linear_only: .633 / .633 / .629 / .626 / .636
- abl_no_panel: .630 / .633 / .620 / .625 / .632
- ctl_clipmean_mert: .615 / .620 / .592 / .611 / .614
- ref_audio_final: .632 / .632 / .616 / .626 / .635
- ref_w4r1_listening: .651 / .649 / .636 / .645 / .633

Open pool, TUNE (sauc all / new / known / wa / p20):
- final_ens: .747 / .730 / .752 / .616 / .125. A second table (open_love_full) shows final_ens at .731 / .716 / .732 / .605 / .170.
- abl_linear_only .734, abl_no_panel .732, ctl_clipmean .697.
- ref_audio_final .705, ref_w4r1_listening .736, ref_w4r1_music .740.
- Caveat: the open pool carries a missing-preview shortcut and decoy-selection caveats.

LATE (run 1 of 2; 6m08s against an 8 min estimate). Columns: sauc / wx / new-artist sauc (from the breakdown).
- final_ens: .615 [.549,.67] / .603 / new .594
- abl_linear_only: .640 / .631 / .613
- abl_no_panel: .608 / .598 / .571
- ctl_clipmean_mert: .592 / .589 / .580
- ref_audio_final .621; ref_w4r1_listening .653; ref_w4r1_music .642

LATE paired deltas for final_ens:
- vs ref_audio_final: sauc -.006
- vs ref_w4r1_listening: sauc -.038, P .01 (the final is clearly below it)
- vs ref_w4r1_music: sauc -.026, P .04

ALL slice (TUNE + LATE):
- final_ens .630; abl_linear_only .636; abl_no_panel .622; ctl_clipmean .607.
- ref_audio_final .628; ref_w4r1_listening .652; ref_w4r1_music .645.

On LATE, nets cost -.025 relative to the linear-only ablation, and the panel signal adds +.007 on LATE for the final. LATE is partly used up, so this carries little weight.

HOLDOUT (run once, on final.py; 6m48s against a 12 min estimate; the predictor was not changed after this run)
HOLDOUT-ALL, artist-disjoint rows. Columns: sauc [CI] / wa / wx / new-artist, in the order the harness prints them where available.
- final_ens: .657 [.586,.725], wa .575, wx .645.
- abl_linear_only: .665 [.577,.734].
- abl_no_panel: .656.
- ctl_clipmean_mert: .636.
- ref_audio_final: .657.
- ref_w4r1_listening: .640.
- ref_w4r1_music: .664.
- artist_recent: .521.
- nonaudio_gbm: .540.
- duration: .510.

Paired deltas for final_ens on HOLDOUT-ALL (not graded):
- vs ref_audio_final: sauc +.001 (P .49)
- vs ref_w4r1_listening: sauc +.017 (lo -.006, P .94)
- vs ref_w4r1_music: sauc -.006 (P .28)
- new-artist deltas: +.026, +.043, +.040 (all with lo95 below zero)
- vs duration: sauc +.147 (lo +.063)
- vs nonaudio_gbm: sauc +.117 (lo +.016)

DEV+HOLDOUT pooled (14 folds; not graded):
- final_ens .627 [.595,.655]; abl_linear_only .631; abl_no_panel .622; ctl_clipmean_mert .610.
- ref_audio_final .626; ref_w4r1_listening .643; ref_w4r1_music .642.
- final_ens vs ref_audio_final: +.001 (P .56)
- final_ens vs ref_w4r1_listening: -.016 (P .03)
- final_ens vs ref_w4r1_music: -.015 (P .04)
- final_ens vs duration: sauc +.066 (lo +.028)
- final_ens vs artist_recent: sauc +.079 (lo +.028)
- The full verbatim HOLDOUT and DEV+HOLDOUT tables are in <W4 scratch path, not available> They are reproduced here only as the key rows above, because of length.

ARTIST CHECKS
- New-artist sauc on TUNE: final .627, linear-only .619, clip-mean control .593. A learned-versus-linear difference exists only in the nets: MLP .627-.637 and attention .625-.631 against linear .60-.62, but not significant. The nets do better on new-artist pairs and worse on known-artist pairs, which is the opposite of the "nets memorise artist timbre" worry.
- Final re-scored with all training streams of the candidate's own artist removed (excl_check.py, fast TUNE, 5 artist groups with the whole group removed in each fit; slightly conservative; 4m32s):

| model | normal | excluded | new | known |
|---|---|---|---|---|
| final_ens | .638 | .619 | .620 | .611 (normal known .627) |
| abl_linear_only | .633 | .610 | .587 | .606 |
| ctl_clipmean_mert | .615 | .601 | .594 | .593 |

  - The final drops .019 (wa .608 to .554 in the excluded run).
  - So about 0.02 of the TUNE score depends on same-artist training songs (artist timbre, or panel and target signal from the same artist), and the excluded final is NOT better than ref_audio_final.
  - A fair reading: the content signal that survives artist removal is about .61-.62, about the same as the clip-mean control.

NULL CONTROL: PASS (see null_control_result). Per-seed null sauc .445-.573 shows how wide random-label scores are.

DOES LEARNED OR TIME-RESOLVED STRUCTURE ADD ANYTHING?
Evidence on fast TUNE, plus LATE and HOLDOUT for the final's ablations. No test is significant.
1. Nonlinear nets (MLP, attention) versus linear on the same inputs:
   - Alone they are worse in sauc, by .01 to .04: MERT MLP .592 to .623 against patch-ridge .624 to .635, and essentia nets .55-.58 against ridge .56-.58.
   - They are higher in new-artist sauc on MERT (.63 against .60-.62). Not significant.
   - On LATE the final (with nets) is -.025 against its linear-only ablation. On HOLDOUT it is -.008, and on DEV+HOLDOUT -.004. In the final, the nets add +.005 on TUNE and nothing elsewhere.
2. Time structure:
   - Local rows (patch-ridge) beat clip mean by +.01 to +.02 on both MERT (.624 against .615) and essentia (.570 against .559). That is consistent in direction but within noise, and could just be augmentation.
   - Attention, conv over neighbouring patches, 12-token layer-by-window attention and a rank loss gave no gain over mean pooling (.576-.60).
   - So within a 30 s preview there is no demonstrated temporal signal beyond clip means.
3. Essentia (effnet embedding or head) models are clearly weaker than MERT: .56-.58 against .62-.635. They add nothing in the final apart from a small head-activation member.
4. Panel rows help nets and linear models on TUNE: +.011 for MERT patch-ridge, +.027 for the MERT MLP, +.008 for the final (.630 to .638). On LATE +.007, on HOLDOUT +.001. This matches round 1: helps on dev, not on HOLDOUT.

STRONGEST CASE AGAINST MY OWN RESULT
- The final is statistically tied with ref_audio_final, below ref_w4r1_listening on LATE and DEV+HOLDOUT (P .01 to .04), and the artist-excluded final (.619) is under the reference.
- The walk-forward composite .625 is the honest expectation for a pick made in advance.
- Random-label refits score .445-.573 (SD about .04), so a .638 on TUNE is only about +.12 above the null mean, and differences of .01 to .02 between my variants are noise.
- I tried about 30 variants on TUNE, so the best one is optimistically selected.
- The hyperparameters were chosen by eye, not by CV inside train.
- The panel signal uses the same artists' recent plays: it can carry artist identity into the target, so its TUNE gain may partly be artist recognition.
- The new-artist advantage of the nets (about +.02) has a CI of about +-.07.

NOT DONE
- No artist-grouped CV for hyperparameters.
- No sequence models beyond one conv layer.
- No second --late run, and no use of the second holdout.
- No frame-level handcrafted descriptors (w4-descriptors was never built).
- The excl diagnostic has not been run on LATE or HOLDOUT.

WHAT I ACTUALLY RAN (all through the harness, 2 threads, wall clock)
- Fast TUNE iteration runs v1 to v6 (about 2 to 5 min each) and f1 (2m28s).
- Walk-forward (2m46s).
- excl_check fast (4m32s; I estimated 8-12 min and it took 4.5).
- Full TUNE (4m19s).
- Null control (12m04s).
- --late once (6m08s).
- --holdout once (6m48s).
- build_patches (5 s).
- All runs were estimated before launch and fit the cap.
- Scratch logs and TIMING: <W4 scratch path, not available> (v1-v6.log, f1.log, wf.log, excl.log, full_tune.log, null.log, late1.log, holdout.log, DECLARATION.txt, TIMING.txt).
- I did not run --sealed, make_sealed, decoy tools, raw stream reads, or read PLAN.md or the .claude folder.

WHAT I ONLY BELIEVE (not tested)
- Neural net training is slightly non-deterministic across process runs (the same MERT MLP scored .619 once and .623 another time), so differences of .003-.004 between my reruns are not meaningful.
- The identical numbers for panel weight 0.5 and 1.0 on the MERT MLP are unexplained. A weight-equivalence bug is possible but unchecked.
- I believe the clip-mean-versus-patch-ridge gain is augmentation rather than time structure; not tested separately.
- I believe nets are data-starved at 165-1,050 rows; I did not test with larger training sets.
- variants.py has not been re-run end-to-end as a file; its configs are the ones run via predict.py's make() in the six fast runs (some under different model names).

CLEANUP
- Deleted: nothing remains from failed attempts as code except what is kept as configs in variants.py (the earlier exploratory PREDICTORS dicts were overwritten in place).
- The `.cache/w4r2-lr/` store (1.1 GB, git-ignored) is regenerable with build_patches.py.
- __pycache__ removed.

FILES
- /home/user/Listener/taste-model/predictors/w4r2-learned-representations/{predict.py, final.py, excl_check.py, variants.py, build_patches.py}
- /home/user/Listener/taste-model/.cache/w4r2-lr/ (cache)

## null_control_result
PASS for final_ens under the v4.1 cluster-aware band (TUNE, 5 seeds). Per-seed null sauc .498/.549/.524/.573/.445, seed-average .518 against a real .638 (gap +.120, CI .071-.147); wa .499 and new-artist .537, both inside their bands. Under the old song-level band the new-artist row is OUT, so that label reads FLAG (comparison only, the band is too narrow for feature models). The ablations also PASS: abl_linear_only, abl_no_panel and ctl_clipmean_mert (the last at .524). Among the baselines only `duration` FLAGs. The per-seed null scores swing .445-.573, so a TUNE difference of 0.02 is within selection noise. Null control took 12m04s against my 10-15 min estimate.