# Research Contract: Certified Robust Site Selection for PASS — Global Screening Under Position Errors (Idea A7 v2, no learning)

> **Updated 2026-09-27** with the GPT-6 Pro deep-verification upgrades. The authoritative files are `refine-logs/FINAL_PROPOSAL.md` (v2) and `refine-logs/EXPERIMENT_PLAN.md` (v2). Sections below this note that were not rewritten describe v1.

> Focused working document for the active idea. Read this on session recovery instead of the full `IDEA_REPORT.md`.

## Selected Idea

- **Description.** One waveguide carries a desired receiver D and a protected receiver P. From M desired-phase-aligned pinching sites (N0 construction), select N sites so that the worst-case SLNR under per-element actuator-position boxes $|\delta_n| \le \epsilon$ is maximized. The objective is replaced by a certified lower bound:
  - a desired-gain lower bound (N1);
  - a sector-support leakage upper bound with a rigorous angular-grid correction.
  
  Improvement over the **exhaustive nominal optimum** in the same matched family is shown by **certified dominance**: $L(S_R) > U(S_N)$.
- **Source:** `idea-stage/IDEA_REPORT.md`, candidate A7. Jury rank 1; novelty 6/10 PROCEED; external review "proceed without learning"; refined to 7.70/10.
- **Selection rationale:**
  - It has the strongest task, structure, and mathematics.
  - The mechanism gate passed strongly, and it survives exhaustive-nominal and identical-endpoint controls in reviewer reruns.
  - Learning was tested and dropped (not necessary).
  - A2 (calibration) is weaker in novelty (5/10) and missing its residual certificate.
  - The user asked for the highest acceptance probability, with strong math, structure, and task; AI optional.

## Core Claims (v2)

1. **C1:** within the robust-clearance, D-aligned family (free and identical-endpoint), the GCS-selected layout has certifiably higher worst-case SLNR than the exhaustive nominal optimum: $L(\hat S) > U(S_N)$. Negative cases and the nominal sacrifice are reported.
2. **C2:** the global certification yield. A shared bank of at most 2M exact endpoint witnesses gives safe screening, the exact certificate optimum, the global bracket $L \le W^\star \le U^\star$, and a unique robust-optimality test.
3. **C3:** protection limits. The converse/achievability bracket $F_{\rm end} \le \min_S\max_\delta I_P \le \bar I(\hat S)$ and interference-temperature feasibility, as functions of tolerance.

## Method Summary

- **PASS phase is strictly monotone.** For $n_{\mathrm{eff}} > 1$ the slope is $\psi' = k_0(n_{\mathrm{eff}} + \sin\theta) \ge k_0(n_{\mathrm{eff}} - 1)$ (Lemma 0, from the graduation-report sensitivity C1). So each site's feasible phase set under an actuator box is exactly its endpoint interval, and its amplitude range has closed-form extrema.
- **Sector enclosures.** These give (Prop. 1) a lower bound on the desired gain of D-aligned sites and (Prop. 2) an upper bound on leakage via the closed-form support function of each annular sector, maximized over a θ grid with a Lipschitz pad. Both are separable per site, so a subset is evaluated in $O(NK)$.
- **Search and certification.** The certified SLNR $L(S) = L_D/(\sigma^2 + \bar I)$ is maximized by swap search started from the exhaustive nominal optimum plus 8 random starts. Feasible witnesses (all corners plus L-BFGS-B) give $U(S)$, and $L(S_R) > U(S_N)$ certifies $W(S_R) > W(S_N)$.
- **Fragility.** Lemma 3 (random-sign bound with remainder) explains nominal-null fragility conditionally.

## Experiment Design

- **Data:** simulation only, on a declared grid:
  - 33 P geometries;
  - $\epsilon/\lambda \in \{0, .01, .03, .05, .08\}$;
  - reference SNR {10, 20, 30, 40} dB;
  - 2 controls: common region and identical endpoints;
  - M = 24, N = 8, 28 GHz, $n_{\mathrm{eff}} = 1.44$, d = 3 m.
- **Baselines:**
  - exhaustive nominal SLNR (B-NOM, strongest);
  - graduation-report-style desired-only aligned centered block (B-GR, corrected N0 physics);
  - sampled-error robust heuristic (B-SAMP).
- **Metrics:** fraction of cases with certified dominance; fraction with certified gain > 5%; median gain; desired/leakage at witnesses; U/L quantiles; search optimality gap.
- **Key settings:** angular grid K = 1440 with pad; 8 restarts; seed 2026; clearance $d_{\min} = 0.5\lambda$.
- **Compute:** under 3 CPU-hours.
- **Plan / tracker:** `refine-logs/EXPERIMENT_PLAN.md`, `refine-logs/EXPERIMENT_TRACKER.md`.

## Baselines

| Method | Setting | Metric | Score | Source |
|---|---|---|---|---|
| Exhaustive nominal (B-NOM) | declared grid | worst-case SLNR (upper witness) | TBD (R005) | this work |
| Graduation-report-style block (B-GR) | B2 slice | certified L / U | TBD (R007) | this work (N0 physics) |
| Sampled-error heuristic (B-SAMP) | B2 slice | certified L / U | TBD (R008) | this work |

## Current Results

These are pilot results only, **not paper evidence**. The paper uses `a7_main.py` outputs.

| Method | Setting | Metric | Score | Notes |
|---|---|---|---|---|
| A7 robust vs local nominal | 528-case κ sweep | certified gain | median 0 → +11% across κ bins | `a7_kappa_results.csv` (archived pilot) |
| A7 robust vs exhaustive nominal | reviewer rerun, 528 cases | fraction certified positive / > 5% | 359/528 / 247/528 | reviewer-generated; not in repo |
| A7, identical endpoints | reviewer rerun, 33 geoms × 4 settings | fraction > 5% | 16–22/33 | reviewer-generated; not in repo |

## Key Decisions

- **No learning.** The MLP selector reached 0.669 of the reference, and the learned warm start ≈ random. The reviewer said to drop it.
- **Exhaustive nominal comparator.** Robust search is initialized from $S_N$, so $L(S_R) \ge L(S_N)$.
- **ε = 0 is special-cased** to avoid the 2.78% pad artifact.
- **No universal κ threshold and no universal directional-spreading claim.**
- **Graduation-report curves are not physical baselines** (N0 misalignment finding). Its C1 theory and corrected design live on as Lemma 0 and B-GR.
- **Refinement stopped after round 2 of 3.** The remaining gap is evidence.

## Status

- [x] Idea selected (2026-09-26)
- [x] Pilot mechanism validated
- [x] Experiment plan v1 written
- [x] GPT-6 Pro deep verification. All statements [PROVEN]; corrections accepted; global screening reproduced locally (2026-09-27).
- [x] Proposal and experiment plan upgraded to v2 (2026-09-27)
- [ ] M0: port GCS into `a7_gcs.py` plus sanity checks and the cross-check — **on hold until user approval**
- [ ] M1: main grid (1,360 cases; go/no-go)
- [ ] M2: baselines (B-CR, B-GR), yield, M-scaling
- [ ] M3: protection limits and the non-ideal control
- [ ] `/result-to-claim` (GPT-6 Astra, ultra)
- [ ] Paper draft (`/paper-writing`, IEEE_CONF)
