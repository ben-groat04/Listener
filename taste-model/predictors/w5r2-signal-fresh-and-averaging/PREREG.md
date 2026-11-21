# Pre-registration (written 2026-11-21 before any new scoring; only the w5_default reproduction check had been run)
Code: grid.py (family, averaging sets, staleness variants), predict.py (procedures).  Harness v5.1, --fast, TUNE.
## Lead (a) family (20 non-default configs + default)
mat in {60,30,0} x partial in {trunc,scale} x grp in {quarter(q), roll91(r91), all} = 18, plus mat90+trunc with grp in {r91, all} = 2. (mat90+scale == default.) Names f_m<mat><t|s>_<grp>.
All other numbers = default (pct_plays target, hor 90, panel K2/P91/hl180, wnew 0.5).
## Lead (b) procedures (all equal-weight means of members' standardised blended scores; all SECONDARY)
avg21 (all 21 family incl. default); avg_mat {default, m60s_q, m30s_q, m0s_q}; avg_grp {default, m90t_r91, m90t_all}; avg_fresh2 {default, m0s_q}.
Nested: nested_shr50 = per outer cutoff pick the family member with best pooled inner sauc (evalkit.inner, 4 folds x 3 months, 90-day horizon) if it beats default's inner sauc, else default; final score = 0.5*default + 0.5*chosen (shrinkage toward default).
## PRIMARY comparison (one)
f_m0s_q (round-1 'mat0_scale': no maturity wait, play and play-day counts scaled by 90/age for songs younger than 90 days, quarter grouping) minus w5_default, paired sauc delta on default TUNE folds, fast mode. Rule: POS if the 80% interval lower bound > 0 (decision80 = POS; |lo80|<0.005 = UNDECIDED). Everything else is secondary.
## Chance calibration (planned)
Harness null-train relabelling (artist/album bijection + shuffled identities; a fresh relabelling per seed k) re-scored for all 21 family members in fresh processes; per seed: best family delta vs default and m0s_q delta; compare with observed. Many seeds (target >= 12, as time allows).
## Null control (planned)
harness --null-control for: avg21, avg_mat, nested_shr50, f_m0s_q, and the final predictor.
## Robustness (planned)
leave-one-fold-out of the primary, FOLD_META, five alt fold sets with --best-ref ref_w4r1_listening (primary, averages), below-0.5 AUC audit of 2021 folds.
## Staleness (secondary)
stale_new{30,90,180} (only new-song signal cut back), stale_pan{..} (only panel signal), stale_all{..} (both). The recipe's listening record enters only as training targets (features are audio-only), so "model vs record" is split by signal: new-song targets vs recent-period panel targets.
## Variant count
1 default + 20 family + 4 averages + 1 nested + 9 staleness = 35 scored configurations.
## Declaration of final predictor (written 22:21 UTC after the fast TUNE scoring of all 35 configs; the primary was UNDECIDED, so this is the 'closest non-identical procedure I would recommend', not an evidence-backed improvement)
final.py: final_avg21 = equal-weight average of the 21 family configs (avg21, pre-registered secondary). Chosen over avg_mat / avg_grp / avg_fresh2 because it is the least dependent on which single value is 'plausible'; it was nevertheless picked among 4 pre-registered averages after seeing fast TUNE (selection among 4 acknowledged).
