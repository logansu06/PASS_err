# Reviewer Memory

## Round 1 — Score: 7/10

### Raw Reviewer Response (verbatim)

**7/10 for IEEE ICC. Almost ready.** The narrowed research story survives an adversarial review. I found no fatal mathematical or computational flaw in C1–C3. The main acceptance risk is modest novelty; the strongest evidence is the family-wide certification and its measured yield.

I read the artifacts and code, checked the figures, recomputed headline statistics, and independently reconstructed all 899 positive-Γ leakage comparisons. I did not read `NARRATIVE_REPORT.md`, modify files, or rerun the complete experiment suite. **R020 remains provisional.**

The main results check out:

- Certified SLNR dominance: **462/528 free**, **437/528 endpoints**.
- Unique robust-optimality certificates: **204/528**, **239/528**, within the stated finite families.
- Protection bracket: maximum \(\bar I/F_{\rm end}=1.011322\), supporting **within 1.14%**.
- R021: the reported enclosure bounds and **4/16** newly certified co-aligned stress pairs reproduce.
- I found no certified reverse ordering in the stored main-grid or stress-panel comparisons. That does not establish universal superiority.

**The pending leakage claim is valid.**

Let \(\tilde\delta_N\) be the feasible, best-found SLNR witness for \(S_N\). Then

\[
\max_\delta I_P(\hat S,\delta)
\le \bar I(\hat S)
< I_P(S_N,\tilde\delta_N)
\le \max_\delta I_P(S_N,\delta).
\]

The witness need neither maximize leakage nor globally minimize SLNR. Its feasibility is sufficient.

Reconstructing the bounds and nominal witnesses reproduced **893/899**, comprising **457/462 free** and **436/437 endpoints**. Every reconstructed witness satisfied the error-box constraint. The smallest successful relative separation was \(3.67\times10^{-4}\), comfortably above numerical noise.

The pooled median of
\[
r_{\rm cert}=\frac{\bar I(\hat S)}
{I_P(S_N,\tilde\delta_N)}
\]
is **0.799830779 across all 899 positive-Γ cases**, including the six unsuccessful leakage comparisons. It bounds the true worst-case leakage ratio from above.

Safe paper wording:

> “Among the 899 declared-grid cases with certified SLNR improvement, 893 (99.3%) also certify strictly lower worst-case leakage than exhaustive nominal selection. Across these 899 cases, the median certified upper bound on the worst-case leakage ratio is at most 0.800.”

Retain the analytical-certificate/float64 qualification. This specific claim can pass review without changing R020’s overall provisional status. See [the calculation](/Users/logansu/Documents/PASS/experiments/a7/summarize_r019.py:55).

**Remaining weaknesses, ranked by severity**

1. **Novelty is credible but narrow. This is the largest rejection risk.**

   Auxiliary-angle enumeration for rank-2 binary optimization is established mathematics. Sector/support-function uncertainty bounds also have substantial precedent. Generic feasible witnesses already imply screening, brackets, and sufficient uniqueness tests. The distinctive observation is that one arrangement built from all candidate sites supplies exact endpoint-leakage coverage for every subset, enabling the integrated PASS certificate framework. The [Karystinos–Liavas paper](https://www.telecom.tuc.gr/~liavas/publications/Efficient%20Computation%20of%20the%20Binary%20Vector%20that%20Maximizes%20a%20Rank-deficient%20Quadratic%20Form.pdf) makes the prior-art boundary clear.

   **Minimum fix:** explicitly credit these tools and center the contribution on family-wide coverage, protection limits, and demonstrated certification yield. Cite the recent [Jiang–Schotten position-error paper](https://arxiv.org/abs/2609.31088); actuator errors in PASS are already being studied. No additional experiment is required for this framing.

2. **The comparison establishes improvement over particular baselines, with limited evidence about computational superiority.**

   B-CR uses fewer resources and optimizes the shared-template witness objective. GCS adds global enumeration and certificate evaluation. Its certified wins are valid, but cannot establish equal-compute superiority over robust optimization generally. The present table correctly acknowledges this; [the proposal](/Users/logansu/Documents/PASS/refine-logs/FINAL_PROPOSAL.md:64) still says “same-budget.”

   Likewise, screening still requires the family-wide bank pass. At \(M=32\), the free-family median total time is about 35 seconds; co-aligned cases retain essentially the entire family.

   **Minimum fix:** consistently say “same-start shared-template swap heuristic; budgets unmatched.” Report inclusive runtime and cap hits. Claim tractability on the tested families. A matched-budget or random-bank experiment is unnecessary unless stronger comparative claims are retained.

3. **Worst-case improvement can carry substantial operating costs, and the model scope is narrow.**

   A concrete case deserves attention: endpoints, \(30\) dB, \(\epsilon=0.03\lambda\), \(P=(-3.6,2)\). It has **7.85% certified worst-case improvement**, while its estimated mean SLNR falls **14.95%**, estimated fifth percentile falls **12.53%**, and nominal SLNR falls **39.17%**. These values are in the [raw Monte Carlo results](/Users/logansu/Documents/PASS/experiments/a7/results/r017_mc_average.csv) and main grid.

   The experiment uses one desired/protected receiver pair, a roughly 17.1 cm aligned candidate aperture, equal site power, and separable channels. The attenuation controls involve model-aware redesign and model-specific noise normalization.

   **Minimum fix:** include one explicit substantial-loss example alongside the median sacrifice, and keep these model restrictions visible. Treat Monte Carlo results as descriptive. Hardware, depletion, and broader geometry experiments are unnecessary for the licensed claims.

4. **A small, genuine implementation-to-proof inconsistency remains.**

   [Production code](/Users/logansu/Documents/PASS/experiments/a7/a7_core.py:135) accepts tiny nominal phase residuals but omits them from \(\beta_D\). The [ablation implementation](/Users/logansu/Documents/PASS/experiments/a7/ablation_gaps.py:100) already includes the correction.

   Replaying all 1,056 stored winners with residual enlargement reduces \(L\) by at most approximately \(2.7\times10^{-12}\) relatively and changes no dominance or uniqueness signs. This is a real cleanup item, with no observed effect on the conclusions.

   **Minimum fix:** use the existing corrected coefficients in production and regenerate affected A7 outputs and summaries. No interval-arithmetic framework is needed.

5. **Some source wording can still contaminate the manuscript.**

   [The results report](/Users/logansu/Documents/PASS/refine-logs/EXPERIMENT_RESULTS.md:81) calls the numerical points “SLNR-minimizing witnesses.” Corner enumeration plus local refinement does not certify global minimization.

   **Minimum fix:** write “best-found SLNR witnesses.” Preserve the float64 qualification, family restriction, six leakage exceptions, and inconclusive cases. Include a compact R021 ablation block; it provides more scientific value than repeating featured-instance numbers already illustrated elsewhere.

**Submission readiness: Almost.** The research is sufficient for a credible ICC submission after these focused fixes. I would not spend the remaining three days on a broad new simulation campaign. Prioritize contribution positioning, the small bound correction, and a six-page presentation that preserves the qualifications. The manuscript itself still needs review once written.

Score: 7/10  
Verdict: almost

## Memory update

- **Resolved:** 893/899 leakage ordering is valid; 0.800 is a median certified ratio upper bound over all 899 positive-Γ cases.
- **Resolved:** core screening, uniqueness, leakage-converse mathematics, and reported R021 results survived inspection.
- **Track:** production desired-phase residual correction and regenerated certificate decisions.
- **Track:** novelty attribution; stale “same-budget” and “SLNR-minimizing” wording.
- **Track:** substantial nominal/mean/tail losses must remain visible.
- **Track:** final manuscript must distinguish completed certificate optimization, conditional uniqueness, and capped cases.
- **Unchanged:** R020 is provisional; no formal experiment audit was performed.

---


# Run 2 (hard, run_20260929_449a523d)

## Run 2, Round 1 (hard) — Score: 7/10

### Raw Reviewer Response (verbatim)

**7/10 for IEEE ICC. Almost ready.** The revised narrative is substantially better, and the core C1–C3 results remain credible. However, one round-1 repair was disclosed instead of completed, and the new opening contains an unsupported—and demonstrably overbroad—ablation conclusion.

I read the complete narrative and requested diff, checked the code, figures and tables, recomputed headline statistics from raw files, and replayed the phase-residual correction. No files were changed. I did not rerun the full experiment suite or perform `/experiment-audit`; **R020 remains provisional**.

The principal numbers reproduce:

| Result | Verified |
|---|---:|
| Certified SLNR dominance, free / endpoints | 462/528 / 437/528 |
| Unique robust-optimality certificates | 204/528 / 239/528 |
| Certified lower worst-case leakage | 893/899 |
| Median certified leakage-ratio upper bound | 0.799830779 |
| Maximum protection-bracket ratio | 1.011321939 |
| Median inclusive runtime, free / endpoints | 3.939 s / 0.551 s |

The substantial-loss example also checks out: **+7.85% certified worst-case gain, −39.17% nominal SLNR, −14.95% estimated mean, and −12.53% estimated fifth percentile**.

The unmatched-budget wording, “best-found” witnesses, non-ideal model qualifications, operating-cost example, and mathematical attribution are genuine improvements. I found no new fatal flaw in the shared-bank, screening, uniqueness, or protection-converse arguments.

Remaining weaknesses, ranked by severity:

1. **Novelty remains narrow—the largest acceptance risk.**

   Attribution is now substantially correct. Auxiliary-angle enumeration and low-rank binary optimization are established; the [Karystinos–Liavas paper](https://www.telecom.tuc.gr/~liavas/publications/Efficient%20Computation%20of%20the%20Binary%20Vector%20that%20Maximizes%20a%20Rank-deficient%20Quadratic%20Form.pdf) directly establishes that lineage. The added [Jiang–Schotten citation](https://arxiv.org/abs/2609.31088) also correctly acknowledges existing PASS position-error analysis.

   What remains distinctive is the **reuse of one full-site arrangement across every subset**, its integration with feasible common D/P witnesses, and the resulting measured family-wide certification yield. Generic witness bounds and sufficient uniqueness inequalities alone are not substantial novelty.

   **Minimum fix:** make that shared-family property the technical center, with its short proof visible in the paper. Present sector bounds and rank-2 enumeration as credited ingredients. Replace the blanket “[None of them …]( /Users/logansu/Documents/PASS/NARRATIVE_REPORT.md:36)” literature exclusion with a carefully scoped “to our knowledge” statement about the combined framework. No additional simulation is needed.

2. **The opening ablation conclusion exceeds the evidence and has a concrete counterexample.**

   [Narrative line 47](/Users/logansu/Documents/PASS/NARRATIVE_REPORT.md:47) says conservatism comes “almost entirely” from separately bounding desired power and leakage. Later, [line 189](/Users/logansu/Documents/PASS/NARRATIVE_REPORT.md:189) correctly acknowledges that the full-grid remainder mixes dependency with unresolved witness slack.

   This is more than missing qualification. For the stored **free GCS layout, \(P=(6,1)\), \(\epsilon=0.03\lambda\), 40 dB**, the enclosure accounts for **at least 98.4% of the logarithmic certificate gap**. The total gap is small, approximately **0.07394%**, and dependency loss is bounded above by **0.001113%**. See the [raw stress row](/Users/logansu/Documents/PASS/experiments/a7/results/ablation_stress.csv:60).

   **Minimum fix:** replace the opening conclusion with:

   > “Combined enclosure loss is at most 0.0934% on the primary fixed layouts; joint refinement establishes substantial D/P-dependency losses on the selected co-aligned stress panel.”

   Preserve the full-grid witness-slack qualification. No new experiment is required.

3. **The requested code–proof correction remains unfixed, and the theorem handoff needs completion.**

   [Production code](/Users/logansu/Documents/PASS/experiments/a7/a7_core.py:143) still omits the accepted nominal phase residual from \(\beta_D\). The [corrected implementation already exists](/Users/logansu/Documents/PASS/experiments/a7/ablation_gaps.py:100). Recording this under “Known Weaknesses” is transparent, but it does not satisfy the previous minimum fix.

   The new read-only replay covers all **1,056 primary stored winners**: the correction reduces \(L\) by at most approximately **\(2.12\times10^{-12}\)** relatively, with **no dominance or uniqueness sign changes**. That confirms negligible observed scientific impact; it does not replace a corrected selection run.

   There is also a real statement mismatch in [Theorem 1](/Users/logansu/Documents/PASS/NARRATIVE_REPORT.md:108): the displayed secant/grid formula is generally conservative even at \(\epsilon=0\). Exactness comes from the code’s [explicit nominal branch](/Users/logansu/Documents/PASS/experiments/a7/a7_core.py:165). The narrative also leaves \(\beta_D\) and the sector support insufficiently defined.

   **Minimum fix:** apply the existing residual enlargement in production and regenerate affected A7 outputs and summaries. In the theorem, explicitly define the desired-phase excursion, sector support—including the negative-cosine amplitude branch—the uniform angular grid, and the exact zero-tolerance branch. Restrict the simple amplitude-extrema statement to the ideal amplitude model. These are focused repairs; an interval-arithmetic framework is unnecessary.

4. **The six-page plan needs prioritization, and a few population qualifiers could still disappear during writing.**

   The [page budget](/Users/logansu/Documents/PASS/NARRATIVE_REPORT.md:267) allocates space to two full-width figures, two additional figures, two tables, several formal statements, seven experimental blocks and references. It is possible to make this fit, but preserving everything risks compressing the actual contribution into an unreadable proof sketch.

   **Minimum fix:** remove the repeated featured-instance block from Table II before cutting essential evidence. Keep the shared-family proof, protection bracket, compact R021 block and substantial-loss example. If Fig. 4(b) is removed, retain inclusive runtimes and cap counts in text.

   Also make these small scope corrections:

   - **48 cap hits** applies to the primary population; the full 1,360-row grid has **64**.
   - **At least 99.998% surviving** applies to the scaling slice. A main-grid co-aligned case retains only **392,384/735,471 = 53.35%**, though it still hits the cap. [Raw row](/Users/logansu/Documents/PASS/experiments/a7/results/main_grid.csv:1254)
   - The other 61 inconclusive cases have median \(\Gamma\approx-0.19\%\), but are not uniformly marginal: **13 have \(\Gamma<-5\%\)**, with a minimum near **−11.07%**. Report the median without implying every case is close to certification.
   - Failure to certify uniqueness does **not** imply failure to complete certificate optimization. Preserve that distinction alongside capped cases.

**Submission readiness: Almost.** The research can support a credible ICC submission without a broad new campaign. The narrative is close to a usable writing handoff, but the code correction, ablation wording and theorem definitions should be fixed first. The resulting six-page manuscript still requires review.

Score: 7/10  
Verdict: almost

## Memory update

- **Resolved:** most round-1 presentation fixes are genuinely implemented; headline numbers and substantial-loss example reproduce.
- **Unresolved:** production phase-residual correction and regenerated outputs. Disclosure has substituted for repair.
- **New finding:** opening R021 attribution is overbroad; a stored off-axis stress case is enclosure-dominated.
- **Track:** zero-tolerance exactness requires the explicit nominal branch; theorem definitions must survive manuscript compression.
- **Track:** population scope for 48 versus 64 caps, scaling-only survivor claims, and the nontrivial tail of inconclusive cases.
- **Pattern:** detailed sections contain qualifications that the executive summary drops.
- **Unchanged:** novelty is credible but narrow; R020 remains provisional; the manuscript itself has not been reviewed.

---

