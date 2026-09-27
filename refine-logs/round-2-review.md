# Round 2 Review (GPT-6 Astra, ultra; same thread)

- **Thread:** `01a0dc09-8626-7381-8ced-5aeb34168c36`
- **Trace:** `.aris/traces/research-refine/2026-09-26_run01/002-round2-review`
- **Verdict:** REVISE
- **Overall:** 7.70 / 10 (round 1: 7.40)
- **Estimated acceptance:** 40–50% at the current state; 60–70% if the corrected evaluation shows useful gains with identical endpoints and the claims are qualified.

| Problem Fidelity | Method Specificity | Contribution Quality | Frontier Leverage | Feasibility | Validation Focus | Venue Readiness |
|---|---|---|---|---|---|---|
| 9 | 8 | 6 | 9 | 8 | 8 | 6 |

## Key findings

**Fixed**
- The κ threshold is gone.
- The fragility floor is now conditional.
- The PASS-vs-free-space claim is corrected.
- Bracket reporting and "certificate optimum" terminology are correct.
- The amended success condition is an acceptable narrowing, not damaging drift.

**Lemma 0 — correct, but modest novelty.** It is a direct consequence of C1, so it belongs in the model/certificate setup.

$$|z'|^2 = A'^2 + A^2\psi'^2 \ge k_0^2(n_{\mathrm{eff}} - 1)^2A^2$$

Required qualifications:
- The floor concerns each complex channel contribution; received power and SLNR can still have zero first-order sensitivity.
- The floor scales with $A$.
- The feed-side asymmetry is about $\xi$, not about ordering the aggregate leakage.

**Wording fixes**
- Write "sector enclosures with exact marginal phase and amplitude ranges".
- Write "rigorous angular-grid correction".

**The directional mechanism is not universal.**
- $T$ increases in 5 of the 357 archived comparisons with positive gain.
- Example: $P = (4.8, 4)$, $\epsilon = 0.03\lambda$, $\sigma^2 = 10^{-4}$ gives gain +2.21% with $T_R/T_N = 1.011$.
- Directions matter modulo $\pi$, and $h_0 \ne 0$ matters.
- Safe wording: "directional leakage sensitivity explains substantial gains in the examined cases, while the certificate also trades nominal leakage and desired gain."

**Noise condition**
- It is correct for a fixed pair and a fixed witness. It is sufficient, not necessary, and belongs inside the dominance corollary.
- In an SNR sweep, either recompute the selections at every point or freeze the pair.

**Code (at review time)**
- The helpers are verified.
- Still missing: the evaluation path (the old `run_case` ignores `fix_ends`), nominal initialization, the $\epsilon = 0$ special case (the grid pad costs 2.78%), and witness logging with a clearance check.
- *Post-review:* `a7_main.py` now has exhaustive nominal selection, fixed endpoints, nominal-initialized search, the $\epsilon = 0$ special case, the clearance assert, and witness vectors. It has **not been run**, per user instruction. `run_case` is marked deprecated.

**Highest-value next step:** one reproducible principal figure/table of certified dominance over exhaustive nominal selection with identical endpoints, including negative cases and the desired/leakage components.

**Modernization:** NONE.
