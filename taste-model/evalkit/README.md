# evalkit: does a method predict which NEW songs the user comes to love?

Protocol (code in data.py): a *song* (normalised title + primary artist, merging re-releases) is a candidate for
cutoff C if it was never played before C and is first played in [C, C+3 months). The predictor sees only streams
< C (`train`), plus the candidate list (ids/names, no labels, no timing) and static metadata, and must rank the pool.
Label `love` = >=6 plays on >=3 distinct days within 90 days of first play (`strong` = >=15 plays on >=5 days).
Dev folds: 8 quarterly cutoffs 2023-01..2024-10 (open; tune freely). Sealed: 5 cutoffs 2025-04..2026-04
(1617 songs); never look at streams >= 2025-04-01 or tune on it (`load_streams` refuses; `run --sealed` is logged
to .sealed/runs.log). Metrics (metrics.py): fold AUC, AP (+lift), precision in top 10%, recall in top 20%,
macro-averaged over folds, bootstrap 95% CIs over songs, paired AUC-difference CI vs `artist_love_rate`;
reported for all songs and for new-artist / known-artist subsets.

    python -m evalkit.selftest            # leakage + sanity checks
    python -m evalkit.run [pred.py ...]   # dev scores (no args = baselines); pred.py exposes predict(train,cands,meta,cutoff)
    python -m evalkit.run --sealed pred.py   # final, once per candidate method
    python -m evalkit.make_sealed         # regenerate .sealed/labels.csv, verify vs sealed_manifest.json
Note: AP-lift of a random ranking is slightly >1 in small pools; judge by AUC and the CIs.
