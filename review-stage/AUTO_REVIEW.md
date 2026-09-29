# Auto Review Loop — A7 v2 GCS (IEEE ICC 2027)

- Run ID: run_20260929_ac8029ec
- Started: 2026-09-29 16:55 (macOS)
- Reviewer: Codex MCP, gpt-6-astra, reasoning effort ultra (explicit user directive; no backend probe)
- Difficulty: medium; MAX_ROUNDS = 2 (user asked for limited rounds; deadline 2026-10-02)
- Scope: the research as it will appear in the 6-page paper (claims, evidence, figures). The paper is not written yet.
  `NARRATIVE_REPORT.md` is the stale graduation-project narrative and is out of scope.
- `/experiment-audit` skipped by user decision; R020 stays provisional.
- The earlier graduation-project review loop is archived in `fyp_report/review-stage/`.

## Round 1 (2026-09-29 17:04)

### Assessment (Summary)
- Score: 7/10
- Verdict: almost
- Reviewer backend: codex (gpt-6-astra, ultra); threadId 01a0ec61-047e-7c03-ac6a-1737bf392e79; trace `.aris/traces/auto-review-loop/2026-09-29_run01/001-round-1-review`
- Key criticisms:
  - Novelty is credible but narrow: auxiliary-angle enumeration for rank-2 binary optimization and sector/support-function bounds are established tools. The distinctive part is one shared bank that gives exact endpoint-leakage coverage for every subset of the family.
  - Baseline and cost claims: B-CR is a same-start shared-template swap with unmatched budgets; screening still needs the family-wide bank pass (M = 32 free: about 35 s per case), and co-aligned cases keep almost the whole family.
  - Worst-case gains can carry large operating costs; the model scope is narrow (one D/P pair, one aligned aperture, equal site power, separable channels).
  - Code–proof inconsistency: `a7_core.py:135` omits the tiny nominal D-phase residual (effect ≤ about 2.7e-12 relative, no sign change).
  - Stale source wording: "SLNR-minimizing witnesses", "same-budget".
- Verified by the reviewer: C1 counts 462/528 and 437/528; uniqueness 204/528 and 239/528; Ī/F_end max 1.011322; the R021 enclosure bounds and 4/16 co-aligned flips; the pending 893/899 certified leakage comparison (valid; median certified ratio ≤ 0.800 over all 899).

### Reviewer Raw Response

<details>
<summary>Click to expand full reviewer response</summary>

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
</details>

### Actions Taken
- Stop gate (`review_gate.py`): `decision: stop` (codex backend, score 7 ≥ 6, verdict "almost").
- `CLAIMS_FROM_RESULTS.md`: new "Auto-Review Round 1 Update": licensed 893/899 leakage sentence; required paper items (novelty positioning, baseline wording, one substantial-loss example, model scope, witness wording); the known code–proof inconsistency.
- Verified the reviewer's loss example from raw files: endpoints, 30 dB, ε = 0.03λ, P = (−3.6, 2): Γ = +7.85%, nominal sacrifice 39.17%, MC mean ratio 0.8505, 5th-percentile ratio 0.8747.
- `refine-logs/EXPERIMENT_RESULTS.md`: "SLNR-minimizing witnesses" → "best-found SLNR witnesses".
- `refine-logs/FINAL_PROPOSAL.md`: "same-budget corner-robust heuristic" → "same-start shared-template swap heuristic (budgets unmatched)".
- Not done: fixing `a7_core.py:135` and regenerating every A7 output. The reviewer's replay shows no sign change, and regeneration would touch every result file three days before the deadline. Recorded as a known inconsistency in `CLAIMS_FROM_RESULTS.md` and `HANDOFF.md`.

### Results
- No new experiments.

### Status
- Stopping after round 1: positive assessment (7/10, almost).
- Difficulty: medium

## Final Summary

- Rounds: 1 of 2. Score 7/10, verdict "almost". The narrowed research story (C1–C3 with R021) held up under an adversarial read of the claims, code and raw results. No broad new simulation is needed.
- The remaining work is presentation: novelty positioning, baseline and cost wording, one substantial-loss example, model scope, and keeping the qualifications (float64 evaluation, finite family, capped cases, inconclusive cases, the six leakage exceptions). These are inputs to the `NARRATIVE_REPORT.md` rewrite and `/paper-writing`.
- The manuscript itself still needs review once written (`/paper-writing` runs its own improvement loop, then `/paper-claim-audit` and `/citation-audit`).
- `/result-to-claim` was not re-run at termination. `CLAIMS_FROM_RESULTS.md` already carries the R020 jury verdict plus the R019, R021 and round-1 updates; a fresh run would overwrite those curated updates without new evidence.

## Method Description

GCS (Global Certified Selection) chooses N = 8 of M = 24 desired-phase-aligned pinching sites on one dielectric waveguide that serves a desired user D and protects a user P, when every activated site's actuator position is off by at most ε. Theorem 1 gives, for any subset, a certified SLNR lower bound L (a projection bound on the desired power, and an asymmetric-sector support-function bound on the leakage with a sec(π/K) angular correction) and an exact value at ε = 0. Theorem 2 builds one shared bank of at most 2M endpoint sign templates from all candidate sites. Evaluated on any subset, the bank gives that subset's exact endpoint-leakage maximum and feasible SLNR witnesses U_H.

The pipeline is: build the robust-clearance family; compute per-site tables and the bank; evaluate U_H for every subset in one batched pass; run a swap search for an incumbent L; then scan only the subsets whose U_H exceeds the incumbent (safe screening). This returns the exact certificate optimum Ŝ when the scan completes within the cap, a global bracket L(Ŝ) ≤ W* ≤ max U_H, and a uniqueness certificate when L(Ŝ) exceeds every rival's U_H. Protection limits follow from the endpoint converse F_end and the achievability bound Ī(Ŝ). Evaluation compares Ŝ with the exhaustive nominal optimum S_N through certified dominance L(Ŝ) > U(S_N).
