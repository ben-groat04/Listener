# Metric variants scored (listed before scoring; count at the end)
Score families (S) x label/outcome (L) x weighting (W). All on harness v5.1 dumps (tried pool, TUNE-era fold sets); artist-cluster bootstrap.
S1 pooled within-fold sauc (default, W=pooled)            S2 IV-weighted per-fold mean delta (fold_meta)       S3 macro (mean per-fold AUC, equal-weight)
S4 per-quarter pooled (pair group quarter on monthly folds) S5 top-decile within-fold lift of love  S6 top-20% recall of love (within fold)
S7 precision@k, k=10 per fold  S8 within-fold concordance with plays90 (gc)   S9 same with share90   S10 AUC vs keep (days 90-365)
S11 AUC vs love_4_2  S12 AUC vs love_10_4  S13 AUC vs strong  S14 AUC vs love at 180d horizon (>=6 plays, >=3 days)  S15 AUC vs love at 365d
S16 open-pool sauc / p20 (harness default --fast text, decoys)
Weightings: pooled pairs, IV, equal-per-fold, sqrt(n) per fold.
Counted in report ("n_variants").
