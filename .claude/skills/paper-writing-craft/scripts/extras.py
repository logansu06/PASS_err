#!/usr/bin/env python3
"""extras.py - letter vs journal register, title patterns, citation/typography habits."""
import json
import re
import statistics as st
import sys
from collections import Counter
from pathlib import Path

from style_stats import flatten, read_sources

d = Path(sys.argv[1])
R = json.load(open(d / "per_paper.json", encoding="utf-8"))
M = {r["id"].split("v")[0]: r for r in json.load(open(sys.argv[2], encoding="utf-8"))}


def ptype(r):
    return "technical" if ("sim" in r["kinds"] and "model" in r["kinds"]) else "survey"


def q(v):
    v = sorted(v)
    return "-" if not v else f"{st.median(v):.1f} [{v[int(.25*(len(v)-1))]:.0f}-{v[int(.75*(len(v)-1))]:.0f}]"


tech = [r for r in R if ptype(r) == "technical"]
for r in tech:
    t = (d / "texts" / f"{r['id']}.txt").read_text(encoding="utf-8")
    r["letter"] = bool(re.search(r"\b[Tt]his letter\b|\b[Ii]n this letter\b", t))
    r["paper_word"] = bool(re.search(r"\b[Tt]his paper\b|\b[Ii]n this paper\b", t))
for r in tech:
    r["conference"] = (not r["letter"]) and ("conference" in r["docclass"])
groups = {
    "letter": [r for r in tech if r["letter"]],
    "conference": [r for r in tech if r["conference"]],
    "full paper": [r for r in tech if not r["letter"] and not r["conference"]],
}
print("# register split (technical)\n")
print("| metric | " + " | ".join(f"{k} (n={len(v)})" for k, v in groups.items()) + " |")
print("|---|" + "---|" * len(groups))
rows = [
    ("body words", lambda r: r["all"]["n_words"]),
    ("abstract words", lambda r: r["abstract_words"]),
    ("intro words", lambda r: r["words_by_kind"].get("intro", 0)),
    ("intro paragraphs", lambda r: r["intro_n_par"]),
    ("sections", lambda r: r["n_sections"]),
    ("subsections", lambda r: r["n_subsections"]),
    ("display eq", lambda r: r["n_display"]),
    ("figures", lambda r: r["n_figs"]),
    ("bibitems", lambda r: r["bibitems"]),
    ("sim words", lambda r: r["words_by_kind"].get("sim", 0)),
    ("conclusion words", lambda r: r["words_by_kind"].get("conclusion", 0)),
    ("sentence mean", lambda r: r["all"]["sent_mean"]),
    ("algorithms", lambda r: r["env_algorithm"]),
    ("lemma+prop+thm+cor", lambda r: r["env_lemma"] + r["env_proposition"] + r["env_theorem"] + r["env_corollary"]),
    ("remarks", lambda r: r["env_remark"]),
    ("appendix words", lambda r: r["appendix_words"]),
]
for k, fn in rows:
    print(f"| {k} | " + " | ".join(q([fn(r) for r in v]) for v in groups.values()) + " |")


def sh(v, pred):
    return f"{sum(1 for r in v if pred(r))}/{len(v)} ({100*sum(1 for r in v if pred(r))/max(len(v),1):.0f}%)"


for label, pred in [
    ("contribution list", lambda r: r["contrib"]["has_list"]),
    ("'organized as follows'", lambda r: r["has_organized"]),
    ("Notations paragraph", lambda r: r["notation_loc"] != "none"),
    ("(P1)-style labels", lambda r: r["problem_labels"] > 0),
    ("has algorithm", lambda r: r["env_algorithm"] > 0),
    ("has remark", lambda r: r["env_remark"] > 0),
    ("has lemma/prop/thm", lambda r: r["env_lemma"] + r["env_proposition"] + r["env_theorem"] + r["env_corollary"] > 0),
    ("has appendix", lambda r: r["appendix_words"] > 0),
    ("future work in conclusion", lambda r: r["concl_future"]),
]:
    print(f"- {label}: " + " | ".join(f"{k}: {sh(v, pred)}" for k, v in groups.items()))

print("\n# by 'tense of conclusion opener' and era")
past = Counter()
for r in tech:
    s = r["concl_first_sent"].lower()
    y = int(r["pub"][:4])
    era = "<=2022" if y <= 2022 else ">=2023"
    m = re.search(r"\b(?:paper|letter|work)\s+(?:has |have )?(\w+)", s) or re.search(r"\bwe\s+(?:have\s+)?(\w+)", s)
    verb = m.group(1) if m else "?"
    tense = "past" if verb.endswith("ed") or verb in ("proposed", "considered", "studied") else "present" if verb.endswith("s") else "other"
    past[(era, tense)] += 1
print(dict(past))

print("\n# titles (all 102 papers)\n")
titles = [M[k]["title"] for k in M]
wc = [len(re.findall(r"[A-Za-z0-9\-]+", t)) for t in titles]
print("- words in title:", q(wc))
print("- has colon:", sum(":" in t for t in titles), "/", len(titles))
print("- question form:", sum(t.strip().endswith("?") for t in titles), "/", len(titles))
pat = {
    "X-Enabled/Enhanced/Aided/Assisted/Empowered/Empowering": r"\b(?:Enabled|Enhanced|Aided|Assisted|Empowered|Enhancing|Empowering|Enabling|Assisting)\b",
    "Optimization": r"\bOptimization\b",
    "Design": r"\bDesign\b",
    "Performance Analysis": r"\bPerformance Analysis\b|\bAnalysis\b",
    "Tutorial/Survey/Overview": r"\bTutorial\b|\bSurvey\b|\bOverview\b|\bFundamentals\b",
    "Meet(s)": r"\bMeets?\b",
    "Joint": r"\bJoint\b",
    "for/via/with": r"\b(?:for|via|with|in)\b",
    "'A ... Approach/Perspective'": r"\b(?:Approach|Perspective|Framework)\b",
}
for k, rx in pat.items():
    print(f"- {k}: {sum(bool(re.search(rx, t)) for t in titles)}")
print("- title case (each major word capitalised):", sum(1 for t in titles if all(w[0].isupper() or not w[0].isalpha() or w.lower() in ('a','an','the','of','for','in','on','with','via','and','to','by','at','or','as','from','under') for w in re.findall(r"[A-Za-z][A-Za-z\-]*", t))), "/", len(titles))
print("- title samples: ")
for t in titles[:12]:
    print("   ", t)

print("\n# citation / typography habits (all sources)\n")
cnt = Counter()
multi = []
per_cite_len = []
for r in R:
    doc, bbl = flatten(read_sources(d.parent / "src" / f"{r['id']}.eprint"))
    body = doc.partition(r"\begin{document}")[2]
    cnt["cite_total"] += len(re.findall(r"\\cite\w*\{", body))
    cnt["tilde_cite"] += len(re.findall(r"~\\cite\w*\{", body))
    cnt["space_cite"] += len(re.findall(r"[^~\s\{\(\[]\s+\\cite\w*\{", body))
    cnt["In_cite_sentence"] += len(re.findall(r"(?:^|[.!?]\s+)In~?\s*\\cite\w*\{", body, re.M))
    cnt["authors_in_cite"] += len(re.findall(r"authors? (?:in|of)~?\s*\\cite", body))
    cnt["see_cite"] += len(re.findall(r"\((?:see|e\.g\.,?|cf\.)\s*(?:~)?\\cite|\bsee(?:,? e\.g\.,)?~?\\cite", body))
    for m in re.finditer(r"\\cite\w*\{([^}]*)\}", body):
        per_cite_len.append(len(m.group(1).split(",")))
    cnt["nonbreaking_tilde_Fig"] += len(re.findall(r"Fig\.~", body))
    cnt["space_Fig"] += len(re.findall(r"Fig\.\s\\ref", body))
    cnt["Section_tilde"] += len(re.findall(r"Section~", body))
    cnt["Section_space"] += len(re.findall(r"Section\s\\ref", body))
    cnt["math_dash_ndash"] += len(re.findall(r"\$-\$|\\text\{-\}", body))
    cnt["etal"] += len(re.findall(r"et al\.", body))
    cnt["wrt"] += len(re.findall(r"w\.r\.t\.", body))
    cnt["ie_comma"] += len(re.findall(r"i\.e\.,", body))
    cnt["ie_nocomma"] += len(re.findall(r"i\.e\.\s+[a-z\\$]", body))
    cnt["eg_comma"] += len(re.findall(r"e\.g\.,", body))
    cnt["bibstyle_IEEEtran"] += 1 if "IEEEtran" in re.findall(r"\\bibliographystyle\{([^}]*)\}", body + doc)[:1] else 0
    cnt["emph_total"] += len(re.findall(r"\\emph\{|\\textit\{", body))
    cnt["textbf_total"] += len(re.findall(r"\\textbf\{", body))
    cnt["footnote"] += len(re.findall(r"\\footnote\{", body))
    cnt["papers"] += 1
print(dict(cnt))
print("- citations per \\cite command:", Counter(per_cite_len).most_common(8))
print("- share of cites with ~ before:", f"{100*cnt['tilde_cite']/cnt['cite_total']:.0f}%")
print("- Fig.~ vs 'Fig. \\ref':", cnt["nonbreaking_tilde_Fig"], cnt["space_Fig"])
print("- Section~ vs 'Section \\ref':", cnt["Section_tilde"], cnt["Section_space"])
print("- i.e., vs i.e. no comma:", cnt["ie_comma"], cnt["ie_nocomma"])
