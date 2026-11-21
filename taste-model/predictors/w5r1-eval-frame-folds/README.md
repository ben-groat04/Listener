# w5r1-eval-frame-folds (Workflow 5 round 1, builder: evaluation-frame study)
Regenerate everything from taste-model/ (scratch dir S = the builder scratch folder; dumps live there, regenerable):
1. `python3 -W ignore -m evalkit.run --fast --folds tune,tune_q1,tune_q2,tune_m,tune_h,tune_y --dump-scores $S/dump_all.pkl predictors/w5r1-eval-frame-folds/predict.py predictors/w5r1-eval-frame-folds/diag_stack2.py` (about 5.5 min; the first run had both models in predict.py, identical scores)
2. `python3 -W ignore -m evalkit.run --fast --refs none --folds tune,tune_q1,tune_q2,tune_m,tune_h,tune_y --dump-scores $S/dump_bars.pkl predictors/w5r1-eval-frame-folds/bars.py` (2 min; bar variants)
3. analyses (all read the dumps; seconds each): a1_folds.py, a2_weights.py [tune|tune_m], a3_labels.py, a4_wx.py (reads TUNE-era streams < 2024-01-01 via data.load_streams), a5_bar.py, a6_nboot.py, a7_below_chance.py, a8_staleness.py (needs a1 output), a9_siblings.py -> results/*.txt|csv
lib.py = shared metric code (evalkit.metrics.Block / group_auc). predict.py = the declared final (w5r1_stack3). diag_stack2.py = diagnostic only.
