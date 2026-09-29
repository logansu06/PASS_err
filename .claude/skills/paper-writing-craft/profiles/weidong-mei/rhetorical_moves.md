# Rhetorical moves, section by section

> The skeleton of a wireless-optimization paper as it appears in the corpus: 85 technical papers,
> of which 30 follow `Introduction > System Model > Solution > Solution > Numerical Results >
> Conclusion` and 24 follow the five-section variant with one solution section. No paper has a
> Related Work section. Frames use `<placeholders>`; they are forms, not text to copy.
> `L` = letter, `Cf` = conference paper (ICC / GLOBECOM, 5-6 pp.), `F` = full journal paper, `T` = tutorial / magazine.

## Skeleton and section titles

| section | typical title (count among 85) | notes |
|---|---|---|
| I | Introduction (85) | also carries the literature review, contributions, organization, notation |
| II | System Model (40) / System Model and Problem Formulation (33) / Problem Formulation (10) | letters and short papers merge model and problem |
| III... | Proposed Solution to (P1) (11+) / Proposed Algorithm / Single-User Case / Multi-User Case / Performance Analysis / Special Case Analysis | one or two sections; name the problem label |
| n-1 | Numerical Results (58) / Simulation Results (25) | Numerical Results dominates since 2023 |
| n | Conclusion (51) / Conclusions (29) / Conclusion and Future Work (2) | |
| | Appendix "Proof of Lemma 1" | 28% of papers; F 45%, Cf 17%, L 8% |

Titles are Title Case in 89% of papers; keep one style inside a paper.

## Title

`<Technology>-<Enabled | Enhanced | Aided | Assisted | Empowered> <Function or System>` (43%) ·
`<Task> for | via | with | in <Technology>` (71% contain for / via / with / in) · colon subtitle (42%):
`<Headline>: <Performance Analysis and Optimization | Architecture and Design | Fundamentals, Design Issue, and Prototype>` ·
question form only for a head-to-head comparison (5%: `X Meets Y: Friends or Foes?`, `NOMA or OMA?`).
9.5 words [8-12], Title Case (98%). `Optimization` in 32% of titles, `Design` 10%, `Joint` 9%.
Keywords (IEEE index terms): 5.

## Abstract (one paragraph, no citations, no equations; L 182 words, Cf 195, F 268; 8 sentences)

| move | function | frame | corpus |
|---|---|---|---|
| A1 | technology and its promise | `<Technology (ACR)> has emerged as a promising <solution> for <goal>` / `has attracted increasing attention in <field>` / `offers <extra DoF>` | first sentence: technology-promise 54%, problem/context 31%, `This paper ...` 15% |
| A2 | gap or challenge | `However, <challenge>` / `Despite ..., <limit of prior work>` | 1 sentence |
| A3 | what this paper does | `In this paper/letter, we investigate <scenario>, where <system>. We aim to <maximize/minimize> <metric> by jointly optimizing <variables>.` | `we` x3 |
| A4 | difficulty, then method | `However, the problem is <non-convex / coupled / combinatorial>. To tackle this challenge, we first <special case or key idea>. Then, we <general algorithm>.` Name the algorithm family once (`alternating optimization (AO)`, `graph-based`, `successive convex approximation`). | 2-3 sentences |
| A5 | result, qualitative | `Numerical results show/demonstrate that the proposed <method> outperforms <benchmark(s)> ...` | 96% mention simulation/numerical results; 1% contain a number |

Define acronyms inside the abstract (81% define one in the first ten words). A coined scheme name
is introduced with `termed as` / `named`. Variants: technical-letter abstracts are shorter
(A1+A2 merge); tutorial abstracts replace A3-A5 with `In this article, we present / provide an
overview of ...` and a closing sentence about open directions.

## Introduction

| move | function | frame | notes |
|---|---|---|---|
| I1 | driver | `In future 6G wireless systems, <application demands> ...` | 1 paragraph, 2-5 cites |
| I2 | technology and benefit | `Recently, <technology> has emerged ...`. `Compared to <conventional baseline>, <technology> can <benefit> by <mechanism>.` | define acronym, alias (`also known as`); F 1-2 paragraphs, L and Cf merge I1 and I2 |
| I3 | prior art by cluster | `The authors in [x] studied ...`; `In [x], ... was proposed`; group with `Furthermore`, `On the other hand` | 1-3 paragraphs; ~14 cites; past tense |
| I4 | gap | `However, all of the above works only <limitation> / rely on <assumption>, which may limit their generality / without delving into <missing aspect>. It remains unclear whether <question>.` | the gap is scoped and hedged ("may not fully exploit") |
| I5 | this paper | `To fill this gap / Motivated by the above, in this paper we <verb> <scenario>, as shown in Fig. 1.` then one sentence on the objective and variables | Fig. 1 is the system model |
| I6 | contributions | see below | F: bullet list 60%; L: in-paragraph |
| I7 | scope note (optional) | `It is worth noting that <related but different setting> is beyond the scope of this paper.` | |
| I8 | organization and notation | `The rest of this paper is organized as follows. Section II ... Finally, Section VI concludes the paper and discusses future directions.` then `Notations: ...` | F 90%, Cf 11%, L 0%; Notations F 62%, Cf 67%, L 32%, always last in the introduction |

**Contribution list (F, 83% of full papers).** `The main contributions of this paper are summarized as follows.`
Three `itemize` bullets of ~110 words [93-130], plain sentences without bold labels (0 of 37 lists
use one). Item 1: formulation and difficulty (`We formulate ... by jointly optimizing ... Since the
problem is non-convex, we first ...`). Item 2: solution and insights (`Next, to solve ..., we propose
... Specifically, ...`; the purpose clause `To gain insights, ...` often opens it). Item 3: evidence
(`Finally, numerical results show / demonstrate ...`). Openers seen: `We formulate`, `To ...`,
`First, we`, `Next, ...`, `Finally, numerical results ...`. **Contributions (L and Cf; a bullet list occurs in 1 of 25 letters and 1 of 18 conference papers)**: the same three
moves as two or three sentences inside the `This paper ...` paragraph, no bullets.

**Letter / conference shape.** 4 paragraphs (L ~550, Cf ~600 words): [I1+I2] · [I3+I4] · [I5+I6] · Notations (Cf 67%, L 32%).

## System model

| move | frame | notes |
|---|---|---|
| S1 scenario | `As shown in Fig. 1, we consider <system>, where <entity A> equipped with <N> <antennas> serves <K> <users>.` | Fig. 1 first cited here if not in the introduction |
| S2 sets and variables | `Let X denote ...` (about 2% of sentences start with `Let`), `Denote by ...`, `For convenience, we refer to ... as ...`, `For ease of exposition, ...` | one symbol, one meaning; sets calligraphic |
| S3 assumptions, justified and scoped | `We assume <X> for simplicity / to focus on <Y>.` `Without loss of generality, we assume ...` `Note that <the model> can be extended to <richer case>.` Practical caveats go into a `\footnote` (174 footnotes in 102 papers) | every assumption gets a reason or a scope statement |
| S4 channel / signal model | equation + `where <symbol> denotes ...` | numerical values stay for the results section |
| S5 metric | `The received SNR is given by ...` | |
| S6 remark | `Remark 1: ...` (35% of papers) or `It is worth noting that ...` | comparison with a conventional model, or an implication |

## Problem formulation

1. `we aim to <maximize | minimize> <objective> by jointly optimizing <variables>, subject to <constraints>` (`we aim to` in 69 of 85 papers).
2. The problem, labelled `(P1)`, in an `align` block with `s.t.` and each constraint labelled; `where` explains constraints. (67% of papers label problems; chains `(P1) -> (P2) -> (P3)`.)
3. Difficulty: `However, (P1) is a non-convex problem that is challenging to solve due to <coupling / constraints>.`
4. Roadmap: `To reveal essential insights, we first ... Next, ...`

## Solution sections

| move | frame |
|---|---|
| A1 opener | `In this section, we <verb> ... Note that for any given <X>, the optimal <Y> is given by ...` |
| A2 special case first | `To gain useful insights, we first consider <single-user | far-field | simplified> case ...` then `Next, we extend to the general case.` |
| A3 decomposition | `First, we optimize <X> for given <Y>. ... Then, (P1) can be simplified as (P2). ... which, however, is still non-convex. To tackle this challenge, we utilize <method>. Specifically, it can be easily shown that ...` |
| A4 key result | Lemma / Proposition (59% of papers use one; median 1) with `Proof: See Appendix A.` Interpretation follows in a `Remark` or `It is worth noting that ...` |
| A5 algorithm | `The overall procedure is summarized in Algorithm 1.` |
| A6 complexity, convergence | `The complexity of Algorithm 1 is in the order of O(...)` ; `the objective value is non-decreasing over iterations and bounded, hence Algorithm 1 converges` |
| A7 quality of the answer | `high-quality suboptimal solution` / `near-optimal` / `suboptimal` (60% of papers use at least one) ; `closed-form` (52%) |
| A8 extension | `Note that the proposed algorithm can be extended to <case> by <change>.` |

## Numerical results

| move | frame |
|---|---|
| R1 opener | `In this section, we provide numerical results to evaluate the performance of our proposed <method>.` (variants: `present`; `numerical results are provided to validate the efficacy of ...`; all registers; `In this section, we` opens a section in 94% of papers) |
| R2 setup | `Unless otherwise stated, the simulation settings are as follows.` Parameters run inline in prose: carrier frequency, array size, geometry, path-loss model and exponent, noise power / transmit SNR, channel model with its reference. `All results are averaged over <1000> independent channel realizations.` Tables of parameters are rare (median 0 tables per paper). |
| R3 benchmarks | `We compare our proposed algorithm with the following benchmarks:` as an `itemize` with `\textbf{<Name>}:` then one or two sentences describing what the benchmark omits (`Benchmark 1: ...`, or descriptive names such as `FPA`, `Antenna selection (AS)`, `MA-RPS`). Include a conventional baseline and, when one exists, the optimal or an upper-bound benchmark. |
| R4 result paragraphs | one per figure; anatomy in `craft_reference.md` section 4. Sweep order: the main variable first, then the parameters that drive the mechanism. |
| R5 anomalies | when curves coincide or a benchmark wins: state it and give `The possible reason is ...` |
| R6 algorithm behavior | convergence curve, run time, or complexity comparison whenever an algorithm is proposed |

## Conclusion (one paragraph; L 104 words, Cf 102, F 236)

C1 recap in the past tense: `In this paper, we investigated <problem> for <system>. <One or two
sentences on the method, with the key technical idea>.` · C2 result recap, qualitative:
`Numerical results showed / validated ...` · C3 (F 71%, L 40%, Cf 6%) future work:
`This paper can be extended along several directions in future work. For example, <direction>.`
No new content, no numbers repeated, no acknowledgements of limitations that contradict the
claims.

## Appendix

`Appendix A: Proof of Lemma 1`. Proofs are compact: restate the setup, chain the equalities
with `where`, close with the conclusion of the lemma. 28% of papers have an appendix.

## Tutorial / magazine variant

`Introduction (with a comparison table) > Fundamentals > Applications / Design issues > Open
challenges and future directions > (Prototype and experimental results) > Conclusion`.
Enumerated `First, ... Second, ...`; each subsection opens with the takeaway then the mechanism;
figures are rendered scenes and block diagrams (`figures_tables.md`); numerical evidence is one
or two figures at the end.
