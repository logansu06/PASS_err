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
