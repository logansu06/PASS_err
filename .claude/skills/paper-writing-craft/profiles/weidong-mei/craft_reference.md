# Craft reference: how these papers are written (positive layer)

> Distilled from 102 arXiv papers that carry Weidong Mei's name (85 technical papers, 17
> tutorial / magazine / survey papers, 2016-2026). Read it while drafting; the gates
> (`gate_mechanical.md`, `gate_semantic.md`) catch the defects. Figures in brackets are
> `[papers using it / 85 technical papers]` or `median [IQR]`; all evidence is in `stats_*.md`.
> Every rule describes a habit of form. None of it licenses reusing the corpus's sentences,
> claims, or numbers: the content of the user's paper is always the user's own.

## 0. Choose the register first

The papers fall into four registers. Sentence-level habits are the same in all of them (mean
sentence 23.0-24.4 words); what changes is size and skeleton. `scripts/style_gate.py` detects the
register (`this letter` in the text -> letter; `\documentclass[conference]` -> conference; no
simulation section -> tutorial; else full) and compares the draft with that register's norms.

| | Letter (IEEE WCL style) | **Conference** (ICC / GLOBECOM, 5-6 pp.) | Full paper (TWC / TCOM / JSAC style) | Tutorial / magazine / overview |
|---|---|---|---|---|
| n in corpus | 25 | 18 | 42 | 17 |
| body words | 3,124 [2,896-3,508] | 3,155 [2,984-3,451] | 7,415 [6,247-7,896] | 8,682 [4,625-18,183] |
| abstract words | 182 [156-201] | 195 [177-224] | 268 [234-290] | 189 [150-209] |
| introduction | 553 words, 4 paragraphs | 597 words, 4 paragraphs | 1,407 words, 10 paragraphs | 1,450 words, 13 paragraphs |
| sections / subsections | 6 / 6 | 6 / 4 | 7 / 10.5 | 6 / 19 |
| display equations | 21 | 23.5 | 48 | 0 [0-22] |
| figures | 3 | 5 [4-7] | 9 [7-10] | 7 [6-19] |
| simulation section | 627 words | 705 words | 1,541 words | rare |
| conclusion | 104 words | 102 words | 236 words | 181 words |
| references (bibitems) | ~15 | ~17 [15-19] | ~40 | 58 cites [22-267] |
| contribution bullet list | 4% | 6% | 83% | n/a |
| "The rest of this paper is organized as follows" | 0% | 11% | 90% | in some |
| `Notations:` paragraph (end of introduction) | 32% | 67% | 62% | in some |
| `(P1)`-labelled problems | 56% | 83% | 67% | n/a |
| algorithm box | 44% | 67% | 69% | rare |
| lemma / proposition / theorem | 48% | 44% | 71% | rare |
| appendix | 8% | 17% | 45% | 0% |
| future-work sentence in the conclusion | 40% | 6% | 71% | in some |

Default register: `conference` when the target is a 5-6 page IEEE conference paper (the format of
ICC and GLOBECOM: 18 corpus papers use `\documentclass[conference]{IEEEtran}`), `letter` for a 5-page
letter, `full` for a regular journal paper. A conference paper is written like a letter, not like a
shortened journal paper: three or four introduction paragraphs, contributions inside the
`This paper ...` paragraph, no roadmap sentence, no future-work sentence.

## 1. Base rules (all registers)

1. **Sentence length.** Mean 23.7 words [21.6-25.1], median 22, p90 37. About 7% of sentences
   pass 40 words (p10-p90 of papers: 3-14%); 100+ words is a defect. Inline symbols count as
   one word each. Do not compress to the 21-word target of the default profile: the corpus is
   consistently longer, and short staccato prose is not this voice.
2. **Paragraph.** 4.2 sentences [3.5-4.7]; one function per paragraph (claim, evidence,
   interpretation, or transition). Topic sentence first.
3. **Front-load, then "we".** "We" occurs 10.7 times per 1,000 words but starts only 2% of
   sentences. The signature frame is `[purpose | condition | reference], we [verb] ...`:
   `To <verb> <problem>, we ...` (98% of papers use To tackle / address / overcome / solve /
   handle) · `Based on <X>, we ...` · `For any given <X>, we ...` · `Motivated by the above, we ...`
   (51%) · `As shown in Fig. N, we consider ...` · `In this section, we ...` (94%).
   Three consecutive sentences that start with "We" do not occur.
4. **Verbs after "we"**, by frequency: can (obtain / see / express), consider, have, assume,
   propose, set, aim to, define, show, plot, present, derive, focus on, introduce, denote,
   adopt, compare, obtain, apply, employ, formulate, optimize, investigate, develop, analyze.
5. **Voice.** Active `we` carries choices, claims, and the walk through the argument. Passive
   is idiomatic in three places: set-up (`is given by`, `can be expressed as`, `is assumed to
   be`, `is set to`, `is equipped with`, `is denoted by`, `is defined as`), derivation (`can be
   obtained by`, `can be simplified as`), and reading a result (`It is observed that` [78%]).
   The measured passive rate is ~19 per 1,000 words (regex upper bound). Passive is a defect
   only when it hides the actor of a design choice or a contribution (`a scheme is proposed`
   in the contribution list; prefer `we propose`).
6. **Tense.** Present for the model, the method, and what a figure shows (`the received SNR
   increases with N`). Past for prior work (`the authors in [x] proposed`) and, since 2023, for
   the conclusion recap (57 of 65 papers: `In this paper, we investigated ...`). Papers before
   2022 often recap in the present (`This paper studies ...`); pick past.
7. **Terms.** Define at first use with the acronym in parentheses (81% of abstracts do it in
   the first ten words), then use the acronym only. Plurals `MAs`, `FPAs`. Hyphenate
   compounds: `MA-enhanced`, `IRS-aided`, `graph-based`, `high-quality`, `near-optimal`. Coin
   a term with `termed as / referred to as / named` [58%] and set it in `\emph{}` once.
   One concept, one name for the whole paper (`antenna position vector (APV)` stays APV).
8. **Hedging is asymmetric.** Hedge claims about other people's work and about approximations
   (`may not fully exploit`, `mostly focused on`, `may incur`, `generally`, `usually`, `in
   practice`); assert your own results (`outperforms`, `achieves`). Modal counts: `can` 8.0
   per 1k words, `may / might / could` 1.1 per 1k. Never hedge a number you measured.
9. **Novelty by contrast, not by adjective.** `Unlike / Different from / In contrast to existing
   works [x], ...` [74%]. `novel` appears in 21% of papers at 0.06 per 1k words; `for the first
   time` in 1%; `state-of-the-art` in 1%; `To the best of our knowledge` in 25%.
10. **Result verbs.** outperform, achieve, yield, validate, demonstrate, show, verify;
    `efficacy / effectiveness / superiority` [79%]. `significantly` is in every paper (1.1 per 1k):
    allowed in the abstract, introduction, conclusion, and result commentary; in the results
    section attach a quantified gap in the same paragraph (`about 1.1 dB higher`, `165%`).
11. **Numbers live in the results.** Abstract: no numbers (1% have one). Introduction: rarely.
    Results: dB, bps/Hz, %, m, GHz, dBm, complexity orders `O(.)`.
12. **Insight language.** `to unveil / reveal / uncover [useful | essential] insights` [67%];
    `insight(s)` [51%]. The recurring device is *special case first*: `To gain useful insights,
    we first consider a single-user case ..., then extend to the general case`.
13. **Punctuation.** No dash used as punctuation [98%]. No exclamation mark, no rhetorical
    question in the body. Parentheses ~20 per 1k (acronyms, `e.g.,`, `i.e.,`); both always
    followed by a comma [99%]. Colons introduce lists and benchmark names; semicolons are
    rare (0.5 per 1k). `w.r.t.` and `s.t.` are accepted abbreviations.
14. **Equations are sentences.** A display equation ends with `,` when `where ...` follows and
    with `.` when it closes the sentence [83% punctuated]. Introduce with `is given by`, `can be
    expressed as`, `is formulated as`, `can be recast as`. Follow with `where X denotes ...`.
    Cite an equation as a bare `(12)` (`\eqref`), never `Eq. (12)` [23 uses in 102 papers].
15. **Cross-references.** `Fig. N` (never `Figure N`), `Figs. N and M`, `Section N`, `Table N`,
    `Algorithm N`, `Lemma N`, `Proposition N`, `Remark N`, `problem (P1)`.
16. **Own prior work is cited and its delta stated**: `In our previous work [x], we developed
    ... but only considered a simplified single-MA single-user setup.` (Then say what is new.)

## 2. Transition inventory (share of papers using it; per 1,000 words)

| function | use | avoid |
|---|---|---|
| add | Moreover [98%, 0.87] · Furthermore [86%, 0.60] · In addition [75%, 0.44] · Besides [38%] · Additionally [22%] | Indeed [3%] · Importantly [4%] |
| contrast | However [~1.3] · Nonetheless [58%] · In contrast [58%] · On the other hand [55%] · Unlike [74%] | On the one hand [6%] |
| consequence | Thus [86%] · Hence [78%] · As a result [71%] · Accordingly [68%] · Therefore [62%, 0.38] · Consequently [44%] | |
| specify | Specifically [99%, 0.94] · In particular [92%, 0.61] · For example [76%] · Particularly [49%] | |
| sequence | First / Second / Next / Then / Finally [2.5 combined] · To this end [62%] | Firstly / Lastly [~20%; `First,` / `Finally,` is the majority] |
| attention | Note that [94%, 0.8] · It is worth noting that [61%] · Recall that | It should be noted that [16%] |
| observe | It is observed that [78%, 0.44] · It is also observed that · It can be shown that [45%] | As expected [26%, sparingly] |
| explain | This is because [66%] · thanks to [47%] · due to [99%] · The reason is that [25%] · The possible reason is | |

Stack at most two additive connectors (Moreover / Furthermore / In addition / Besides /
Additionally) in one paragraph; three in a paragraph occurs in 4% of papers.

## 3. Introduction: how the argument moves

Paragraph openers after the first, by frequency: `To ...` (to tackle / overcome / address),
`However,`, `Motivated by the above`, `In ...`, `Recently,`, `Despite ...`. The introduction is
the review of prior work: no separate Related Work section exists in any of the 85 technical
papers. Review by cluster, using `the authors in [x] ...` [61% of papers, ~3 per paper among those that use it] and
sentence-initial `In [x], ...`, then close the cluster with a limitation sentence
(`However, all of the above works only ...`, `most of them rely on ... which may limit their
generality`, `without delving into ...`, `it remains unclear whether ...` [22%]). Citations:
14 in the introduction [10-23], ~26 in the paper.

## 4. Results commentary: the paragraph anatomy

Every result paragraph is anchored on one figure and runs
`pointer -> observation -> mechanism -> quantified gap -> implication`:

`First, we plot <metric> versus <sweep variable> in Fig. N.` (or `As shown in Fig. N, ...`,
45% of figure-citing sentences) → `It is observed that <trend>` → `thanks to <mechanism>` /
`This is because <mechanism>` → `<proposed> achieves about <x> dB higher <metric> than
<benchmark>` → `This suggests / implies <consequence>.`

When two curves coincide or the benchmark wins in some regime, say so and explain it
(`The possible reason is ...`). Next paragraph starts with `Next,` / `Moreover,` / `Finally,`.

## 5. Tutorial / magazine register (deltas)

`we` drops to 2.9 per 1k (from 10.7); `Note that` to 0.2; equations nearly vanish; `promising`,
`efficient`, `critical`, `emerged` rise (0.5-2.6 per 1k) because the piece surveys a field;
subsections average 19; enumerations use `First, ... Second, ...` and named categories; each
algorithm family gets a short paragraph (`The core idea is ...`, `The merits are threefold`),
a comparison table (`Comparison of ...`), and a guidance list (`For scenarios demanding X, Y is
the most suitable choice`). Figures are richer (3D-rendered scenes, block diagrams).
The conclusion closes with a wider-scope sentence about follow-up technologies.

## 6. Do not

- Do not import sentences, numbers, or claims from the corpus. Reuse only forms.
- Do not use `Indeed`, `truly`, `really`, `we believe`, `shed light`, `game-changing`.
- Do not open a technical-paper abstract with a number; open with the technology and its promise
  (54%), the problem (31%), or `This paper ...` (15%).
- Do not add a Related Work section, a claim-first heading, or a bold-labelled contribution
  list; the corpus has none of them (see `gate_mechanical.md` MM14, MM29).
