#!/usr/bin/env python3
"""aggregate_floats.py - summarise floats.json / float_papers.json (markdown to stdout)."""
import json
import re
import statistics as st
import sys
from collections import Counter
from pathlib import Path

d = Path(sys.argv[1])
F = json.load(open(d / "floats.json", encoding="utf-8"))
P = json.load(open(d / "float_papers.json", encoding="utf-8"))
figs = [f for f in F if f["kind"] == "figure"]
tabs = [f for f in F if f["kind"] == "table"]
algs = [f for f in F if f["kind"] == "algorithm"]


def q(v):
    v = sorted(v)
    if not v:
        return "-"
    return f"{st.median(v):.1f} [{v[int(.25*(len(v)-1))]:.0f}-{v[int(.75*(len(v)-1))]:.0f}]"


def share(pred, pool):
    return f"{sum(1 for x in pool if pred(x))}/{len(pool)} ({100*sum(1 for x in pool if pred(x))/max(len(pool),1):.0f}%)"


print(f"# floats: {len(figs)} figures, {len(tabs)} tables, {len(algs)} algorithms, {len(P)} papers\n")
print("## Figures")
print("- caption words (main):", q([f["cap_words"] for f in figs if f["caption"]]))
print("- caption sentences:", Counter(f["cap_sents"] for f in figs if f["caption"]).most_common(5))
print("- caption ends with period:", share(lambda f: f["ends_period"], [f for f in figs if f["caption"]]))
print("- has subfigures:", share(lambda f: f["n_sub"] > 0, figs), "| sub per fig median:", q([f["n_sub"] for f in figs if f["n_sub"]]))
print("- sub-caption words:", q([w for f in figs for w in f["sub_words"]]))
print("- sub-caption ends with period:", share(lambda x: x, [e for f in figs for e in f["sub_ends_period"]]))
print("- 'versus/vs' in caption:", share(lambda f: f["versus"], figs))
print("- schematic (system model/illustration...):", share(lambda f: f["schematic"], figs))
print("- placement spec:", Counter(f["place"] for f in figs).most_common(6))
print("- figure* (double column):", share(lambda f: f["star"], figs))
print("- caption contains math:", share(lambda f: f["has_math"], figs))
print("- label prefixes:", Counter(re.split(r"[:_]", f["label"])[0].lower() for f in figs if f["label"]).most_common(6))
widths = Counter()
exts = Counter()
for f in figs:
    for opt, name in f["includes"]:
        m = re.search(r"width\s*=\s*([^,\]]+)", opt or "")
        widths[m.group(1).strip() if m else "none"] += 1
        exts[Path(name).suffix.lower() or "noext"] += 1
print("- includegraphics widths:", widths.most_common(10))
print("- graphics extensions:", exts.most_common(6))
print("\n### Caption openers (first 3 words, figures)")
op = Counter(" ".join(re.findall(r"[A-Za-z]+", f["caption"])[:3]).lower() for f in figs if f["caption"])
print(op.most_common(40))
print("\n### Caption first word")
print(Counter((re.findall(r"[A-Za-z]+", f["caption"]) or [""])[0].lower() for f in figs if f["caption"]).most_common(20))
print("\n### Sub-caption openers (first 2 words)")
print(Counter(" ".join(re.findall(r"[A-Za-z]+", s)[:2]).lower() for f in figs for s in f["sub_captions"]).most_common(25))

print("\n## Tables")
print("- caption words:", q([f["cap_words"] for f in tabs if f["caption"]]))
print("- caption ends with period:", share(lambda f: f["ends_period"], [f for f in tabs if f["caption"]]))
print("- booktabs:", share(lambda f: f["booktabs"], tabs), "| \\hline used:", share(lambda f: f["hline"] > 0, tabs))
print("- small font:", share(lambda f: f["small"], tabs), "| arraystretch:", share(lambda f: f["arraystretch"], tabs))
print("- caption before tabular:", share(lambda f: f["caption_first"], tabs))
print("- rows median:", q([f["n_rows"] for f in tabs]))
print("- placement spec:", Counter(f["place"] for f in tabs).most_common(5))
print("- caption openers:", Counter(" ".join(re.findall(r"[A-Za-z]+", f["caption"])[:3]).lower() for f in tabs if f["caption"]).most_common(20))

print("\n## Algorithms")
print("- count:", len(algs), "| papers with algorithm:", len({f['id'] for f in algs}))
print("- lines median:", q([f["n_lines"] for f in algs]))
print("- style:", Counter(f["style"] for f in algs))
print("- Require/Ensure (Input/Output):", share(lambda f: f["require_ensure"], algs), "| comments:", share(lambda f: f["has_comment"], algs), "| repeat-until:", share(lambda f: f["repeat_until"], algs))
print("- caption words:", q([f["cap_words"] for f in algs if f["caption"]]))
print("- caption ends with period:", share(lambda f: f["ends_period"], [f for f in algs if f["caption"]]))
print("- caption openers:", Counter(" ".join(re.findall(r"[A-Za-z]+", f["caption"])[:3]).lower() for f in algs if f["caption"]).most_common(15))

print("\n## Cross-references in prose")
tot = Counter()
for p in P:
    tot.update(p["fig_ref_patterns"])
n = sum(p["n_fig_ref_sents"] for p in P)
print("- sentences citing a figure:", n, "| citing a table:", sum(p["n_tab_ref_sents"] for p in P))
print("- patterns (share of figure-citing sentences):", {k: f"{100*v/n:.0f}%" for k, v in tot.most_common()})
pk = Counter()
for p in P:
    pk.update(p["pkgs"])
print("\n## Packages (papers using; of", len(P), ")")
print(pk.most_common(30))
print("- epsfig:", sum(1 for p in P if p["epsfig"]), "| captionsetup:", sum(1 for p in P if p["captionsetup"]))

print("\n## Caption samples (LOCAL READING ONLY): 60 figure captions, spread by year")
import random
random.seed(3)
S = [f for f in figs if f["caption"]]
S.sort(key=lambda f: f["pub"])
step = max(len(S) // 60, 1)
for f in S[::step][:60]:
    print(f"- [{f['id']}] {f['caption'][:190]}")
print("\n## Table caption samples")
for f in [t for t in tabs if t["caption"]][:25]:
    print(f"- [{f['id']}] {f['caption'][:160]}")
print("\n## Algorithm caption samples")
for f in [t for t in algs if t["caption"]][:20]:
    print(f"- [{f['id']}] {f['caption'][:160]}")
print("\n## Sub-caption samples")
seen = 0
for f in figs:
    if f["sub_captions"] and seen < 30:
        print(f"- [{f['id']}] main: {f['caption'][:100]} || subs: {f['sub_captions'][:3]}")
        seen += 1
