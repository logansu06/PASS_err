#!/usr/bin/env python3
"""render_gate_doc.py - keep gate_mechanical.md's rule table in sync with rules.json.

  python render_gate_doc.py --profile weidong-mei --backtest backtest.md

`backtest.md` is the stdout of calibrate.py. The table between the markers
<!-- BEGIN RULES --> and <!-- END RULES --> in profiles/<profile>/gate_mechanical.md is replaced.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent


def parse_backtest(text: str) -> dict:
    out = {}
    for ln in text.splitlines():
        m = re.match(r"\| (MM\w+) .*?\| (FAIL|WARN|INFO) \| (\d+)/(\d+) \((\d+)%\) \|", ln)
        if m:
            out[m.group(1)] = (int(m.group(3)), int(m.group(4)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", default="weidong-mei")
    ap.add_argument("--backtest", required=True)
    a = ap.parse_args()
    pdir = SKILL / "profiles" / a.profile
    rules = json.load(open(pdir / "rules.json", encoding="utf-8"))["rules"]
    bt = parse_backtest(Path(a.backtest).read_text(encoding="utf-8"))
    rows = ["| id | sev | rule | tolerated | fix | corpus papers flagged |", "|---|---|---|---|---|---|"]
    for r in rules:
        tol = []
        if r.get("max_hits") is not None:
            tol.append(f"{r['max_hits']} per paper")
        if r.get("max_per_1k") is not None:
            tol.append(f"{r['max_per_1k']} per 1k words")
        f = bt.get(r["id"])
        fl = f"{f[0]}/{f[1]}" if f else "-"
        rows.append(f"| {r['id']} | {r['severity']} | {r['name']} | {'; '.join(tol) or '0'} | {r.get('fix','')} | {fl} |")
    doc = pdir / "gate_mechanical.md"
    t = doc.read_text(encoding="utf-8")
    new = "<!-- BEGIN RULES -->\n" + "\n".join(rows) + "\n<!-- END RULES -->"
    t2 = re.sub(r"<!-- BEGIN RULES -->.*?<!-- END RULES -->", lambda m: new, t, flags=re.S)
    doc.write_text(t2, encoding="utf-8")
    print(f"updated {doc} with {len(rules)} rules")


if __name__ == "__main__":
    main()
