# Review Summary

**Problem:** certified robust-SLNR selection of desired-phase-aligned pinching-antenna sites under bounded actuator errors (IEEE ICC 2027).
**Reviewer:** GPT-6 Astra, `ultra` (thread `01a0dc09-8626-7381-8ced-5aeb34168c36`; traces in `.aris/traces/research-refine/2026-09-26_run01/`).
**Rounds:** 2 / 3. The user-approved cap was lowered from 5 to 3 because of the deadline; refinement stopped after round 2.
**Final Verdict:** REVISE (7.70/10). The remaining gap is evidence from the planned experiment, not method design.

## Problem Anchor
See `FINAL_PROPOSAL.md`. Success condition 2 was narrowed in round 1 (reviewer-accepted as acknowledged narrowing, not drift).

## Score Evolution

| Round | Problem Fidelity | Method Specificity | Contribution Quality | Frontier Leverage | Feasibility | Validation Focus | Venue Readiness | Overall | Verdict | Est. acceptance |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 9 | 7 | 6 | 9 | 8 | 7 | 6 | 7.40 | REVISE | 30–40% (55–65% after repairs) |
| 2 | 9 | 8 | 6 | 9 | 8 | 8 | 6 | 7.70 | REVISE | 40–50% (60–70% if matched-endpoint gains hold) |

## What Changed and Why

**Round 1 → 2:**
- Universal κ threshold → conditional fragility lemma plus a candidate-dependent noise condition. κ failed as a predictor: a counterexample, and a vacuous remainder in 72/528 cases.
- "Reduces Σ|b|" → directional mechanism.
- False PASS-vs-free-space claim → Lemma 0 (monotone guided phase, sensitivity floor).
- Novelty wording narrowed (Pakravan; Chen H-PASS).
- Evaluation repairs specified: exhaustive nominal, fixed endpoints, nominal initialization, ε = 0 special case, bracket quantiles.

**Round 2 → final:**
- Lemma 0 moved into the setup; its qualifications added.
- Mechanism made non-universal (T rose in 5/357 positive-gain comparisons).
- Noise condition folded into the dominance corollary; SNR sweeps recompute the selections.
- Wording: "sector enclosures with exact marginal ranges"; "rigorous angular-grid correction".
- Driver `a7_main.py` completed: exhaustive nominal, fixed endpoints, nominal-initialized search, ε = 0 special case, clearance assert, witness logging. **Not yet run.**

## Unresolved (carried into the experiment plan)

1. **CRITICAL (Venue Readiness):** a reproducible principal table/figure of certified dominance over exhaustive nominal selection with identical endpoints, including negative cases and desired/leakage components.
2. **IMPORTANT (Contribution Quality):** the contribution rests on established tools. It must be carried by the audited PASS design result; another lemma would not help.
