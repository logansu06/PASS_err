#!/usr/bin/env python3
"""calibrate.py - back-test rules.json on the corpus and (re)generate norms.json.

  python calibrate.py --src <dir with <id>.eprint> --meta profiles/weidong-mei/_corpus_meta.json
                      --profile weidong-mei [--write-norms] [--upstream-report out.md]

For every technical paper it runs the profile's mechanical rules (exactly as
style_gate.py does for a user's draft) and prints, per rule, the share of the
author's own papers that the rule would flag. A FAIL rule with a non-zero
share is a calibration bug. It also computes p10/p25/p50/p75/p90 of the gate's
metrics per register and writes them to profiles/<profile>/norms.json.
"""
from __future__ import annotations

import argparse
import json
import re
import statistics as st
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import style_gate as G  # noqa: E402
from style_stats import flatten, read_sources, words  # noqa: E402

UPSTREAM_M = {
    "M1 em-dash": r"---|—|–|(?<=\s)--(?=\s)",
    "M5 banned adjectives": r"\bnovel\b|\bsignificant\b|\bsubstantial\b|\bimpressive\b|\bpromising\b|\bcomprehensive\b|\brobust\b|\bpowerful\b|\bstate-of-the-art\b|\bparadigm\b|\bleverag\w*|\butiliz\w*",
    "M6 throat-clearing openers": r"(?:(?<=[.!?] )|^)(?:Moreover|Furthermore|Additionally|Notably|Importantly|Indeed|Ultimately|Crucially|In turn|That said),",
    "M6 'It is worth noting / should be noted'": r"\bIt is worth noting that\b|\bIt should be noted that\b",
    "M11 passive voice": r"\b(?:is|are|was|were|be|been|being)\s+(?:[a-z]+ed|done|made|shown|given|taken|held|built|drawn|chosen|written|known|found|seen|set|put|sent|kept|met|run|used|based)\b",
    "M12 in order to / in terms of / the fact that": r"\bthe fact that\b|\bin order to\b|\bin terms of\b|\bone of the most\b",
    "M13 weak qualifiers": r"\b(?:rather|very|pretty|little|quite|somewhat|fairly|certainly)\b",
    "M16 pompous single words": r"\bfinaliz\w*|\bfeature[ds]?\b|\bmeaningful\b|\binsightful\b|\bpossess\w*|\bcurrently\b|\bimpact(?:s|ed|ing)?\b|\bfactor\b",
    "M17 fancy verbs (delve/harness/orchestrate ...)": r"\bdelv\w+ into\b|\bharness\w*|\borchestrat\w+|\bforge[sd]?\b|\bweav\w+|\bgrappl\w+ with\b",
    "M18 'In this paper/section, we'": r"\bIn this (?:paper|section|letter),? we\b",
    "M14 firstly/secondly": r"\b(?:firstly|secondly|thirdly)\b",
    "M2 antithesis (rather than / not only ... but / on the other hand)": r"\brather than\b|\bnot only\b.{0,80}\bbut\b|\bon the other hand\b",
}


def pct(v, p):
    v = sorted(v)
    return v[int(round(p * (len(v) - 1)))] if v else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--meta", required=True)
    ap.add_argument("--profile", default="weidong-mei")
    ap.add_argument("--write-norms", action="store_true")
    ap.add_argument("--upstream-report")
    ap.add_argument("--only-technical", action="store_true", default=True)
    a = ap.parse_args()
    pdir = G.SKILL / "profiles" / a.profile
    rules = json.load(open(pdir / "rules.json", encoding="utf-8"))["rules"]
    meta = json.load(open(a.meta, encoding="utf-8"))
    tmp = Path(tempfile.mkdtemp(prefix="gate_cal_"))
    per_rule = defaultdict(list)  # id -> list of (paper, n_hits, status)
    rate_rule = defaultdict(list)
    metrics = defaultdict(lambda: defaultdict(list))  # register -> metric -> values
    up_rates = defaultdict(list)
    n_tech = 0
    examples = defaultdict(list)
    for r in meta:
        base = r["id"].split("v")[0]
        ep = Path(a.src) / f"{base}.eprint"
        if not ep.exists():
            continue
        doc_txt, _ = flatten(read_sources(ep))
        if not doc_txt:
            continue
        f = tmp / f"{base}.tex"
        f.write_text(doc_txt, encoding="utf-8")
        try:
            doc = G.Doc(f)
        except Exception as e:  # noqa: BLE001
            print("skip", base, e)
            continue
        kinds = " ".join(h["title"].lower() for h in doc.heads if h["level"] == "section")
        technical = bool(re.search(r"simulat|numerical|experiment|evaluat|result", kinds)) and bool(re.search(r"model|problem|system", kinds))
        if a.only_technical and not technical:
            continue
        n_tech += 1
        reg = G.detect_register(doc)
        res = G.run_rules(doc, rules, reg)
        for x in res:
            per_rule[x["id"]].append((base, x["n"], x["status"], reg))
            rate_rule[x["id"]].append(1000.0 * x["n"] / max(len(words(doc.prose_norm)), 1))
            if x["n"] and len(examples[x["id"]]) < 3:
                examples[x["id"]].append((base, x["hits"][:2]))
        m = G.compute_metrics(doc)
        for reg_key in (reg, "all"):
            for k, v in m.items():
                metrics[reg_key][k].append(v)
        nw = max(len(words(doc.prose_norm)), 1)
        for name, rx in UPSTREAM_M.items():
            c = len(re.findall(rx, doc.prose_norm))
            up_rates[name].append(1000.0 * c / nw)
    print(f"# back-test on {n_tech} technical papers ({a.profile})\n")
    print("| rule | sev | papers flagged | papers with any hit | median hits (papers with hits) | p90 hits | hits/1k p50 / p90 / p95 |")
    print("|---|---|---|---|---|---|---|")
    for rid, rows in per_rule.items():
        rule = next(x for x in rules if x["id"] == rid)
        flagged = sum(1 for _, n, s, _ in rows if s != "PASS")
        anyhit = [n for _, n, _, _ in rows if n > 0]
        print(f"| {rid} {rule['name'][:58]} | {rule['severity']} | {flagged}/{len(rows)} ({100*flagged/len(rows):.0f}%) | {len(anyhit)}/{len(rows)} | {st.median(anyhit) if anyhit else 0:.0f} | {pct([n for _,n,_,_ in rows], .9):.0f} | {pct(rate_rule[rid],.5):.2f} / {pct(rate_rule[rid],.9):.2f} / {pct(rate_rule[rid],.95):.2f} |")
    print("\n## examples of flagged corpus text (for calibration only; not shipped)\n")
    for rid, ex in examples.items():
        for base, hits in ex:
            for h in hits:
                print(f"- {rid} {base}: {h[2][:110]}")
    if a.write_norms:
        out = {}
        for reg, ms in metrics.items():
            out[reg] = {}
            for k, vals in ms.items():
                if len(vals) < 5:
                    continue
                out[reg][k] = {"n": len(vals), "p10": round(pct(vals, .1), 3), "p25": round(pct(vals, .25), 3), "p50": round(pct(vals, .5), 3), "p75": round(pct(vals, .75), 3), "p90": round(pct(vals, .9), 3)}
        (pdir / "norms.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
        print(f"\nwrote {pdir/'norms.json'}; registers: { {k: len(next(iter(v.values())) and [1] or []) for k, v in out.items()} }")
        print({k: max(x['n'] for x in v.values()) for k, v in out.items()})
    if a.upstream_report:
        lines = [f"# Upstream (snl-default) mechanical gate applied to {n_tech} technical papers of the corpus", "",
                 "Per-1,000-word hit rate of the upstream regexes on the author's own papers. Every non-zero row is text the upstream gate would have rejected.", "",
                 "| upstream rule | median /1k | p90 /1k | papers with >=1 hit |", "|---|---|---|---|"]
        for name, vals in up_rates.items():
            lines.append(f"| {name} | {st.median(vals):.2f} | {pct(vals,.9):.2f} | {sum(1 for v in vals if v>0)}/{len(vals)} ({100*sum(1 for v in vals if v>0)/len(vals):.0f}%) |")
        Path(a.upstream_report).write_text("\n".join(lines) + "\n", encoding="utf-8")
        print("wrote", a.upstream_report)


if __name__ == "__main__":
    main()
