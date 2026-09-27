# Pipeline Summary (v2, 2026-09-27)

**Problem:** certified robust selection of desired-phase-aligned pinching-antenna sites under bounded actuator-position errors (one waveguide, desired D, protected P).
**Final Method Thesis:** Within a robust-clearance, finite, D-aligned PASS family, nonlinear field enclosures plus a shared bank of at most 2M exact endpoint witnesses give computable robust brackets, safe global screening, and verifiable layout-optimality certificates.
**Final Verdict:**
- refine rounds (GPT-6 Astra ultra): REVISE 7.70/10;
- upgraded with the GPT-6 Pro deep verification: estimated 60–70% acceptance after the evidence is complete (subjective).

**Date:** 2026-09-27

## Final Deliverables
- Proposal: `refine-logs/FINAL_PROPOSAL.md` (v2)
- Experiment plan: `refine-logs/EXPERIMENT_PLAN.md` (v2)
- Tracker: `refine-logs/EXPERIMENT_TRACKER.md` (v2)
- Review history: `refine-logs/REVIEW_SUMMARY.md`, `refine-logs/round-*.md`
- GPT-6 Pro review, verification, and code: `idea-stage/handoff/`

## Contribution Snapshot
- **Dominant:** global witness screening and certification — Theorem 2 (at most 2M shared endpoint templates; exact endpoint cover; safe screening; exact max L) and Corollary 1 (global bracket; unique robust-optimality test). It rests on Theorem 1, the nonlinear SLNR bracket with asymmetric sectors and sec correction.
- **Supporting:** Corollary 2 (leakage converse/achievability; interference-temperature feasibility); certified dominance over exhaustive nominal selection with identical endpoints; the nominal–robust trade-off.
- **Rejected:**
  - learning;
  - A2;
  - secrecy as the main line;
  - κ threshold;
  - directional-spreading story;
  - Lemma 3 Taylor;
  - N2/A8;
  - Dinkelbach "exact" solver;
  - validated interval arithmetic.

## Must-Prove Claims
- **C1:** $L(\hat S) > U(S_N)$ on a reported fraction of the declared grid, free and matched. Negative cases and nominal sacrifice are included.
- **C2:** the global certification yield (uniqueness rate, bracket width, survivors, runtime, selection gap).
- **C3:** protection limits vs tolerance.

## First Runs to Launch (after user go-ahead)
1. R001: port GCS into `a7_gcs.py`; verify it matches the bundle bit-for-bit on the featured case.
2. R002–R008: sanity checks, featured margin audit, and the cross-check rerun of GPT-6 Pro's 132-case grid.
3. R009: the main 1,360-case grid. **Go/no-go:** Γ > 5% in at least 20% of endpoint cases.

## Main Risks
- Matched effect smaller than free → pre-declared gate and claims matrix.
- Screening degrades at large ε → evaluation cap and bracket-only reporting.
- Float64 margins → featured margin audit; careful wording.

## Next Action
- **On hold by user instruction:** do not start experiments yet. When approved, start with R001.
