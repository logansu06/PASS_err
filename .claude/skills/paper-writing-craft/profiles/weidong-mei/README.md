# Profile `weidong-mei`: writing-style profile for wireless-communication papers

Distilled on 2026-09-29/30 from **every arXiv paper that lists Weidong Mei as an author** (102 records,
2016-11 to 2026-07; selection rule set by the user: all papers carrying his name, not only first- or
corresponding-author papers). It is a *style model*: how the papers are structured, how sentences,
captions, figures, and LaTeX are written, and how often. It is not a store of text.

## What was analysed

| | |
|---|---|
| papers | 102 (85 technical: 25 letters, 18 conference papers, 42 full papers; 17 tutorial / magazine / survey) |
| author position | 23 first, 77 middle, 2 last (`corpus_manifest.md`) |
| eras | 2016-19: 10 · 2020-22: 17 · 2023-26: 75 |
| topics | physical-layer security and service integration, cellular-connected UAV, IRS beam routing, movable / 6D / rotatable antennas, near-field and THz beamforming, IRS channel estimation |
| floats | 821 figures, 108 tables, 87 algorithm boxes |
| sources | arXiv LaTeX (`arxiv.org/e-print/<id>`, latest version) |

**Methods.** (1) LaTeX-source statistics: sentence and paragraph length, lexical and punctuation rates per
1,000 words, section skeletons, abstract / introduction / conclusion size, contribution-list form, equation and
theorem density, caption text, float environments, cross-reference spelling (`scripts/style_stats.py`,
`fig_stats.py`, `extras.py`). (2) n-gram document frequency for formulaic phrases (`phrases.py`).
(3) Close reading of about a dozen papers across eras and roles (2016-2026, first- and middle-author) plus the
opening and closing sentences of all 85 technical papers, for moves and frames. (4) Visual inspection of 12
figure files (curves, layouts, heat maps, block diagrams, a magazine illustration). (5) **Back-test**: the
mechanical gate was run on the same 85 papers and every rule that fired on many of them was relaxed
(`calibrate.py`; the first version rejected 65-95% of the papers on sentence length alone because of a
sentence-splitting bug and an over-strict threshold; both were fixed).

## Findings that differ from the default (SNL) profile

Sentences are longer (mean 23.7, not 21); passive is idiomatic (~19 per 1,000 words); `Moreover`,
`Note that`, `It is worth noting`, `In this section, we` are signature phrases; `promising` and
`significantly` occur routinely; abstracts carry no numbers; no Related Work section; headings are topic
headings; figure captions are 8 words with no takeaway; figures follow the MATLAB curve template and
PowerPoint schematics. Applying the default gate to the corpus rejects 99% of the papers on M5, M6 and M18
(`stats_upstream_gate_on_corpus.md`).

## How to use

- Default of `paper-writing-craft` (`PROFILE = weidong-mei`); switch with `— profile: snl-default`.
- Read order while drafting: `craft_reference.md` -> `rhetorical_moves.md` -> `figures_tables.md` ->
  `latex_idioms.md` -> `lexicon.md`. While auditing: `scripts/style_gate.py` (+ `gate_mechanical.md`) and
  `gate_semantic.md`.
- Plots: `../../assets/mei_ieee.mplstyle` + `../../scripts/mei_plot.py`.

## Limits (read before trusting a number)

- Statistics come from LaTeX sources with regex-based text cleaning; they rank tendencies and are not
  exact linguistics. `passive` is an upper bound (it also counts `is set`, `is used`). Inline math counts
  as one word per symbol.
- arXiv versions can differ from the published papers; copy-editing by the journal is not in the corpus.
- 77 of the 102 papers have him as a middle author: the text is co-authored with students and
  collaborators. The comparison by role (`stats_body.md`) shows first- and middle-author papers within
  about 1.5 words of mean sentence length and within the same range for `we`, `Note that`, `Specifically`,
  so the profile describes the shared group voice that he leads; it cannot separate his own edits.
- One subfield (physical-layer wireless optimization, IEEE format). For another field, re-run the pipeline
  on that author's or venue's papers.
- Style drifts: abstracts shortened (285 -> 208 words), introductions shortened (1,660 -> 825), `Moreover /
  Furthermore` doubled (0.8 -> 1.5 per 1k), conclusions moved to the past tense (88% since 2023). The
  profile follows the 2023-26 papers when the eras differ.

## Scope of use

For writing the user's **own** papers in this register. Do not copy sentences, claims, numbers, or figures
from the corpus; do not present text as written by the author; cite prior work honestly. Only aggregates and
short generic collocations (n-gram document frequencies) are stored in this skill; no paper text and no
LaTeX source is redistributed. arXiv content is read for statistics only.

## Regenerate or extend (another author, or newer papers)

```bash
python scripts/fetch_corpus.py --author "Mei_Weidong" --out corpus/
python scripts/style_stats.py --src corpus/src --meta corpus/meta.json --out corpus/out
python scripts/aggregate.py corpus/out > corpus/summary.md
python scripts/fig_stats.py  --src corpus/src --meta corpus/meta.json --out corpus/out
python scripts/aggregate_floats.py corpus/out > corpus/floats_summary.md
python scripts/phrases.py corpus/out > corpus/phrases.md
python scripts/extras.py  corpus/out corpus/meta.json > corpus/extras.md
python scripts/calibrate.py --src corpus/src --meta corpus/meta.json --profile <name> --write-norms \
       --upstream-report profiles/<name>/stats_upstream_gate_on_corpus.md > corpus/backtest.md
python scripts/render_gate_doc.py --profile <name> --backtest corpus/backtest.md
```
Then rewrite the prose files (`craft_reference.md` ... `lexicon.md`) from the new tables; start from a copy of
this directory and change every number that no longer matches.

## Files

| file | content |
|---|---|
| `craft_reference.md` | sentence-level and register rules, transitions, results-paragraph anatomy |
| `rhetorical_moves.md` | skeleton and move sequences per section; letter / conference / full / tutorial |
| `figures_tables.md` | figures, captions, plots, schematics, tables, algorithm boxes, float citations |
| `latex_idioms.md` | class, packages, notation, equations, problems (P1), theorem environments, snippets |
| `lexicon.md` | formulaic collocations with document frequencies |
| `editorial_principles.md` | 14 principles with evidence, and where the default principles do not apply |
| `gate_mechanical.md`, `rules.json`, `norms.json` | the script-run gate, rule table, corpus norms |
| `gate_semantic.md` | reader-judgment gate: inherited S-items, overrides, W1-W16 |
| `compression_overrides.md` | page-limit compression without changing the voice |
| `stats_*.md`, `corpus_manifest.md`, `_corpus_meta.json` | evidence tables and the paper list |
