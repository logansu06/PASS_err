# Experiment Plan (v2)

**Problem:** certified robust selection of N of M desired-phase-aligned pinching-antenna sites under per-element actuator-position boxes (one waveguide, desired D, protected P).
**Method Thesis:** Within a robust-clearance, finite, D-aligned PASS family, nonlinear field enclosures plus a shared bank of at most 2M exact endpoint witnesses give computable robust brackets, safe global screening, and verifiable layout-optimality certificates. The chosen layout then provably beats the exhaustive nominal optimum, and often provably beats every other layout.
**Date:** 2026-09-27 (v2; v1 kept as `EXPERIMENT_PLAN_20260926_130108.md`)
**Target:** IEEE ICC 2027, 6 pages, deadline 2026-10-02.
**Status:** PLAN ONLY — no paper runs have been started. The numbers quoted below are pilot or review evidence, labeled as such.
**Inputs:**
- `refine-logs/FINAL_PROPOSAL.md` (v2);
- `idea-stage/handoff/GPT6_PRO_REPLY.md` and `GPT6_PRO_VERIFICATION.md`;
- the GPT-6 Pro code bundle in `idea-stage/handoff/gpt6pro_bundle/bundle/a7_verification_bundle/`.

## What Changed from v1

- **Method.**
  - The v1 swap search is replaced by **Global Certified Selection (GCS)**: a shared endpoint-witness bank, safe screening, exact certificate optimization, a global bracket, and a uniqueness test.
  - Leakage sectors are now asymmetric, with a $\sec(\pi/K)$ correction instead of the additive pad.
  - ε = 0 uses the exact SLNR; β_D > π/2 is rejected rather than clipped.
  - The family is filtered for robust clearance.
- **New claims:**
  - C2: the global certification yield;
  - C3: protection limits (converse/achievability, interference temperature).
- **New baseline:** a same-budget corner-robust swap heuristic (uncertified).
- **New negative controls:** P = D, and a noise-dominated SNR.
- **New cross-check:** rerun GPT-6 Pro's independent 132-case grid.
- **Cut:** κ analysis; directional-mechanism figure; Lemma 3 Taylor; N2/A8; the learning pilot. All stay in the research record only.

## Planning Gate

- **Dominant contribution:** Theorem 2 + Corollary 1 (global witness screening and certification), built on Theorem 1 (nonlinear bracket).
- **Complexity rejected:**
  - learning;
  - calibration (A2);
  - secrecy as the main line;
  - multi-user;
  - validated interval arithmetic;
  - Dinkelbach "exact" solver (invalid).
- **Reviewer concerns that still matter:**
  1. the principal matched-endpoint result against exhaustive nominal selection, with negative cases;
  2. a robust (not only nominal) baseline;
  3. separate reporting of the four gaps;
  4. a non-ideal channel control with an explicit power convention;
  5. numerical margins, with wording that avoids "machine-verified".
- **Frontier primitive:** absent by design (the "Frontier necessity" block is skipped).

## Claim Map

| Claim | Why it matters | Minimum convincing evidence | Blocks |
|---|---|---|---|
| **C1 (primary):** the GCS-selected layout has certifiably higher worst-case SLNR than the exhaustive nominal optimum in the same robust-clearance family, including identical endpoints | The central design result; it answers "is robust selection worth it?" against the strongest matched comparator | On the declared grid, report both controls: the fraction with $L(\hat S) > U(S_N)$; the fraction > 5%; median gain; inconclusive fraction; nominal sacrifice; desired/leakage decomposition | B0, B1, B2 |
| **C2 (supporting):** GCS certifies family-wide optimality often and cheaply | Lifts the paper above "bounds + heuristic search". This is the new mathematical contribution in action | Across the grid, for both controls: the uniqueness-certificate rate; the distribution of global bracket width $U^\star/L - 1$; survivors; runtime; the selection gap of plain swap search vs the exact certificate optimum | B3 |
| **C3 (supporting):** protection limits are quantifiable | Engineering meaning: which leakage ceilings are impossible under tolerance ε | $F_{\rm end}$ vs $\bar I(\hat S)$ bracket vs ε for pre-specified geometries; interference-temperature feasibility thresholds | B4 |
| **Anti-claims to rule out:** "gain = aperture freedom / weak comparator / loose-bound artifact / any robust heuristic does this / ideal-model artifact" | The obvious rebuttals | Identical-endpoint control; exhaustive nominal; the robust lower bound compared against the comparator's upper witness; the corner-robust baseline; a non-ideal control | B1, B2, B5 |

## Declared Test Grid (fixed before running)

| Item | Setting |
|---|---|
| Physics | 28 GHz ($\lambda = 10.714$ mm), $n_{\mathrm{eff}} = 1.44$, $d = 3$ m, $x_f = -10$ m; D at $(0, 0, 0)$ |
| Family | M = 24 D-aligned sites (N0), min spacing $0.68222\lambda$; N = 8; robust clearance $d_{\min} = 0.5\lambda$ (all subsets are feasible for ε ≤ 0.0911λ; the family is still filtered in code) |
| P geometries (33) | $x_P \in \mathrm{linspace}(-6, 6, 11)$ m × $y_P \in \{1, 2, 4\}$ m |
| Negative controls | P = D at $(0, 0)$; SNR 10 dB (noise-dominated); ε = 0 (L = W = U = exact) |
| Tolerance | $\epsilon/\lambda \in \{0, 0.01, 0.03, 0.05, 0.08\}$ |
| Noise | Fixed physical noise from reference SNR ∈ {10, 20, 30, 40} dB relative to $A_{\rm ref}$ (central 8-block toward D) |
| Controls | `free` ($\mathcal F_\epsilon$) and `endpoints` ($\mathcal F_\epsilon^{\rm end}$, sites 0 and 23 forced) |
| Certificates | Asymmetric sectors; $K = 1440$ with $\sec(\pi/K)$; β_D ≤ π/2 guard (reject); ε = 0 exact |
| Witnesses | Shared bank ($H \le 48$) for all layouts; for $S_N$ and $\hat S$ also all $2^8$ corners plus L-BFGS-B (4–8 restarts) |
| Search | Incumbent: swap from $S_N$ + 8 random starts (seed 2026). Exact screening afterwards. **Evaluation cap:** $2\times10^5$ certificate evaluations per case (pre-declared; reported) |
| Main grid size | 2 controls × 4 SNR × 5 ε × 34 geometries (33 + P = D) = **1,360 cases** |

## Experiment Blocks

### B0 — Sanity, correctness, and numerical audit (MUST-RUN)

- **Claim tested:** preconditions for all claims.
- **Checks:**
  1. **Bound validity.** For 20 pre-listed cases × 5 ε, draw $10^5$ random feasible δ plus all corners. Require no $\mathrm{SLNR} < L$ beyond $10^{-10}$ relative.
  2. **Endpoint-bank identity.** Across 40 random subsets, the bank maximum must equal the 256-corner endpoint maximum.
  3. **ε = 0.** $L = W = U =$ exact nominal, and $\hat S = S_N$.
  4. **Angular correction.** $K \in \{720, 1440, 5760\}$ with sec: the change in L is below the $\sec^2$ bound.
  5. **Clearance and β guard.** Clearance filtering is active; an artificial ε > 0.0911λ must shrink the family; β > π/2 must raise.
  6. **Reproducibility.** Two runs must match bit-for-bit.
  7. **Featured-instance margin audit.** For $P = (3, 2)$, ε = 0.05λ, 30 dB: recompute $L(\hat S)$, the top-5 rival $U_H$, and $U(S_N)$ in an independent implementation (and in extended precision for the winner and rivals). Report the margins.
- **Cross-check.** Rerun GPT-6 Pro's `a7_grid.py` (its independent 132-case matched grid). Compare with its stored results (108/132 positive, 79/132 above 5%).
- **Setup:** `a7_unit_checks.py` (from the bundle) plus `a7_checks.py` (new).
- **Success criterion:** all checks pass and the cross-check reproduces.
- **Failure interpretation:** any validity violation is a bug. Stop and fix before B1.
- **Target:** one sentence plus supplementary material.

### B1 — Main result: certified dominance over exhaustive nominal selection (MUST-RUN)

- **Claim:** C1.
- **Task:** the full declared grid (1,360 cases).
- **Systems:** GCS-selected $\hat S$ vs the exhaustive nominal optimum $S_N$, in the same family and control.
- **Metrics (decisive first):**
  1. fraction with certified gain $\Gamma = L(\hat S)/U(S_N) - 1 > 0$;
  2. fraction > 5%;
  3. median and IQR of Γ;
  4. inconclusive fraction.
  - Secondary: nominal sacrifice $1 - \mathrm{SLNR}_{\rm nom}(\hat S)/\mathrm{SLNR}_{\rm nom}(S_N)$; desired power and leakage at the witnesses.
- **Pre-declared go/no-go for C1 as the headline:** Γ > 5% in at least 20% of the **endpoints** cases with ε > 0 and P ≠ D. Otherwise reframe per the claims matrix.
- **Target:**
  - **Fig. 2:** Γ distribution per (ε, SNR), in two panels (free vs endpoints), with the inconclusive fraction shaded;
  - **Table II:** summary rows.

### B2 — Baselines and novelty isolation (MUST-RUN)

- **Claim:** C1 anti-claims.
- **Task:** SNR ∈ {20, 30} dB × ε ∈ {0.03, 0.05}λ × 34 geometries × 2 controls = 272 cases.
- **Systems (3 baseline families, all evaluated with the same L and U):**
  - **B-NOM:** exhaustive nominal-SLNR optimum (the B1 comparator).
  - **B-CR:** same-budget **corner-robust** swap heuristic. It maximizes $U_H(S)$, the min SLNR over the shared endpoint templates. It is uncertified, and it uses the same restarts and swap budget as the incumbent step.
  - **B-GR:** graduation-report-style corrected design — the desired-only aligned centered 8-block, blind to P.
- **Metrics:** $L$, $U$; the certified-dominance fraction of $\hat S$ over each; runtime.
- **Success:** $\hat S$ certifiably dominates B-GR in most cases. Against B-CR, the certified L is equal or higher, and a witness refutes B-CR's apparent robustness in some cases.
- **Failure interpretation:** if B-CR ≈ $\hat S$, then the certificate's value is verification plus the global bracket, not selection. C2 carries the novelty.
- **Target:** Table II (baseline rows).

### B3 — Global certification yield and screening efficiency (MUST-RUN)

- **Claim:** C2.
- **Task:** reuse the B1 runs, which already log GCS internals. Add M-scaling on 6 pre-listed geometries × ε ∈ {0.03, 0.05}λ × 30 dB with M ∈ {16, 24, 32} (N = 8; M = 32 means about 10.5 M subsets, batched).
- **Metrics:**
  - uniqueness-certificate rate (rival-dominance margin > 0);
  - global bracket width $U^\star/L(\hat S) - 1$;
  - survivors after screening;
  - certificate evaluations;
  - runtime;
  - **selection gap** of the plain swap incumbent vs the exact $\max L$ (v1 had 53.42 vs 56.56 on the featured case);
  - cap hits.
- **Success:** a reported distribution. No threshold is set; honest reporting of instances where uniqueness fails or the cap is hit.
- **Target:** **Fig. 4** (survivors, runtime, and uniqueness vs geometry and M); a featured-instance row in Table II.

### B4 — Protection limits and trade-offs (MUST-RUN, compact)

- **Claim:** C3.
- **Task:**
  - 3 pre-specified geometries: well-separated $(3, 2)$; near-endpoint $(6, 1)$; near-D $(0, 1)$;
  - ε/λ ∈ {0.01, 0.02, …, 0.09};
  - SNR 30 dB;
  - both controls.
- **Metrics:**
  - the bracket $F_{\rm end} \le \min_S \max_\delta I_P \le \bar I(\hat S)$ vs ε;
  - the interference-temperature thresholds $I_{\max}/\bar I$ and $I_{\max}/F_{\rm end}$ for a fixed $p$;
  - the SLNR bracket $[L(\hat S), U^\star]$ vs ε;
  - the nominal sacrifice vs ε.
- **Target:** **Fig. 3** (tolerance vs converse/achievability and SLNR brackets).

### B5 — Non-ideal channel control (MUST-RUN on a slice; extras NICE-TO-HAVE)

- **Claim:** C1 is not an artifact of the ideal model.
- **Model:**
  - 0.08 dB/m attenuation ($\alpha = \ln 10/20 \cdot \ell$);
  - $\cos^2\theta$ **field** directivity;
  - **fixed per-site feed power** convention, stated explicitly;
  - the phase is unchanged, so the D-aligned family is unchanged;
  - amplitude extrema from endpoints plus stationary roots.
- **Task:** the B2 slice (272 cases).
- **Metrics:** as in B1 and B3.
- **Nice-to-have:** 1 dB/m; Monte Carlo average SLNR (practitioner view); the D/P joint-box refinement (D.6) on the 5 widest-gap cases.
- **Target:** one row in Table II, or one sentence.

## Results → Claims Matrix (pre-declared)

| Outcome | Allowed claim | Avoid |
|---|---|---|
| $L(\hat S) > U(S_N)$ in a substantial reported fraction, both controls | Certified worst-case SLNR improvement over exhaustive nominal selection within the matched robust-clearance family | Superiority over all PASS designs or continuous placements |
| $L(\hat S) > \max_{S \ne \hat S} U_H$ | Unique global robust-optimal layout within the stated family, model, and float64 margins | Unrestricted global optimum; "machine-verified" |
| Only $L \le W^\star \le U^\star$ holds | A global bracket; performance ratio at least $L/U^\star$ | Exact optimizer |
| Free gain large, matched gain small | Report both separately | Presenting the free gain as a fixed-aperture gain |
| $L(\hat S) \le U(S_N)$ | Certificate inconclusive | "Robust is worse" |
| $pF_{\rm end} > I_{\max}$ | No family member meets that ceiling under ε | All architectures are infeasible |
| B-CR ≈ $\hat S$ | The certificate's value is verification plus the global bracket | That certification is necessary for selection |
| Non-ideal control holds | Persists under the tested separable attenuation/directivity | Hardware validation; coupled depletion |
| Nominal SLNR drops while the robust bound rises | An explicit nominal–robust trade-off | "No-cost robustness" |
| Cap hit in some cases | A bracket without an exact argmax there | An exact certificate optimum for those cases |

## Run Order and Milestones

| Milestone | Date | Goal | Runs | Decision gate | Cost | Risk |
|---|---|---|---|---|---|---|
| **M0 Implement + sanity** | Sep 27 | Port GCS into `a7_gcs.py` (from the bundle's `a7_audit.py`/`a7_global.py`, attributed); unit checks; B0; cross-check rerun | R001–R008 | All B0 checks pass; the cross-check reproduces | < 1 CPU-h | Port bug (mitigation: bit-for-bit comparison with the bundle on the featured case) |
| **M1 Main** | Sep 27–28 | B1 full grid (logs B3 internals) | R009–R010 | **C1 go/no-go** (pre-declared) | ~0.5–1 CPU-h | Weaker endpoint effect; cap hits at ε = 0.08 |
| **M2 Baselines + yield** | Sep 28 | B2 and B3 (M-scaling) | R011–R014 | B-CR comparison fixes the framing of C1 | ~1 CPU-h | M = 32 memory/time → batch; drop M = 32 if over budget |
| **M3 Limits + non-ideal** | Sep 28–29 | B4, B5 | R015–R017 | Non-ideal holds → keep the general wording | < 1 CPU-h | Benefit model-dependent |
| **M4 Freeze** | Sep 29 | Figures, number reconciliation, featured margin audit, `/result-to-claim` (GPT-6 Astra ultra) | R018–R020 | Claims gated by the verdict | — | Claims narrowed |
| **Writing** | Sep 30 – Oct 1 | Rewrite `NARRATIVE_REPORT.md`, then `/paper-writing — venue: IEEE_CONF, human checkpoint: true` | — | 6 pages; claim audit; citation audit | — | Time |
| **Submit** | Oct 2 | EDAS | — | — | — | — |

## Compute and Data Budget

- Total under 4 CPU-hours. No GPU and no data.
- **Bottleneck:** the M0 port and audit, then writing.

## Risks and Mitigations

- **Matched effect smaller than free.** Pre-declared gate plus the claims matrix. GPT-6 Pro's independent 132-case grid already shows 79/132 above 5% (to be reproduced in M0).
- **Screening efficiency degrades at large ε or co-aligned receivers.** Pre-declared cap; report bracket-only cases.
- **Float64 margins.** Margin audit on the featured instances; wording "evaluated numerically".
- **Novelty pushback.** Lead with Theorem 2 / Corollary 1; credit the tools (see `FINAL_PROPOSAL.md`, Novelty Statement).
- **Scope creep.** Nice-to-have runs happen only after M3.

## Figures and Tables (at most 4 figures)

- **Fig. 1:** geometry (D, P, waveguide, matched endpoints) plus a certificate-construction inset (true contribution curve, asymmetric sector, endpoint zonotope).
- **Fig. 2:** Γ distributions (free vs endpoints; per ε, SNR) with the inconclusive fraction (B1).
- **Fig. 3:** tolerance sweep: SLNR bracket and leakage converse/achievability (B4).
- **Fig. 4:** global screening yield and efficiency (B3).
- **Table I:** protocol and parameters.
- **Table II:** featured global certification plus baselines plus the non-ideal row (B1, B2, B3, B5).

## Final Checklist

- [x] Main paper tables and figures covered (Fig. 2 / Table II ← B1, B2; Fig. 3 ← B4; Fig. 4 ← B3)
- [x] Novelty isolated (B-CR, B-GR, exhaustive nominal; C2 global certification)
- [x] Simplicity defended (no learning; cut list)
- [x] Frontier contribution explicitly not claimed
- [x] Must-run vs nice-to-have separated; evaluation cap and go/no-go pre-declared
