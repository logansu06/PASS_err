# Compression: overrides to `snl-default/compression_patterns.md`

Compression here means **fitting a page limit** (IEEE letters: 5 pages; conference papers: 5-6 including references; regular papers: 12-14) without
changing the voice. The default profile's target of 30-50% reduction and a 21-word sentence mean does not
fit: the finished papers have a 23.7-word mean and 4-paragraph letter introductions, so a draft that already
matches the register norms in `norms.json` needs no compression.

Order of operations (stop when the page count fits):

1. **Merge, do not shorten.** Fold the prior-art clusters of the introduction into fewer paragraphs
   (`the authors in [x] ...` chains), keep one limitation sentence per cluster.
2. **Move parameters into prose; drop parameter tables** (median 0 tables per technical paper).
3. **Turn a secondary remark into a footnote** (`\footnote{Note that ...}`; 137 in the corpus) or delete it.
4. **Merge result figures into sub-panels** only when they share an axis or a parameter; use the
   `\subfloat[]` idiom with panels enumerated in the caption (`figures_tables.md`).
5. **Move long proofs to the appendix** (`Proof of Proposition 1`, referred to as `Proof: See Appendix A.`);
   letters and conference papers use an appendix in 8% and 17% of papers, so prefer a sketch in the main text plus a footnote.
6. **Cut a whole sentence, not its connective.** Keep `Specifically,`, `Note that`, `To this end,` where they
   carry a real logical move; delete the sentences that only restate an equation.
7. **Last resort, layout**: `\vspace{-...}` after figures and equations (68 of 85 papers do this), caption
   font `\footnotesize`, `\balance` on the last page (20 papers).

Do not: shorten the mean sentence below ~21 words, drop the `Notations:` paragraph without checking that no
undefined symbol remains, drop the benchmarks list, or (letter 40%, full 71%) drop the future-work sentence to
save one line if the conclusion would then stop at a recap of the abstract. In a conference paper the
future-work sentence is the first thing to go (6% of the corpus's conference papers have one).

Report before and after: words, pages, sentence mean (script metrics), and which operation supplied each cut.
