#!/usr/bin/env python3
"""fact_guard.py - style edits may change form, never facts.

Compares two versions of a .tex file (or two directories with the same file names) and reports
every difference in the *fact tokens* of the text:

  numbers (with unit suffix), \\cite keys, \\ref / \\eqref / \\label names, inline math,
  and the number of display equations, figures, tables, algorithm boxes.

  python fact_guard.py BEFORE.tex AFTER.tex [--allow-math-reorder] [--json out.json]

Exit status 0 = identical fact tokens; 1 = differences (each printed as -removed / +added);
2 = usage error. A polish / rewrite / compression pass must end with exit 0 unless the removal
of a token is intended and logged in the audit ledger.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


def strip(t: str) -> str:
    return "\n".join(re.sub(r"(?<!\\)%.*", "", ln) for ln in t.split("\n"))


def tokens(text: str) -> dict:
    t = strip(text)
    body = t.split(r"\begin{document}")[-1]
    out: dict[str, Counter] = {}
    out["cite_keys"] = Counter(k.strip() for m in re.finditer(r"\\cite\w*\*?(?:\[[^\]]*\])*\{([^}]*)\}", body) for k in m.group(1).split(","))
    out["ref_labels"] = Counter(m.group(2).strip() for m in re.finditer(r"\\(ref|eqref|autoref|cref|Cref)\{([^}]*)\}", body))
    out["labels"] = Counter(m.group(1).strip() for m in re.finditer(r"\\label\{([^}]*)\}", body))
    math = Counter(re.sub(r"\s+", "", m.group(1)) for m in re.finditer(r"(?<!\$)\$([^$]+)\$(?!\$)", body))
    out["inline_math"] = math
    prose = re.sub(r"\$[^$]*\$|\\begin\{(?:equation|align|eqnarray|gather|multline)\*?\}.*?\\end\{(?:equation|align|eqnarray|gather|multline)\*?\}|\\\[.*?\\\]", " ", body, flags=re.S)
    prose = re.sub(r"\\(?:cite|ref|eqref|label)\w*\{[^}]*\}", " ", prose)
    nums = Counter()
    for m in re.finditer(r"(?<![\w.\\])(\d+(?:\.\d+)?)\s*(%|dB|dBm|GHz|MHz|THz|Hz|bps/Hz|bps|m|s|ms|km|W|mW|x|times)?(?![\w])", prose):
        nums[m.group(1) + (m.group(2) or "")] += 1
    out["numbers_in_prose"] = nums
    envs = Counter()
    for e in ("figure", "table", "algorithm", "lemma", "proposition", "theorem", "corollary", "remark", "equation", "align"):
        envs[e] = len(re.findall(r"\\begin\{" + e + r"\*?\}", body))
    out["environments"] = envs
    return out


def diff(a: dict, b: dict, allow_math_reorder: bool):
    rows = []
    for k in a:
        if allow_math_reorder and k == "inline_math":
            if sum(a[k].values()) == sum(b[k].values()):
                continue
        rem = a[k] - b[k]
        add = b[k] - a[k]
        for tok, n in sorted(rem.items()):
            rows.append((k, "-", tok, n))
        for tok, n in sorted(add.items()):
            rows.append((k, "+", tok, n))
    return rows


def collect(p: Path):
    if p.is_dir():
        return {f.name: f for f in sorted(p.glob("*.tex"))}
    return {p.name: p}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("before")
    ap.add_argument("after")
    ap.add_argument("--allow-math-reorder", action="store_true", help="only compare the count of inline-math items")
    ap.add_argument("--json")
    a = ap.parse_args(argv)
    A, B = collect(Path(a.before)), collect(Path(a.after))
    if Path(a.before).is_file() and Path(a.after).is_file():
        pairs = [(Path(a.before), Path(a.after))]
    else:
        common = sorted(set(A) & set(B))
        pairs = [(A[n], B[n]) for n in common]
        for n in sorted(set(A) ^ set(B)):
            print(f"note: {n} exists on one side only")
    report = []
    bad = 0
    for pa, pb in pairs:
        ta = tokens(pa.read_text(encoding="utf-8", errors="ignore"))
        tb = tokens(pb.read_text(encoding="utf-8", errors="ignore"))
        rows = diff(ta, tb, a.allow_math_reorder)
        report.append({"file": pb.name, "diffs": rows})
        print(f"== {pb.name}: {'IDENTICAL fact tokens' if not rows else str(len(rows)) + ' difference(s)'}")
        for k, sign, tok, n in rows[:80]:
            print(f"  {sign} [{k}] {tok!r} x{n}")
        if len(rows) > 80:
            print(f"  ... {len(rows) - 80} more")
        bad += bool(rows)
    if a.json:
        Path(a.json).write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
