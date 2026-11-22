"""Pull the 80% intervals of paired differences (candidate minus artist_recent / ref_w4r1_listening) out of a full-run output file for the secondary measures.
Usage: python3 parse_deltas.py full_run.txt MODEL_NAME.  Asserts the table headers exist and 12 comparator columns were parsed."""
import re, sys
f, model = sys.argv[1], sys.argv[2]; L = open(f).read().split("\n")
TABLES = ["dSAUC_80ci", "dMACRO_80ci", "dWA_80ci", "dWX_80ci", "dGC_80ci", "dNEWSAUC_80ci", "open_dSAUC_80ci", "open_dSAUC_new_80ci", "open_dSAUC_known_80ci"]
for t in TABLES:
    i = [k for k, l in enumerate(L) if l.startswith("== ") and l.rstrip().endswith(f"TUNE {t}")]
    assert i, t
    j = i[0] + 1
    while j < len(L) and not L[j].startswith("== "):
        if L[j].lstrip().startswith(model):
            cells = re.findall(r"\(([-+0-9.eEna]+), ?([-+0-9.eEna]+)\)", L[j])
            assert len(cells) >= 12, (t, len(cells))
            print(f"{t:<24} vs artist_recent 80%[{cells[2][0]},{cells[2][1]}]   vs ref_w4r1_listening 80%[{cells[10][0]},{cells[10][1]}]")
        j += 1
