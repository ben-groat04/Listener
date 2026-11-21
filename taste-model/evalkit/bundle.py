"""Predictor bundle hashes (evalkit v4.1).

A predictor file may import (or load by path) other code of this project. `bundle_members(entry)` finds those files WITHOUT running the predictor: it imports the entry file in a
fresh subprocess (every module whose __file__ lies under taste-model/ but not under evalkit/ is collected; modules loaded with importlib.util.spec_from_file_location at import time are
recorded too) and adds files the entry (or a member) names by path or imports by name from its own folder (static scan, so lazy loads at call time are found as well).
`bundle_sha256(entries)` = sha256 over the sorted (relative path, file sha256) of all members plus the (entry marker, sha256) of every entry file.
Data caches (.npz etc.) are not hashed; the harness' own code (evalkit/) is not part of a bundle."""
import hashlib, json, os, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVALKIT = ROOT / "evalkit"
_PATH_RX = [re.compile(r"""predictors/[\w\-\.]+/[\w\-\.]+\.py"""), re.compile(re.escape(str(ROOT)) + r"""/[\w\-\./]+\.py""")]

def sha256_file(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def _is_member(p):
    try: p = Path(p).resolve()
    except Exception: return False
    return p.suffix == ".py" and p.is_file() and ROOT in p.parents and EVALKIT not in p.parents and "__pycache__" not in p.parts and ".cache" not in p.relative_to(ROOT).parts

_PROBE = r'''
import sys, os, json, importlib.util
rec = set(); _o = importlib.util.spec_from_file_location
def _hook(name, location=None, *a, **k):
    if location is not None: rec.add(os.path.abspath(str(location)))
    return _o(name, location, *a, **k)
importlib.util.spec_from_file_location = _hook
entry = sys.argv[1]; sys.path.insert(0, os.path.dirname(os.path.abspath(entry)))
spec = _o("evalkit_bundle_probe", entry); m = importlib.util.module_from_spec(spec); sys.modules["evalkit_bundle_probe"] = m; spec.loader.exec_module(m)
files = set(rec)
for mod in list(sys.modules.values()):
    f = getattr(mod, "__file__", None)
    if f: files.add(os.path.abspath(f))
print("BUNDLE_JSON " + json.dumps(sorted(files)))
'''

def _static_refs(p):
    """Files named by a path literal in the CODE (docstrings and comments are ignored) or imported by name from the folder of `p` (static; finds lazy loads at call time too)."""
    import ast
    out = set()
    try: src = Path(p).read_text(errors="ignore"); tree = ast.parse(src)
    except Exception: return out
    doc = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.body and isinstance(node.body[0], ast.Expr) and isinstance(getattr(node.body[0], "value", None), ast.Constant): doc.add(id(node.body[0].value))
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in doc:
            for rx in _PATH_RX:
                for m in rx.findall(node.value):
                    q = (ROOT / m) if not m.startswith("/") else Path(m)
                    if _is_member(q): out.add(str(q.resolve()))
        elif isinstance(node, ast.Import): names |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module: names.add(node.module.split(".")[0])
    for name in names:
        q = Path(p).resolve().parent / (name + ".py")
        if _is_member(q): out.add(str(q.resolve()))
    return out

def bundle_members(entry, timeout=600):
    """Absolute paths (sorted, entry excluded) of the project code the entry file uses, see the module docstring."""
    entry = str(Path(entry).resolve()); found = set()
    r = subprocess.run([sys.executable, "-W", "ignore", "-c", _PROBE, entry], cwd=str(ROOT), capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0: raise RuntimeError(f"bundle probe failed for {entry} (the predictor file must be importable):\n{r.stderr[-2000:]}")
    line = [l for l in r.stdout.splitlines() if l.startswith("BUNDLE_JSON ")][-1]
    for f in json.loads(line[len("BUNDLE_JSON "):]):
        if _is_member(f): found.add(str(Path(f).resolve()))
    todo = list(found | {entry}); seen = set()
    while todo:   # fixed point of the static references
        p = todo.pop()
        if p in seen: continue
        seen.add(p)
        for q in _static_refs(p):
            if q not in found and q != entry: found.add(q)
            todo.append(q)
    found.discard(entry)
    return sorted(found)

def _rel(p):
    p = Path(p).resolve()
    return str(p.relative_to(ROOT)) if ROOT in p.parents else p.name

def bundle_sha256(entries, members=None):
    """Hash of the bundle of `entries` (one path or a list). members: precomputed bundle_members (union over entries) or None."""
    entries = [entries] if isinstance(entries, (str, Path)) else list(entries)
    if members is None: members = sorted({m for e in entries for m in bundle_members(e)})
    items = sorted({("member", _rel(m), sha256_file(m)) for m in members} | {("entry", "", sha256_file(e)) for e in entries})
    return hashlib.sha256("\n".join("|".join(i) for i in items).encode()).hexdigest()

def describe(entry):
    """dict(entry_sha256, members={relpath: sha256}, bundle_sha256) for one entry file."""
    mem = bundle_members(entry)
    return dict(entry_sha256=sha256_file(entry), members={_rel(m): sha256_file(m) for m in mem}, bundle_sha256=bundle_sha256([entry], mem))
