# Figures, tables, algorithms, and captions

> Distilled from 1,016 floats in 102 papers (821 figures, 108 tables, 87 algorithm boxes),
> their LaTeX environments, and visual inspection of 12 figure files (curves, layouts,
> heat maps, block diagrams, a magazine illustration). Counts are over the technical papers
> unless stated. Ready-made code: `latex_idioms.md` (environments), `../../assets/mei_ieee.mplstyle`
> and `../../scripts/mei_plot.py` (matplotlib reproduction of the curve style).

## 1. How many, and what kind

| | letter | conference | full paper | tutorial |
|---|---|---|---|---|
| figures | 3 [2-4] | 5 [4-7] | 9 [7-10] | 7 [6-19] |
| tables | 0 | 0 | 0 [0-1] | 1 [0-7] |
| algorithm boxes | 0-1 | 1 [0-1] | 1 [0-2] | rare |

About 26% of figures are schematics (system model, protocol, layout, architecture), 74% are
result plots. The first figure is the system model or scenario: its caption names a system, scenario, model,
or architecture in 66 of 85 technical papers (78%), and it is cited in the introduction
(`as shown in Fig. 1`) or in the first line of Section II. Result figures follow
the order of the result paragraphs; each figure is discussed in its own paragraph.
Only 12% of figures use sub-panels (2-3 panels); most result figures are single panels.
Simulation parameters are given in running text; a parameter table appears in a minority of papers.

## 2. Figure captions

Median 8 words [6-12]. 96% are one sentence, 94% end with a period, 88% are in sentence case
(acronyms and proper nouns capitalised), 19% contain inline math. The caption names *what is
plotted*; the paragraph in the text says what it shows. Captions essentially never carry the takeaway, a
bold lead, or a citation of the text (a hand-typed `Fig. N.` prefix occurs once in 821 figures
and is a defect).

| kind | frame | examples of the form (placeholders) |
|---|---|---|
| curve (35% contain "versus") | `<Metric> versus <swept variable>[ with <fixed parameters>].` | `Received SNR versus the number of sampling points.` · `Average sum rate versus total transmit power for different benchmarks.` · `Achievable rates of <system> versus the number of antennas at the relay with $N=8$.` |
| set of curves | `<Metric> of <scheme> versus <variable>[, <parameter>].` | `Worst-case SNR of the <scheme> versus number of transmit MAs.` |
| schematic | `Illustration of <object>.` / `<System> with <feature>.` / `System model of <X>.` / `An example of <X>.` / `Simulation setup of <X>.` | `Illustration of multi-MA movements with $N=2$.` · `IRS-aided multi-user MISO MA system.` |
| layout / result map | `Optimized positions of <X> by all schemes.` / `Distribution of <quantity> in <scenario>.` | `Trajectories of different schemes under different time durations.` |
| convergence | `Convergence of <algorithm>.` / `<Algorithm>: convergence of the <metric>.` | |
| comparison | `Comparison of <A> and <B>.` / `Performance comparison of <schemes> in <case>.` | |

First words of captions, by count: Illustration (61) · The (56) · A / An (58) · Achievable (29)
· Average (28) · Optimized (19) · Received (19) · Secrecy (17) · Sum (15) · EE (15).

**Sub-panels.** Two idioms occur. (a) Group idiom (seen in the recent group papers read closely): `\subfloat[]{...}` with *empty* labels and a
main caption that enumerates the panels inside one sentence, separated by semicolons:
`(a) Pull-out torque; (b) Output power versus the angular speed of the stepper motor.`
(b) Panel captions of 2-4 words (`Beam domain: wide-beam coverage`, `Case 1.1`, `Isotropic`,
`Proposed`, `Benchmark 1`), 63% ending with a period. Do not mix the two in one paper.

**Placement and size.** `[!t]` (311) or `[t]` (357) or `[t!]`; `\centering`; single column unless
the content needs the width (`figure*` 20%). `\includegraphics[width=...]`: 0.4-0.5
`\textwidth` for schematics, 0.78 `\linewidth` or 3.2-3.5 in for plots; graphics files: PDF 472, EPS 436, no extension 111, PNG 45, JPG 3. Captions are set left-aligned at
`\footnotesize` in recent group papers (`\captionsetup{justification=raggedright,singlelinecheck=false}`,
`\captionsetup{font=footnotesize}`).

## 3. Result plots (curves): the visual template

Observed in the plotting files of 2019-2026 papers (MATLAB exports; the style is stable across
years and across first authors):

- **Canvas**: 4:3 (or 1:1 for one-parameter beam-gain plots) at column width; vector export.
- **Axes**: boxed, all four spines; light-grey grid on both axes (major only); ticks inward; no minor
  grid; no plot title inside a single-panel figure (the caption is the title). Multi-panel MATLAB
  `subplot` files may carry short Title Case panel titles (`Proposed Multi-Path Beam Routing`).
- **Text**: sans-serif (Helvetica / Arial look), large at export so it stays legible at 3.5 in
  (about 8-9 pt in the final column). Axis label = `Quantity (unit)`, first letter of each
  major word capitalised in most files: `Received SNR (dB)`, `Number of Sampling Points`,
  `Bandwidth (GHz)`, `UAV Transmit Rate (bps/Hz)`, `x (m)`. Units in parentheses with correct case (dBm, dB, GHz, bps/Hz).
- **Curves**: line plus a marker at every data point; markers are hollow (unfilled) in the
  same colour as the line; line width ~1.5-2 pt; 5-11 sweep points, x ticks placed exactly on the
  sweep values (`12 24 36 48 60`); y-limits fitted to the data with round tick values.
- **Series identity**: the proposed / optimal scheme is black (solid, `*` or `v` marker) or is the
  last legend entry; the suboptimal variant is red; benchmarks blue and magenta (classic MATLAB
  k / r / b / m) or the current MATLAB default colour order (blue, orange, yellow, purple, green).
  Upper bounds and idealised references are dashed or dotted; a constant benchmark is a
  horizontal line with markers. Distinct markers per series: `* v o ^ > s d x`.
- **Legend**: inside the axes, boxed with a thin black frame on white, single column, placed in
  the emptiest corner (bottom-right, bottom-left or top-right), no title. Labels are short and
  identical to the names used in the text: `Optimal Solution`, `Sequential Update`, `FPA w/ AS`,
  `FPA w/o AS`, `Benchmark 1`, `Proposed`, `MA+FMCW`.
- **Benchmarks ordered** optimal or proposed first, then suboptimal, then benchmarks (or
  `Benchmark 1..n` then `Proposed`).
- **Special plots**: heat map / surface with the `jet` colour map, colour bar on the right, the
  worst-case point annotated (`Min: 4.88 dB`) for max-min designs; geometry plots with users as
  black triangles, BS as a red square, relays / IRSs as blue circles, chosen path as thick red arrows,
  other links thin black arrows, node indices in black, axes `x (m)`, `y (m)`; beam patterns and
  gain-versus-frequency curves use the same line-and-marker rule.

## 4. Schematics

Drawn in PowerPoint / Visio style and exported to PDF, not generated by a plotting library.

- Icon-based: antenna tower, user avatar, IRS as a panel of blue tiles, movable antenna as red
  squares with blue double arrows, RF chains as green rounded rectangles, digital processing as a
  grey rectangle, movement region as a yellow rectangle, beams as coloured ellipses or lobes.
- Node coordinates in parentheses next to nodes in layout figures: BS and user in red, IRS in black.
- Text in the figure: serif (Times) for plain words (`Transmitter`, `Receiver`), italic serif for
  math labels, sets in calligraphic type; dashed rectangles group items of one set; `...` marks omitted elements.
- Graph diagrams (used to explain graph-based algorithms): open circles for vertices, black edges,
  dashed boxes for vertex groups, math labels `v(p_i^{(k)})`.
- Tutorial / magazine hero figure: a rendered 3D city scene with translucent beam lobes and short
  bold sans-serif labels (`Element-level MAs`, `Array-level MAs`); one such figure per article.
- Colour is used freely (red / green / yellow / blue); the figure must still read in grayscale
  through shapes and labels (a check the corpus does not always pass; do not copy the failures).

## 5. Tables

Rare in technical papers (median 0), common in tutorials (comparisons, standard parameter maps).
Caption above the table (99%); `\hline` rules (94%), `booktabs` only 5%; `\small` or
`\footnotesize` in 25%, `\renewcommand{\arraystretch}{...}` in 41%; placement `[t]`. Caption
median 7 words, Title Case in 61% (of the 31 tables in technical papers), final period in 30% (of all 108 tables); the majority form is
`<Noun> <Noun>` with no period: `Simulation Parameters`, `Comparison of Different Codebooks`.
Survey tables: `Comparison of ...`, `List of Main ...`, `Summary of ...`, `Mapping of ...`.

## 6. Algorithm boxes

61% of papers, 87 boxes: package `algorithm` + `algorithmic` (85 of 87), line numbers `[1]`,
median 10 lines. Caption 5 words, Title Case, no final period (87%): `Proposed Algorithm for
Solving (P1)`, `Proposed AO Algorithm`, `Overall Algorithm for Solving (P2)`, `Sequential Update
Algorithm`. Steps start with a verb: `Initialize`, `Set`, `Calculate`, `Update`, `Construct`,
`Sort`, `Output`; each computation cites its equation (`according to (12)`, `via (15)`); loops use
`\REPEAT ... \UNTIL{<criterion>}` (25%) or `\FOR`; last step `Output <solution> as the optimized
solution to (P1)`. `\REQUIRE / \ENSURE` (Input / Output headers) in 22%; in-line comments 2%.
The text says `The overall procedure is summarized in Algorithm 1.` and states the complexity.

## 7. Citing floats in the text

Of 1,172 sentences that cite a figure: `as shown in Fig. N` / `as illustrated in Fig. N` 45% ·
`Fig. N shows / plots / illustrates / compares ...` 12% · sentence-initial `In Fig. N, ...` 8% ·
`we plot <metric> versus <variable> in Fig. N` 7% · `(see Fig. N)` 5% · `Figs. N(a) and N(b)` 5%.
Always `Fig.`; never `Figure`. Tables: `Table N lists ...`. Algorithms: `Algorithm N`.
Every figure is cited before or where it appears, and every figure is cited.
The result paragraph, not the caption, carries the interpretation.

## 8. Checks (also run by `scripts/style_gate.py` MM05, MM21-MM27)

- Figure caption: one sentence, final period, sentence case, <= 25 words (median 8).
- `\subfloat[]` labels are empty exactly when the caption enumerates `(a)`, `(b)`.
- Table caption above the tabular; algorithm caption Title Case without a period.
- `Fig.~\ref{...}` never `Figure`; equations cited as `(12)`.
- Plot legend labels equal the benchmark names used in the text; sweep values are the x ticks.
