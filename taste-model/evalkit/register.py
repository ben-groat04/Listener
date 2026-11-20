"""Main session only: pre-register the final model file(s) for the sealed run.  python -m evalkit.register pred.py name
The sealed runner refuses unregistered files and files already evaluated. (A filesystem convention plus an audit trail,
not a cryptographic lock: builders share the filesystem, so registration is the main session's job by policy.)"""
import sys, json, hashlib
from .run import REGISTRY
p, name = sys.argv[1], sys.argv[2]
h = hashlib.sha256(open(p, "rb").read()).hexdigest()
reg = json.loads(REGISTRY.read_text()) if REGISTRY.exists() else {}
reg[h] = name; REGISTRY.write_text(json.dumps(reg, indent=1)); print("registered", h[:12], name)
