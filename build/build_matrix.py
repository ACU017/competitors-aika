#!/usr/bin/env python3
"""Rebuild index.html's matrix body + rawData from competitors.json + coverage_*.json."""
import json, re, html, glob, os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # competitors-list-website/
CTX = os.path.dirname(os.path.abspath(__file__))  # build/
INDEX = os.path.join(BASE, "index.html")

src = open(INDEX, encoding="utf-8").read()

# --- extract the canonical feature taxonomy from the existing rawData ---
m = re.search(r"const rawData = (\{.*?\});\s*\n", src, re.S)
if not m:
    sys.exit("could not locate rawData in index.html")
old = json.loads(m.group(1))
features = old["features"]          # list of [group, feature]
feature_names = [f[1] for f in features]

# --- load competitors (preserve CSV order) ---
comps = json.load(open(os.path.join(CTX, "competitors.json"), encoding="utf-8"))

# --- merge coverage files ---
coverage = {}
for fp in sorted(glob.glob(os.path.join(CTX, "coverage_*.json"))):
    coverage.update(json.load(open(fp, encoding="utf-8")))

# --- validate feature names from coverage against taxonomy ---
valid = set(feature_names)
unknown = {}
for name, feats in coverage.items():
    for fk in feats:
        if fk not in valid:
            unknown.setdefault(name, []).append(fk)
if unknown:
    print("WARNING: unknown feature names (will be dropped):")
    for n, fks in unknown.items():
        print(f"  {n}: {fks}")

MARK = {
    "Strong":  ("strong",  "●", "Direct fit", "Strong"),
    "Partial": ("partial", "◐", "Adjacent",   "Partial"),
    "None":    ("none",    "○", "Gap",        "Weak/None"),
}

def esc(s):
    return html.escape(s or "", quote=True)

# --- build tbody rows + rawData competitors/coverage ---
rows_html = []
rd_competitors = []
rd_coverage = {}
missing_cov = []

for c in comps:
    name = c["Company Name"]
    ctype = c["Type"]
    note = c["One-Liner Description"]
    cov = coverage.get(name)
    if cov is None:
        missing_cov.append(name)
        cov = {}
    # clean coverage to valid features only
    cov = {k: v for k, v in cov.items() if k in valid and v in ("Strong", "Partial")}

    rd_competitors.append({"name": name, "type": ctype, "where_exposed": note})
    rd_coverage[name] = cov

    cells = []
    for fname in feature_names:
        val = cov.get(fname, "None")
        cls, mark, small, dataval = MARK[val]
        cells.append(
            f'<td class="cell {cls}" data-feature="{esc(fname)}" data-value="{dataval}">'
            f'<span class="mark">{mark}</span><small>{small}</small></td>'
        )
    row = (
        '<tr><td>\n'
        f'      <div class="comp-name">{esc(name)}</div>\n'
        f'      <div class="comp-type">{esc(ctype)}</div>\n'
        f'      <div class="comp-note">{esc(note)}</div>\n'
        '    </td>' + "".join(cells) + '</tr>'
    )
    rows_html.append(row)

if missing_cov:
    print("WARNING: no coverage data for:", missing_cov)

new_tbody = "<tbody>\n            " + "\n            ".join(rows_html) + "\n\n          </tbody>"
src = re.sub(r"<tbody>.*?</tbody>", lambda _: new_tbody, src, count=1, flags=re.S)

new_rawData = {"features": features, "competitors": rd_competitors, "coverage": rd_coverage}
rd_line = "const rawData = " + json.dumps(new_rawData, ensure_ascii=False) + ";\n"
src = re.sub(r"const rawData = \{.*?\};\s*\n", lambda _: rd_line, src, count=1, flags=re.S)

open(INDEX, "w", encoding="utf-8").write(src)

# --- report ---
strong = sum(1 for c in rd_coverage.values() for v in c.values() if v == "Strong")
partial = sum(1 for c in rd_coverage.values() for v in c.values() if v == "Partial")
print(f"OK: wrote {len(comps)} competitors x {len(feature_names)} features")
print(f"    {strong} Strong, {partial} Partial cells")
