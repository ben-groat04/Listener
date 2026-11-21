"""Procedures compared with the fixed default (declared before scoring): avg81 = equal-weight average over the 81-member family (grid.FAMILY_AVG);
sel_* = nested in-train selection over grid.SELECT_FAMILY (57 configs, 4 inner folds via evalkit.inner, fallback to default with <2 usable inner folds) with shrinkage:
margin = required inner-sauc gain over the default; pen = penalty per changed parameter."""
import os, sys, atexit, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import procs
_sel = {"sel_m005": procs.nested(0.005), "sel_m010": procs.nested(0.010), "sel_m020": procs.nested(0.020), "sel_pen003": procs.nested(0.0, 0.003)}
PREDICTORS = {"default": procs.variant({}), "avg81": procs.avg_family(), **_sel}
def _dump():
    try: json.dump({k: v.chosen for k, v in _sel.items()}, open(os.environ.get("W5R2_OUT", "/tmp") + "/chosen_%d.json" % os.getpid(), "w"), indent=1)
    except Exception: pass
atexit.register(_dump)
