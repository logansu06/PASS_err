# Paper Plan

**Title**: Robustness Analysis of Constructive Phase-Aligned PASS Placement Under Bounded Position Errors  
**Format**: Graduation report  
**Template**: `Final Report Template.docx`  
**Date**: 2026-04-19  
**Template Order Lock**: cover page -> coursework declaration and feedback form -> abstract -> acknowledgements -> table of contents -> main body -> references -> appendices  
**Template Writing Rules**: each Heading 1 section starts on a new page; `References` starts on a new page; each appendix starts on a new page; no separate list of figures or tables; use numeric square-bracket citations.

**Planning note**: `findings.md` is the latest claim gate for any baseline-comparison language. `CLAIMS_FROM_RESULTS.md` remains the source for the narrower one-design story where no baseline wording is involved.
**Contribution boundary**: treat `2501.05657v2.pdf` as the foundational PASS array-gain paper and `fyp.pdf` as the project's theory-and-derivation bridge into the robustness problem. The final report must explicitly separate inherited theory from the base paper, project-side derivation/reformulation, and the new robustness evidence produced in this repository.

## Claims-Evidence Matrix

| Claim | Evidence | Status | Planned Section |
|---|---|---|---|
| The deterministic lower bound tightly characterizes bounded-error degradation inside the guaranteed small-error region. | `results/config.json`: `epsilon_valid_norm = 0.17126776184398004`; `results/data_main.csv`: max `|wc_norm - lb_full_norm|` is about `3.40e-6` over the guaranteed region. | Supported | 2.1.3, 2.3.1, 3.2, 4.1 |
| In the pre-null regime, the harmful bounded-error pattern is empirically a left-right split-mode phase-spread pattern, while common-bias motion is nearly harmless. | `results/data_main.csv`: before `epsilon/lambda = 0.175`, max split-vs-box gap is about `1.57e-5`; at `0.1`, `box = 0.38172695`, `split = 0.38174263`, `common-bias = 0.99993864`. | Supported, empirical | 2.1.4, 2.3.1, 3.1, 4.1 |
| A second-order covariance / phase-variance predictor explains the observed stochastic trends for the studied iid uniform, common-bias, and correlated Gaussian models over the tested small-error range. | `results/data_error_scenarios.csv` at `epsilon/lambda = 0.1`: iid `0.76980750` vs `0.74416072`; common-bias `0.99997949` vs `0.99997959`; correlated Gaussian `0.84576180` vs `0.83094739`. | Supported, scoped | 2.1.4, 2.3.3, 3.1, 4.1 |
| The constructive aligned placement is more robust than the naive uniform-aperture baseline in the tested same-aperture comparison, especially in box-best-found robustness. | `results/data_baseline_summary.csv` at `epsilon/lambda = 0.10`: nominal `+1.1%`, box-best-found `+14.1%`, iid mean `+0.9%` versus uniform aperture. | Partial, narrow comparative claim only | 2.3.4, 3.3, 4.1 |
| The constructive aligned placement is not the best same-aperture placement among the tested candidates because the direct nominal optimizer performs better on all reported metrics. | `results/data_baseline_summary.csv` at `epsilon/lambda = 0.10`: direct nominal optimizer beats aligned constructive on nominal, box-best-found, and iid mean; `results/data_baseline_curves.csv` shows the same ordering across the sampled curves. | Supported | 2.3.4, 3.3, 4.1 |
| The report must not claim an exact continuous-box optimum or any general design optimality. | `AUTO_REVIEW.md`, `CLAIMS_FROM_RESULTS.md`, and `findings.md` all explicitly reject those stronger claims. | Constraint | 1.3, 3.2, 3.4, 4.1 |

## Structure

### Front Matter

#### Cover Page
- Purpose: satisfy the template's required first page exactly.
- Claims covered: none.
- Required fields: `Final Year Project Report`, degree line, final project title, student name, GUID, UESTC ID, supervisor line, academic year field.
- Template handling: keep the supervisor line blank for Moodle submission if that rule still applies; fill it only for hardcopy if required by the program.
- Figures or tables: none.
- Citations: none.
- Target length: 1 page.
- Reader takeaway: the document is clearly identified as the final-year project report for this PASS robustness study.

#### Coursework Declaration and Feedback Form
- Purpose: preserve the required second page from the template.
- Claims covered: none.
- Template handling: do not rewrite or reorder the form; keep it as a form page.
- Figures or tables: none.
- Citations: none.
- Target length: 1 page.
- Reader takeaway: the template compliance pages are complete before the technical content begins.

#### Abstract
- Purpose: summarize the problem, method, strongest supported findings, and evidence scope in template-compliant form.
- Claims covered: lower-bound tightness, split-mode/common-bias contrast, stochastic predictor, narrow baseline takeaway.
- Source material: `findings.md`, `CLAIMS_FROM_RESULTS.md`, `THEORY_EXTENSIONS.md`, `results/data_main.csv`, `results/data_error_scenarios.csv`, `results/data_baseline_summary.csv`.
- Figures or tables: none.
- Citations needed: 2-4 core background citations only, all `[VERIFY]`.
- Target length: 100-250 words, plus one `Keywords:` line.
- Reader takeaway: this is a robustness-characterization report for one constructive PASS design in a studied symmetric setting, not a global design-optimality paper.

#### Acknowledgements
- Purpose: keep the template's front-matter order.
- Claims covered: none.
- Figures or tables: none.
- Citations: none.
- Target length: short single page.
- Reader takeaway: standard acknowledgements only.

#### Table of Contents
- Purpose: follow the template's required placement after acknowledgements.
- Claims covered: none.
- Template handling: do not add a list of figures or a list of tables.
- Figures or tables: auto-generated table of contents only.
- Citations: none.
- Target length: auto-generated.
- Reader takeaway: the report structure is legible before the body begins.

### 1 Introduction
- Purpose: define the engineering problem, explain why PASS is sensitive to position errors, state the project scope, and lock the contribution wording before any derivation.
- Claims covered: the scoped contribution set and the non-claims.
- Source material: `Intro.md`, `2501.05657v2.pdf`, `fyp.pdf` Section 1, `AUTO_REVIEW.md`, `findings.md`.
- Subsection plan:
  - `1.1 Background and motivation`: PASS near-field focusing, why physical pinching-point errors matter, why robustness matters for realizable deployments.
  - `1.2 Relationship to the base paper and this project`: state clearly that the graduation project extends `Array Gain for Pinching-Antenna Systems (PASS)` by moving from nominal array-gain analysis to robustness under bounded and stochastic position errors.
  - `1.3 Gap and report scope`: explain what the base paper does not cover, what `fyp.pdf` derives for this project, and what the final repository results now support.
  - `1.4 Objectives and contribution bullets`: use 3-4 conservative bullets only.
  - `1.5 Report roadmap`: one short paragraph mapping Sections 2-4.
- Figures or tables needed: `Fig. 1` PASS geometry and report problem setup schematic.
- Citations needed:
  - `Array Gain for Pinching-Antenna Systems (PASS)`, Chongjun Ouyang, Zhaolin Wang, Yuanwei Liu, and Zhiguo Ding, arXiv:2501.05657v2, 2025.
  - `[VERIFY]` PASS array-gain or near-field focusing reference.
  - `[VERIFY]` position-error robustness reference for related arrays or movable antennas.
- Target length: about 10-15% of the body.
- Reader takeaway: the report is an extension study built on the base PASS array-gain paper, with new focus on robustness of a constructive phase-aligned feasible placement under bounded and stochastic position errors in one symmetric setup.

### 2 Body of the Report
- Purpose: follow the template's research-project variant inside the fixed Heading 1 title `Body of the Report`.
- Claims covered: all technical claims, but only as evidence presentation, not as discussion-level interpretation.
- Source material: `fyp.pdf`, `THEORY_EXTENSIONS.md`, `Intro.md`, `results/config.json`, all relevant result CSV files.
- Target length: about 50-55% of the body.

#### 2.1 Theory and Problem Formulation
- Purpose: build the technical model cleanly enough that the later robustness results and limitations are credible.
- Claims covered: lower-bound mechanism, sensitivity definition, split-mode intuition, quadratic stochastic predictor.
- Source material:
  - use `2501.05657v2.pdf` as the source for the base PASS geometry, array-gain model, and constructive alignment context;
  - use `fyp.pdf` Sections 2-5 as the project-specific bridge that reformulates those ideas toward nominal placement and position-error sensitivity;
  - use `THEORY_EXTENSIONS.md` to replace the old same-sign upper-bound story with the weighted phase-variance line;
  - rewrite any inherited `near-optimal` or `exact worst-case` wording.
- Subsection plan:
  - `2.1.1 Base PASS model from the literature`
  - `2.1.2 Project reformulation to constructive phase-aligned feasible placement`
  - `2.1.3 Position-error model, phase sensitivity xi, and guaranteed small-error region`
  - `2.1.4 Weighted phase variance, split-mode construction, and covariance-based stochastic predictor`
- Figures or tables needed:
  - `Fig. 1` PASS geometry and alignment pipeline schematic.
  - `Fig. 2` phase-sensitivity / `xi_n` distribution across the constructive placement.
  - `Table 1` simulation configuration and notation (`N=16`, `d=3 m`, `f_c=28 GHz`, `n_eff=1.44`, `delta_p=0.5 lambda`, seeds, Monte Carlo counts).
- Citations needed:
  - `Array Gain for Pinching-Antenna Systems (PASS)`, Chongjun Ouyang, Zhaolin Wang, Yuanwei Liu, and Zhiguo Ding, arXiv:2501.05657v2, 2025.
  - `[VERIFY]` any cited phase-alignment or near-field reference.
  - `[VERIFY]` any cited numerical-optimization method if `L-BFGS-B` is explicitly named in prose.
- Target length: about 20-25% of the body.
- Reader takeaway: the reader understands which equations are inherited from the base PASS paper, which derivation steps are part of the graduation project's reformulation, and why phase variance becomes the right local mechanism for the new robustness analysis.

#### 2.2 Experimental or Numerical Techniques
- Purpose: document exactly how the report evaluates robustness, so the results are reproducible and the evidence scope is explicit.
- Claims covered: none directly; this section sets up trustworthy evidence.
- Source material: `Intro.md`, `results/config.json`, `run_log.txt`, `AUTO_REVIEW.md`, repository modules listed in `AGENTS.md`.
- Subsection plan:
  - `2.2.1 Reproducible setup and fixed configuration`
  - `2.2.2 Deterministic bounded-error evaluation: lower bound, split-mode, and box-best-found search`
  - `2.2.3 Stochastic scenarios: iid uniform, common-bias, correlated Gaussian`
  - `2.2.4 Placement baselines: constructive aligned, uniform aperture, direct nominal optimizer`
  - `2.2.5 Secondary sensitivity sweeps over frequency and n_eff`
- Figures or tables needed:
  - `Table 1` simulation configuration.
  - `Table 2` representative evaluation points and what each experiment is testing.
- Citations needed:
  - `[VERIFY]` only if external algorithms or borrowed baseline definitions are explicitly discussed.
- Target length: about 12-15% of the body.
- Reader takeaway: the reader knows which experiments are theorem-backed, which are empirical, how the baselines were constructed, and what counts as reproducible evidence in this repository.

#### 2.3 Results
- Purpose: present the measured evidence in the order that supports the claims matrix.
- Claims covered: all supported and partial claims, with conservative scope markers.
- Source material: `results/data_main.csv`, `results/data_box_validation.csv`, `results/data_error_scenarios.csv`, `results/data_baseline_summary.csv`, `results/data_baseline_curves.csv`, `results/data_freq_sweep.csv`, `results/data_neff_sweep.csv`, `CLAIMS_FROM_RESULTS.md`, `findings.md`.
- Subsection plan:
  - `2.3.1 Main bounded-error robustness curve`
    - show ideal, box-best-found, split-mode, common-bias, lower bound, and Monte Carlo mean;
    - mark `epsilon_valid / lambda = 0.17126776184398004`;
    - state clearly that tightness inside this region is theorem-backed and anything beyond is empirical.
  - `2.3.2 Box validation and adversarial pattern comparison`
    - compare corner, split-mode, and continuous-box best-found at representative `epsilon / lambda`;
    - show the first-null region as the point where the empirical near-match starts to break.
  - `2.3.3 Stochastic scenario validation`
    - report iid uniform, common-bias, and correlated Gaussian means together with the quadratic approximation;
    - keep the scope to the tested range up to `epsilon / lambda = 0.1`.
  - `2.3.4 Placement baseline comparison`
    - compare constructive aligned, uniform aperture, and direct nominal optimizer;
    - emphasize that the constructive design beats the naive uniform baseline mainly in box-best-found robustness but loses to the direct nominal optimizer on all reported metrics.
  - `2.3.5 Secondary sweeps`
    - include only a compact summary in the body if space permits;
    - otherwise move the full `f_c` and `n_eff` curves to the appendices and reference them briefly.
- Figures or tables needed:
  - `Fig. 3` main robustness curve from `results/data_main.csv`.
  - `Fig. 4` corner / split-mode / box-best-found validation from `results/data_box_validation.csv`.
  - `Fig. 5` stochastic scenarios plus quadratic approximation from `results/data_error_scenarios.csv`.
  - `Fig. 6` baseline box-best-found curves from `results/data_baseline_curves.csv`.
  - `Fig. 7` baseline tradeoff summary or iid-mean baseline curves from `results/data_baseline_summary.csv` and `results/data_baseline_curves.csv`.
  - `Fig. A1` frequency sweep from `results/data_freq_sweep.csv`.
  - `Fig. A2` `n_eff` sweep from `results/data_neff_sweep.csv`.
  - `Table 3` key numeric checkpoints for `epsilon/lambda = 0.05, 0.10, 0.15`, plus the guaranteed-region threshold.
- Citations needed: usually none beyond the earlier theory citations, because this section is mostly own results.
- Target length: about 20-25% of the body.
- Reader takeaway: the evidence supports a coherent one-design robustness story, a useful stochastic extension, and only a narrow comparative design statement.

### 3 Analysis and Discussion
- Purpose: do the most important work in the report: reason from the evidence to the actual conclusions without overstating what the data shows.
- Claims covered: all final interpreted claims and all explicit limitations.
- Source material: `AUTO_REVIEW.md`, `findings.md`, `CLAIMS_FROM_RESULTS.md`, `THEORY_EXTENSIONS.md`, key result tables.
- Subsection plan:
  - `3.1 Mechanism interpretation`
    - explain why weighted phase variance unifies the split-mode and stochastic stories;
    - explain why common-bias motion mostly rotates global phase instead of destroying relative coherence.
  - `3.2 Guarantee versus empirical region`
    - separate theorem-backed lower-bound tightness from empirical pre-null tracking;
    - use `box-best-found` wording consistently.
  - `3.3 Comparative design takeaway`
    - state the narrow baseline lesson: aligned constructive is better than naive uniform aperture in the tested setup, especially for box-best-found robustness, but it is not the best tested design because the direct nominal optimizer does better.
  - `3.4 Limitations and what remains unsupported`
    - no globally certified continuous-box optimum;
    - no theorem that split-mode is the exact minimizer;
    - no `N` sweep or `d` / `delta_p` sweep yet;
    - stochastic predictor validated only for the studied placement and tested small-error range.
- Figures or tables needed:
  - optional reuse of `Table 3` for discussion anchor;
  - no new figure required if the argument can point back to Sections 2.3 figures.
- Citations needed:
  - `[VERIFY]` prior PASS / MA robustness references for comparison language in the discussion only.
- Target length: about 20-25% of the body.
- Reader takeaway: the report's main value is a disciplined robustness characterization, not a broad optimization or certification result.

### 4 Conclusions and Further Work
- Purpose: close the report in the exact template structure while preserving evidence discipline.
- Claims covered: only the claims already defended in Sections 2 and 3.
- Source material: claims matrix, `findings.md`, `AUTO_REVIEW.md`.
- Subsection plan:
  - `4.1 Conclusions`
    - summarize the supported one-design story and the narrow baseline takeaway;
    - restate the strongest quantitative anchors once.
  - `4.2 Suggestions for Further Work`
    - stronger near-null global-search validation;
    - `N` sweep and `d` / `delta_p` sweeps;
    - a genuinely robust-tuned baseline;
    - verified related-work expansion and cleaner literature positioning.
- Figures or tables needed: none.
- Citations needed: none unless directly comparing future directions to prior literature.
- Target length: about 8-10% of the body.
- Reader takeaway: the contribution is complete and credible for the current studied setup, but the next scientific step is broader design comparison and stronger generality evidence.

### References
- Purpose: satisfy the template's required post-body reference section.
- Claims covered: none.
- Formatting rule: numeric square-bracket citations only.
- Source handling: verify all bibliographic metadata before drafting; treat `2501.05657v2.pdf` as a mandatory foundational citation; do not carry over placeholder references from `fyp.pdf` unchanged.
- Target length: as needed.
- Reader takeaway: every cited source is traceable without further searching.

### Appendices
- Purpose: hold supporting material that is useful but too detailed for the main body.
- Claims covered: no new core claims.
- Appendix plan:
  - `Appendix A` notation, derivation details, and any algebra omitted from Section 2.1.
  - `Appendix B` extra robustness curves and validation tables, including full frequency and `n_eff` sweeps if they are not in the body.
  - `Appendix C` reproducibility details: configuration snapshot, output file map, and any implementation notes useful for continuation.
  - `Appendix D` optional code-listing or solver-detail appendix only if the program requires it.
- Figures or tables needed:
  - `Fig. A1` frequency sweep.
  - `Fig. A2` `n_eff` sweep.
  - `Table A1` complete baseline summary.
  - `Table A2` full box-validation checkpoints.
- Citations needed: only if appendix material cites additional sources.
- Target length: flexible; appendices are supporting material only.
- Reader takeaway: the report remains concise in the main body while preserving reproducibility and technical detail.

## Figure Plan

| ID | Type | Placement | Description | Data Source | Priority | Word-Editable Note |
|---|---|---|---|---|---|---|
| Fig. 1 | Schematic | 1.1 or 2.1.1 | PASS geometry, user location, waveguide path, and aligned-placement pipeline | manual redraw from `fyp.pdf` + current notation | HIGH | build as editable vector diagram for Word |
| Fig. 2 | Line / stem plot | 2.1.3 | `xi_n` distribution over the constructive placement, highlighting `xi_max` and symmetry structure | `results/fig_xi_distribution.*` or regenerate from design data | MEDIUM | regenerate as vector or high-res editable chart |
| Fig. 3 | Multi-curve line plot | 2.3.1 | ideal, box-best-found, split-mode, common-bias, lower bound, Monte Carlo mean with uncertainty band versus `epsilon/lambda` | `results/data_main.csv` | HIGH | regenerate so caption and legend remain editable |
| Fig. 4 | Validation line plot or grouped markers | 2.3.2 | corner-restricted, split-mode, and box-best-found comparison at representative error levels | `results/data_box_validation.csv` | HIGH | editable plot |
| Fig. 5 | Multi-panel line plot | 2.3.3 | stochastic scenario means and quadratic approximations for iid uniform, common-bias, and correlated Gaussian errors | `results/data_error_scenarios.csv` | HIGH | editable plot |
| Fig. 6 | Multi-curve line plot | 2.3.4 | box-best-found robustness curves for aligned constructive, uniform aperture, and direct nominal optimizer | `results/data_baseline_curves.csv` | HIGH | editable plot |
| Fig. 7 | Scatter or compact line plot | 2.3.4 or 3.3 | nominal gain versus robustness tradeoff, or iid baseline comparison, across the three placements | `results/data_baseline_summary.csv` and `results/data_baseline_curves.csv` | HIGH | editable plot |
| Fig. A1 | Line plot | Appendix B | frequency sweep as a secondary sensitivity check | `results/data_freq_sweep.csv` | MEDIUM | appendix figure |
| Fig. A2 | Line plot | Appendix B | `n_eff` sweep as a secondary sensitivity check | `results/data_neff_sweep.csv` | MEDIUM | appendix figure |
| Table 1 | Table | 2.1 or 2.2 | system configuration, notation, and solver settings | `results/config.json` | HIGH | create as editable Word table |
| Table 2 | Table | 2.2 | experiment matrix: which experiment tests which claim | claims matrix + result file map | HIGH | editable Word table |
| Table 3 | Table | 2.3 or 3.2 | key numeric checkpoints for the main deterministic and stochastic story | `results/data_main.csv`, `results/data_error_scenarios.csv`, `results/data_box_validation.csv` | HIGH | editable Word table |
| Table A1 | Table | Appendix B | full baseline summary | `results/data_baseline_summary.csv` | MEDIUM | editable Word table |
| Table A2 | Table | Appendix B | full box-validation checkpoints including the near-null case | `results/data_box_validation.csv` | MEDIUM | editable Word table |

## Citation Plan

| Section | Required Citation Types | Status |
|---|---|---|
| Cover / declaration / acknowledgements / TOC | none | ready |
| Abstract | 2-4 core background citations only if the final abstract wording needs them | `[VERIFY]` |
| 1 Introduction | mandatory base-paper citation to `Array Gain for Pinching-Antenna Systems (PASS)` plus PASS background and position-error robustness references for related arrays or movable antennas | base paper verified from local PDF; others `[VERIFY]` |
| 2.1 Theory and Problem Formulation | same core PASS references as the introduction; explicitly cite the base paper when reusing model equations or alignment context; cite external optimization method only if explicitly named | base paper verified from local PDF; others `[VERIFY]` |
| 2.2 Experimental or Numerical Techniques | usually no external citations beyond algorithm references and any borrowed baseline definitions | `[VERIFY]` where needed |
| 2.3 Results | mainly own results; cite only when comparing directly to prior art | mostly ready |
| 3 Analysis and Discussion | prior work only for carefully scoped comparison language, not for inflated novelty claims | `[VERIFY]` |
| 4 Conclusions and Further Work | usually none | ready |
| References | verify author, year, title, venue, pages or article number, URL/date for web sources, and numbering consistency | required before drafting |

**Citation guardrails**
- Do not invent bibliographic metadata.
- When a model, equation, or design insight is inherited from `2501.05657v2.pdf`, cite it explicitly and mark the report's extension point clearly.
- Do not keep the placeholder `fyp.pdf` references as final references without verification.
- Default to numeric square-bracket citation output to match the template.
- If a source is only weakly remembered, mark it `[VERIFY]` in the drafting stage.

## Reviewer Feedback

- `AUTO_REVIEW.md` changes the report strategy: the final document should be a disciplined robustness argument, not a broad venue-style paper claim.
- The final report should explicitly identify `2501.05657v2.pdf` as the starting point and frame this project as an extension from nominal PASS array-gain analysis to robustness analysis.
- The strongest supported story is the lower-bound + split-mode + stochastic-predictor bundle for one constructive design in one studied symmetric setting.
- The report must use `box-best-found` or `best-found adversary`, never `exact worst-case`.
- The old same-sign adversarial construction from `fyp.pdf` should be removed from the main claim story or explicitly described as a superseded weak construction.
- The baseline section should be kept, but written conservatively: constructive aligned beats naive uniform aperture mainly in box-best-found robustness, yet loses to the direct nominal optimizer on all reported metrics.
- `findings.md` should be treated as the final claim gate for all baseline-comparison wording.
- No new delegated reviewer pass was run during this planning turn; this section synthesizes `AUTO_REVIEW.md` and `findings.md`.

## Next Steps

- [ ] Draft `PAPER_FIGURE_PLAN.md` or run the figure workflow to regenerate Word-friendly versions of Figs. 1-7 and Tables 1-3.
- [ ] Write the report against this plan while preserving the template front matter and Heading 1 page breaks.
- [ ] Verify bibliography metadata before drafting the Introduction and Related-Work portions.
- [ ] During drafting, explicitly replace any legacy `near-optimal`, `exact worst-case`, or broad design-optimality wording inherited from `fyp.pdf`.
- [ ] Compile the final Word manuscript against `Final Report Template.docx`.
