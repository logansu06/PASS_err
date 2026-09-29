# PASS Result-to-Claim Evaluation (2026-04-17, updated after placement baselines)

- claim_supported: partial
- confidence: medium
- note: local judgment only; secondary reviewer delegation was unavailable in this session.

## Supported Scope

The updated experiments strongly support the narrow one-design robustness story for the current constructive phase-aligned PASS placement in the studied symmetric setting:

- The deterministic lower bound tightly characterizes normalized degradation inside the guaranteed small-error region.
- In the pre-null regime, the harmful bounded-error pattern is empirically a left-right split-mode phase-spread pattern, while common-bias motion is nearly harmless.
- The second-order covariance / phase-variance predictor explains the observed stochastic trends for the studied iid uniform, common-bias, and correlated Gaussian models over the tested small-error range.
- The results still do not support any globally certified continuous-box optimum claim or any general design-optimality claim.

The new baseline section supports only a narrower comparative design claim:

- The constructive aligned placement is better than the naive uniform-aperture baseline on the sampled robustness metrics, especially for box-best-found robustness.
- The constructive aligned placement is not the best same-aperture placement among the tested candidates, because the direct nominal optimizer is better on every reported metric in the new section.

## Key Evidence

- `results/config.json` logs `epsilon_valid_norm = 0.17126776184398004`.
- Over the guaranteed region, the maximum absolute gap between `wc_norm` and `lb_full_norm` in `results/data_main.csv` is about `3.40e-6`.
- Before `epsilon/lambda = 0.175`, the maximum split-versus-box-best-found gap in `results/data_main.csv` is about `1.57e-5`.
- At `epsilon/lambda = 0.1` for the aligned design:
  - `wc_norm = 0.38172695`
  - `split_norm = 0.38174263`
  - `common_bias_norm = 0.99993864`
- In `results/data_error_scenarios.csv` at `epsilon/lambda = 0.1`:
  - iid uniform mean `0.76980750`, quadratic approximation `0.74416072`
  - common-bias mean `0.99997949`, quadratic approximation `0.99997959`
  - correlated Gaussian mean `0.84576180`, quadratic approximation `0.83094739`
- In `results/data_baseline_summary.csv` at `epsilon/lambda = 0.10`:
  - aligned constructive vs uniform aperture:
    - nominal `1.70115737` vs `1.68249052` (`+1.1%`)
    - box-best-found `0.44350703` vs `0.38857314` (`+14.1%`)
    - iid mean `1.31150359` vs `1.29980612` (`+0.9%`)
  - direct nominal optimizer vs aligned constructive:
    - nominal `+1.69%`
    - box-best-found `+11.09%`
    - iid mean `+1.68%`
- In `results/data_baseline_curves.csv`, aligned constructive stays above uniform aperture on the sampled box-best-found and iid-mean curves, while the direct nominal optimizer stays above aligned constructive on those same sampled curves.

## Why The Verdict Is Not `yes`

The new design claim is not fully supported as currently phrased:

- `materially outperforms a naive uniform-aperture baseline` is too broad if it is read across all reported metrics. The only clearly material gain is box-best-found robustness; nominal gain and stochastic means improve only by about `1%`.
- The direct nominal optimizer beats the constructive aligned design on every reported same-aperture metric in the new section, so any near-optimal or generally preferable design language would be unsupported.

Because the intended claim bundle now includes this comparative design statement, the overall verdict should be `partial`, not `yes`.

## Limits

- Continuous-box search is still best-found, not globally certified.
- The split-mode construction is empirically near-adversarial in the current symmetric setting, not a theorem.
- The stochastic predictor is validated only for the studied placement and the tested range up to `epsilon/lambda = 0.1`.
- No `N` sweep or `d` / `delta_p` sweep yet, so comparative placement conclusions are not established beyond the current setup.

## Recommended Working Claim

For the current constructive phase-aligned PASS placement in the studied symmetric setting, the deterministic lower bound tightly characterizes normalized bounded-error degradation inside the guaranteed small-error region; in the pre-null regime, degradation is empirically dominated by a left-right split-mode phase-spread pattern while common-bias motion is nearly harmless; and a second-order covariance / phase-variance predictor explains the observed stochastic trends for the studied iid uniform, common-bias, and correlated Gaussian models. In the tested same-aperture comparison, the constructive aligned placement is more robust than a naive uniform-aperture baseline, especially in box-best-found robustness, but it is not the best placement among the tested candidates because the direct nominal optimizer performs better on all reported metrics. We do not claim a globally certified continuous-box optimum or any general design optimality.

---

# 2026-09-25 — Pre-conversion audit for ICC 2027 (no new claim verdict)

- claim_supported: unadjudicated (no cross-model verdict exists for the current evidence)
- note: this entry records housekeeping and deterministic evidence checks only. It issues no support verdict; that remains the job of `/result-to-claim` with the Codex reviewer.

## Target Change

- The project is being converted from the graduation report into an IEEE ICC 2027 symposium paper (`IEEE_CONF`, 6 printed pages including references, EDAS deadline 2026-10-02).
- Writing input is now `NARRATIVE_REPORT.md` (repo root). The graduation-report LaTeX and the graduation-report `PAPER_PLAN.md` were archived under `fyp_report/` so that `/paper-writing` starts a fresh 6-page plan instead of reusing the report outline.

## Claim Gate Status

- The 2026-04-17 verdicts (`CLAIMS_FROM_RESULTS.md`: `yes`; the entry above: `partial`) were executor-side judgments without a cross-model reviewer (see the note in the entry above), and the `yes` file also predates the placement-baseline section.
- Under the `result-to-claim` fail-closed rule, `CLAIMS_FROM_RESULTS.md` now contains only `verdict: REVIEW_UNAVAILABLE`, so `/paper-plan` treats it as absent and tags claims `[unadjudicated]`. The superseded file text is preserved at git commit `3fa8650`.
- Required before submission-grade writing: rerun `/result-to-claim` (Codex) on the claims listed in `NARRATIVE_REPORT.md`.

## Deterministic Evidence Re-check (Type-A: values exist in stored artifacts)

Recomputed on 2026-09-25 directly from `results/` (no reruns of `src/main.py`):

- All numbers quoted in the 2026-04-17 entry reproduce from `results/config.json`, `results/data_main.csv`, `results/data_box_validation.csv`, `results/data_error_scenarios.csv`, and `results/data_baseline_summary.csv`.
- `lb_full_norm <= wc_norm` holds at all 35 grid points with `eps_norm <= epsilon_valid_norm` in `results/data_main.csv`; the maximum gap is `3.398e-06`.
- Stochastic predictor error over `0 <= eps_norm <= 0.10` (`results/data_error_scenarios.csv`, 21 levels, 2000 samples each): iid uniform MAE `5.671e-03` (max `2.565e-02` at `0.100`); common bias MAE `8.413e-08` (max `3.659e-07` at `0.080`); correlated Gaussian MAE `3.387e-03` (max `1.526e-02` at `0.095`).
- Sensitivity sweeps: `results/data_neff_sweep.csv` at `eps_norm = 0.1` gives `wc_norm` `0.38173 / 0.20610 / 0.09921` for `n_eff = 1.44 / 1.75 / 1.99`; `results/data_freq_sweep.csv` at `eps_m = 0.001` gives `0.96755 / 0.44105 / 3.75e-18` for `f_c = 6 / 28 / 60 GHz`.

## Provenance Gaps Found in the Graduation Report

- `fig_corr_length_sweep` and its checkpoints (mean `0.7757` at normalized correlation length `0.25`, `0.9612` at `32`) have no generating code in `src/` and no data file in `results/`. Only the length-4 point (`0.8458`) matches `results/data_error_scenarios.csv`. This figure cannot be used as paper evidence until it is regenerated from committed code.
- Graduation report Section 3.1 compares the iid Monte Carlo mean `0.769808` at `eps_norm = 0.10` with the main bounded-error curve. That value comes from `results/data_error_scenarios.csv` (2000 samples); the main-curve Monte Carlo mean in `results/data_main.csv` is `0.7703564` (1000 samples). The paper should quote one source per figure.
- `xi_min = 1.4203` is not stored in `results/`; it follows from `2 * xi_mean - xi_max` under the symmetric placement (`xi_mean = 1.44`, `xi_max = 1.4597026` in `results/config.json`).

## Open Evidence Gaps (unchanged since AUTO_REVIEW round 2)

- No `N` sweep.
- No `d` or `delta_p` sweep.
- Near-null continuous-box validation still uses 6 local restarts (`results/config.json` `box_search.local_restarts`); no independent global-search cross-check.
- Novelty against 2025-2026 PASS literature and classical array phase-error tolerance theory has not been checked (`/comm-lit-review`, `/novelty-check`).

---

# 2026-09-25 — Literature review and novelty check (positioning for ICC 2027)

- claim_supported: unchanged (still unadjudicated; no `/result-to-claim` run)
- artifacts: `idea-stage/LIT_REVIEW.md`, `idea-stage/NOVELTY_REPORT.md`, `.aris/novelty/`, trace `.aris/traces/novelty-check/2026-09-25_run01/`

## Correctness Finding (N0) — affects every stored result

- `src/design_delta_star.py` solves the phase-alignment equation on the positive side only and mirrors it (`delta_star = concat(-delta_pos[::-1], delta_pos)`). Because `Phi(Delta) = k0 (R + n_eff Delta)` is not even in `Delta`, the upstream half is not aligned: residual phases reach 0.683 rad, and the raw nominal gain is `1.70116 = 0.957 * a_ideal`.
- Every `*_norm` curve in `results/` subtracts per-element nominal phases (`phi_ref`), so it describes an idealized phase-compensated array, not the physical PASS. The graduation report's C6 ("constructive loses on every metric to the nominal comparator") likely stems from this.
- Prototype fix (`.aris/novelty/proto.py::aligned`): solve for each of N consecutive wavelength levels; the root is unique because `dPhi/dDelta > 0`. Raw nominal gain becomes `1.77754 = a_ideal`. The main pipeline has not been changed yet.

## Novelty Verdict

- 6/10, PROCEED WITH CAUTION (Codex `gpt-6-astra`, xhigh). No named published paper contains the combined result.
- Literature corrections (both verified by Claude):
  - Yang et al., TVT 2026 (arXiv 2601.17825), use per-element box errors, not ℓ2 balls.
  - Chen, Qi, Dobre, Yuen, "Hybrid Pinching Antenna Systems", TWC 2026 (DOI 10.1109/TWC.2026.3664320), already simulate multi-PA position-error degradation.
- The variance / covariance law (C1) and the linearized bound with split mode (C2) are not headline novelty. The recommended lead is N2 (tolerance-aware upstream placement), certified by N1 (nonlinear worst-case enclosure).
- Prototype evidence (scratch, not in `results/`; reviewer-reproduced):
  - N1 enclosure width peaks at about `2.82e-4` near `eps/lambda ≈ 0.125`.
  - N2 certified worst-case raw-gain improvement over centered placement: at least `+1.9%` / `+37.6%` / `6.86x` at `eps/lambda = 0.05 / 0.10 / 0.15`.
- The dossier's split-mode gap bound `(sum a|sin|)^2` is false for the aligned design (gap `9.894e-5` > bound `9.857e-5`). The valid bound is `(sum a xi s)^2`.

---

# 2026-09-27 — GPT-6 Pro deep verification of A7; proposal and plan upgraded to v2

- claim_supported: unchanged (no `/result-to-claim` run; all numbers below are verification or pilot evidence, not paper results)
- **Route:** Oracle MCP (local patched 0.21.3, browser, `modelStrategy: current`).
  - Model verified from the conversation record: `gpt-6-pro`.
  - Oracle's answer capture failed (it returned 8 tokens); the full 57k-character answer was recovered read-only from the conversation API.
  - Reply, Claude's check, and the sandbox code bundle are in `idea-stage/handoff/`. Trace: `.aris/traces/oracle-gpt6pro-handoff/2026-09-26_run01/`.
- **Math:** every A7 statement was returned [PROVEN] with explicit assumptions. Claude checked the key derivations (z'', zonotope template theorem, screening, converse, sec correction).
- **Corrections:**
  - robust-clearance filtering must define the family; it binds only for ε > 0.0911λ;
  - ε = 0 uses the exact SLNR, and the "2.78%" figure is instance-specific;
  - β_D > π/2 is rejected, not clipped.
- **New result (reproduced locally, 1.28 s, bit-for-bit):** a shared endpoint bank (H = 48 ≤ 2M) with safe screening gives the exact certificate optimum and a unique global robust-optimality certificate. Featured case: P = (3,2), ε = 0.05λ, 30 dB.
  - free: L = 56.559, U* = 56.583, +34.17% certified over exhaustive nominal;
  - identical endpoints: L = 55.574, U* = 55.604, +2.79%;
  - v1 swap search reached only L = 53.42 (a selection gap).
- **Not yet reproduced by Claude:** GPT-6 Pro's independent matched grid, 108/132 certified positive and 79/132 above 5%. Scheduled as R008.
- **Retired:** the earlier 359/528 and 247/528 pilot counts (incomplete protocol).

---

# 2026-09-27 — /experiment-bridge: A7 v2 experiments R001–R017 complete

- claim_supported: pending (`/result-to-claim` not yet run; the numbers below are paper-candidate results from the frozen drivers, not yet claim-gated)
- **Where:** code in `experiments/a7/`; results in `experiments/a7/results/`; report in `refine-logs/EXPERIMENT_RESULTS.md`.
- **Code review:** GPT-6 Astra (ultra), 2 rounds, 0 CRITICAL. Trace: `.aris/traces/experiment-bridge/2026-09-27_run01/`.
  - Fixed: ε = 0 now uses one arithmetic path (Γ = 0 exactly); the selection gap is undefined when the screening cap is hit.
- **M0 (8/8 PASS):** bound validity (0 violations in 120 × 4 × 100,256 evaluations); bank identity; ε = 0 exact; K sensitivity within sec²; guards; reproducibility; 50-digit featured margins (free 0.3209, endpoints 0.0466).
  - GPT-6 Pro's 132-case grid is reproduced exactly: 108/132 positive, 79/132 above 5%. This closes the "not yet reproduced" item above.
- **C1 (1,360 cases):** the pre-declared gate passes. Γ > 5% in 56.2% of endpoint cases (ε > 0, P ≠ D), threshold 20%.
  - Certified Γ > 0: 87.5% free / 82.8% endpoints; medians 11.3% / 6.9%.
  - The effect grows with SNR (leakage-limited regime) and is small at 10 dB.
  - Mechanism at the witnesses: same desired power, 21% lower worst-case leakage.
- **Negative region:** every x_P = 0 case (P directly behind D, co-aligned) is inconclusive, and every screening-cap hit is there too.
  - Cause: Theorem 1 bounds desired power and leakage separately. D.6 joint-box refinement closes 51–61% of the log-gap there within the budget, but no case flips.
  - The other 61 inconclusive cases are marginal (median Γ −0.19%).
- **C2:**
  - uniqueness certificate in 39% / 45% of cases, falling with ε;
  - median global bracket U*/L − 1 = 0.5%;
  - median survivors ≤ 0.02% of the family;
  - the swap incumbent is strictly below the exact certificate optimum in 68% of exact cases (max 25.9%);
  - M = 32 (10.5M subsets): 608 median survivors, 35 s per case.
- **Baselines:**
  - the corner-robust swap (B-CR) differs from Ŝ in 78–92% of cases; Ŝ certifiably beats it in 51–69%;
  - the P-blind FYP-style layout is certifiably beaten in 100% of x_P ≠ 0 cases.
- **C3:** leakage converse and achievability agree within 1% (Ī/F_end ≤ 1.01) on all tested geometries and ε. F_end grows about as ε². At (0,1), F_end ≈ 0.80.
- **Non-ideal channel (0.08 and 1 dB/m, cos² directivity):** the Γ > 0 rate persists (82–89%); the median gain roughly halves.
- **Monte Carlo average:** Ŝ costs about 0.4% of mean SLNR and improves the lower tail.

---

# 2026-09-28 — /result-to-claim (R020): A7 v2 claim gate

- **claim_supported: partial; confidence: high; integrity_status: unavailable** (provisional — no `/experiment-audit` run). Working claims: `CLAIMS_FROM_RESULTS.md`.
- **Reviewers:** two independent GPT-6 Astra `ultra` threads, same neutral prompt, merged conservatively; they agreed on every verdict. Traces: `.aris/traces/result-to-claim/2026-09-28_run01/`.
- **Per claim:** C1 yes; C2 yes (exact certificate optimum only when uncapped; uniqueness only when its test passes); C3 yes for the bracket and conditional feasibility; A1 baselines partial; A2 non-ideal yes, narrowly; A3 x_P = 0 partial; A4 Monte Carlo partial.
- **Independently recomputed from the CSVs** (all match the persisted summaries):
  - gate 297/528 = 56.25%;
  - Γ > 0 462/528 (free) and 437/528 (endpoints);
  - uniqueness 204/528 and 239/528;
  - median global gap 0.508% / 0.489%.
- **Definition audit:** no CRITICAL defect. The chain L ≤ W ≤ U is valid, D and P share the same witness, the family is exhaustive and matched, cap handling is correct, and F_end is a valid converse. Weakest positive margins preserved their signs at 50–60 digits.
- **Corrections to the 2026-09-27 entry above** (it stays as history):
  - "Ī/F_end ≤ 1.01" is false. The maximum is 1.0113 (free, P = (6,1), ε = 0.09λ; 2/54 rows > 1.01). Use "within 1.14%".
  - "Same-budget" B-CR is not established. Rename it "same-start shared-template swap".
  - The negative region is shown to be bound-conservative on 5 cases. It is **not** shown to be only a decoupling artifact.
  - "Unprotectable at (0,1)" holds only as I_max < p·F_end within the family.
  - "Costs about 0.4% of mean SLNR" is a median. Individual losses reach 22.9% / 15.0%.
  - Non-ideal runs use model-specific reference SNR with model-aware redesign.
  - Minor: gate 56.25%; 70.5% (not 71%) at ε = 0.05λ free; survivors "≈ 0.02%"; U* at (0,1) free = 1.11.
- **Evidence gap (R019):** 25 numbers in `EXPERIMENT_RESULTS.md` were never persisted. They include the mechanism ratios (1.000 / 0.79), the x_P ≠ 0 subgroup, the sacrifice tail (13.5% / 88.5%), the inconclusive breakdown (157 / 96 / 61), the pooled swap gap (68%) and ×70 growth. They are `evidence_not_found` until a script persists them; otherwise drop them. The per-family swap gap (77.7% / 59.1%) is already persisted and can replace the pooled figure.
- **No new broad simulation is required** for the narrowed claims. Stronger claims would need matched-budget B-CR, fixed-noise non-ideal runs, refinement of both layouts at x_P = 0, or MC seed uncertainty.
- **Open plan item (executor note):** the sector-enclosure gap is still not measured separately (four-gap reporting; GPT-6 Pro D.2). This is the `/ablation-planner` candidate.
- **Targeted novelty check (same day):** `idea-stage/NOVELTY_TARGETED_A7v2.md`.
  - The "≤ 2M templates" per-subset fact is the known rank-2 binary quadratic maximization (Karystinos–Pados 2007; Karystinos–Liavas 2010; Allemand et al. 2001; Ferrez et al. 2005). Cite it; do not claim it.
  - What is new: family-wide sharing across all subsets, templates used as common D/P feasible witnesses, and the resulting safe screening, exact certificate optimum, global bracket and uniqueness test.
  - New must-cite neighbor: Jiang–Schotten, arXiv:2609.31088 (PASS position errors, TDMA/NOMA; statistical, no selection or certificate).
  - Verdict: PROCEED with repositioning.

---

# 2026-09-28 — R019 number reconciliation (after R020)

- All 25 `evidence_not_found` numbers were real but unpersisted: `summarize_r019.py` reproduces every one from the stored CSVs (→ `results/r019_derived.{json,md}`). The ×70 growth is ×67–71; the extreme-case Γ is +44.5%.
- One more rounding error: F_end at endpoints, P = (6,1), ε = 0.01λ is 1.17e-4 (was 1.18e-4; double rounding through the 4-digit table).
- **New certified mechanism (pending jury review):** in 893/899 Γ > 0 cases, Ī(Ŝ) < I_P(S_N) at S_N's SLNR witness. This proves Ŝ's worst-case leakage is lower; the median certified ratio is 0.80. It is stronger than the descriptive witness ratios (1.000 / 0.79).
- **Weakest-margin audit at 50 digits** (independent code, residual misalignment included): smallest positive Γ 5.69686e-6 and uniqueness margins 4.74e-5 / 3.94e-5 keep their signs. The a7_core.py:135 residual-phase omission changes these by ~1e-6 relative.
- **Inclusive per-case cost** is 3.9 s (free) / 0.55 s (endpoints) median, against 0.20 / 0.12 s for the selection stage alone.
- `EXPERIMENT_RESULTS.md` revised; `r019_numbers.py` reports 237/237 quoted numbers consistent; ARIS pre-check 191/191.

---

# 2026-09-28 — R018 figures (/paper-figure)

- Four figures and two tables are in `figures/`, one script each, reading only from `experiments/a7/results/`.
  - Fig. 1 is a computed schematic, not hand-drawn. Featured case: S_N has nominal |h_P| = 3.4e-4 (deep null) but endpoint worst case ≥ 0.360; Ŝ is certified ≤ 0.308. The single-site sector is almost exact (radial width 1.5e-4 relative), so Theorem 1's conservatism comes from the Minkowski sum and the D/P decoupling, not from the per-site enclosure.
  - Fig. 4 shows x_P = 0 separately. There screening prunes almost nothing: at least 99.998% of the family survives, and the cap is hit at free M ≥ 24 and endpoints M = 32. The median over all 12 cases would hide this.
- GPT-6 Astra ultra review, round 1: 0 CRITICAL, 2 MAJOR, 12 MINOR, all fixed.
  - Recurring overclaim pattern: an absolute word ("no pruning") written from a visual impression. The same class as R020's "≤ 1%". Test every absolute statement against every data row.
- No TeX engine on this machine. LaTeX widths are estimated only (Table I fixed for padding; Table II labels shortened). Compile check deferred at the user's request.
- R018 closed after three GPT-6 Astra ultra review rounds. All six artifacts are "Ready". Round 2 caught one more self-introduced overclaim: a certificate inequality in a caption was rounded to nearest, which breaks it. Caption bounds must be rounded outward (upper bounds up, witnesses down), and the rounded values are now persisted in `figures/fig1_values.json`.

---

# 2026-09-29 — R021 ablation: certificate-gap accounting on fixed layouts (/ablation-planner)

- **Design and audit:** GPT-6 Astra (ultra), one thread for design, feasibility and result audit. Traces: `.aris/traces/ablation-planner/2026-09-29_run01/` (001–003).
- **Where:** code `experiments/a7/ablation_gaps.py`; results `experiments/a7/results/ablation_*`. Every number below is in `ablation_summary.md`, with bound endpoints rounded outward. No layout is re-selected: every row uses the stored Ŝ / S_N.
- **Validity:** all 2,720 layout-rows pass. Production L reproduces the stored values; the symmetric sector + additive pad equals the literal v1 certificate; sector ⊇ true curve ⊇ corners; witnesses are nested.
- **Certificate refinements (GPT-6 Pro D.2), primary Ŝ:**
  - pad → sec: median +0.936%, p95 +4.86%, max ≤ +11.76%;
  - symmetric → asymmetric: ≤ +0.0183%;
  - certified-positive Ŝ against the stored U(S_N): 437 → 462 (free) and 403 → 437 (endpoints) from literal v1 to production.
- **Enclosure losses are small** (both layouts, 2,112 primary rows, upper endpoints): angular ≤ 0.000476%, P-side sector ≤ 0.0797%, desired projection ≤ 0.0141%, combined ≤ 0.0934%. This closes the "sector gap not measured" item from R020.
- **Dependency (stress panel, joint refinement of both layouts, 100,351 boxes each):**
  - off-axis: W is pinned; the median dependency factor lies in [0.0359%, 0.0436%];
  - co-aligned (x_P = 0): median in [13.71%, 21.11%]; certified lower endpoints 1.82%–28.3%, which are lower bounds, not the losses;
  - 4/16 co-aligned pairs become certified dominance (all P = (0,4), ε = 0.03λ, both families, 10/40 dB; gain in [0.887%, 0.972%]). The other 12 stay inconclusive. R020's A3 statement (5 other cases, none flips) stays correct.
  - On the full grid, the remainder after the enclosure factors mixes dependency with unresolved witness slack. "Dependency dominates the full-grid gap" is **not** licensed.
- **Witness ladder:** the shared bank reaches the all-corner minimum on every fixed primary layout (|U_H/U_C − 1| ≤ 2.44e-15); refinement lowers it by up to 13%; 56 extra starts on the stress panel give no numerically resolved improvement.
- **Selection:** swap → completed GCS improves the certificate objective in 373/480 exact free and 312/528 endpoint cases. On the M = 16 slice, GCS returns the exhaustive certificate maximum and layout in 24/24 (correctness only; no speedup claim).
- **Literal v1 at ε = 0:** artificial penalty median 0.1635%, max ≤ 8.53% (544 layout-rows). Production uses the exact branch.
- **Correction to the 2026-09-28 R018 entry** ("Theorem 1's conservatism comes from the Minkowski sum and the D/P decoupling"): For independent actuator errors, Minkowski addition introduces no relaxation; the ablations bound the combined angular, sector-enclosure and desired-projection loss by 0.0934% on the primary fixed-layout grid and establish positive D/P-dependency losses on the audited co-aligned stress layouts.
- **Process lessons:**
  - A wall-clock refinement budget made the stress panel machine-dependent (co-aligned bounds moved by up to 0.6% between runs). The budget is now a box count (deterministic).
  - The first M = 16 timing compared paths with different batch sizes, so it is not a screening speedup. It was dropped.
- **Deferred (priority 2/4):** random vs geometric bank, equal-CPU B-CR, fixed-noise transfer. A1 keeps the "same-start shared-template heuristic" wording.
