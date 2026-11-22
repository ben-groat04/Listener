# PREREG (written before any scored run), w6r1-content-ranker-final
Base = avg21_dev (= final_avg21 recipe, dev excerpt only, read through evalkit.features). Training always on the dev excerpt (Deezer clips exist only for tried songs, not train songs).
Hypotheses
 H1 two excerpts (mean of the model's z-scores over dev and Deezer clip; one excerpt if only one exists) beat one: avg21_two - avg21_dev > 0 (lo80), bigger for songs whose clips cover different parts.
 H2 window pooling: mean is as good as or better than max / top2 (exploratory, 2 variants).
 H3 source robustness: Deezer-only sauc within ~0.02 of dev-only on the same songs; per-song cross-source Spearman >= 0.7. Otherwise Deezer previews must not be scored with the dev-trained model.
 H4 pre-registered combos with the essentia music recipe (ref_w4r1_music): z(avg21_two)+z(music) and z(avg21_dev)+z(music) (z over the fold's candidates).
Scored variants (fast): avg21_dev avg21_dz avg21_two avg21_dev_max avg21_dev_top2 avg21_two_max def_dev def_dz def_two combo_two_music combo_dev_music (+ diagnostics file diag.py: has_dz, align offset/score, same flags; not candidates).
Final-candidate rule (fixed now): declare at most 3: final_avg21 recipe re-expressed here is NOT redeclared (its own file is declared in w5); declare (i) avg21_two, (ii) combo_two_music if it beats combo_dev_music or avg21_two-only in fast mode by > 0.003 else combo_dev_music, (iii) avg21_dev only if needed as own-base full run. Group definitions for 'same part': same_excerpt flag from p2_clips.csv (|offset|<=2s & score>=0.5, n=75 clips) and a broader group |offset|<=10s & align_score>=0.4 (381 clips); 'different' = rest with an alignment. Heuristics, not ground truth.
