#!/usr/bin/env python3
"""style_stats.py - aggregate, prose-free style statistics over arXiv e-print sources.

Input : a directory of `<arxiv-id>.eprint` files (tar.gz or single .gz LaTeX source)
        plus a metadata JSON (list of {id, title, authors, pub, ...}).
Output: <out>/per_paper.json   one record of statistics per paper
        <out>/texts/<id>.txt   cleaned prose per section (LOCAL READING ONLY, never ship)

Stdlib only. Statistics are approximate (regex-based); they are meant to rank
stylistic tendencies, not to be exact linguistics.
"""
from __future__ import annotations

import argparse
import gzip
import io
import json
import re
import statistics
import tarfile
from collections import Counter
from pathlib import Path

# --------------------------------------------------------------------------
# source loading
# --------------------------------------------------------------------------


def _decode(b: bytes) -> str:
    for enc in ("utf-8", "latin-1"):
        try:
            return b.decode(enc)
        except UnicodeDecodeError:
            continue
    return b.decode("utf-8", "ignore")


def read_sources(path: Path) -> dict[str, str]:
    data = path.read_bytes()
    files: dict[str, str] = {}
    try:
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:*") as t:
            for m in t.getmembers():
                if m.isfile() and m.name.lower().endswith((".tex", ".bbl")):
                    f = t.extractfile(m)
                    if f:
                        files[m.name] = _decode(f.read())
        if files:
            return files
    except tarfile.TarError:
        pass
    try:
        raw = gzip.decompress(data)
    except OSError:
        raw = data
    files["main.tex"] = _decode(raw)
    return files


def strip_comments(t: str) -> str:
    return "\n".join(re.sub(r"(?<!\\)%.*", "", ln) for ln in t.split("\n"))


def flatten(files: dict[str, str]) -> tuple[str, str]:
    """Return (main tex with \\input resolved, concatenated bbl)."""
    tex = {k: strip_comments(v) for k, v in files.items() if k.lower().endswith(".tex")}
    bbl = "\n".join(v for k, v in files.items() if k.lower().endswith(".bbl"))
    mains = [k for k, v in tex.items() if r"\begin{document}" in v]
    if not mains:
        return "", bbl
    main = max(mains, key=lambda k: len(tex[k]))
    by_base = {Path(k).name: v for k, v in tex.items()}
    by_stem = {Path(k).stem: v for k, v in tex.items()}

    def resolve(text: str, depth=0) -> str:
        if depth > 6:
            return text

        def rep(m):
            name = m.group(1).strip()
            body = by_base.get(name) or by_base.get(name + ".tex") or by_stem.get(Path(name).stem)
            return resolve(body, depth + 1) if body else ""

        return re.sub(r"\\(?:input|include)\s*\{([^}]*)\}", rep, text)

    return resolve(tex[main]), bbl


# --------------------------------------------------------------------------
# brace helpers
# --------------------------------------------------------------------------


def group_at(s: str, i: int) -> tuple[str, int]:
    """s[i] == '{'. Return (content, index after closing brace)."""
    depth = 0
    for j in range(i, len(s)):
        c = s[j]
        if c == "\\":
            continue
        if c == "{" and (j == 0 or s[j - 1] != "\\"):
            depth += 1
        elif c == "}" and (j == 0 or s[j - 1] != "\\"):
            depth -= 1
            if depth == 0:
                return s[i + 1 : j], j + 1
    return s[i + 1 :], len(s)


def find_cmd_args(s: str, cmd: str) -> list[str]:
    out = []
    for m in re.finditer(r"\\" + cmd + r"\*?\s*(?:\[[^\]]*\])?\s*\{", s):
        g, _ = group_at(s, m.end() - 1)
        out.append(g)
    return out


# --------------------------------------------------------------------------
# sections
# --------------------------------------------------------------------------

SEC_RE = re.compile(r"\\(section|subsection|subsubsection)\*?\s*(?:\[[^\]]*\])?\s*\{")


def split_sections(body: str):
    """Return list of dict(level, title, text) for top-level sections."""
    heads = []
    for m in SEC_RE.finditer(body):
        title, end = group_at(body, m.end() - 1)
        heads.append((m.group(1), title, m.start(), end))
    secs = []
    top = [h for h in heads if h[0] == "section"]
    for i, h in enumerate(top):
        end = top[i + 1][2] if i + 1 < len(top) else len(body)
        seg = body[h[3] : end]
        subs = [x for x in heads if x[0] != "section" and h[2] < x[2] < end]
        secs.append({"title": clean_inline(h[1]), "text": seg, "n_sub": len(subs), "n_subsub": sum(1 for x in subs if x[0] == "subsubsection")})
    pre = body[: top[0][2]] if top else body
    return pre, secs


def classify(title: str, idx: int, n: int) -> str:
    t = title.lower()
    if "introduc" in t:
        return "intro"
    if re.search(r"conclu|summary|concluding", t):
        return "conclusion"
    if re.search(r"simulat|numerical|experiment|evaluat|performance eval|result", t):
        return "sim"
    if re.search(r"related work|literature|prior work", t):
        return "related"
    if re.search(r"system model|signal model|channel model|problem formul|network model|system description|preliminar|background|model", t):
        return "model"
    if re.search(r"^appendix|proof of|^proof|appendi", t):
        return "appendix"
    return "method"


# --------------------------------------------------------------------------
# cleaning to prose
# --------------------------------------------------------------------------

DISPLAY_ENVS = r"equation|align|eqnarray|gather|multline|IEEEeqnarray|displaymath|flalign|split"


def display_punct_stats(body: str) -> Counter:
    c: Counter = Counter()
    for m in re.finditer(r"\\begin\{(" + DISPLAY_ENVS + r")(\*?)\}(.*?)\\end\{\1\2\}", body, re.S):
        inner = m.group(3)
        inner = re.sub(r"\\label\{[^}]*\}|\\nonumber|\\notag|\\tag\{[^}]*\}", "", inner)
        inner = re.sub(r"(\\\\|\\,|\\;|\\quad|\\qquad|\\!|\\ |\s)+$", "", inner)
        last = inner[-1:] if inner else ""
        c["comma" if last == "," else "period" if last == "." else "none"] += 1
    for m in re.finditer(r"\\\[(.*?)\\\]", body, re.S):
        inner = m.group(1).rstrip()
        last = inner[-1:] if inner else ""
        c["comma" if last == "," else "period" if last == "." else "none"] += 1
    return c


def clean_inline(t: str) -> str:
    t = re.sub(r"\\(?:textbf|textit|emph|textsc|texttt|mathrm|text|underline|mbox)\{([^{}]*)\}", r"\1", t)
    t = re.sub(r"\\[a-zA-Z]+\*?", " ", t)
    t = re.sub(r"[{}$~]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def to_prose(text: str) -> str:
    t = text
    # drop floats / algorithms / bibliography (captions counted elsewhere)
    t = re.sub(r"\\begin\{(figure|table|algorithm|algorithmic|thebibliography|tikzpicture|tabular)(\*?)\}.*?\\end\{\1\2\}", " ", t, flags=re.S)
    # display math
    t = re.sub(r"\\begin\{(" + DISPLAY_ENVS + r"|array|matrix|cases)(\*?)\}.*?\\end\{\1\2\}", " DMATH ", t, flags=re.S)
    t = re.sub(r"\\\[.*?\\\]", " DMATH ", t, flags=re.S)
    t = re.sub(r"\$\$.*?\$\$", " DMATH ", t, flags=re.S)
    # inline math
    t = re.sub(r"\$[^$]*\$", " MATH ", t)
    t = re.sub(r"\\\(.*?\\\)", " MATH ", t, flags=re.S)
    # refs / cites / labels
    t = re.sub(r"\\(?:cite|citep|citet|nocite)\*?(?:\[[^\]]*\])*\{[^}]*\}", "", t)
    t = re.sub(r"\\eqref\{[^}]*\}", "(REF)", t)
    t = re.sub(r"\\(?:ref|autoref|cref|Cref|pageref)\{[^}]*\}", "REF", t)
    t = re.sub(r"\\(?:label|index|vspace|hspace|vskip|noindent|centering|newpage|clearpage)\*?(?:\{[^}]*\})?", " ", t)
    t = re.sub(r"\\footnote\{[^{}]*\}", " ", t)
    t = re.sub(r"\\(?:begin|end)\{[^}]*\}(?:\[[^\]]*\])?", "\n\n", t)
    t = re.sub(r"\\item\b", "\n\n", t)
    # formatting wrappers keep their argument
    for _ in range(3):
        t = re.sub(r"\\(?:textbf|textit|emph|textsc|texttt|mathrm|text|underline|mbox|bf|it)\s*\{([^{}]*)\}", r"\1", t)
    t = re.sub(r"\\(?:sub)*section\*?\s*(?:\[[^\]]*\])?\{[^{}]*\}", "\n\n", t)
    t = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", t)
    t = t.replace("~", " ").replace("{", " ").replace("}", " ").replace("\\", " ")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n\n", t)
    return t.strip()


ABBR = [r"i\.e\.", r"e\.g\.", r"et al\.", r"Fig\.", r"Figs\.", r"Eq\.", r"Eqs\.", r"Sec\.", r"vs\.", r"cf\.", r"resp\.", r"w\.r\.t\.", r"s\.t\.", r"a\.k\.a\.", r"i\.i\.d\.", r"Prof\.", r"Dr\.", r"No\.", r"approx\.", r"wrt\.", r"w\.l\.o\.g\."]
ABBR_RE = re.compile("|".join(ABBR), re.I)


def sentences(par: str) -> list[str]:
    p = ABBR_RE.sub(lambda m: m.group(0).replace(".", "<D>"), par)
    p = re.sub(r"\b([A-Z])\.(?=\s[A-Z])", r"\1<D>", p)
    parts = re.split(r"(?<=[.!?])[\"')\]]?\s+(?=[A-Z(\d])", p.replace("\n", " "))
    return [s.replace("<D>", ".").strip() for s in parts if len(s.split()) >= 2]


def words(s: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z'\-]*|MATH|DMATH", s)


# --------------------------------------------------------------------------
# lexicons (regex, matched case-insensitively on cleaned prose)
# --------------------------------------------------------------------------

LEX = {
    # sentence-initial connectors
    "specifically": r"(?:^|(?<=[.!?] ))Specifically,",
    "in_particular": r"(?:^|(?<=[.!?] ))In particular,",
    "moreover": r"(?:^|(?<=[.!?] ))Moreover,",
    "furthermore": r"(?:^|(?<=[.!?] ))Furthermore,",
    "additionally": r"(?:^|(?<=[.!?] ))(?:Additionally|In addition),",
    "however": r"(?:^|(?<=[.!?] ))However,",
    "therefore": r"(?:^|(?<=[.!?] ))(?:Therefore|Thus|Hence|As a result|Consequently),",
    "first_second": r"(?:^|(?<=[.!?] ))(?:First|Second|Third|Finally|Lastly|Next|Then),",
    "for_example": r"(?:^|(?<=[.!?] ))(?:For example|For instance),",
    "to_this_end": r"(?:^|(?<=[.!?] ))(?:To this end|To address (?:this|these)[a-z ]*|To tackle (?:this|these)[a-z ]*|To overcome (?:this|these)[a-z ]*),",
    "note_that": r"\bNote that\b",
    "it_is_worth": r"\bit is (?:worth|worthy) (?:noting|mentioning|pointing)",
    "it_can_be_shown": r"\bit can be (?:shown|proved|verified|readily shown|easily shown|seen|observed)\b",
    "as_shown_in": r"\b(?:as|is) (?:shown|illustrated|depicted|seen) in\b",
    "it_is_observed": r"\bit is (?:observed|seen|found|expected|shown|evident|clear)\b",
    "one_can_observe": r"\b(?:one|we) can (?:observe|see|find|note|conclude|infer|verify)\b",
    "as_expected": r"\bas expected\b",
    "this_is_because": r"\b(?:This|this) is (?:because|due to|attributed to|expected|mainly because|mainly due to)\b",
    "this_implies": r"\b(?:This|this) (?:implies|indicates|suggests|means|reveals|shows|demonstrates|validates|confirms|verifies)\b",
    "without_loss": r"\bwithout loss of generality\b",
    "in_this_paper": r"\b[Ii]n this (?:paper|letter|work|article),",
    "this_paper": r"\b[Tt]his (?:paper|letter|work|article) (?:studies|investigates|proposes|considers|addresses|focuses|aims|develops|introduces|presents|characterizes|reviews)",
    "organized_as_follows": r"\borganized as follows\b",
    "notation": r"\bNotations?\b\s*[:.]",
    "respectively": r"\brespectively\b",
    "denotes": r"\b(?:denotes?|denoted|represents?)\b",
    "where": r"(?:^|(?<=[.!?,] ))where\b",
    "we": r"\b[Ww]e\b",
    "our": r"\b[Oo]ur\b",
    "the_authors": r"\bthe authors?\b",
    "ie_eg": r"\b(?:i\.e\.|e\.g\.)",
    "etc": r"\betc\.",
    # hedging / stance
    "may_might_could": r"\b(?:may|might|could)\b",
    "can": r"\bcan\b",
    "potentially": r"\b(?:potentially|possibly|perhaps|arguably)\b",
    "expect": r"\b(?:expected to|is expected|we expect|it is expected)\b",
    # fillers / intensifiers
    "novel": r"\bnovel\b",
    "promising": r"\bpromising\b",
    "significantly": r"\b(?:significantly|substantially|greatly|dramatically|remarkably|considerably|drastically)\b",
    "soa": r"\bstate-of-the-art\b",
    "robust_comprehensive": r"\b(?:robust|comprehensive)\b",
    "efficient_effective": r"\b(?:efficient|efficiently|effective|effectively)\b",
    "critical_crucial": r"\b(?:critical|crucial|essential|vital)\b",
    "emerged": r"\b(?:emerged|emerging|has attracted|have attracted|has drawn|received (?:significant|great|considerable)|growing (?:interest|attention))\b",
    "recently": r"\b(?:[Rr]ecently|[Ii]n recent years|[Ii]n the past (?:few )?years)\b",
    "envision": r"\b(?:envisioned|envisage|envision)\b",
    # punctuation
    "emdash": r"---|—|(?<=\s)--(?=\s)",
    "semicolon": r";",
    "colon": r":",
    "question": r"\?",
    "exclaim": r"!",
    "paren": r"\(",
}
LEX_RE = {k: re.compile(v, re.M) for k, v in LEX.items()}

PASSIVE_RE = re.compile(
    r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+ly\s+)?"
    r"(\w+ed|given|shown|obtained|known|made|seen|found|chosen|built|written|done|taken|set|used|needed|held|left|run|kept)\b",
    re.I,
)
PASSIVE_STOP = {"need", "used_to", "supposed", "based"}  # ignore "is based"


def stats_for(text: str) -> dict:
    """Prose statistics for a body of cleaned prose."""
    paras = [p for p in re.split(r"\n\s*\n", text) if len(p.split()) > 3]
    sents = [s for p in paras for s in sentences(p)]
    lens = [len(words(s)) for s in sents]
    lens = [n for n in lens if n > 0]
    nw = sum(lens) or 1
    out = {
        "n_words": nw,
        "n_sent": len(lens),
        "n_par": len(paras),
        "sent_mean": round(statistics.mean(lens), 1) if lens else 0,
        "sent_median": statistics.median(lens) if lens else 0,
        "sent_p90": sorted(lens)[int(0.9 * (len(lens) - 1))] if lens else 0,
        "sent_gt40": round(sum(1 for n in lens if n > 40) / max(len(lens), 1), 3),
        "par_sent_mean": round(len(lens) / max(len(paras), 1), 1),
    }
    joined = " ".join(sents)
    for k, rx in LEX_RE.items():
        out["lex_" + k] = len(rx.findall(joined))
    out["passive"] = sum(1 for m in PASSIVE_RE.finditer(joined) if m.group(1).lower() not in PASSIVE_STOP)
    out["first_words"] = Counter((words(s) or [""])[0].lower() for s in sents)
    out["we_verbs"] = Counter(m.group(1).lower() for m in re.finditer(r"\b[Ww]e\s+(?:also\s+|then\s+|first\s+|further\s+)?([a-z]+)", joined))
    return out


# --------------------------------------------------------------------------
# per-paper analysis
# --------------------------------------------------------------------------


def contributions(intro_raw: str) -> dict:
    m = re.search(r"\\begin\{(itemize|enumerate)\}(.*?)\\end\{\1\}", intro_raw, re.S)
    if not m:
        return {"has_list": False}
    items = [i for i in re.split(r"\\item\b", m.group(2))[1:] if i.strip()]
    lead_labels = sum(1 for i in items if re.match(r"\s*(?:\[[^\]]*\])?\s*\\(?:textbf|emph|textit)\{", i))
    firstw = Counter()
    for i in items:
        w = words(to_prose(i))
        firstw[" ".join(w[:2]).lower()] += 1
    before = intro_raw[: m.start()]
    lead = to_prose(before)[-260:]
    lead = re.split(r"(?<=[.!?])\s+", lead)[-1] if lead else ""
    return {
        "has_list": True,
        "kind": m.group(1),
        "n_items": len(items),
        "item_words_mean": round(statistics.mean(len(words(to_prose(i))) for i in items), 1),
        "lead_labelled": lead_labels,
        "first_words": firstw,
        "lead_in": " ".join(lead.split()[:14]).lower(),
    }


def analyse(eprint: Path, meta: dict, outdir: Path) -> dict | None:
    files = read_sources(eprint)
    doc, bbl = flatten(files)
    if not doc:
        return None
    pre_doc, _, body = doc.partition(r"\begin{document}")
    body = body.split(r"\end{document}")[0]
    bib_cut = re.search(r"\\bibliography\{|\\begin\{thebibliography\}", body)
    main_body = body[: bib_cut.start()] if bib_cut else body
    app = re.search(r"\\appendix|\\begin\{appendices\}", main_body)
    appendix_raw = main_body[app.start():] if app else ""
    main_body = main_body[: app.start()] if app else main_body

    rec: dict = {"id": meta["base"], "title": meta["title"], "pub": meta["pub"], "pos": meta["pos"], "n_authors": meta["n"], "cat": meta["cat"]}
    dc = re.search(r"\\documentclass\s*(?:\[([^\]]*)\])?\s*\{([^}]*)\}", pre_doc)
    rec["docclass"] = (dc.group(2) if dc else "") + "[" + (dc.group(1).replace(" ", "") if dc and dc.group(1) else "") + "]"

    # abstract
    ab = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", body, re.S)
    ab_txt = to_prose(ab.group(1)) if ab else ""
    ab_sents = sentences(ab_txt)
    rec["abstract_words"] = len(words(ab_txt))
    rec["abstract_sents"] = len(ab_sents)
    rec["abstract_has_sim"] = bool(re.search(r"simulation|numerical|experiment", ab_txt, re.I))
    rec["abstract_has_number"] = bool(re.search(r"\d+(?:\.\d+)?\s*(?:%|dB|×|x\b)", ab.group(1) if ab else ""))
    rec["abstract_we"] = len(re.findall(r"\b[Ww]e\b", ab_txt))
    rec["abstract_first"] = " ".join(ab_txt.split()[:10])
    kw = re.search(r"\\begin\{IEEEkeywords\}(.*?)\\end\{IEEEkeywords\}", body, re.S)
    rec["n_keywords"] = len([k for k in re.split(r"[,;]", to_prose(kw.group(1))) if k.strip()]) if kw else 0

    pre, secs = split_sections(main_body)
    rec["n_sections"] = len(secs)
    rec["sections"] = [s["title"] for s in secs]
    rec["n_subsections"] = sum(s["n_sub"] for s in secs)
    kinds = []
    for i, s in enumerate(secs):
        k = classify(s["title"], i, len(secs))
        if i == 0 and k == "method":
            k = "intro"
        kinds.append(k)
    rec["kinds"] = kinds

    # per-section prose stats
    sec_prose = {}
    texts_out = []
    for s, k in zip(secs, kinds):
        pr = to_prose(s["text"])
        sec_prose.setdefault(k, []).append(pr)
        texts_out.append(f"##### [{k}] {s['title']}\n{pr}\n")
    (outdir / "texts").mkdir(parents=True, exist_ok=True)
    (outdir / "texts" / f"{meta['base']}.txt").write_text(f"# {meta['title']}\n\n## ABSTRACT\n{ab_txt}\n\n" + "\n".join(texts_out), encoding="utf-8")

    rec["words_by_kind"] = {k: sum(len(words(p)) for p in v) for k, v in sec_prose.items()}
    all_prose = "\n\n".join(p for k, v in sec_prose.items() for p in v)
    rec["all"] = stats_for(all_prose)
    rec["intro_stats"] = stats_for("\n\n".join(sec_prose.get("intro", [])))
    rec["sim_stats"] = stats_for("\n\n".join(sec_prose.get("sim", [])))
    rec["concl_stats"] = stats_for("\n\n".join(sec_prose.get("conclusion", [])))

    # intro details
    intro_raw = next((s["text"] for s, k in zip(secs, kinds) if k == "intro"), "")
    rec["contrib"] = contributions(intro_raw)
    intro_par = [p for p in re.split(r"\n\s*\n", to_prose(intro_raw)) if len(p.split()) > 5]
    rec["intro_first_sents"] = [" ".join(sentences(p)[0].split()[:14]) if sentences(p) else "" for p in intro_par[:3]]
    rec["intro_n_par"] = len(intro_par)
    rec["intro_related_par"] = sum(1 for p in intro_par if len(re.findall(r"\bREF\b|\[\d|(?:et al)", p)) >= 1)
    rec["has_related_section"] = "related" in kinds
    rec["has_organized"] = bool(re.search(r"organized as follows|remainder of this paper|rest of (?:this|the) paper", to_prose(main_body), re.I))
    rec["cites_in_intro"] = len(re.findall(r"\\cite\w*\{[^}]*\}", intro_raw))
    rec["cites_total"] = len(re.findall(r"\\cite\w*\{[^}]*\}", main_body))
    rec["bibitems"] = len(re.findall(r"\\bibitem", bbl + main_body + body))

    # notation paragraph location
    loc = "none"
    for s, k in zip(secs, kinds):
        if re.search(r"\\(?:emph|textit|textbf)\{\s*Notations?\s*[:.]?\s*\}|Notations?\s*:", s["text"]):
            loc = k
            break
    rec["notation_loc"] = loc

    # math / environments
    rec["n_display"] = len(re.findall(r"\\begin\{(?:" + DISPLAY_ENVS + r")\*?\}", main_body)) + len(re.findall(r"\\\[", main_body))
    rec["n_inline"] = len(re.findall(r"\$[^$]+\$", main_body))
    rec["display_punct"] = dict(display_punct_stats(main_body))
    for env in ["lemma", "proposition", "theorem", "corollary", "remark", "definition", "assumption", "property", "proof", "algorithm", "example"]:
        rec["env_" + env] = len(re.findall(r"\\begin\{" + env + r"\*?\}", body))
    rec["appendix_words"] = len(words(to_prose(appendix_raw)))
    rec["problem_labels"] = len(re.findall(r"\(\\?(?:mathrm|text|textbf|mathcal)?\{?P\d?[a-z]?\}?\)|\\text\{\(P\d", main_body))
    rec["n_figs"] = len(re.findall(r"\\begin\{figure\*?\}", body))
    rec["n_tabs"] = len(re.findall(r"\\begin\{table\*?\}", body))
    caps = find_cmd_args(body, "caption")
    caps = [to_prose(c) for c in caps]
    rec["caption_words_mean"] = round(statistics.mean(len(words(c)) for c in caps), 1) if caps else 0
    rec["caption_ends_period"] = round(sum(1 for c in caps if c.strip().endswith(".")) / len(caps), 2) if caps else 0
    rec["caption_sample"] = [" ".join(c.split()[:12]) for c in caps[:3]]

    # reference-format habits
    rec["ref_Section"] = len(re.findall(r"Section~?\s*\\ref", main_body))
    rec["ref_Fig"] = len(re.findall(r"Fig(?:s)?\.~?\s*\\ref", main_body))
    rec["ref_Figure"] = len(re.findall(r"Figure~?\s*\\ref", main_body))
    rec["ref_eqref"] = len(re.findall(r"\\eqref", main_body))
    rec["ref_paren_ref"] = len(re.findall(r"\(\s*\\ref\{", main_body))
    rec["ref_Eq"] = len(re.findall(r"(?:Eq\.|Eqs\.|Equation)~?\s*\(?\s*\\(?:eq)?ref", main_body))
    rec["macros"] = len(re.findall(r"\\(?:newcommand|renewcommand|def|DeclareMathOperator)\b", pre_doc))
    rec["pkg_bm"] = bool(re.search(r"\{bm\}|\{amsmath|\{amsthm", pre_doc))

    # simulation opening
    sim_raw = next((s["text"] for s, k in zip(secs, kinds) if k == "sim"), "")
    sim_par = [p for p in re.split(r"\n\s*\n", to_prose(sim_raw)) if len(p.split()) > 5]
    rec["sim_first_sent"] = " ".join(sentences(sim_par[0])[0].split()[:18]) if sim_par and sentences(sim_par[0]) else ""
    rec["sim_bench_labels"] = len(re.findall(r"(?:Benchmark|benchmark)\s*\d|\\textbf\{[A-Za-z\- ]+\}\s*:", sim_raw))
    rec["concl_first_sent"] = " ".join(sentences(sec_prose.get("conclusion", [""])[0])[0].split()[:14]) if sec_prose.get("conclusion") and sentences(sec_prose["conclusion"][0]) else ""
    rec["concl_future"] = bool(re.search(r"future (?:work|research|direction)|interesting|worth (?:investigat|study|explor)|left for|remains? (?:open|to be)", " ".join(sec_prose.get("conclusion", [""])), re.I))
    return rec


def _to_jsonable(o):
    if isinstance(o, Counter):
        return dict(o.most_common(40))
    if isinstance(o, dict):
        return {k: _to_jsonable(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_to_jsonable(v) for v in o]
    return o


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="dir with <id>.eprint files")
    ap.add_argument("--meta", required=True, help="metadata json (mei_list.json)")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    src, out = Path(a.src), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    meta = json.load(open(a.meta, encoding="utf-8"))
    recs, skipped = [], []
    for r in meta:
        base = r["id"].split("v")[0]
        r["base"] = base
        pos = 0
        for i, au in enumerate(r["authors"]):
            if "Weidong Mei" in au:
                pos = i + 1
        r["pos"], r["n"] = pos, len(r["authors"])
        p = src / f"{base}.eprint"
        if not p.exists() or p.stat().st_size == 0:
            skipped.append((base, "missing"))
            continue
        try:
            rec = analyse(p, r, out)
        except Exception as e:  # keep going; report at the end
            skipped.append((base, f"error: {e!r}"))
            continue
        if rec is None:
            skipped.append((base, "no main tex"))
            continue
        recs.append(rec)
    json.dump(_to_jsonable(recs), open(out / "per_paper.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"analysed {len(recs)} papers; skipped {len(skipped)}")
    for s in skipped:
        print("  skipped", *s)


if __name__ == "__main__":
    main()
