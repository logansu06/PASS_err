#!/usr/bin/env python3
"""style_gate.py - deterministic mechanical style gate, driven by a profile.

Replaces the hand-run grep block of the upstream skill with one script that
reports counts, line numbers and metric-vs-corpus deltas. Rules live in
profiles/<profile>/rules.json; corpus norms in profiles/<profile>/norms.json.

Usage
-----
  python style_gate.py PATH [PATH ...] [--profile weidong-mei]
                       [--register auto|letter|full|tutorial]
                       [--json report.json] [--max-hits 6] [--no-metrics]

PATH is a .tex file (its \\input / \\include children are followed) or a
directory (the file containing \\begin{document} is the root).

Exit status: 0 no FAIL rule violated; 1 at least one FAIL; 2 usage / IO error.
Standard library only.
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
sys.path.insert(0, str(HERE))
from style_stats import (  # noqa: E402  (shared cleaning / metrics keep gate and norms comparable)
    ABBR_RE,
    display_punct_stats,
    stats_for,
    to_prose,
    words,
)

# ---------------------------------------------------------------------------
# loading and line-preserving cleaning
# ---------------------------------------------------------------------------


def _strip_comment(line: str) -> str:
    return re.sub(r"(?<!\\)%.*", "", line)


def load_lines(path: Path, seen=None, depth=0):
    """Return [(file, lineno, text)] with \\input / \\include expanded in place."""
    seen = seen or set()
    out = []
    if depth > 8 or path in seen:
        return out
    seen = seen | {path}
    try:
        raw = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raw = path.read_text(encoding="latin-1")
    for i, ln in enumerate(raw.split("\n"), 1):
        txt = _strip_comment(ln)
        m = re.fullmatch(r"\s*\\(?:input|include)\s*\{([^}]*)\}\s*", txt)
        if m:
            name = m.group(1).strip()
            cand = [path.parent / name, path.parent / (name + ".tex")]
            child = next((c for c in cand if c.is_file()), None)
            if child:
                out.extend(load_lines(child, seen, depth + 1))
                continue
        out.append((str(path.name), i, txt))
    return out


def find_root(p: Path) -> Path:
    if p.is_file():
        return p
    skip = {"build", "node_modules", "templates", "__pycache__"}
    cands = [
        f
        for f in p.rglob("*.tex")
        if not any(part.startswith(".") or part in skip for part in f.relative_to(p).parts[:-1])
        and r"\begin{document}" in f.read_text(encoding="utf-8", errors="ignore")
    ]
    if not cands:
        raise SystemExit(f"no .tex root with \\begin{{document}} under {p}")
    return max(cands, key=lambda f: f.stat().st_size)


def sub_nl(pattern, repl, s, flags=re.S):
    """re.sub that keeps the number of newlines of every match (line numbers survive)."""
    return re.sub(pattern, lambda m: repl + "\n" * m.group(0).count("\n"), s, flags=flags)


class Doc:
    def __init__(self, path: Path):
        self.root = find_root(path)
        self.lines = load_lines(self.root)
        self.flat = "\n".join(t for _, _, t in self.lines)
        self.n_lines = len(self.lines)
        m0 = self.flat.find(r"\begin{document}")
        self.body_off = m0 + len(r"\begin{document}") if m0 >= 0 else 0
        body = self.flat[self.body_off:]
        bib = re.search(r"\\bibliography\{|\\begin\{thebibliography\}|\\end\{document\}", body)
        self.body = body[: bib.start()] if bib else body
        # number of newlines before the body start, to translate offsets to flat lines
        self.body_line0 = self.flat.count("\n", 0, self.body_off)
        app = re.search(r"\\appendix|\\begin\{appendices\}", self.body)
        self.main_body = self.body[: app.start()] if app else self.body
        self._build()

    # -- helpers ------------------------------------------------------------
    def origin(self, flat_line: int):
        """1-based line inside self.flat -> (file, lineno)."""
        i = min(max(flat_line - 1, 0), len(self.lines) - 1)
        f, ln, _ = self.lines[i]
        return f, ln

    def line_in_body(self, s: str, pos: int) -> int:
        return self.body_line0 + 1 + s.count("\n", 0, pos)

    # -- structure ------------------------------------------------------------
    def _build(self):
        b = self.body
        self.floats = []
        for m in re.finditer(r"\\begin\{(figure|table|algorithm)(\*?)\}(\[[^\]]*\])?(.*?)\\end\{\1\2\}", b, re.S):
            kind, blk = m.group(1), m.group(4)
            caps = _find_args(blk, "caption")
            sub_empty = len(re.findall(r"\\subfloat\s*\[\s*\]|\\subfigure\s*\[\s*\]", blk))
            n_sub = len(re.findall(r"\\subfloat|\\subfigure|\\begin\{subfigure\}", blk))
            main = caps[-1] if caps else ""
            self.floats.append(
                {
                    "kind": kind,
                    "line": self.line_in_body(b, m.start()),
                    "place": (m.group(3) or "")[1:-1],
                    "caption_raw": main,
                    "caption": re.sub(r"\s+", " ", to_prose(main)).strip(),
                    "n_sub": n_sub,
                    "sub_empty": sub_empty,
                    "hline": len(re.findall(r"\\hline", blk)),
                    "booktabs": bool(re.search(r"\\toprule|\\midrule", blk)),
                    "caption_first": (blk.find("\\caption") < blk.find("\\begin{tabular")) if "\\begin{tabular" in blk else True,
                }
            )
        self.heads = []
        for m in re.finditer(r"\\(section|subsection|subsubsection)\*?\s*(?:\[[^\]]*\])?\s*\{", b):
            g, _ = _group_at(b, m.end() - 1)
            self.heads.append({"level": m.group(1), "title": re.sub(r"\s+", " ", to_prose(g)).strip(), "line": self.line_in_body(b, m.start())})
        ab = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", self.flat, re.S)
        self.abstract_raw = ab.group(1) if ab else ""
        self.abstract = re.sub(r"\s+", " ", to_prose(self.abstract_raw)).strip()
        self.abstract_line = self.flat.count("\n", 0, ab.start()) + 1 if ab else 1
        # line-preserving prose
        t = self.main_body
        # front matter that is not running prose
        t = sub_nl(r"\\begin\{(abstract|IEEEkeywords|IEEEbiography|IEEEbiographynophoto)\}.*?\\end\{\1\}", " ", t)
        for cmd in ("title", "author", "thanks", "markboth", "IEEEauthorblockN", "IEEEauthorblockA", "IEEEauthorrefmark"):
            t = _remove_cmd(t, cmd)
        t = sub_nl(r"\\begin\{(figure|table|algorithm|algorithmic|tikzpicture|tabular|thebibliography|verbatim)(\*?)\}.*?\\end\{\1\2\}", " ", t)
        t = sub_nl(r"\\begin\{([A-Za-z]*(?:eq|align|gather|multline|split|cases|array|matrix|display)[A-Za-z]*)(\*?)\}.*?\\end\{\1\2\}", " DMATH ", t)
        t = sub_nl(r"\\\[.*?\\\]", " DMATH ", t)
        t = sub_nl(r"\$\$.*?\$\$", " DMATH ", t)
        t = sub_nl(r"\$[^$]*\$", " MATH ", t)
        t = sub_nl(r"\\\(.*?\\\)", " MATH ", t)
        t = sub_nl(r"\\(?:cite|citep|citet|nocite)\*?(?:\[[^\]]*\])*\{[^}]*\}", "", t)
        t = sub_nl(r"\\eqref\{[^}]*\}", "(REF)", t)
        t = sub_nl(r"\\(?:ref|autoref|cref|Cref|pageref)\{[^}]*\}", "REF", t)
        t = sub_nl(r"\\(?:label|index|vspace|hspace|vskip|noindent|centering|newpage|clearpage)\*?(?:\{[^}]*\})?", " ", t)
        t = sub_nl(r"\\footnote\{[^{}]*\}", " ", t)
        t = sub_nl(r"\\(?:sub)*section\*?\s*(?:\[[^\]]*\])?\{[^{}]*\}", "\n\n", t)
        t = sub_nl(r"\\(?:begin|end)\{[^}]*\}(?:\[[^\]]*\])?", "\n\n", t)
        for _ in range(3):
            t = sub_nl(r"\\(?:textbf|textit|emph|textsc|texttt|mathrm|text|underline|mbox|bf|it)\s*\{([^{}]*)\}", "\\1", t)
        t = re.sub(r"\\item\b", "\n\n", t)
        t = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", t)
        t = t.replace("~", " ").replace("{", " ").replace("}", " ").replace("\\", " ")
        t = re.sub(r"[ \t]+", " ", t)
        self.prose = t
        self.prose_norm = ABBR_RE.sub(lambda m: m.group(0).replace(".", "\x01"), t).replace("\n", " ")
        self.prose_rx = self.prose_norm.replace("\x01", ".")  # same length; abbreviations keep their dots for regex rules
        # Sentence spans. A blank line always ends a sentence (a paragraph that
        # ends on a display equation has no final period), so split per paragraph.
        self.sent = []
        for pm in re.finditer(r"[^\n]+(?:\n(?![ \t]*\n)[^\n]*)*", self.prose_norm_paragraph_source()):
            base = pm.start()
            para = pm.group(0).replace("\n", " ")
            start = 0
            for m in re.finditer(r"(?<=[.!?])[\"')\]]*\s+(?=[A-Z(\[\d`])", para):
                self._push(base, para, start, m.start())
                start = m.end()
            self._push(base, para, start, len(para))

    def prose_norm_paragraph_source(self):
        # abbreviation-protected text that still contains the original newlines
        return ABBR_RE.sub(lambda m: m.group(0).replace(".", "\x01"), self.prose)

    def _push(self, base, para, a, b):
        seg = para[a:b]
        s = seg.strip()
        if len(s.split()) >= 2:
            off = base + a + (len(seg) - len(seg.lstrip()))
            self.sent.append((off, s.replace("\x01", ".")))

    def line_of_prose(self, pos: int):
        return self.origin(self.line_in_body(self.prose, pos))


def _group_at(s, i):
    depth = 0
    for j in range(i, len(s)):
        c = s[j]
        if c == "\\":
            continue
        if c == "{" and s[j - 1] != "\\":
            depth += 1
        elif c == "}" and s[j - 1] != "\\":
            depth -= 1
            if depth == 0:
                return s[i + 1 : j], j + 1
    return s[i + 1 :], len(s)


def _remove_cmd(t, cmd):
    """Delete \\cmd{...} (brace-aware), keeping newline count."""
    out, i = [], 0
    for m in re.finditer(r"\\" + cmd + r"\*?\s*(?:\[[^\]]*\])?\s*\{", t):
        if m.start() < i:
            continue
        g, end = _group_at(t, m.end() - 1)
        out.append(t[i : m.start()])
        out.append(" " + "\n" * t[m.start() : end].count("\n"))
        i = end
    out.append(t[i:])
    return "".join(out)


def _find_args(s, cmd):
    out = []
    for m in re.finditer(r"\\" + cmd + r"\*?\s*(?:\[[^\]]*\])?\s*\{", s):
        g, _ = _group_at(s, m.end() - 1)
        out.append(g)
    return out


# ---------------------------------------------------------------------------
# rule engine
# ---------------------------------------------------------------------------

STOP_TITLE = {"a", "an", "the", "and", "or", "of", "for", "in", "on", "to", "via", "with", "by", "at", "from", "as", "versus", "vs", "under", "over", "into", "is", "are", "do", "we", "does"}
CONNECTORS = re.compile(r"(?:Moreover|Furthermore|Additionally|In addition|Besides),")


def snippet(text, a, b, pad=38):
    s = text[max(a - pad, 0) : min(b + pad, len(text))].replace("\n", " ")
    return re.sub(r"\s+", " ", s).replace("\x01", ".").strip()


def run_regex_rule(rule, doc: Doc):
    hits = []
    flags = re.I if "i" in rule.get("flags", "") else 0
    rx = re.compile(rule["regex"], flags)
    scope = rule.get("scope", "prose")
    if scope == "prose":
        skip = re.compile(rule["skip_if_near"]) if rule.get("skip_if_near") else None
        for m in rx.finditer(doc.prose_rx):
            if skip and skip.search(doc.prose_rx[max(m.start() - 25, 0) : m.end() + 25]):
                continue
            f, ln = doc.line_of_prose(m.start())
            hits.append((f, ln, snippet(doc.prose_rx, m.start(), m.end())))
        for m in rx.finditer(doc.abstract):  # the abstract is not part of the running prose
            if skip and skip.search(doc.abstract[max(m.start() - 25, 0) : m.end() + 25]):
                continue
            hits.append(("abstract", doc.abstract_line, snippet(doc.abstract, m.start(), m.end())))
    elif scope == "raw":
        for i, (f, ln, txt) in enumerate(doc.lines):
            for m in rx.finditer(txt):
                hits.append((f, ln, snippet(txt, m.start(), m.end())))
    elif scope == "abstract":
        for m in rx.finditer(doc.abstract):
            hits.append(("abstract", doc.abstract_line, snippet(doc.abstract, m.start(), m.end())))
    elif scope == "sentence_start":
        for off, s in doc.sent:
            m = rx.match(s)
            if m:
                f, ln = doc.line_of_prose(off)
                hits.append((f, ln, s[:70]))
    elif scope == "abstract_raw":
        for m in rx.finditer(doc.abstract_raw):
            hits.append(("abstract", doc.abstract_line, snippet(doc.abstract_raw, m.start(), m.end())))
    return hits


def custom_duplicate_word(rule, doc):
    hits = []
    words_ = "the a an of to in is are and that for with by on as we can be this which it from at or our not".split()
    alts = "|".join(sorted(set(words_) | {w.capitalize() for w in words_}))
    # case-sensitive: 'an AN-aided' is not a repeat, 'The the' and 'a a' are
    rx = re.compile(r"\b(" + alts + r")\s+\1\b|\b([Tt]he|[Aa]) ([Tt]he|[Aa])\b")
    for m in rx.finditer(doc.prose_rx):
        if m.group(2) and m.group(2).lower() != m.group(3).lower():
            continue
        f, ln = doc.line_of_prose(m.start())
        hits.append((f, ln, snippet(doc.prose_rx, m.start(), m.end())))
    for m in rx.finditer(doc.abstract):
        if m.group(2) and m.group(2).lower() != m.group(3).lower():
            continue
        hits.append(("abstract", doc.abstract_line, snippet(doc.abstract, m.start(), m.end())))
    return hits


def custom_sentence_length(rule, doc):
    hits = []
    lim = rule.get("words_gt", 45)
    for off, s in doc.sent:
        n = len(words(s))
        if n > lim:
            f, ln = doc.line_of_prose(off)
            hits.append((f, ln, f"{n} words: {s[:80]}..."))
    return hits


def custom_connector_stacking(rule, doc):
    """>= max_per_paragraph sentence-initial additive connectors inside one paragraph."""
    hits = []
    cap = rule.get("max_per_paragraph", 2)
    offs = []
    pos = 0
    for para in re.split(r"\n\s*\n", doc.prose):
        cnt = 0
        first = None
        for m in re.finditer(r"(?:(?<=[.!?] )|^|(?<=\n))\s*(Moreover|Furthermore|Additionally|In addition|Besides),", ABBR_RE.sub(lambda m: m.group(0).replace(".", "\x01"), para).replace("\n", " ")):
            cnt += 1
            first = first if first is not None else m.start()
        if cnt >= cap:
            f, ln = doc.line_of_prose(pos + (first or 0))
            hits.append((f, ln, f"{cnt} additive connectors in one paragraph"))
        pos += len(para) + 2
    return hits


def custom_consecutive_we(rule, doc):
    hits = []
    run = 0
    for off, s in doc.sent:
        if re.match(r"We\b", s):
            run += 1
            if run == rule.get("run", 3):
                f, ln = doc.line_of_prose(off)
                hits.append((f, ln, f"{run} consecutive sentences start with 'We'"))
        else:
            run = 0
    return hits


def custom_heading_case(rule, doc):
    hits = []
    for h in doc.heads:
        if h["level"] != rule.get("level", "section"):
            continue
        ws = re.findall(r"[A-Za-z][A-Za-z\-']*", h["title"])
        bad = [w for i, w in enumerate(ws) if w.lower() not in STOP_TITLE and w[0].islower() and not re.match(r"^[a-z]+[A-Z]", w)]
        if h["title"] and bad:
            f, ln = doc.origin(h["line"])
            hits.append((f, ln, f"heading not in Title Case: '{h['title']}' ({', '.join(bad[:3])})"))
    return hits


def custom_related_work_section(rule, doc):
    return [
        (doc.origin(h["line"])[0], doc.origin(h["line"])[1], f"separate section '{h['title']}'")
        for h in doc.heads
        if h["level"] == "section" and re.search(r"related work|literature review|prior work|background", h["title"], re.I)
    ]


def custom_fig_caption(rule, doc):
    hits = []
    mode = rule["mode"]
    for fl in doc.floats:
        if fl["kind"] != "figure" or not fl["caption"]:
            continue
        cap = fl["caption"]
        f, ln = doc.origin(fl["line"])
        nsent = len([s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z])", ABBR_RE.sub(lambda m: m.group(0).replace(".", "\x01"), cap)) if len(s.split()) > 1])
        nw = len(words(cap))
        if mode == "one_sentence" and nsent > 1:
            hits.append((f, ln, f"{nsent} sentences: {cap[:70]}"))
        elif mode == "period" and not cap.rstrip().endswith("."):
            hits.append((f, ln, f"no final period: {cap[:70]}"))
        elif mode == "length" and nw > rule.get("words_gt", 25):
            hits.append((f, ln, f"{nw} words: {cap[:70]}"))
        elif mode == "sentence_case":
            ws = [w for w in re.findall(r"[A-Za-z][A-Za-z'\-]*", cap) if len(w) > 3 and not w.isupper()]
            if len(ws) >= 3 and sum(w[0].isupper() for w in ws) / len(ws) >= 0.6:
                hits.append((f, ln, f"Title Case caption: {cap[:70]}"))
        elif mode == "empty_subfloat" and fl["sub_empty"] >= 2 and not re.search(r"\(a\)", fl["caption_raw"]):
            hits.append((f, ln, f"{fl['sub_empty']} empty \\subfloat[] labels but the caption does not enumerate (a), (b)"))
    return hits


def custom_table_caption_position(rule, doc):
    return [(*doc.origin(fl["line"]), "table caption is below the tabular; IEEE tables carry the caption above") for fl in doc.floats if fl["kind"] == "table" and not fl["caption_first"]]


def custom_alg_caption(rule, doc):
    return [(*doc.origin(fl["line"]), f"algorithm caption ends with a period: {fl['caption'][:60]}") for fl in doc.floats if fl["kind"] == "algorithm" and fl["caption"].rstrip().endswith(".")]


def custom_display_punct(rule, doc):
    c = display_punct_stats(doc.main_body)
    n = sum(c.values())
    if n < 5:
        return []
    share = c.get("none", 0) / n
    if share > rule.get("max_share_unpunctuated", 0.4):
        return [("<doc>", 0, f"{c.get('none',0)}/{n} display equations carry no final , or . ({100*share:.0f}%; corpus p90 ~ 40%)")]
    return []


def custom_abstract(rule, doc):
    hits = []
    a = doc.abstract
    if not a:
        return [("abstract", 1, "no abstract found")]
    n = len(words(a))
    lo, hi = rule["range"]
    if n < lo or n > hi:
        hits.append(("abstract", doc.abstract_line, f"abstract has {n} words; register range {lo}-{hi}"))
    if re.search(r"\\cite|\\ref|\\eqref", doc.abstract_raw):
        hits.append(("abstract", doc.abstract_line, "abstract contains \\cite / \\ref"))
    if re.search(r"\\begin\{(equation|align)|\\\[|\$\$", doc.abstract_raw):
        hits.append(("abstract", doc.abstract_line, "abstract contains display math"))
    return hits


def custom_contrib_list(rule, doc):
    hits = []
    intro = doc.main_body
    m = re.search(r"\\section\*?\{[^}]*[Ii]ntroduction[^}]*\}(.*?)(?=\\section)", intro, re.S)
    if not m:
        return hits
    blk = m.group(1)
    lm = re.search(r"\\begin\{(itemize|enumerate)\}(.*?)\\end\{\1\}", blk, re.S)
    if not lm:
        return hits
    items = [i for i in re.split(r"\\item\b", lm.group(2))[1:] if i.strip()]
    labelled = sum(1 for i in items if re.match(r"\s*(?:\[[^\]]*\])?\s*\\(?:textbf|emph|textit)\{", i))
    f, ln = doc.origin(doc.line_in_body(intro, m.start(1) + lm.start()))
    if labelled:
        hits.append((f, ln, f"{labelled} contribution item(s) start with a bold/italic label; the corpus writes items as plain 'We ...' / 'To ...' / 'Finally, ...' sentences"))
    if len(items) > 5:
        hits.append((f, ln, f"{len(items)} contribution items; corpus median 3 (max 4)"))
    short = [i for i in items if len(words(to_prose(i))) < 40]
    if short and len(items) >= 2:
        hits.append((f, ln, f"{len(short)} contribution item(s) under 40 words; corpus items run ~110 words (claim + mechanism + evidence)"))
    return hits


def custom_passive_contribution(rule, doc):
    """agentless 'is proposed/developed/...' in abstract / conclusion (writer-side claim voice)."""
    rx = re.compile(r"\b(?:is|are|was|were|has been|have been)\s+(?:also\s+)?(?:proposed|developed|designed|studied|investigated|considered|presented|introduced|formulated)\b", re.I)
    hits = []
    for m in rx.finditer(doc.abstract):
        hits.append(("abstract", doc.abstract_line, snippet(doc.abstract, m.start(), m.end())))
    concl = None
    for i, h in enumerate(doc.heads):
        if h["level"] == "section" and re.search(r"conclu", h["title"], re.I):
            concl = h
    if concl:
        seg = doc.main_body[doc.main_body.find(concl["title"]) :]
        for m in rx.finditer(to_prose(seg)):
            hits.append(("conclusion", concl["line"], snippet(to_prose(seg), m.start(), m.end())))
    return hits


CUSTOM = {
    "duplicate_word": custom_duplicate_word,
    "sentence_length": custom_sentence_length,
    "connector_stacking": custom_connector_stacking,
    "consecutive_we": custom_consecutive_we,
    "heading_case": custom_heading_case,
    "related_work_section": custom_related_work_section,
    "fig_caption": custom_fig_caption,
    "table_caption_position": custom_table_caption_position,
    "alg_caption": custom_alg_caption,
    "display_punct": custom_display_punct,
    "abstract": custom_abstract,
    "contrib_list": custom_contrib_list,
    "passive_contribution": custom_passive_contribution,
}


def run_rules(doc: Doc, rules, register: str):
    results = []
    for r in rules:
        if r.get("registers") and register not in r["registers"]:
            continue
        rr = dict(r)
        if r.get("custom"):
            rr2 = dict(r)
            if r["custom"] == "abstract":
                rr2["range"] = r["range_by_register"].get(register, r["range_by_register"]["full"])
            hits = CUSTOM[r["custom"]](rr2, doc)
        else:
            hits = run_regex_rule(r, doc)
        words_n = max(len(words(doc.prose_norm)), 1)
        allowed = r.get("max_hits", 0)
        if r.get("max_per_1k") is not None:
            allowed = max(allowed, r["max_per_1k"] * words_n / 1000.0)
        status = "PASS" if len(hits) <= allowed else r["severity"]
        results.append({"id": r["id"], "name": r["name"], "severity": r["severity"], "hits": hits, "n": len(hits), "allowed": round(allowed, 1), "status": status, "fix": r.get("fix", "")})
    return results


# ---------------------------------------------------------------------------
# metrics vs corpus norms
# ---------------------------------------------------------------------------


def detect_register(doc: Doc) -> str:
    t = doc.prose_norm
    if re.search(r"\b[Tt]his letter\b|\b[Ii]n this letter\b", t):
        return "letter"
    kinds = " ".join(h["title"].lower() for h in doc.heads if h["level"] == "section")
    if not re.search(r"simulat|numerical|experiment|evaluat|result", kinds):
        return "tutorial"
    pre = doc.flat[: doc.body_off]
    if re.search(r"\\documentclass\s*\[[^\]]*\bconference\b[^\]]*\]", pre):
        return "conference"  # 5-6 page IEEE conference paper (ICC, GLOBECOM, ...)
    return "full"


def compute_metrics(doc: Doc):
    st_all = stats_for(to_prose(doc.main_body))
    nw = max(st_all["n_words"], 1)
    per1k = lambda k: 1000.0 * st_all.get("lex_" + k, 0) / nw  # noqa: E731
    conn = sum(len(CONNECTORS.findall(s)) for _, s in doc.sent)
    ab_words = len(words(doc.abstract))
    secs = [h for h in doc.heads if h["level"] == "section"]
    return {
        "sentence_mean": st_all["sent_mean"],
        "sentence_p90": st_all["sent_p90"],
        "share_gt40": st_all["sent_gt40"],
        "sentences_per_paragraph": st_all["par_sent_mean"],
        "we_per_1k": per1k("we"),
        "passive_per_1k": 1000.0 * st_all["passive"] / nw,
        "note_that_per_1k": per1k("note_that"),
        "connectors_per_1k": 1000.0 * conn / nw,
        "parens_per_1k": per1k("paren"),
        "abstract_words": ab_words,
        "body_words": nw,
        "n_sections": len(secs),
        "n_figures": sum(1 for f in doc.floats if f["kind"] == "figure"),
        "n_display_eq": len(re.findall(r"\\begin\{(?:equation|align|eqnarray|gather|multline)\*?\}", doc.main_body)) + len(re.findall(r"\\\[", doc.main_body)),
    }


def compare_metrics(m, norms, register):
    n = norms.get(register) or norms.get("all", {})
    rows = []
    for k, v in m.items():
        ref = n.get(k)
        if not ref:
            continue
        status = "in" if ref["p10"] <= v <= ref["p90"] else ("LOW" if v < ref["p10"] else "HIGH")
        rows.append((k, v, ref["p10"], ref["p50"], ref["p90"], status))
    return rows


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def run_gate(path: Path, profile: str = "weidong-mei", register: str = "auto", metrics: bool = True):
    pdir = SKILL / "profiles" / profile
    rules = json.load(open(pdir / "rules.json", encoding="utf-8"))["rules"]
    doc = Doc(path)
    reg = detect_register(doc) if register == "auto" else register
    res = run_rules(doc, rules, reg)
    out = {"file": str(doc.root), "register": reg, "words": len(words(doc.prose_norm)), "results": res}
    if metrics:
        nf = pdir / "norms.json"
        if nf.exists():
            norms = json.load(open(nf, encoding="utf-8"))
            out["metrics"] = compare_metrics(compute_metrics(doc), norms, reg)
    return out


def render(rep, max_hits=6):
    lines = [f"== style_gate  file={rep['file']}  register={rep['register']}  prose_words={rep['words']} =="]
    lines.append(f"{'RULE':<6}{'sev':<6}{'hits':>5}{'ok<=':>6}  status  name")
    for r in rep["results"]:
        lines.append(f"{r['id']:<6}{r['severity']:<6}{r['n']:>5}{r['allowed']:>6.1f}  {r['status']:<6}  {r['name']}")
    bad = [r for r in rep["results"] if r["status"] != "PASS"]
    if bad:
        lines.append("")
        lines.append("-- details (rule, file:line, evidence) --")
        for r in bad:
            lines.append(f"[{r['id']} {r['status']}] {r['name']}  -> fix: {r['fix']}")
            for f, ln, sn in r["hits"][:max_hits]:
                lines.append(f"    {f}:{ln}  {sn}")
            if r["n"] > max_hits:
                lines.append(f"    ... {r['n'] - max_hits} more")
    if rep.get("metrics"):
        lines.append("")
        lines.append(f"-- metrics vs corpus ({rep['register']}); 'in' = inside corpus p10-p90 --")
        lines.append(f"{'metric':<26}{'value':>9}{'p10':>9}{'median':>9}{'p90':>9}  status")
        for k, v, p10, p50, p90, s in rep["metrics"]:
            flag = "" if s == "in" else "  <--"
            lines.append(f"{k:<26}{v:>9.2f}{p10:>9.2f}{p50:>9.2f}{p90:>9.2f}  {s}{flag}")
    fails = [r for r in rep["results"] if r["status"] == "FAIL"]
    warns = [r for r in rep["results"] if r["status"] == "WARN"]
    lines.append("")
    lines.append(f"SUMMARY: FAIL rules={len(fails)} (hits={sum(r['n'] for r in fails)}), WARN rules={len(warns)} (hits={sum(r['n'] for r in warns)})")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--profile", default="weidong-mei")
    ap.add_argument("--register", default="auto", choices=["auto", "letter", "conference", "full", "tutorial"])
    ap.add_argument("--json")
    ap.add_argument("--max-hits", type=int, default=6)
    ap.add_argument("--no-metrics", action="store_true")
    a = ap.parse_args(argv)
    reports = []
    for p in a.paths:
        try:
            reports.append(run_gate(Path(p), a.profile, a.register, not a.no_metrics))
        except (OSError, SystemExit) as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
    for rep in reports:
        print(render(rep, a.max_hits))
        print()
    if a.json:
        Path(a.json).write_text(json.dumps(reports, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    return 1 if any(r["status"] == "FAIL" for rep in reports for r in rep["results"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
