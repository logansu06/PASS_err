# Refinement Report

## Starting Point
Idea A7 from `/idea-discovery`.
- Jury rank 1.
- Novelty 6/10, PROCEED.
- External review: 4/10 weak reject in its pilot state; proceed without learning.

## Final Method Thesis
For desired-phase-aligned pinching sites, cheap sector enclosures with exact marginal phase and amplitude ranges yield a certified worst-case SLNR. Maximizing it selects sites whose worst-case SLNR certifiably exceeds that of the exhaustive nominal optimum in the same matched family.

## Dominant Contribution
The certified robust-SLNR selection framework and task, evaluated by certified dominance against exhaustive nominal selection with identical endpoints.

## Intentionally Rejected Complexity
- Learning: negative pilot.
- A2 calibration.
- Full-duplex or multi-user extensions.
- A universal κ threshold.
- A universal directional-spreading story.
- N0/N2/A8 comparators in the main text.
- Continuous global optimization.

## Frontier Primitive
**Absent by design.** The reviewer judged "Modernization: NONE" in both rounds.

## Key Claims and Must-Run Ablations
- **C1:** certified dominance (main table/figure).
- **C2:** mechanism and fragility diagnostics, bracket tightness.
- **Must-run:**
  - exhaustive nominal comparator;
  - identical-endpoint control;
  - ε = 0 sanity check;
  - small-instance certificate optimum;
  - one non-ideal channel check.

## Remaining Risks
- The matched-endpoint effect may be modest in some regimes. Report it honestly; the reviewer's independent rerun gives 16–22/33 above 5%.
- Brackets are conservative for co-aligned receivers.
- Novelty rests on the PASS design result, not on new tools.

## Files
- `round-0-initial-proposal.md`, `round-1-review.md`, `round-1-refinement.md`, `round-2-review.md`
- `FINAL_PROPOSAL.md` (+ timestamped copy)
- `REVIEW_SUMMARY.md`
- `REFINE_STATE.json`
