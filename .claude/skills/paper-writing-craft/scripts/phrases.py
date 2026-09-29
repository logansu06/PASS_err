#!/usr/bin/env python3
"""phrases.py - document-frequency of n-grams and of individual gate words.

Reads out/per_paper.json (for technical/survey split) and out/texts/<id>.txt (cleaned prose).
Prints markdown. Shipped output is aggregate only.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

d = Path(sys.argv[1])
R = json.load(open(d / "per_paper.json", encoding="utf-8"))


def ptype(r):
    return "technical" if ("sim" in r["kinds"] and "model" in r["kinds"]) else "survey"


tech = [r for r in R if ptype(r) == "technical"]
N = len(tech)


def load(r):
    t = (d / "texts" / f"{r['id']}.txt").read_text(encoding="utf-8")
    # drop appendix-ish and heading markers
    t = re.sub(r"^#+ .*$", " ", t, flags=re.M)
    return t


docs = {r["id"]: load(r) for r in tech}
TOK = re.compile(r"[a-z][a-z'\-]*|math|dmath", re.I)


def toks(t):
    return [w.lower() for w in TOK.findall(t)]


print(f"# phrase document-frequency over {N} technical papers\n")
for n, minfrac in [(3, 0.55), (4, 0.40), (5, 0.30), (6, 0.25)]:
    df = Counter()
    for t in docs.values():
        w = toks(t)
        seen = set()
        for i in range(len(w) - n + 1):
            g = tuple(w[i : i + n])
            if any(x in ("math", "dmath") for x in g):
                continue
            seen.add(g)
        df.update(seen)
    keep = [(g, c) for g, c in df.items() if c >= minfrac * N]
    keep.sort(key=lambda x: -x[1])
    print(f"\n## {n}-grams in >= {int(minfrac*100)}% of papers ({len(keep)})\n")
    out = []
    for g, c in keep[:120]:
        out.append(f"{' '.join(g)} ({c})")
    print("; ".join(out))

# individual words / phrases: number of papers using at least once, and total count
WORDS = {
    "novel": r"\bnovel\b", "promising": r"\bpromising\b", "significant(ly)": r"\bsignificant(?:ly)?\b", "substantial(ly)": r"\bsubstantial(?:ly)?\b",
    "state-of-the-art": r"state-of-the-art", "comprehensive": r"\bcomprehensive\b", "robust": r"\brobust\b", "powerful": r"\bpowerful\b", "leverage": r"\bleverag\w+",
    "utilize": r"\butiliz\w+", "paradigm": r"\bparadigm\b", "seamless": r"\bseamless\w*\b", "crucial/critical": r"\b(?:crucial|critical)\b", "appealing": r"\bappealing\b",
    "great/considerable": r"\b(?:great|considerable|substantially|remarkabl\w+|dramatic\w*)\b", "significant performance": r"significant (?:performance|gain|improvement|throughput)",
    "Moreover": r"\bMoreover\b", "Furthermore": r"\bFurthermore\b", "Additionally": r"\bAdditionally\b", "Notably": r"\bNotably\b", "Importantly": r"\bImportantly\b", "Indeed": r"\bIndeed\b",
    "In addition": r"\bIn addition\b", "Besides": r"\bBesides\b", "Nonetheless": r"\bNonetheless\b", "Accordingly": r"\bAccordingly\b", "Hence": r"\bHence\b", "Thus": r"\bThus\b",
    "Therefore": r"\bTherefore\b", "Consequently": r"\bConsequently\b", "As a result": r"\bAs a result\b", "Meanwhile": r"\bMeanwhile\b", "Similarly": r"\bSimilarly\b", "In contrast": r"\bIn contrast\b",
    "On the other hand": r"\bOn the other hand\b", "On the one hand": r"\bOn the one hand\b", "Nevertheless": r"\bNevertheless\b",
    "It is worth noting": r"\bIt is worth (?:noting|mentioning|pointing out)\b", "worth mentioning/noting (any)": r"\bworth(?:y)? (?:of )?(?:noting|mentioning|pointing out|further noting)\b",
    "Note that": r"\bNote that\b", "It should be noted": r"\bIt should be (?:noted|mentioned|emphasized)\b", "It is noted": r"\bIt is (?:noted|mentioned|emphasized)\b",
    "In this paper, we": r"\bIn this (?:paper|letter|article|work),? we\b", "In this section, we": r"\bIn this section,? we\b", "In order to": r"\bin order to\b", "so as to": r"\bso as to\b",
    "as compared to/with": r"\bas compared (?:to|with)\b", "compared with/to": r"\bcompared (?:with|to)\b", "thanks to": r"\bthanks to\b", "w.r.t.": r"\bw\.r\.t\.?",
    "due to": r"\bdue to\b", "owing to": r"\bowing to\b", "the fact that": r"\bthe fact that\b", "delve": r"\bdelv\w+\b", "dispense with": r"\bdispens\w+ with\b", "circumvent": r"\bcircumvent\w*\b",
    "unveil/reveal/uncover": r"\b(?:unveil\w*|reveal\w*|uncover\w*)\b", "insight(s)": r"\binsights?\b", "shed light": r"\bshed(?:s|ding)? light\b", "tackle": r"\btackl\w+\b", "resort to": r"\bresort(?:ing)? to\b",
    "very": r"\bvery\b", "quite": r"\bquite\b", "rather than": r"\brather than\b", "not only ... but": r"\bnot only\b", "in fact": r"\bin fact\b", "indeed": r"\bindeed\b", "actually": r"\bactually\b",
    "essentially/fundamentally": r"\b(?:essentially|fundamentally|inherently)\b", "simply": r"\bsimply\b", "truly/really": r"\b(?:truly|really|genuinely)\b",
    "exclamation": r"!", "question mark": r"\?", "em-dash": r"---|—|\s--\s",
    "It can be shown/verified": r"\bit can be (?:shown|verified|proved|proven|readily shown|easily shown|easily verified)\b", "It is not difficult to": r"\bit is not difficult to\b",
    "It is easy to": r"\bit is (?:easy|straightforward|readily seen)\b",
    "It is observed/seen that": r"\bIt is (?:observed|seen|found) that\b", "it can be observed/seen": r"\bit can be (?:observed|seen)\b", "It is interesting to": r"\bIt is (?:interesting|intriguing) to\b",
    "as expected": r"\bas expected\b", "This is because": r"\bThis is (?:because|due to|attributed to|mainly because)\b", "The reason is": r"\bThe (?:reason|main reason) (?:is|lies)\b",
    "In particular": r"\bIn particular\b", "Specifically": r"\bSpecifically\b", "Particularly": r"\bParticularly\b", "For example": r"\bFor (?:example|instance)\b",
    "Motivated by": r"\bMotivated by\b", "To this end": r"\bTo this end\b", "To tackle/address/overcome": r"\bTo (?:tackle|address|overcome|solve|handle|resolve|deal with)\b",
    "to gain insights": r"\bto (?:gain|draw|obtain|drive|unveil|reveal)\b[^.]{0,30}\binsights?\b", "the authors": r"\b[Tt]he authors? (?:in|of)\b", "termed as/named": r"\b(?:termed|named|referred to as|called)\b",
    "unlike": r"\b(?:[Uu]nlike|[Dd]ifferent from|[Ii]n contrast to)\b", "it remains": r"\b(?:it remains|remains) (?:an )?(?:open|unclear|unknown|challenging)\b",
    "to the best of our knowledge": r"[Tt]o the best of our knowledge", "for the first time": r"\bfor the first time\b", "we believe": r"\bwe (?:believe|hope|envision|anticipate)\b",
    "future work": r"\bfuture (?:work|research|direction|study)\b", "extend": r"\bextend\w*\b",
    "high-quality suboptimal": r"\bhigh-quality (?:sub)?optimal|near-optimal|sub-?optimal\b", "closed-form": r"\bclosed-form\b", "computational complexity": r"\bcomplexity\b",
    "significantly outperform": r"\bsignificantly outperform\w*|\boutperform\w*\b", "superiority": r"\b(?:superior|superiority|effectiveness|efficacy)\b",
    "gain(s)": r"\bgains?\b", "trade-off": r"\btrade-?offs?\b",
}
print("\n\n# gate words: papers using at least once / total occurrences (technical papers)\n")
print("| word | papers | share | total | per 1k words |")
print("|---|---|---|---|---|")
tot_words = sum(len(toks(t)) for t in docs.values())
rows = []
for k, rx in WORDS.items():
    rgx = re.compile(rx)
    np_, tot = 0, 0
    for t in docs.values():
        c = len(rgx.findall(t))
        np_ += c > 0
        tot += c
    rows.append((k, np_, tot))
for k, np_, tot in rows:
    print(f"| {k} | {np_}/{N} | {100*np_/N:.0f}% | {tot} | {1000*tot/tot_words:.2f} |")

# caption case for figures/tables/algorithms
F = json.load(open(d / "floats.json", encoding="utf-8"))
tech_ids = {r["id"] for r in tech}


def case(s):
    ws = [w for w in re.findall(r"[A-Za-z][A-Za-z'\-]*", s)]
    ws = [w for w in ws if len(w) > 3 and not w.isupper()]
    if len(ws) < 2:
        return "n/a"
    cap = sum(1 for w in ws if w[0].isupper())
    frac = cap / len(ws)
    return "title" if frac >= 0.6 else "sentence" if frac <= 0.34 else "mixed"


print("\n\n# caption case (technical papers)\n")
for kind in ["figure", "table", "algorithm"]:
    c = Counter(case(f["caption"]) for f in F if f["kind"] == kind and f["id"] in tech_ids and f["caption"])
    print(f"- {kind}: {dict(c)}")
sub = Counter()
for f in F:
    if f["kind"] == "figure" and f["id"] in tech_ids:
        for s in f["sub_captions"]:
            sub[case(s)] += 1
print("- sub-captions:", dict(sub))

print("\n\n# abstract first sentences (first 12 words), technical papers (LOCAL)\n")
for r in tech:
    print(f"- {r['id']}: {r['abstract_first']}")
print("\n\n# intro paragraph-first sentences (first 14 words), technical papers (LOCAL)\n")
for r in tech[:45]:
    print(f"- {r['id']}: {' || '.join(r['intro_first_sents'])}")
print("\n\n# simulation first sentence, conclusion first sentence (LOCAL)\n")
for r in tech:
    print(f"- {r['id']}: SIM: {r['sim_first_sent']} | CONC: {r['concl_first_sent']}")
