# Pipeline Summary

**Problem:** certified robust-SLNR selection of desired-phase-aligned pinching-antenna sites under bounded actuator-position errors (PASS, one waveguide, desired receiver D, protected receiver P).
**Final Method Thesis:** For desired-phase-aligned pinching sites, cheap sector enclosures with exact marginal phase and amplitude ranges yield a certified worst-case SLNR. Maximizing it selects sites whose worst-case SLNR certifiably exceeds that of the exhaustive nominal optimum in the same matched family.
**Final Verdict:** REVISE (7.70/10 after 2 rounds, GPT-6 Astra at `ultra`). The remaining gap is the principal controlled result, which the experiment plan supplies.
**Date:** 2026-09-26

## Final Deliverables
- Proposal: `refine-logs/FINAL_PROPOSAL.md`
- Review summary: `refine-logs/REVIEW_SUMMARY.md`
- Refinement report: `refine-logs/REFINEMENT_REPORT.md`
- Experiment plan: `refine-logs/EXPERIMENT_PLAN.md`
- Experiment tracker: `refine-logs/EXPERIMENT_TRACKER.md`

## Contribution Snapshot
- **Dominant contribution:** the certified robust-SLNR selection framework (Propositions 1–2 plus the dominance Corollary), with search started from the exhaustive nominal optimum. It is evaluated by certified dominance over exhaustive nominal selection with identical endpoints.
- **Supporting:**
  - Lemma 0 (monotone guided phase and sensitivity floor, inherited from the graduation-report C1);
  - Lemma 3 (conditional leakage fragility);
  - one paired mechanism analysis;
  - the fixed-pair noise regime.
- **Explicitly rejected complexity:**
  - learning (negative pilot);
  - A2 calibration;
  - full-duplex or multi-user systems;
  - a universal κ threshold;
  - a universal directional-spreading story;
  - N0/N2/A8 in the main text;
  - continuous global optimization.

## Must-Prove Claims
- **C1:** certified dominance over exhaustive nominal selection within the matched family, including identical endpoints. Negative cases and desired/leakage components are reported.
- **C2:** why and when — conditional fragility, the pointwise noise regime, directional sensitivity as a partial (non-universal) explanation, and honest bracket tightness.

## First Runs to Launch (after user go-ahead)
1. R001–R004 (M0 sanity): bound validity, ε = 0 equality, angular-grid refinement, reproducibility and clearance.
2. R005 (M1): `python idea-stage/pilots/a7_main.py`, the full 1,320-case grid. **Go/no-go:** >5% certified gain in ≥ 20% of identical-endpoint cases.
3. R007–R009 (M2): B-GR and B-SAMP baselines, plus search adequacy against the exhaustive certificate optimum at 12/4.

## Main Risks
- **Modest endpoint effect.** Mitigation: pre-declared gate and claims matrix; honest reporting.
- **Conservative brackets for co-aligned receivers.** Mitigation: quantiles by geometry class.
- **"Established tools" novelty pushback.** Mitigation: narrow positioning; the audited PASS design result carries the paper.

## Next Action
- **On hold by user instruction:** do not start experiments yet. When approved, run `/run-experiment` (or execute R001→R006 directly), then `/result-to-claim` (GPT-6 Astra, ultra), then `/paper-writing — venue: IEEE_CONF`.
