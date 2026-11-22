"""evalkit v5.3: the extra output blocks of the SEALED slice (also produced, with the TUNE folds under a synthetic slice name, by `--synthetic-sealed` and the selftest).
  coverage_table / coverage_verdicts : per-fold feature coverage at the TOP of the output; interpretation STOPS when the tried-song coverage of a registered model is below 90%
  sauc80_lines                       : every model's sauc with its 80% interval and a line saying whether lo80 > 0.5
The COMPARATOR_SET (pooled / IV / heaviest-out), FILE_DELTAS80 comparator rows for every model, LABEL VARIANTS (strong) and the exposure_before BREAKDOWN come from run.summarize(sealed_style=True)."""
import numpy as np, pandas as pd
from . import features

STOP_BELOW = 0.90
NEEDS = {"ref_audio_final": ("mert",), "ref_w4r1_listening": ("mert",), "ref_w4r1_music": ("mert", "essentia")}   # builder files declare theirs with a module-level FEATURES tuple (default ("mert",)); kinds: mert, essentia, deezer

def needs_of(name, modules=()):
    if name in NEEDS: return NEEDS[name]
    for m in modules:
        if name in (getattr(m, "PREDICTORS", None) or {}): return tuple(getattr(m, "FEATURES", ("mert",)))
    return tuple(getattr(modules[0], "FEATURES", ("mert",))) if modules else ("mert",)

def coverage_table(Fs, fold_names, kinds):
    """One row per fold and group (tried / decoy / train): tracks and the share with each feature kind. Group flags only; no labels."""
    rows = []
    for F in Fs:
        f = str(F["c"].date())
        if f not in fold_names: continue
        meta, cands = F["meta"], F["cands"]; dec = F["pool"].is_decoy.values[F["order"]] == 1; ids = cands.trackId.values
        for g, t in (("tried", ids[~dec]), ("decoy", ids[dec]), ("train", pd.Index(F["train"].trackId.unique()).values)):
            c = features.coverage(meta, t, kinds); rows.append(dict(fold=f, group=g, tracks=len(t), **{k: round(v, 3) for k, v in c.items()}))
    return pd.DataFrame(rows)

def coverage_verdicts(tab, models_needs):
    """(lines, stop): per registered model the pooled tried-song coverage of each feature kind it needs (track-weighted over the folds), STOP if any is < 90%; folds below 90% are listed."""
    lines, stop = [], False; tr = tab[tab.group == "tried"]
    for name, kinds in models_needs.items():
        cov = {k: float((tr[k] * tr.tracks).sum() / tr.tracks.sum()) for k in kinds}; low = {k: ",".join(tr.fold[tr[k] < STOP_BELOW]) for k in kinds}
        bad = [k for k in kinds if cov[k] < STOP_BELOW]; stop |= bool(bad)
        lines.append(f"COVERAGE {name}: tried-song coverage " + ", ".join(f"{k}={cov[k]:.3f}" for k in kinds) + ("  -> STOP: below 90%, DO NOT INTERPRET this model's sealed numbers" if bad else "  -> ok (>= 90%)")
                     + ("".join(f"  [folds below 90% for {k}: {v}]" for k, v in low.items() if v)))
    return lines, stop

def sauc80_lines(S, models, nboot):
    """S = tabs['_S'] of summarize: one line per model: sauc, its 80% bootstrap interval (artist-cluster resamples) and whether lo80 > 0.5."""
    out = []
    for n in models:
        st = S[n]["all"]; pt = float(np.asarray(st["sauc"]).ravel()[0]); lo, hi = np.nanpercentile(st["sauc_b"], [10, 90])
        out.append(f"SAUC80 {n}: sauc={pt:.3f} 80%[{lo:.3f},{hi:.3f}] ({nboot} artist-cluster resamples)  lo80 > 0.5: {'YES' if lo > 0.5 else 'NO'}")
    return out
