"""evalkit v5.0: alternative TUNE-era fold sets (`--folds NAME[,NAME...]`).  Definitions only (no data access, no streams).

A fold set is a list of windows (start, end). Fold k tests songs FIRST played in [start_k, end_k), with training streams before start_k.
All windows lie in [FIRST, LAST) = [2021-07-01, 2024-01-01): no LATE-era row (first play >= 2024-01-01) and no HOLDOUT-era look is ever scored by these sets
(HOLDOUT ARTISTS are removed exactly as in the default folds). Fold names = the window start date (str, YYYY-MM-DD).

  tune     the default 10 quarterly folds 2021-07-01 .. 2023-10-01 (each 3 months)
  tune_q1  quarterly, cutoffs shifted by +1 month: boundaries 2021-07-01, 2021-08-01, then every 3 months, final boundary 2024-01-01 (first fold 1 month, last fold 2 months)
  tune_q2  quarterly, shifted by +2 months: boundaries 2021-07-01, 2021-09-01, then every 3 months, final boundary 2024-01-01 (first fold 2 months, last fold 1 month)
  tune_m   monthly, 2021-07-01 .. 2023-12-01 (30 folds)
  tune_h   half-yearly: 2021-07-01, 2022-01-01, ..., 2023-07-01 (5 folds; the last ends 2024-01-01)
  tune_y   2021-07-01, 2022-07-01, 2023-07-01 (3 folds; the last ends 2024-01-01 and is 6 months long)
"""
import pandas as pd

FIRST = pd.Timestamp("2021-07-01")
LAST = pd.Timestamp("2024-01-01")
SETS = ("tune", "tune_q1", "tune_q2", "tune_m", "tune_h", "tune_y")

def _stepped(first_inner, step):
    """FIRST, first_inner, first_inner + step, ... (all < LAST), LAST."""
    b = [FIRST]; t = pd.Timestamp(first_inner); k = 0
    while t < LAST: b.append(t); k += 1; t = pd.Timestamp(first_inner) + pd.DateOffset(months=step * k)
    return b + [LAST]

def boundaries(name):
    if name == "tune": return [FIRST + pd.DateOffset(months=3 * i) for i in range(11)]          # 2021-07-01 .. 2024-01-01
    if name == "tune_q1": return _stepped("2021-08-01", 3)
    if name == "tune_q2": return _stepped("2021-09-01", 3)
    if name == "tune_m": return [FIRST + pd.DateOffset(months=i) for i in range(31)]
    if name == "tune_h": return [FIRST + pd.DateOffset(months=6 * i) for i in range(6)]
    if name == "tune_y": return [pd.Timestamp("2021-07-01"), pd.Timestamp("2022-07-01"), pd.Timestamp("2023-07-01"), LAST]
    raise KeyError(f"unknown fold set {name!r}; choose from {', '.join(SETS)}")

def windows(name):
    """[(start, end)] of the folds of set `name` (Timestamps)."""
    b = boundaries(name); return list(zip(b[:-1], b[1:]))

def parse(arg):
    """'tune_m,tune_q1' -> ['tune_m', 'tune_q1'] (validated, order kept, duplicates dropped)."""
    out = list(dict.fromkeys(x.strip() for x in str(arg).split(",") if x.strip()))
    if not out: raise SystemExit("--folds needs at least one fold-set name: " + ", ".join(SETS))
    for n in out: boundaries(n)
    return out

def quarter_label(ts):
    """Calendar quarter of a timestamp, e.g. '2021Q3' (used by --pair-group quarter)."""
    ts = pd.Timestamp(ts); return f"{ts.year}Q{(ts.month - 1) // 3 + 1}"
