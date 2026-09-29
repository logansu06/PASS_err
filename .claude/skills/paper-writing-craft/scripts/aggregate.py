#!/usr/bin/env python3
"""aggregate.py - turn per_paper.json into medians/IQRs by stratum (markdown to stdout)."""
import json
import statistics as st
import sys
from collections import Counter
from pathlib import Path

R = json.load(open(Path(sys.argv[1]) / "per_paper.json", encoding="utf-8"))


def ptype(r):
    return "technical" if ("sim" in r["kinds"] and "model" in r["kinds"]) else "survey"


def era(r):
    y = int(r["pub"][:4])
    return "2016-19" if y <= 2019 else "2020-22" if y <= 2022 else "2023-26"


for r in R:
    r["ptype"] = ptype(r)
    r["era"] = era(r)
    r["role"] = "first" if r["pos"] == 1 else ("last" if r["pos"] == r["n_authors"] else "middle")


def q(v):
    v = sorted(v)
    if not v:
        return "-"
    def pct(p):
        return v[int(round(p * (len(v) - 1)))]
    return f"{st.median(v):.1f} [{pct(.25):.1f}-{pct(.75):.1f}]"


def rate(r, key, part="all"):
    d = r[part]
    return 1000.0 * d.get("lex_" + key, d.get(key, 0)) / max(d["n_words"], 1)


def table(title, groups, fns):
    print(f"\n### {title}\n")
    names = list(groups)
    print("| metric | " + " | ".join(f"{n} (n={len(groups[n])})" for n in names) + " |")
    print("|---|" + "---|" * len(names))
    for label, fn in fns:
        print(f"| {label} | " + " | ".join(q([fn(r) for r in groups[n]]) for n in names) + " |")


tech = [r for r in R if r["ptype"] == "technical"]
surv = [r for r in R if r["ptype"] == "survey"]
print(f"# corpus: {len(R)} papers; technical={len(tech)}, survey/tutorial/magazine={len(surv)}")
print("first-author:", sum(r["role"] == "first" for r in R), "| middle:", sum(r["role"] == "middle" for r in R), "| last:", sum(r["role"] == "last" for r in R))
print("eras:", Counter(r["era"] for r in R))
print("docclass:", Counter(r["docclass"].split("[")[0] + ("[journal]" if "journal" in r["docclass"] else "[conf]" if "conference" in r["docclass"] else "") for r in R))

G = {"technical": tech, "survey": surv}
core = [
    ("words (body, no appendix)", lambda r: r["all"]["n_words"]),
    ("sentence mean (words)", lambda r: r["all"]["sent_mean"]),
    ("sentence median", lambda r: r["all"]["sent_median"]),
    ("sentence p90", lambda r: r["all"]["sent_p90"]),
    ("share of sentences >40 words", lambda r: r["all"]["sent_gt40"]),
    ("sentences per paragraph", lambda r: r["all"]["par_sent_mean"]),
    ("abstract words", lambda r: r["abstract_words"]),
    ("abstract sentences", lambda r: r["abstract_sents"]),
    ("abstract mentions simulation/numerical", lambda r: float(r["abstract_has_sim"])),
    ("abstract has quantified number", lambda r: float(r["abstract_has_number"])),
    ("abstract 'we' count", lambda r: r["abstract_we"]),
    ("n keywords", lambda r: r["n_keywords"]),
    ("sections", lambda r: r["n_sections"]),
    ("subsections", lambda r: r["n_subsections"]),
    ("intro words", lambda r: r["words_by_kind"].get("intro", 0)),
    ("intro paragraphs", lambda r: r["intro_n_par"]),
    ("intro cites", lambda r: r["cites_in_intro"]),
    ("total cites", lambda r: r["cites_total"]),
    ("bibitems", lambda r: r["bibitems"]),
    ("sim words", lambda r: r["words_by_kind"].get("sim", 0)),
    ("conclusion words", lambda r: r["words_by_kind"].get("conclusion", 0)),
    ("display equations", lambda r: r["n_display"]),
    ("inline math per 1k words", lambda r: 1000 * r["n_inline"] / max(r["all"]["n_words"], 1)),
    ("lemma+proposition+theorem+corollary", lambda r: r["env_lemma"] + r["env_proposition"] + r["env_theorem"] + r["env_corollary"]),
    ("remarks", lambda r: r["env_remark"]),
    ("algorithms", lambda r: r["env_algorithm"]),
    ("figures", lambda r: r["n_figs"]),
    ("tables", lambda r: r["n_tabs"]),
    ("caption words", lambda r: r["caption_words_mean"]),
    ("appendix words", lambda r: r["appendix_words"]),
]
table("Structure and size", G, core)

lex_keys = [
    "we", "our", "the_authors", "passive", "specifically", "in_particular", "moreover", "furthermore", "additionally", "however", "therefore",
    "first_second", "for_example", "to_this_end", "note_that", "it_is_worth", "it_can_be_shown", "as_shown_in", "it_is_observed",
    "one_can_observe", "as_expected", "this_is_because", "this_implies", "without_loss", "in_this_paper", "this_paper", "respectively",
    "denotes", "where", "ie_eg", "etc", "may_might_could", "can", "potentially", "expect", "novel", "promising", "significantly", "soa",
    "robust_comprehensive", "efficient_effective", "critical_crucial", "emerged", "recently", "envision", "emdash", "semicolon", "colon", "question", "exclaim", "paren",
]
table("Lexical and punctuation rates per 1,000 prose words (whole body)", G, [(k, (lambda k: lambda r: rate(r, k))(k)) for k in lex_keys])

# by era / role among technical papers
E = {e: [r for r in tech if r["era"] == e] for e in ["2016-19", "2020-22", "2023-26"]}
table("Technical papers by era", E, [
    ("sentence mean", lambda r: r["all"]["sent_mean"]),
    ("abstract words", lambda r: r["abstract_words"]),
    ("intro words", lambda r: r["words_by_kind"].get("intro", 0)),
    ("passive /1k", lambda r: rate(r, "passive")),
    ("we /1k", lambda r: rate(r, "we")),
    ("Note that /1k", lambda r: rate(r, "note_that")),
    ("Specifically /1k", lambda r: rate(r, "specifically")),
    ("Moreover+Furthermore /1k", lambda r: rate(r, "moreover") + rate(r, "furthermore")),
    ("However /1k", lambda r: rate(r, "however")),
    ("emerged/attention /1k (intro)", lambda r: rate(r, "emerged", "intro_stats")),
    ("display eq", lambda r: r["n_display"]),
    ("props/lemmas", lambda r: r["env_lemma"] + r["env_proposition"] + r["env_theorem"] + r["env_corollary"]),
    ("figures", lambda r: r["n_figs"]),
])
Rl = {e: [r for r in tech if r["role"] == e] for e in ["first", "middle", "last"]}
table("Technical papers by author position (does style shift with role?)", Rl, [
    ("sentence mean", lambda r: r["all"]["sent_mean"]),
    ("sentence p90", lambda r: r["all"]["sent_p90"]),
    ("abstract words", lambda r: r["abstract_words"]),
    ("intro words", lambda r: r["words_by_kind"].get("intro", 0)),
    ("passive /1k", lambda r: rate(r, "passive")),
    ("we /1k", lambda r: rate(r, "we")),
    ("Note that /1k", lambda r: rate(r, "note_that")),
    ("Specifically /1k", lambda r: rate(r, "specifically")),
    ("Moreover+Furthermore /1k", lambda r: rate(r, "moreover") + rate(r, "furthermore")),
    ("this_is_because /1k", lambda r: rate(r, "this_is_because")),
    ("novel /1k", lambda r: rate(r, "novel")),
    ("figures", lambda r: r["n_figs"]),
])

# structural counts
def cnt(label, pred, pool=tech):
    n = sum(1 for r in pool if pred(r))
    print(f"- {label}: {n}/{len(pool)} ({100*n/len(pool):.0f}%)")

print("\n### Structural habits (technical papers)\n")
cnt("has a separate Related Work section", lambda r: r["has_related_section"])
cnt("intro has contribution list", lambda r: r["contrib"]["has_list"])
cnt("intro states 'organized as follows'", lambda r: r["has_organized"])
cnt("has 'Notation:' paragraph", lambda r: r["notation_loc"] != "none")
print("  - notation location:", Counter(r["notation_loc"] for r in tech))
cnt("abstract mentions simulation/numerical", lambda r: r["abstract_has_sim"])
cnt("abstract has a quantified number", lambda r: r["abstract_has_number"])
cnt("conclusion mentions future work / open direction", lambda r: r["concl_future"])
cnt("uses remarks", lambda r: r["env_remark"] > 0)
cnt("uses lemma/proposition/theorem/corollary", lambda r: r["env_lemma"] + r["env_proposition"] + r["env_theorem"] + r["env_corollary"] > 0)
cnt("uses algorithm float", lambda r: r["env_algorithm"] > 0)
cnt("labels problems (P1)-style", lambda r: r["problem_labels"] > 0)
cnt("has appendix", lambda r: r["appendix_words"] > 0)
print("- contribution list kind:", Counter(r["contrib"].get("kind") for r in tech if r["contrib"]["has_list"]))
print("- contribution items median:", q([r["contrib"]["n_items"] for r in tech if r["contrib"]["has_list"]]))
print("- contribution item words median:", q([r["contrib"]["item_words_mean"] for r in tech if r["contrib"]["has_list"]]))
print("- items with bold/emph lead label (share of lists):", sum(1 for r in tech if r["contrib"]["has_list"] and r["contrib"]["lead_labelled"] > 0), "/", sum(1 for r in tech if r["contrib"]["has_list"]))
print("- display eq punctuation (all display eqs):", Counter({k: sum(r["display_punct"].get(k, 0) for r in tech) for k in ["comma", "period", "none"]}))
print("- ref habits: Section~\\ref", sum(r["ref_Section"] for r in R), "| Fig.~\\ref", sum(r["ref_Fig"] for r in R), "| Figure~\\ref", sum(r["ref_Figure"] for r in R), "| \\eqref", sum(r["ref_eqref"] for r in R), "| (\\ref{})", sum(r["ref_paren_ref"] for r in R), "| Eq/Equation \\ref", sum(r["ref_Eq"] for r in R))
print("- caption ends with period share (median):", q([r["caption_ends_period"] for r in tech]))

print("\n### Section-title skeleton (technical): top titles and patterns\n")
titles = Counter()
for r in tech:
    for s in r["sections"]:
        t = s.lower()
        if t.startswith(("proof", "appendix")):
            continue
        titles[t] += 1
for t, n in titles.most_common(30):
    print(f"- {t}: {n}")
print("\nsection count distribution:", Counter(r["n_sections"] - sum(1 for s in r["sections"] if s.lower().startswith(("proof", "appendix"))) for r in tech))
print("\nkind sequences:")
seqs = Counter(" > ".join(k for k in r["kinds"] if k != "appendix") for r in tech)
for s, n in seqs.most_common(10):
    print(f"- {n}x {s}")

print("\n### Sentence-initial words (all prose, top 40; per-paper share median)\n")
fw = Counter()
tot = 0
for r in tech:
    for w, n in r["all"]["first_words"].items():
        fw[w] += n
        tot += n
print(", ".join(f"{w}:{100*n/tot:.1f}%" for w, n in fw.most_common(40)))
print("\n### 'we' + verb (top 30)\n")
wv = Counter()
for r in tech:
    for w, n in r["all"]["we_verbs"].items():
        wv[w] += n
print(", ".join(f"{w}:{n}" for w, n in wv.most_common(30)))

print("\n### Intro sentence-initial words (top 25)\n")
fi = Counter()
ti = 0
for r in tech:
    for w, n in r["intro_stats"]["first_words"].items():
        fi[w] += n
        ti += n
print(", ".join(f"{w}:{100*n/ti:.1f}%" for w, n in fi.most_common(25)))
print("\n### Sim-section sentence-initial words (top 25)\n")
fs = Counter()
ts = 0
for r in tech:
    for w, n in r["sim_stats"]["first_words"].items():
        fs[w] += n
        ts += n
print(", ".join(f"{w}:{100*n/ts:.1f}%" for w, n in fs.most_common(25)))

print("\n### Contribution lead-ins and item openers\n")
for r in tech:
    if r["contrib"]["has_list"]:
        print(f"- {r['id']}: {r['contrib']['lead_in']} || {dict(list(r['contrib']['first_words'].items())[:4])}")
