"""evalkit v5.2 declarations: record WHAT is about to be scored before it is scored.
    python3 -m evalkit.declare NAME FILE [FILE ...]
writes .cache/declarations/NAME.json (mode 444) holding the UTC time and the sha256 of every file; refuses to overwrite an existing declaration (a new name is needed).
Every scored run (evalkit.run) prints, per predictor file, whether its sha256 equals a declared file's sha256 (`DECLARED <name> sha256=...` or `UNDECLARED`) and appends the same
to .cache/run_log.jsonl (opened append-only, chmod 444 between writes; this is a speed bump against accidents, not a security boundary: the file owner can still chmod it).
`python3 -m evalkit.declare --list` prints the declarations. Test hook: EVALKIT_DECL_DIR / --dir DIR replaces the declarations folder."""
import sys, os, json, hashlib, datetime, stat
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
def decl_dir(d=None): return Path(d or os.environ.get("EVALKIT_DECL_DIR") or ROOT / ".cache" / "declarations")
def run_log_path(d=None): return (Path(d) if d else ROOT / ".cache") / "run_log.jsonl"
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def utc(): return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def declare(name, files, d=None):
    assert name and all(c.isalnum() or c in "-_." for c in name) and not name.startswith("."), "NAME: letters, digits, - _ . only"
    assert files, "give at least one FILE"
    for f in files: assert Path(f).is_file(), f"not a file: {f}"
    dd = decl_dir(d); dd.mkdir(parents=True, exist_ok=True); p = dd / f"{name}.json"
    rec = dict(name=name, utc=utc(), files={str(Path(f).resolve()): sha(f) for f in files})
    try: fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)   # O_EXCL: refuses to overwrite, even if the old file were writable
    except FileExistsError: raise SystemExit(f"REFUSED: declaration {name!r} already exists ({p}); declarations are never overwritten, choose a new name")
    with os.fdopen(fd, "w") as fh: fh.write(json.dumps(rec, indent=1) + "\n")
    os.chmod(p, 0o444); return rec

def load_all(d=None):
    dd = decl_dir(d); return [json.loads(p.read_text()) for p in sorted(dd.glob("*.json"))] if dd.exists() else []

def status(path, d=None):
    """-> dict(file, sha256, status 'DECLARED'|'UNDECLARED', name, declared_utc, note) for one predictor file."""
    h = sha(path); decs = load_all(d); res = dict(file=str(Path(path).resolve()), sha256=h, status="UNDECLARED", name=None, declared_utc=None, note="")
    for r in decs:
        if h in r["files"].values(): res.update(status="DECLARED", name=r["name"], declared_utc=r["utc"], note=""); return res
    rp = str(Path(path).resolve())
    for r in decs:
        if rp in r["files"]: res["note"] = f"path was declared as {r['name']} with a different hash (file edited after declaration)"; break
    return res

def run_status(mods, d=None):
    return [status(p, d) for p in mods]

def format_status(sts):
    if not sts: return "declaration check: no predictor file in this run (baselines / references only): UNDECLARED"
    return "declaration check: " + "; ".join(f"{Path(s['file']).name} sha256={s['sha256'][:16]} " + (f"DECLARED {s['name']} ({s['declared_utc']})" if s["status"] == "DECLARED" else "UNDECLARED" + (f" [{s['note']}]" if s["note"] else "")) for s in sts)

def append_run_log(rec, d=None):
    """Append one JSON line to the run log; the file is mode 444 except during the append."""
    p = run_log_path(d); p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists(): os.chmod(p, 0o644)
    try:
        with open(p, "a") as fh: fh.write(json.dumps(rec) + "\n")
    finally: os.chmod(p, 0o444)

def main(argv):
    if argv[:1] == ["--list"]:
        for r in load_all(): print(r["name"], r["utc"], {Path(k).name: v[:12] for k, v in r["files"].items()})
        return
    d = None
    if argv[:1] == ["--dir"]: d = argv[1]; argv = argv[2:]
    assert len(argv) >= 2, "usage: python3 -m evalkit.declare NAME FILE [FILE ...]"
    r = declare(argv[0], argv[1:], d); print(f"declared {r['name']} at {r['utc']}:"); [print(f"  {Path(k).name}  sha256={v}") for k, v in r["files"].items()]

if __name__ == "__main__": main(sys.argv[1:])
