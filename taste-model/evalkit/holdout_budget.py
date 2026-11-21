"""evalkit v5.0: regenerate the HOLDOUT budget file.   python3 -m evalkit.holdout_budget --round w5r1 --runs 3

Writes `.cache/holdout_budget.json` = {"round": ROUND, "remaining": RUNS} (the file `run --holdout` reads and decrements; it is the ONLY budget state, apart from the per-file / per-bundle cap of 1 and the fingerprints in
.cache/holdout_runs.log / .cache/holdout_fingerprints.pkl, which are unchanged). Refuses to overwrite a budget file of the SAME round (it would reset a spent budget); a file of another round is replaced.
Round w5r1: 3 runs = one per round-1 builder, on its pre-declared final file."""
import sys, json, os
from pathlib import Path
from . import data

PATH = data.ROOT / ".cache" / "holdout_budget.json"

def write(round_, runs, path=PATH):
    path = Path(path)
    if path.exists():
        old = json.loads(path.read_text())
        if old.get("round") == round_: raise SystemExit(f"REFUSED: {path} already holds round {round_!r} (remaining {old.get('remaining')}); not overwritten (that would reset a spent budget).")
    path.parent.mkdir(parents=True, exist_ok=True); tmp = Path(str(path) + ".tmp"); tmp.write_text(json.dumps(dict(round=round_, remaining=int(runs)))); os.replace(tmp, path)
    return json.loads(path.read_text())

def main(argv):
    if "--round" not in argv or "--runs" not in argv: raise SystemExit("usage: python3 -m evalkit.holdout_budget --round ROUND --runs N")
    print(write(argv[argv.index("--round") + 1], int(argv[argv.index("--runs") + 1])))

if __name__ == "__main__": main(sys.argv[1:])
