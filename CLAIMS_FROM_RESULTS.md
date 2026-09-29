verdict: partial
confidence: high
integrity_status: unavailable (provisional — no /experiment-audit run; see "Provenance")

# Claims From Results — A7 v2 (R020, `/result-to-claim`, 2026-09-28)

This file replaces the fail-closed stub `verdict: REVIEW_UNAVAILABLE`. It is the working claim set for the paper. Every sentence in `NARRATIVE_REPORT.md` and the paper must stay inside it.

## Provenance

- **Reviewers:** two independent GPT-6 Astra threads at `ultra`, same neutral prompt, read-only, run in parallel.
  - Jury A: thread `01a0e664-d87b-7ec1-942e-2c17d7a73811`.
  - Jury B: thread `01a0e66d-7fcf-78a3-9b66-b95d962f6c75`.
  - Traces: `.aris/traces/result-to-claim/2026-09-28_run01/` (`001-jury-A-ultra.*`, `002-jury-B-ultra.*`).
- **Merge rule:** per claim, the more conservative verdict. The two juries agreed on every verdict.
- **What the juries did:**
  - recomputed every headline statistic from the raw CSVs;
  - audited `a7_core.py` and the drivers for bound validity, family coverage, cap handling and case filters;
  - compared the runs with the pre-declared plan (`refine-logs/EXPERIMENT_PLAN.md` v2);
  - re-evaluated the weakest positive margins at 50–60 digits.
- **Deterministic evidence pre-check (Step 1.5):**
  - 160 numbers cited in `refine-logs/EXPERIMENT_RESULTS.md` were checked against result files (`.aris/claims.json` → `.aris/evidence_precheck.json`, rounding check in `.aris/rounding_check.json`).
  - 134 persisted numbers: all present and round-consistent.
  - 25 numbers + 1 spurious match: never persisted → `evidence_not_found` (list below).
- **Integrity audit:** `EXPERIMENT_AUDIT.json` does not exist, so this verdict is **provisional** per the skill. The juries' recomputation and pre-registration check cover much of that ground, but no formal `/experiment-audit` was run.
- **Environment:** reviewed on Windows (Python 3.12.10, NumPy 2.3.5, SciPy 1.15.3). R001 port check re-passed on this machine before review.

## Verdict per Claim

| Claim | Verdict | Confidence | One-line scope |
|---|---|---|---|
| **C1** certified dominance over exhaustive nominal | **yes** | high | Declared grid, ε > 0, P ≠ D, both families; analytical bounds evaluated in float64 |
| **C2** global certification yield / screening | **yes**, qualified | high | Exact certificate optimum only when uncapped; uniqueness only when its test passes |
| **C3** protection limits | **yes** for the bracket and conditional feasibility | high | The "≤ 1%" statement is false; use 1.14% on the 54-case slice |
| **A1** baselines (B-CR, B-GR) | **partial** | high | Not equal-compute; B-CR is a shared-template swap, not an all-corner robust optimizer |
| **A2** non-ideal persistence | **yes**, narrowly | high | After model-aware redesign at model-specific reference SNR |
| **A3** x_P = 0 negative region | **partial** | high | Bound conservatism shown on 5 cases; causality and repair not shown |
| **A4** Monte Carlo average trade-off | **partial** | high (sample stats) / medium (population tail) | Descriptive only; median, not universal |
| **Overall** | **partial** | high | Core C1–C3 hold; the write-up overstates several ancillary points |

## Strongest Licensed Paper Sentences

State once, near the theorems: *"Certificates are analytical statements; all inequalities are evaluated numerically in float64, and decisive margins are reported."*

- **C1:** "On the declared nonzero-tolerance grid (ε > 0, P ≠ D; 528 cases per family), GCS certifies higher worst-case SLNR than exhaustive nominal selection in 87.5% (462/528) of free-family and 82.8% (437/528) of identical-endpoint cases, with certified gains above 5% in 61.9% (327/528) and 56.25% (297/528), respectively." Report inconclusive cases (66 / 91) and the median nominal sacrifice (0.16% / 0.32%).
- **C2:** "A shared bank of at most 2M endpoint witnesses enables safe family-wide screening and exact certificate maximization when the scan completes; on the main grid, a unique robust-optimal layout within the family is certified in 38.6%/45.3% of free/endpoint cases, with median global bracket gaps of 0.508%/0.489%." The uniqueness yield falls with ε (≈ 76–80% at 0.01λ → 9–15% at 0.08λ).
- **C3:** "Across three pre-specified geometries, nine tolerances and both families at 30 dB, the leakage achievability bound lies within 1.14% of the exhaustive endpoint converse; at transmit power p, leakage ceilings below p·F_end are infeasible within the family, and any ceiling ≥ p·Ī(Ŝ) is met by Ŝ."
- **A1:** "On the baseline slice, GCS certifiably outperforms the same-start shared-template swap heuristic in 68.9%/50.8% of free/endpoint cases and the P-blind desired-only baseline in 90.9% of cases for both families."
- **A2:** "After model-aware redesign at model-specific reference SNR, certified dominance persists in 81.8–88.6% (free) and 82.6–84.8% (endpoints) of cases under the two tested separable attenuation/directivity models."
- **A3:** "For five selected co-aligned endpoint cases, joint-box refinement closes 51–61% of the log bracket gap, but none becomes a certified improvement over nominal selection."
- **A4:** "With 10,000 iid-uniform error draws per case, the median estimated mean-SLNR ratio is 0.9968/0.9958 (free/endpoints), while the estimated fifth-percentile SLNR improves in 77.3%/54.5% of cases; individual mean losses can be much larger."

## Phrases That Must Not Appear

- "always improves", "universally superior", "globally optimal PASS placement", "optimal over continuous placements"
- "no-cost robustness", "robustness costs only 0.4%"
- "machine-verified", "exact continuous-box solver/adversary", "polynomial-time global optimization"
- "exact optimum" for capped cases; "all adversaries covered by 2M witnesses"
- "within 1% in every case", "every layout leaks 0.80", "fundamentally unprotectable" (without p, I_max and family)
- "same compute budget", "best robust heuristic", "B-CR solves the worst-case problem"
- "hardware validated", "model-independent", "same physical noise across models"
- "negative cases are only a bound artifact", "the negative region is repaired", "the method still wins there"
- "improves the lower tail" (unqualified), "Monte Carlo worst-case guarantee"
- "robust is worse" (use "certificate inconclusive")

## Required Corrections to `refine-logs/EXPERIMENT_RESULTS.md` (before R018/R019 and writing)

**MAJOR (both juries unless noted)**

1. **C3 tightness is false as written** (lines 140, 204). Max Ī/F_end = **1.011322** (free, P = (6,1), ε = 0.09λ); 2/54 rows exceed 1.01 (also ε = 0.08λ, 1.010553). Write "within 1.14% on the tested 54-case slice".
2. **"Same-budget" B-CR** (line 131) is not established: same starts and neighborhood, but objective-dependent work, and GCS adds the global scan. Rename to "same-start shared-template swap", or measure equal budgets.
3. **Negative-region causality** (lines 92, 191): refinement shows conservatism of the bound for 5 fixed layouts. It does not show that the negative region is "the bound's, not the method's", nor that decoupling is the sole cause.
4. **"Fundamentally unprotectable" / "every layout leaks about 0.80"** (line 154) exceed the converse. State infeasibility only as I_max < p·F_end within the family.
5. **"Costs about 0.4% of average SLNR"** (line 179) is a median. The largest observed mean losses are 22.9% (free) and 15.0% (endpoints).
6. **Unpersisted numbers** (lines 52, 74, 79–85, 101, 153, 167): the 25 items below must be persisted by a script (R019) or removed together with every conclusion that rests on them.
7. **Non-ideal comparison** (jury A: MAJOR if read as physical transfer; jury B: MINOR): the runs recompute A_ref per channel model and redesign both layouts. Say "model-aware redesign at model-specific reference SNR"; do not claim fixed physical noise or transfer of ideal-designed layouts.

**MINOR**

- Go/no-go fraction: use **56.25% (297/528)**; the file mixes 56.2% and 56.3%.
- ε = 0.05λ, free, Γ > 5%: **70.5%** (93/132), not 71% (line 61).
- Median endpoint survivor fraction is 0.0201%: write "≈ 0.02%", not "≤ 0.02%".
- Median L/U* = 99.49% / 99.51%: write "≈ 99.5%", not "≥ 99.5%".
- P = (0,1), free, ε = 0.05λ: U* = 1.108 → rounds to **1.11**, not 1.10.
- Cap hits: 48 under the primary filter; the full 1,360-row grid has 64 (16 more at P = D). Keep the filter label.
- "No layout can be screened out" (line 103) is false for some capped cases: write "screening leaves too many survivors to finish within the cap".
- Timing: the 0.20 / 0.11 s GCS figures are selection-stage times and exclude family construction, the bank pass and nominal enumeration. Label components; use inclusive times for cost comparisons.
- Joint-box: "5 distinct geometry/tolerance pairs"; the budget used 300,031 evaluations; sampling validation is a sanity check, not a proof.
- Code (`experiments/a7/a7_core.py:135`): the production desired-projection bound accepts the residual nominal phase misalignment but omits it from β_D. The residual is tiny and the independent R007 code (`a7_checks.py:227`) includes it; fixing it would align code with proof. No result is expected to change materially.

## R019 Update (2026-09-28): Evidence Resolved, Corrections Applied

- **All 25 items below are now persisted.** `experiments/a7/summarize_r019.py` → `results/r019_derived.{json,md}` recomputes them from the stored CSVs with their original definitions, and every value reproduced the quoted number. The ×70 growth becomes ×67–71; the extreme-case Γ is +44.5%.
- **The corrections listed above are applied** to `refine-logs/EXPERIMENT_RESULTS.md` (pre-revision copy: `EXPERIMENT_RESULTS_20260927_143216.md`; revised copy: `EXPERIMENT_RESULTS_20260928_133938.md`).
  - Reconciliation found one more rounding error: F_end at endpoints, P = (6,1), ε = 0.01λ is 1.17e-4, not 1.18e-4.
- **Numbers table:** `experiments/a7/r019_numbers.py` → `results/r019_numbers.{md,json}`. All 237 quoted numbers in the revised `EXPERIMENT_RESULTS.md` are consistent with their source keys. The ARIS evidence pre-check re-verified 191/191 direct-key values (`.aris/evidence_precheck_r019.json`).
- **Weakest-margin audit persisted:** `r019_derived.json` → `margin_audit`. All signs are preserved at 50 digits for the smallest positive Γ and the two smallest uniqueness margins.
- **New evidence, not yet reviewed by a jury.** Treat as pending until the next review round (`/auto-review-loop`). *(The certified leakage comparison was validated in auto-review round 1, 2026-09-29: see the update below.)*
  - Certified leakage comparison: in 893/899 Γ > 0 cases (99.3%), Ī(Ŝ) is below S_N's leakage at its SLNR witness. This proves max_δ I_P(Ŝ) < max_δ I_P(S_N); the median certified ratio is 0.80.
  - This is a stronger, certificate-based version of the mechanism statement. The witness-ratio version (1.000 / 0.79) stays descriptive: "at the SLNR witnesses".
  - Inclusive per-case runtime: 3.9 s / 0.55 s median (free / endpoints).

## R021 Update (2026-09-29): Ablation, Audited by GPT-6 Astra (ultra)

Source: `experiments/a7/results/ablation_summary.md` (bound endpoints rounded outward), from `experiments/a7/ablation_gaps.py`. Traces: `.aris/traces/ablation-planner/2026-09-29_run01/` (001 design, 002 feasibility, 003 result audit). This is a reviewer audit of the ablation, not a new jury verdict on C1–C3. The main-grid certification rates above are unchanged.

**Licensed sentences (at most one compact table block plus these):**
- "All bounds are analytical statements evaluated numerically in float64, with displayed endpoints rounded outward."
- "On fixed primary GCS layouts, replacing the literal-v1 certificate with the production certificate increases certified-positive counts from 437 to 462 of 528 free cases and from 403 to 437 of 528 identical-endpoint cases."
- "Additional joint-box verification certifies dominance in four of sixteen co-aligned stress pairs, all at P = (0,4), ε = 0.03λ, both families and 10/40 dB, with gains of at least 0.88%; the other twelve remain inconclusive."
- Table rows (percent): pad → sec gain median 0.936 / p95 4.86 / max ≤ 11.76; symmetric → asymmetric ≤ 0.0183; angular / P-sector / desired loss ≤ 0.000476 / ≤ 0.0797 / ≤ 0.0141; combined ≤ 0.0934; median dependency off-axis [0.0359, 0.0436], co-aligned [13.71, 21.11] (stress panel, 32 layout-rows each); swap → completed GCS 373/480 (free), 312/528 (endpoints).

**A3 update (x_P = 0):** R020's statement stays correct for its 5 cases. Add the scoped stress-panel evidence: 4/16 co-aligned pairs certified after joint refinement of both layouts; certified dependency lower endpoints 1.82%–28.3% on co-aligned layouts.

**Must not appear (in addition to the list above):**
- "dependency dominates the full-grid gap" (on the full grid the remainder mixes dependency with unresolved witness slack);
- "Minkowski-sum relaxation" (Minkowski addition is exact for independent errors);
- "exact continuous worst case";
- "sampling validates the bounds";
- "screening delivers 38× speedup" (the M = 16 audit is a correctness check only);
- "the negative region is repaired";
- "dependency losses are at most 28%" (28.3% is a lower endpoint).

## Auto-Review Round 1 Update (2026-09-29): 7/10, "almost"

Reviewer: GPT-6 Astra (ultra), `/auto-review-loop` round 1; raw response in `review-stage/REVIEWER_MEMORY.md` and `.aris/traces/auto-review-loop/2026-09-29_run01/`. The reviewer recomputed the headline statistics and independently reconstructed all 899 positive-Γ leakage comparisons. It found no fatal mathematical or computational flaw in C1–C3. R020 stays provisional.

**Certified leakage comparison (R019): validated.** The chain is max_δ I_P(Ŝ, δ) ≤ Ī(Ŝ) < I_P(S_N, δ̃_N) ≤ max_δ I_P(S_N, δ), where δ̃_N is S_N's feasible best-found SLNR witness. Feasibility of the witness is enough; it need not maximize leakage. Counts: 893/899 pooled (457/462 free, 436/437 endpoints). The smallest successful relative separation is 3.67e-4. Licensed sentence:
- "Among the 899 declared-grid cases with certified SLNR improvement, 893 (99.3%) also certify strictly lower worst-case leakage than exhaustive nominal selection. Across these 899 cases, the median certified upper bound on the worst-case leakage ratio is at most 0.800."

**Required in the paper (reviewer's minimum fixes):**
- **Novelty positioning.** Credit rank-2 binary quadratic maximization (auxiliary-angle enumeration) and sector/support-function bounds as tools. Centre the contribution on family-wide exact endpoint-leakage coverage by one shared bank, the protection limits, and the measured certification yield. Cite Jiang–Schotten (arXiv 2609.31088).
- **Baselines.** Always "same-start shared-template swap heuristic; budgets unmatched". Report inclusive runtime and cap hits; claim tractability only on the tested families.
- **Operating cost.** Show one substantial-loss example next to the median sacrifice. Verified example (endpoints, 30 dB, ε = 0.03λ, P = (−3.6, 2)): certified worst-case gain +7.85%, nominal SLNR −39.17%, estimated mean SLNR −14.95%, estimated 5th percentile −12.53% (`results/main_grid.csv`, `results/r017_mc_average.csv`). Monte Carlo results stay descriptive.
- **Model scope.** Keep visible: one desired/protected pair, a single aligned candidate aperture, equal site power, separable channels; the attenuation controls use model-aware redesign at model-specific reference SNR.
- **Witness wording.** "Best-found SLNR witnesses", never "SLNR-minimizing witnesses".

**Known code–proof inconsistency (not fixed; no effect observed).** `a7_core.py:135` omits the tiny nominal D-phase residual from β_D. Replaying all 1,056 stored winners with the residual included lowers L by at most about 2.7e-12 relative and changes no dominance or uniqueness sign (the reviewer's replay; the R021 ablation code already includes the correction). Fixing it would mean regenerating every A7 output.

## Auto-Review Run 2 Update (2026-09-29, hard): 7/10, "almost"

Reviewer: GPT-6 Astra (ultra), fresh thread with the run-1 memory; review of the rewritten `NARRATIVE_REPORT.md`. Raw response in `review-stage/REVIEWER_MEMORY.md`. No new fatal flaw; headline numbers re-verified.

- **R021 wording (replaces any "almost entirely D/P dependency" phrasing):** "Combined enclosure loss is at most 0.0934% on the primary fixed layouts; joint refinement establishes substantial D/P-dependency losses on the selected co-aligned stress panel." The enclosure can dominate a small gap in an off-axis layout (free, P = (6,1), 0.03λ, 40 dB: ≥ 98.4% of a 0.074% log gap; `results/narrative_checks.md`).
- **Theorem 1 at ε = 0:** exactness comes from the explicit nominal branch (L defined as the nominal SLNR), not from the sector formula.
- **Scope qualifiers:** 48 cap hits in the primary population (64 in the full grid); 565 of 1,056 primary cases are exact but not unique; "at least 99.998% surviving" applies only to the scaling slice (main-grid co-aligned 53.35%–100%); 13 of the 61 off-axis inconclusive cases are below −5% (minimum −11.07%).
- **Must not appear:** "almost entirely due to D/P dependency"; "none of the prior work …" without "to our knowledge"; "all other inconclusive cases are marginal".
- **Not repaired by user decision (2026-09-29):** the production phase-residual correction. It stays disclosed; no A7 output is regenerated before submission.

## Evidence Not Found at R020 Time (resolved by R019; kept for the record)

Numbers reported in `EXPERIMENT_RESULTS.md` but present in no result file at R020 time. Per the skill they were `claim_supported: no`, `integrity_status: evidence_not_found`, and were not re-litigated by the juries.

| ID | Cited | What it supports |
|---|---|---|
| c1_xP_free_pos / c1_xP_end_pos | 96.3% / 91.0% | x_P ≠ 0 subgroup, main grid |
| c1_xP_free_above5 / c1_xP_end_above5 | 68.1% / 61.9% | same |
| c1_xP_free_med / c1_xP_end_med | 14.2% / 8.9% | same |
| c1_mech_desired_ratio (spurious match) / c1_mech_leak_ratio | 1.000 / 0.79 | mechanism (desired unchanged, leakage −21%) |
| c1_sacr_p90 / c1_sacr_max | 13.5% / 88.5% | nominal-sacrifice tail |
| c1_maxcase_nom_slnr / _hat_L / _Gamma | 9,997 / 3.02 / 44% | extreme-sacrifice example |
| c1_inconcl_total / _xP0 / _other | 157 / 96 / 61 | inconclusive breakdown |
| c1_inconcl_other_med / _same_layout | −0.19% / 46% | marginal inconclusive cases |
| c1_xP0_UL_median / _max | 1.09 / 1.73 | x_P = 0 bracket looseness |
| c2_swap_pooled_n / _pos / _med / _p90 | 1,008 / 68% / 0.6% / 7.6% | pooled swap-vs-exact selection gap |
| c3_growth_x70 | ×70 | F_end growth 0.01 → 0.09λ |
| ni_008_xP_pos | 94% | non-ideal, x_P ≠ 0 |

**Already-persisted replacements** (recomputed by the juries; usable now):
- per-family swap gap instead of the pooled one: strictly positive in 373/480 free (77.7%) and 312/528 endpoint (59.1%) exact cases; median 0.92% / 0.29%; max 24.3% / 25.9% (`main_summary.json`, `overall.*.selection_gap_*`);
- B2-slice off-axis B-GR dominance: 120/120 per family (`m2m3_summary.json`, `baselines`).

## Open Items That Strengthen but Are Not Required

None is needed for the sentences above; each is needed only to keep a stronger claim.

- Matched-budget B-CR comparison (evaluations or wall time) — to keep "same-budget".
- Fixed-physical-noise non-ideal rerun, and model-mismatch transfer — to claim physical-link robustness.
- Joint-box refinement of **both** Ŝ and S_N on representative co-aligned cases — to attribute the negative region. *(Done on the R021 stress panel: see the R021 update.)*
- Repeated-seed MC with quantile uncertainty — to make inferential tail claims.
- An interference-temperature operating-point panel computed from the existing C3 bounds (no new simulation).
- Persist the weakest-margin numerical audit (smallest positive Γ = 5.697e-6 and smallest positive uniqueness margin preserved their signs at 50–60 digits in the juries' read-only checks; not yet in a result file).

## Executor Note (not a jury verdict)

The v2 proposal (success condition 4), the plan (reviewer concern 3) and GPT-6 Pro (§7.2) require the four gaps — angular, sector enclosure, D/P dependency, selection — to be reported separately. Angular (R004), selection (swap gap) and D/P dependency (joint-box) have evidence; the **sector-enclosure gap has no separate measurement**. GPT-6 Pro's D.2 minimal experiment (same subset: additive pad vs symmetric-sector sec vs asymmetric-sector sec) was not run. This is the natural `/ablation-planner` item. *(Done in R021, 2026-09-29: sector-enclosure loss ≤ 0.0797% on every primary fixed layout.)*
