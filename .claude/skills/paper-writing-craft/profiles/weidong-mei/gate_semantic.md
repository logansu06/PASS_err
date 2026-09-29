# Semantic gate (profile `weidong-mei`)

> The failures a program cannot catch: undefined symbols, an assumption that changes between
> the model and the simulation, a benchmark that is not the one the text describes, a result
> paragraph that does not explain its figure. Run it in the red-team and loop passes with a
> **fresh-reader** lens: a reviewer who has not seen the paper and did not write the text
> (`red_team_protocol.md`). Each item returns findings (rule id, `file:line`, concrete fix).
> Severity: CRITICAL = structural or logical; MAJOR = reviewer-visible; MINOR = polish.
> The mechanical checks are in `gate_mechanical.md`; the positive guidance in `craft_reference.md`.

## A. Inherited from the default profile, unchanged

Apply `profiles/snl-default/gate_semantic.md` for: **S1-S9** (define before use, term order,
acronyms at first use, recursive followability, parse-accessibility, gloss once, thesis-tie,
lexical consistency, cross-section term-map), **S11-S12** (referents, deliver the noun), **S14**
(dangling modifiers), **S16-S19** (ground critiques in numbers, data integrity, hedge scan,
requirement-to-closure), **S21** (honest positioning, especially of your own prior work),
**S29-S31** (independent lenses, venue calibration, closure gate).
S15 (mappability of every number) is executed by the ARIS audits `/paper-claim-audit` and
`/result-to-claim`; it is not repeated here.

## B. Overridden for this profile

| default item | this profile | reason (corpus evidence) |
|---|---|---|
| S10 no duplication | The three-part contribution statement **must** appear compressed in the abstract, in full in the introduction, and as a recap in the conclusion. Result numbers still appear once, in the results section. | the abstract, the contribution list, and the conclusion recap state the same items in every paper read closely; 96% of abstracts mention numerical results, 1% carry a number |
| S13 gloss pile-ups | Acronym parentheses are normal (about 20 parentheses per 1,000 words). Flag only a sentence with two or more *explanatory* (non-acronym) parentheticals or an appositive chain. | acronym-in-parentheses at first use is the corpus convention |
| S20 positives first | Keep. Limits are stated as (i) hedged limits of prior work, (ii) scoped assumptions of this paper, (iii) an extension or future-work sentence; never as a confession in the abstract. | 74% contrast with prior work; 48% end with future directions |
| S22 enabling system | Not applicable. | systems-paper item |
| S23 claim-first headings | **Reverse.** Section headings are conventional topic headings in Title Case (`Numerical Results`, `System Model and Problem Formulation`, `Proposed Solution to (P1)`); subsection headings name the step (`Optimizing X for Given Y`, `Single-User Case`). | 89% Title Case; no claim-first section title in 85 papers |
| S24 break a wall of text with a table | **Reverse.** Simulation parameters are written inline; a table only for enumerations of eight or more entries or for a comparison in a tutorial. | median 0 tables in technical papers |
| S25-S28 figure rules | Replaced by W14 and `figures_tables.md`. | those rules encode the default profile's systems-paper figure style; this corpus's figures follow a different, measured convention |

## C. Added: wireless-optimization paper checks (W1-W16)

**W1 Scenario first (MAJOR).** The system model opens with `As shown in Fig. 1, we consider ...` and
states every entity with its equipment and count (BS with `N` antennas, `K` single-antenna users,
`M` IRS elements). Fig. 1 exists, is cited in the introduction or at the first line of the model, and
shows the same entities under the same names.

**W2 Symbols (CRITICAL).** Every symbol is defined at first use and before an equation uses it
(`Let X denote ...`); one symbol, one meaning across the whole paper; sets calligraphic, vectors and
matrices bold, iteration counters `l` or `r`. Every symbol in the `Notations:` paragraph is used, and
every operator the paper uses appears there.

**W3 Assumption ledger (MAJOR).** List every assumption; each is stated once, justified (`for simplicity`,
`to focus on`, `in practice X can be acquired by Y`) or scoped (`can be extended to`), and is the same
in the model, the algorithm, and the simulation setup (e.g. perfect CSI in the model and in the
benchmarks). `Without loss of generality` is followed by an argument, not left bare.

**W4 Problem statement (MAJOR).** Objective, variables (`by jointly optimizing ...`), constraints each
explained, then the difficulty (`non-convex`, `coupled`, `combinatorial`) and a roadmap sentence.
The variables in the sentence equal the variables under the `max` / `min` in the equation.

**W5 Problem chain and answer quality (CRITICAL).** Each sub-problem `(Pk)` is derived from an earlier
one with the reformulation stated (`can be simplified as`, `can be recast as`). Each algorithm has
its complexity and a convergence or optimality statement. A `high-quality suboptimal` or
`near-optimal` claim is backed by a comparison with a stronger reference (optimal solution, upper bound, exhaustive
search) in at least one regime of the results. `optimal` is used only with a derivation or a proof.

**W6 Special case earns its place (MAJOR).** If a special case is solved first (`To gain insights, we first
consider ...`), the text says what insight it yields and how it feeds the general algorithm.

**W7 Contribution to evidence map (CRITICAL).** Every contribution item points to a section and to a result
or figure; the abstract, the contribution list, and the conclusion name the same items in the same
terms and order. No contribution is claimed that no result supports.

**W8 Benchmarks (CRITICAL).** Each benchmark has one name, used identically in the text, the caption,
and the legend. Each states what it lacks relative to the proposed scheme. The set contains a conventional
baseline and, when one exists, an optimal or upper-bound reference. Benchmarks receive the same
parameters and channel knowledge unless the difference is the point of the comparison and is stated.

**W9 Simulation reproducibility (MAJOR).** Carrier frequency, geometry and coordinates, array sizes,
channel model with its reference, path-loss model and exponent, noise power or transmit SNR, the
number of independent realizations, and `unless otherwise stated`.

**W10 Result paragraph (MAJOR).** One paragraph per figure with the anatomy pointer, observation, mechanism,
quantified gap, implication. Unexpected behaviour (curves that coincide, a benchmark that wins) gets an
explanation. No figure without a paragraph; no claim in a paragraph that the figure cannot show.

**W11 Claim scope (CRITICAL).** A qualitative word in the abstract or conclusion (`significantly`,
`considerably`) is backed by at least one figure in which the gap is visible; a priority claim (`first`,
`for the first time`) is backed by the literature check; a statement about generality beyond the simulated
parameters carries a hedge; a measured number is never hedged.

**W12 Prior-work positioning (CRITICAL).** Prior work is credited before its limitation is stated; the limitation
is scoped and hedged (`mostly focused on`, `may not fully exploit`) and evidenced (S16); the author's own earlier
work is cited with the delta (`In our previous work [x], ... only ...`); no blanket verdicts (`useless`,
`cannot`). The same prior work is described the same way in every section.

**W13 One name per scheme (MAJOR).** Scheme names, acronyms, and variable names are identical in the
abstract, introduction, model, results, and figure legends (`APV` stays `APV`; `MA positions` is not renamed
`antenna coordinates` in one section).

**W14 Figure legibility, by looking (MAJOR).** Render and inspect each figure at final column width: axis labels
with units, tick labels at least 8 pt, legend not covering data, markers distinguishable in grayscale,
sweep values on the x axis, caption names what is plotted and the parameters that matter. A checklist pass
without rendering does not count.

**W15 Introduction argument (MAJOR).** Read only the first sentence of each introduction paragraph: they form the
argument driver, technology and benefit, prior art, gap, this paper, contributions. Each gap sentence is
answered by a contribution item.

**W16 Future work does not undo the claim (MINOR).** The future-work sentence extends the result; it does not
name a limitation that invalidates a claimed result.

## D. Closure gate

Unchanged from the default (`S31`): iterate the red-team after every substantive change until a final
independent closure reviewer returns zero CRITICAL and MAJOR findings. Record rule ids (`MM#`, `S#`,
`W#`) per section in the audit ledger.
