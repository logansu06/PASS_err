# Editorial principles (profile `weidong-mei`)

> What the corpus shows the papers *do*, stated as rules a draft can be checked against. Each has its
> evidence. These are cross-sectional patterns from 102 finished arXiv papers, not a revision-history
> study (that method of the default profile needs Overleaf histories that are not public). Where a
> principle of the default profile still holds, it is marked *(default Pn)*.

**P1. One skeleton.** Introduction, System Model (and Problem Formulation), one or two solution
sections, Numerical Results, Conclusion. 54 of 85 papers follow exactly this; 6 sections is the median.
No Related Work section in any paper: the review lives in the Introduction. Evidence: `stats_body.md`.

**P2. Context first, then the technology, then the gap, then this paper.** Abstracts open with the
technology and its promise (54%), the problem (31%), or `This paper` (15%). Introduction paragraphs
after the first open with `To ...`, `However,`, `Motivated by the above`, `Recently,`, `Despite`. The
default profile's "problem-first, never technology-first" (default P7) does **not** describe this voice.

**P3. Name the gap by contrast with named prior work, and scope it.** `Unlike / Different from ...` (74%),
`the authors in [x] ...` (61%), then `However, all of the above only ...`. Limitation sentences are hedged
(`may not fully exploit`); own results are asserted. Own earlier work is cited with its delta.

**P4. Claims live in three places and say the same thing.** Abstract (compressed), introduction
(three bullet-length statements or one paragraph), conclusion (recap). Numbers appear only in the results
(abstract: 1%). This replaces the default's "results preview with numbers" (default Move 6).

**P5. One problem, one chain.** The formulation is a labelled `(P1)`; difficulty is stated in the next
sentence; sub-problems `(P2)`, `(P3)` derive from it; each algorithm has complexity and convergence.
67% of papers label problems; 61% contain an algorithm box.

**P6. Insight through a special case.** When the general problem is hard, solve a special case first
(`To gain useful insights, we first consider ...`), state what it reveals, then generalize. The phrase family
`unveil / reveal / uncover ... insights` occurs in 67% of papers.

**P7. Evidence is explained.** Each result paragraph runs pointer, observation, mechanism, quantified
gap, implication (`thanks to`, `This is because`, `The possible reason is`). This is the profile's counterpart
of the default's Takeaway paragraph (default P8), placed inside each paragraph instead of after a cluster.

**P8. Benchmarks are named, explained, and fair.** A conventional baseline, ablation-type variants, and an
optimal or upper-bound reference when available; a bold-named `itemize` in 21 papers, `Benchmark n` in others;
identical names in text, caption, legend.

**P9. Simulation setup is complete and inline.** `Unless otherwise stated, ...` with carrier frequency,
geometry, array sizes, channel model and reference, path loss, noise / SNR, number of realizations;
parameters in prose, not in a table (median 0 tables).

**P10. Honest scope, stated where it applies.** Each assumption is justified (`for simplicity`, `to focus
on`) or scoped (`can be extended to`); practical caveats in footnotes; future work in 52% of full papers.
No `for the first time` (1%), no `novel` as a selling word (0.06 per 1k words), no `state-of-the-art` (1%).

**P11. Terse figure captions, interpretation in the text.** Median 8 words, one sentence, period, sentence
case; `<metric> versus <variable>`. This is the opposite of the default's "bold takeaway in the caption" (G7).

**P12. Notation is set once.** A `Notations:` paragraph at the end of the introduction (F 62%, Cf 67%, L 32%);
`\triangleq` for definitions (70 of 85 papers); calligraphic sets (85 of 85); equations punctuated as
sentences (83%); cited as `(12)`.

**P13. Length follows the register.** Letter: 3,100 words, abstract 182, 4-paragraph introduction, 3 figures.
Conference (ICC / GLOBECOM): 3,150 words, abstract 195, 4-paragraph introduction, 5 figures, no roadmap sentence,
no future-work sentence. Full paper: 7,400 words, abstract 268, 10-paragraph introduction, 9 figures, contribution
list, roadmap, future work. Tutorial: 8,700 words, 19 subsections. Sentence length does not change with register (23.0-24.4).

**P14. Introduction after the results, structure before prose.** *(default P1, P5 and the topic-sentence-first
rule keep their force.)* The evidence cannot show this in a finished paper, so the process rules of the
default pipeline (Draft 0 introduction, results, then final introduction; topic sentences before paragraphs)
remain in force in `SKILL.md`; what changes is the target form of each section.

## Where the default principles are not applicable to this voice

| default principle | verdict | reason |
|---|---|---|
| P3 What-Why-So-What headings (claim-first headings) | not used | every section title in the corpus is a topic title (`Numerical Results`, `System Model`, ...) |
| P4 compress by 30-50% | applies only to page-limit compression; the corpus mean sentence (23.7) is not shortened | see `compression_overrides.md` |
| P6 labelled paragraphs (`\smartparagraph`) | not used | systems-paper convention |
| P7 problem-first | partly | 54% open with the technology |
| P9 dual evaluation | applies as: analysis vs simulation vs prototype sections when present | |
| P14 technical claims need citations | **holds and is stronger**: 26 cites per paper, ~14 in the introduction | |
