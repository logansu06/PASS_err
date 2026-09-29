#!/usr/bin/env python3
"""fig_stats.py - figure / table / algorithm / caption / cross-reference habits.

Reuses the loaders in style_stats.py. Writes:
  <out>/floats.json      per-float records (caption text kept LOCAL for reading)
  <out>/float_papers.json per-paper summary (packages, placement, widths, ...)
Aggregation is done by aggregate_floats.py.
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
from collections import Counter
from pathlib import Path

from style_stats import find_cmd_args, flatten, group_at, read_sources, sentences, to_prose, words

FLOAT_RE = re.compile(r"\\begin\{(figure|table|algorithm)(\*?)\}(\[[^\]]*\])?(.*?)\\end\{\1\2\}", re.S)
SCHEMATIC = re.compile(r"illustrat|system model|diagram|scenario|architecture|framework|flow ?chart|block|setup|configuration|structure|protocol|schematic|example of|overview|timeline|frame structure|deployment", re.I)


def clean_caption(c: str) -> str:
    return re.sub(r"\s+", " ", to_prose(c)).strip()


def main_and_sub_captions(block: str):
    subs = []
    for m in re.finditer(r"\\(?:subfloat|subfigure)\s*\[", block):
        # optional-arg caption: find matching ]
        i = m.end()
        depth = 1
        j = i
        while j < len(block) and depth:
            if block[j] == "[":
                depth += 1
            elif block[j] == "]":
                depth -= 1
            j += 1
        subs.append(clean_caption(block[i : j - 1]))
    for m in re.finditer(r"\\subcaption\s*\{", block):
        g, _ = group_at(block, m.end() - 1)
        subs.append(clean_caption(g))
    for m in re.finditer(r"\\begin\{subfigure\}.*?\\end\{subfigure\}", block, re.S):
        inner = m.group(0)
        for c in find_cmd_args(inner, "caption"):
            subs.append(clean_caption(c))
    # main caption: last \caption not inside a subfigure environment
    stripped = re.sub(r"\\begin\{subfigure\}.*?\\end\{subfigure\}", "", block, flags=re.S)
    caps = find_cmd_args(stripped, "caption")
    main = clean_caption(caps[-1]) if caps else ""
    return main, [s for s in subs if s]


def analyse(eprint: Path, meta: dict):
    files = read_sources(eprint)
    doc, _ = flatten(files)
    if not doc:
        return [], {}
    pre, _, body = doc.partition(r"\begin{document}")
    body = body.split(r"\end{document}")[0]
    recs = []
    for m in FLOAT_RE.finditer(body):
        kind, star, place, blk = m.group(1), m.group(2), (m.group(3) or "")[1:-1], m.group(4)
        main, subs = main_and_sub_captions(blk)
        r = {
            "id": meta["base"],
            "pub": meta["pub"],
            "kind": kind,
            "star": bool(star),
            "place": place,
            "caption": main,
            "cap_words": len(words(main)),
            "cap_sents": len(sentences(main)) if main else 0,
            "ends_period": main.rstrip().endswith("."),
            "n_sub": len(subs),
            "sub_captions": subs,
            "sub_words": [len(words(s)) for s in subs],
            "sub_ends_period": [s.rstrip().endswith(".") for s in subs],
            "has_math": bool(re.search(r"\$[^$]+\$", "".join(find_cmd_args(blk, "caption")))),
            "label": (re.findall(r"\\label\{([^}]*)\}", blk) or [""])[-1],
            "includes": re.findall(r"\\includegraphics\s*(?:\[([^\]]*)\])?\s*\{([^}]*)\}", blk),
            "centering": r"\centering" in blk,
        }
        if kind == "figure":
            r["schematic"] = bool(SCHEMATIC.search(main))
            r["versus"] = bool(re.search(r"\bversus\b|\bvs\.?\b", main, re.I))
            r["with_params"] = bool(re.search(r"\bwith\b|\bfor\b|\bunder\b", main))
        if kind == "table":
            r["booktabs"] = bool(re.search(r"\\toprule|\\midrule", blk))
            r["hline"] = len(re.findall(r"\\hline", blk))
            r["small"] = bool(re.search(r"\\(?:small|footnotesize|scriptsize)\b", blk))
            r["arraystretch"] = "arraystretch" in blk
            r["caption_first"] = blk.find("\\caption") < blk.find("\\begin{tabular")
            r["n_rows"] = len(re.findall(r"\\\\", blk))
        if kind == "algorithm":
            r["n_lines"] = len(re.findall(r"\\(?:STATE|State|REQUIRE|ENSURE|Require|Ensure|IF|If|FOR|For|WHILE|While|REPEAT|Repeat|UNTIL|Until)\b", blk))
            r["style"] = "algorithmic" if "algorithmic" in blk else ("algpseudocode" if "algpseudocode" in pre else "other")
            r["require_ensure"] = bool(re.search(r"\\REQUIRE|\\Require|\\ENSURE|\\Ensure|\\KwIn|\\KwOut", blk))
            r["has_comment"] = bool(re.search(r"\\COMMENT|\\Comment|\\tcp", blk))
            r["repeat_until"] = bool(re.search(r"\\REPEAT|\\Repeat|\\UNTIL|\\Until", blk))
        recs.append(r)
    # cross-reference sentences
    prose = to_prose(body)
    sents = [s for p in re.split(r"\n\s*\n", prose) for s in sentences(p)]
    fig_sents = [s for s in sents if re.search(r"\bFigs?\.?\s*REF", s)]
    tab_sents = [s for s in sents if re.search(r"\bTable\s*REF", s)]
    pats = Counter()
    for s in fig_sents:
        if re.search(r"\b(?:as )?(?:shown|illustrated|depicted) in Fig", s, re.I):
            pats["as_shown_in"] += 1
        if re.search(r"\bwe plot(?: in)?\b|\bplot(?:s|ted)? in Fig|we show in Fig|we present in Fig|we compare .* in Fig", s, re.I):
            pats["we_plot"] += 1
        if re.match(r"(?:In|From) Fig", s):
            pats["sentence_initial_In_Fig"] += 1
        if re.match(r"Fig(?:s)?\.?\s*REF(?:\([a-z]\))?\s+(?:shows?|plots?|illustrates?|depicts?|compares?|presents?)", s):
            pats["Fig_shows"] += 1
        if re.search(r"\bsee Fig|\(see Fig|\(Fig", s):
            pats["parenthetical"] += 1
        if re.search(r"\bFigs\.", s):
            pats["Figs_plural"] += 1
    summary = {
        "id": meta["base"],
        "n_fig_ref_sents": len(fig_sents),
        "n_tab_ref_sents": len(tab_sents),
        "fig_ref_patterns": dict(pats),
        "pkgs": sorted(set(re.findall(r"\\usepackage(?:\[[^\]]*\])?\{([^}]*)\}", pre) and [p.strip() for g in re.findall(r"\\usepackage(?:\[[^\]]*\])?\{([^}]*)\}", pre) for p in g.split(",")])),
        "epsfig": "epsfig" in pre,
        "captionsetup": "captionsetup" in pre,
    }
    return recs, summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--meta", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    meta = json.load(open(a.meta, encoding="utf-8"))
    allrecs, sums = [], []
    for r in meta:
        base = r["id"].split("v")[0]
        r["base"] = base
        p = Path(a.src) / f"{base}.eprint"
        if not p.exists():
            continue
        try:
            recs, s = analyse(p, r)
        except Exception as e:
            print("error", base, repr(e))
            continue
        allrecs += recs
        sums.append(s)
    json.dump(allrecs, open(out / "floats.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(sums, open(out / "float_papers.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(allrecs), "floats from", len(sums), "papers;", Counter(r["kind"] for r in allrecs))


if __name__ == "__main__":
    main()
