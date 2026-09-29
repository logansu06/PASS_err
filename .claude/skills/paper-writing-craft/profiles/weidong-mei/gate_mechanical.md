# Mechanical gate (profile `weidong-mei`)

> Everything a program can check, run by one script. It replaces the hand-run grep block of the
> default profile and is calibrated on the author's own papers: each rule was back-tested on the
> 85 technical papers of the corpus, and a rule that fired on a large share of them was relaxed
> (`rules.json` is the source of truth; the table below is generated from it).
> **Report the script's output, not "audited".** A mental pass is not a run.

## Run

```bash
python scripts/style_gate.py paper/main.tex                 # auto-detects the register
python scripts/style_gate.py paper/ --register letter       # letter | full | tutorial
python scripts/style_gate.py sections/*.tex --json audit.json --max-hits 10
```

- Follows `\input` / `\include`; reports `file:line` and a snippet for every hit.
- Exit status 1 if a FAIL rule is violated. WARN = fix or justify in the audit ledger. INFO = report only.
- `--profile snl-default` is not supported by this script (the default profile is documented in
  prose only); to grade a draft against the original SNL rules use `profiles/snl-default/gate_mechanical.md`.
- Below the rule table the script prints **metrics against corpus norms** for the detected
  register (p10 / median / p90 over the corpus): mean and p90 sentence length, share of sentences
  above 40 words, sentences per paragraph, `we` per 1k words, passive per 1k (approximate),
  additive connectors per 1k, `Note that` per 1k, parentheses per 1k, abstract length, body length,
  sections, figures, display equations. A `LOW` / `HIGH` flag means the draft is outside the range
  spanned by 80% of the author's papers; it is a prompt to look, not a defect.

## Rules

<!-- BEGIN RULES -->
| id | sev | rule | tolerated | fix | corpus papers flagged |
|---|---|---|---|---|---|
| MM01 | FAIL | dash used as punctuation (---, em-dash, spaced --) | 0 per paper | use a comma, parentheses, a colon or a new sentence (98% of corpus papers contain no dash) | 2/85 |
| MM02 | FAIL | exclamation mark in prose | 0 per paper | delete; state the fact | 1/85 |
| MM03 | FAIL | conversational / hype word with zero corpus frequency | 0 per paper | delete, or replace by the measured fact (a number in the results section, a contrast with prior work in the intro) | 0/85 |
| MM03b | WARN | hype word used in <=3% of corpus papers | 1 per paper | delete, or state the measured fact | 3/85 |
| MM04 | FAIL | contraction | 0 per paper | write the full form (possessive 's is fine) | 1/85 |
| MM05 | FAIL | 'Figure' spelled out before a reference (corpus: always 'Fig.') | 0 per paper | write Fig.~\ref{...} (plural Figs.~\ref{..} and \ref{..}) | 3/85 |
| MM06 | WARN | Eq./Equation before an equation reference (corpus: bare '(12)') | 1 per paper | cite equations as \eqref{...} without the word 'Eq.' | 4/85 |
| MM07 | WARN | i.e. / e.g. not followed by a comma | 0 per paper | write i.e., / e.g., (the comma is present in 99% of the corpus's uses; a few papers omit it) | 12/85 |
| MM08 | INFO | Firstly / Secondly / Thirdly / Lastly | 0 per paper | 'First, / Second, / Finally,' is the majority style; Firstly/Lastly appear in ~20% of papers | 17/85 |
| MM09 | FAIL | duplicated function word (the the, is is ...) | 0 per paper | delete the repeat | 7/85 |
| MM10 | WARN | straight double quote in the source | 0 per paper | use ``text'' in LaTeX | 14/85 |
| MM11 | WARN | sentence longer than 100 words | 0 per paper | split; the corpus p95 for >60-word sentences is 0.7 per 1k words | 3/85 |
| MM12 | WARN | sentences longer than 60 words (rate cap) | 1 per paper; 0.8 per 1k words | split at the 'which' / 'where' / 'while' clause; cap = corpus p95 (0.8 per 1k words) | 2/85 |
| MM12b | WARN | sentences longer than 45 words (rate cap) | 2 per paper; 3.0 per 1k words | corpus: p50 1.0 / p90 2.6 per 1k words; mean sentence length is 24 words, p90 37 | 4/85 |
| MM13 | INFO | section heading not in Title Case (89% of corpus papers use Title Case) | 0 per paper | Title Case is the norm (89%); three 2025-26 papers use sentence case, so keep one style within a paper | 9/85 |
| MM14 | INFO | separate Related Work / Background section | 0 per paper | 0/85 technical papers have one; the prior-art review sits in the Introduction | 0/85 |
| MM20 | WARN | abstract length / content | 0 per paper | keep the abstract inside the register range (letter ~180 words, conference ~195, full ~268, tutorial ~190); no citations, no display math | 5/85 |
| MM21 | WARN | figure caption has more than one sentence | 1 per paper | 96% of corpus captions are one sentence; move interpretation into the running text | 2/85 |
| MM22 | WARN | figure caption lacks final period | 1 per paper | end figure captions with a period (94%) | 10/85 |
| MM23 | WARN | figure caption longer than 25 words | 1 per paper | median is 8 words, p75 12; state the quantity versus the swept variable and the fixed parameters | 6/85 |
| MM24 | WARN | figure caption in Title Case | 0 per paper | figure captions use sentence case (88%); acronyms and proper nouns may be capitalised | 9/85 |
| MM25 | WARN | \subfloat[] labels without (a), (b) in the caption | 0 per paper | the group writes empty \subfloat[] and enumerates '(a) ...; (b) ...' inside the main caption | 2/85 |
| MM26 | WARN | table caption below the tabular | 0 per paper | IEEE tables: caption above | 0/85 |
| MM27 | INFO | algorithm caption ends with a period | 0 per paper | 87% of algorithm captions have no final period (Title Case, e.g. 'Proposed Algorithm for Solving (P1)') | 6/85 |
| MM28 | WARN | display equations without final , or . | 0 per paper | equations are part of sentences: end with a comma when 'where ...' follows, a period otherwise | 5/85 |
| MM29 | INFO | contribution list form | 0 per paper | 3 plain-sentence items of ~110 words; see rhetorical_moves.md | 2/85 |
| MM30 | INFO | agentless 'is proposed / was studied' in abstract or conclusion | 0 per paper | both 'we propose ...' and 'is proposed' occur (45% of papers use the agentless form in the abstract or conclusion); recent papers prefer 'we' | 38/85 |
| MM40 | WARN | quality adjective used more than the corpus does | 2 per paper | corpus: 'novel' in 21% of papers at 0.06 per 1k words; claim novelty by contrast ('Unlike existing works ...') | 8/85 |
| MM41 | WARN | weak qualifier | 3 per paper | delete, or replace by the quantity | 7/85 |
| MM42 | WARN | leverage / utilize | 6 per paper | use / employ / apply (corpus: ~1.5 per paper) | 10/85 |
| MM43 | WARN | wordy connective | 4 per paper | to / because / delete | 6/85 |
| MM44 | WARN | additive connectors stacked in one paragraph | 0 per paper | at most three of Moreover / Furthermore / Additionally / In addition / Besides per paragraph | 3/85 |
| MM45 | WARN | three consecutive sentences start with 'We' | 0 per paper | front-load a purpose or condition: 'To ..., we ...', 'Based on ..., we ...' | 0/85 |
| MM46 | WARN | etc. / and so on | 2 per paper | close lists with 'among others' or name the last item | 2/85 |
| MM47 | WARN | priority claim | 0 per paper | corpus: 'for the first time' in 1% of papers; contrast with named prior work instead | 4/85 |
| MM48 | WARN | sentence starting with And / But / So | 0 per paper | However, / Moreover, / Hence, | 3/85 |
| MM49 | WARN | first person singular | 0 per paper | the group writes 'we' even for single-author papers | 0/85 |
<!-- END RULES -->

`Tolerated` is the number of hits per paper that does not fire the rule; `corpus papers flagged`
is how many of the 85 technical papers would be flagged by that rule as configured (the target is
0-5% for FAIL rules; higher values are rules kept because they catch real typography errors).

## Where this profile departs from the default (`snl-default`) gate

| default rule | verdict of the default gate | this profile | evidence (85 technical papers) |
|---|---|---|---|
| M1 no dashes | banned | **kept** (MM01) | 98% of papers contain none |
| M2 antithesis (`rather than`, `not only ... but`, `on the other hand`) | banned as decoration | **not enforced** | `on the other hand` 55% of papers, `rather than` 25%, `not only` 21%; they mark real contrasts |
| M3 / M4 / M8 / M9 / M10 editorial closers, vacuous intensifiers, grandiose setups, metaphor filler, hype verbs | banned | **kept for the words the corpus never uses** (MM03), capped for rare ones (MM03b, MM40, MM41) | `truly / really / genuinely / we believe / shed light`: 0 papers; `indeed` 3%; `cutting-edge` 3% |
| M5 banned adjectives (`novel`, `significant`, `promising`, `comprehensive`, `robust`, `leverage`, `utilize`, ...) | banned | **relaxed** to caps (MM40, MM42) | `significant(ly)` 100% of papers (1.1 per 1k); `promising` 65%; `leverage` 64%; `utilize` 59%; `novel` 21% (0.06 per 1k); `robust` 21%; `state-of-the-art` 1% |
| M6 throat-clearing openers (`Moreover`, `Furthermore`, `It is worth noting`) | banned | **relaxed**: allowed, stacking guarded (MM44) | `Moreover` 98% of papers (0.87 per 1k), `Furthermore` 86%, `It is worth noting that` 61%, `Note that` 94% |
| M7 rule-of-three decoration | audit | not enforced | |
| M11 passive voice | zero tolerance | **relaxed**: idiomatic in set-up, derivation, and result-reading frames; only contribution claims should be active (MM30, INFO) | ~19 passives per 1k words in every paper (100% of papers) |
| M12 wordiness | cut | **kept with caps** (MM43) | `in order to` 19% of papers, `so as to` 25%, `the fact that` 36%; all at <=0.1 per 1k |
| M13 weak qualifiers | delete | **kept with caps** (MM41) | `very` in 48% of papers (~1 per paper); `quite` 5% |
| M14 firstly / secondly | fix | INFO (MM08) | ~20% of papers use `Firstly` / `Lastly` once |
| M15 no `!`, one rhetorical question in an introduction | banned | **kept** (MM02) | 0 exclamation marks; 2 papers contain a `?` outside a title |
| M16 pompous single words, M17 fancy verbs | audit | not enforced | `delve` 18%, `circumvent` 19%, `dispense with` 14% of papers, 1-2 uses each |
| M18 content-free openers (`In this paper, we ...`, `In this section, we ...`) | banned | **reversed**: expected | `In this section, we` opens sections in 94% of papers, `In this paper, we` in 92% |

The upstream regexes applied verbatim to the corpus (`stats_upstream_gate_on_corpus.md`) reject
99% of the author's papers on M5, M6 and M18 and 100% on M11. That is why the default gate cannot be used
to reproduce this voice.

## What no script can check (goes to `gate_semantic.md`)

Define-before-use, notation consistency, claim-evidence tie, honest positioning of prior work,
benchmark fairness, whether a result paragraph explains its figure.
