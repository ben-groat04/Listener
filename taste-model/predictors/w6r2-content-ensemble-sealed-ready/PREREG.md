# PREREG (written before any scored run), w6r2-content-ensemble-sealed-ready
Round-1 count already looked at on TUNE: 11 content variants. All below are round-1 variants or close derivatives (avg21_dev mean, avg21_dev_max, combo_dev_music); this is stated.
Pool-independence method: every member is centred and scaled by mean/sd of its score over the fold's TRAINING songs with a MERT clip (fixed per call, never from candidates). avg21 members already normalise by train stats inside the recipe; the avg21 average and the music reference are then rescaled by their training-song sd. Weight of music: 1.0 (pre-registered, same as round 1; no tuning).
Hypotheses
 H1 avg21_max (MERT-only, max pooling over 4 windows) stays POS vs ref_w4r1_listening (lo80>0) as in round 1 (+0.010).
 H2 combo_mean_ts (avg21 mean + music, train-scaled) keeps most of round-1 combo_dev_music gain (+0.014); the loss from train scaling vs pool z is small.
 H3 combo_max_ts adds on H2 (both max pooled + music).
 H4 no gain on new-artist songs; gains sit on known-artist songs.
Candidate list (max 3 declared): A avg21_max (MERT only); B combo_mean_ts (MERT+essentia); C combo_max_ts (MERT+essentia). Base for FILE_DELTAS80: avg21_dev (mean).
Fast iteration list (all counted): avg21_dev, avg21_max, combo_mean_ts, combo_max_ts (+ any fixes to scaling code; count reported).
Checks before scoring: single-candidate equals in-call score (my own check).
