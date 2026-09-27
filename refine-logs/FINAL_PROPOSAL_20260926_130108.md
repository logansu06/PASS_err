# Final Proposal: Certified Robust-SLNR Site Selection for Pinching-Antenna Systems Under Actuator Position Errors

**Status:** refined through 2 external rounds (GPT-6 Astra, `ultra`). Final verdict **REVISE, 7.70/10**. The remaining gap is evidence that must come from the planned controlled experiment (see `EXPERIMENT_PLAN.md`), not a method issue.
**Target:** IEEE ICC 2027 (Wireless Communications or Signal Processing for Communications symposium), 6 pages; deadline 2026-10-02.
**Date:** 2026-09-26

## Problem Anchor

- **Bottom-line problem.**
  - A pinching-antenna system (PASS) steers energy only through where it pinches the waveguide: no phase shifters, a single feed.
  - Interference-aware PASS designs choose sites nominally.
  - Actuators place pinches with bounded errors of a few percent of a wavelength. Because the PASS phase contains the guided-wave term $k_0 n_{\mathrm{eff}} x$, these errors break nominal interference nulls.
  - A designer needs a site selection whose **SLNR is guaranteed** for every actuator error in the tolerance box, and needs to know when robust selection is worth using.
- **Must-solve bottleneck.**
  - Nominal interference-aware selection has no worst-case guarantee.
  - PASS robustness work has mostly addressed user-location or CSI uncertainty. Pinching-position error has been studied for a single radiator's secrecy (Pakravan et al., 2604.12156) and compensated electronically with extra leaky-wave hardware (Chen et al., H-PASS, TWC 2026).
  - Generic tolerance bounds give no PASS selection guidance.
- **Non-goals.**
  - Learning-based selection (tested negative).
  - Full-duplex or multi-user systems.
  - Hardware validation.
  - Globally optimal continuous placement.
  - Coupled downstream power depletion.
- **Constraints.** 6 pages; ~5 working days; CPU-only NumPy; single executor. Analytic baseline: the graduation report plus C1 / N0 / N1.
- **Success condition.**
  1. On a declared test grid, robust selection **certifiably dominates** the *exhaustive* nominal selection within the same aligned candidate family, including the identical-endpoint control.
  2. *(Amended in round 1; accepted as narrowing in round 2.)* A candidate-dependent sufficient condition certifies when the robust choice improves; a conditional fragility lemma explains why nominal nulls degrade. No universal pre-search threshold is claimed.
  3. The bounds are valid, and their tightness is reported by median, 95th percentile, and maximum.

## Technical Gap

- Nominal interference-aware PASS activation exists (FullPASS, 2607.19546, which leaves position uncertainty to future work; Li et al., 2609.29200).
- Actuator-error enclosures and robust SINR exist for movable antennas (Yang et al., 2601.17825; Zhang et al., 2609.23323).
- Certified interval / sector tolerance bounds exist for generic arrays (Arnestad et al. 2023; Poli et al. 2015).
- **Missing:** a PASS-native, certified answer to "which pinching sites keep the protected receiver protected under actuator tolerance ε?", evaluated against the best nominal choice in a matched family.

## Method Thesis

For desired-phase-aligned pinching sites, cheap sector enclosures with exact marginal phase and amplitude ranges yield a certified worst-case SLNR. Maximizing it selects sites whose worst-case SLNR **certifiably exceeds that of the exhaustive nominal optimum in the same matched family**. In the examined cases, much of the gain comes from lower directional leakage sensitivity, traded against nominal leakage and desired gain.

## Contribution Focus

- **Dominant contribution:** the certified robust-SLNR site-selection task and framework for PASS. Components:
  - Propositions 1–2 (desired-gain lower bound; sector-support leakage upper bound with a rigorous angular-grid correction);
  - the Corollary (SLNR bracket; certified dominance; the fixed-pair noise condition);
  - a search initialized from the exhaustive nominal optimum;
  - evaluation against exhaustive nominal selection with identical endpoints.
- **Supporting:**
  - Lemma 0 (monotone guided phase; per-contribution sensitivity floor; ξ asymmetry), a compact part of the setup;
  - Lemma 3 (conditional leakage fragility), which explains why nominal nulls fail;
  - one paired mechanism analysis (directional leakage sensitivity vs nominal leakage vs desired gain).
- **Explicitly rejected complexity:**
  - learning (pilot: 0.669 of reference; warm start ≈ random);
  - A2 calibration;
  - full-duplex or multi-user systems;
  - a universal κ threshold;
  - a universal "directional spreading" story;
  - N0/N2/A8 comparators in the main text;
  - continuous global optimization.

## Proposed Method

### System and Error Model

- **Geometry.** One waveguide along $x$ at height $d = 3$ m; feed at $x_f = -10$ m; 28 GHz; $n_{\mathrm{eff}} = 1.44$.
- **Receivers.** Desired receiver D at the origin; protected receiver P at $(x_P, y_P, 0)$.
- **Candidate family (N0).** M sites on consecutive D-aligned levels, $R_D(x) + n_{\mathrm{eff}} x \in \lambda\mathbb Z + C$. Each root is unique; spacing is at least $0.682\lambda$.
- **Selection.** Choose $|S| = N$; equal power $P/N$ per site; fixed physical noise $\sigma^2$, referenced to the coherent gain of the central block (identical for every layout).
- **Channel.** $h_r(S, \delta) = \sum_{n \in S} A_r(x_n + \delta_n)\, e^{-j\psi_r(x_n + \delta_n)}$ with $\psi_r = k_0(R_r + n_{\mathrm{eff}}(x - x_f))$.
- **Errors.** $|\delta_n| \le \epsilon$. Robust clearance: spacing $\ge d_{\min} + 2\epsilon$ with $d_{\min} = 0.5\lambda$, which holds for $\epsilon \le 0.09\lambda$.
- **Objective.**
$$W(S) = \min_\delta \frac{|h_D|^2/N}{\sigma^2 + |h_P|^2/N}.$$

### Analysis

**Lemma 0 (monotone guided phase).**
- For $n_{\mathrm{eff}} > 1$: $\psi_r' = k_0(n_{\mathrm{eff}} + \sin\theta_r) \in [k_0(n_{\mathrm{eff}} - 1),\ k_0(n_{\mathrm{eff}} + 1)]$, so each site's phase image over the box is exactly the endpoint interval.
- For a positive differentiable amplitude:
$$|z'|^2 = A'^2 + A^2\psi'^2 \ge k_0^2(n_{\mathrm{eff}} - 1)^2A^2.$$
- The sensitivity $\xi_P = n_{\mathrm{eff}} + \sin\theta_P$ tends to $n_{\mathrm{eff}} + 1$ for sites downstream of P (relative to P) and to $n_{\mathrm{eff}} - 1$ for sites upstream of P.
- Qualifications:
  - the floor concerns each complex contribution, not received power or SLNR;
  - it scales with $A$;
  - the asymmetry concerns $\xi$, not the ordering of aggregate leakage.

**Proposition 1 (desired-gain lower bound).**
- Take the sector enclosures: exact marginal phase interval (Lemma 0) and exact amplitude extrema (endpoints plus closed-form stationary points).
- For D-aligned sites with $\beta_{D,n} \le \pi/2$:
$$|h_D|^2 \ge \Big(\sum_{n \in S} A^-_{D,n}\cos\beta_{D,n}\Big)^2 =: N L_D(S).$$

**Proposition 2 (sector-support leakage upper bound).**
- Using the closed-form support function $s_n(\theta)$ of each annular sector:
$$|h_P| \le \max_\theta\sum_n s_n(\theta) \le \max_{\Theta_K}\sum_n s_n(\theta) + \frac{\Delta\theta}{2}\sum_n A^+_{P,n}.$$
- This is a rigorous angular-grid correction (each $s_n$ is $A^+_n$-Lipschitz). Special case: for $\epsilon = 0$, use the exact SLNR with no pad.

**Corollary (bracket, dominance, noise condition).**
- $L(S) = L_D/(\sigma^2 + \bar I) \le W(S) \le U(S)$, where $U$ is a feasible witness evaluated exactly.
- $L(S_R) > U(S_N)$ certifies $W(S_R) > W(S_N)$.
- For a fixed pair and witness, with $a = L_D(S_R)$, $b = \bar I(S_R)$, $c = G_D(S_N, \hat\delta)$, $d = I_P(S_N, \hat\delta)$, this test holds iff $(a - c)\sigma^2 > cb - ad$. The condition is sufficient, not necessary, for true improvement. In SNR sweeps the selections and witnesses are recomputed at every point.
- Finite-family verification: $\max_{\mathcal F} L \le \max_{\mathcal F} W \le \max_{\mathcal F} U$. Exhaustive maximization of $L$ gives the **certificate optimum**.

**Lemma 3 (conditional leakage fragility).**
- Exact derivative:
$$b_n = e^{-j\psi_n}\big[-t_n/R_n^2 - jk_0(n_{\mathrm{eff}} + t_n)/R_n\big].$$
- With $\nu_0 = |h_0|^2/(N\sigma^2)$, $\kappa_b = \epsilon^2\sum|b_n|^2/(N\sigma^2)$, and $\bar\rho = \rho/\sqrt{N\sigma^2}$:
$$\max_\delta \frac{|h_P|^2}{N\sigma^2} \ge \big[\sqrt{\nu_0 + \kappa_b} - \bar\rho\big]_+^2.$$
- The bound is informative only when $\rho \ll \epsilon\sqrt{\sum|b_n|^2}$; it is vacuous in some large-$\epsilon$ cases. $\kappa_b$ is a diagnostic, not a predictor.

**Mechanism statement (safe form).** Directional leakage sensitivity — the first-order response $\max_\theta[\Re(e^{-j\theta}h_0) + \epsilon\sum_n|\Re(e^{-j\theta}b_n)|]$, with directions taken modulo $\pi$ — explains substantial gains in the examined cases, while the certificate also trades nominal leakage and desired gain. It is **not** universal: $T$ increased in 5 of 357 positive-gain comparisons.

### Algorithm

1. Precompute per-site tables: $c_n$, $s_n(\Theta_K)$ with $K = 1440$, and $A^+_{P,n}$. Cost $O(MK)$.
2. Exhaustive nominal optimum $S_N$ over all $\binom{M}{N}$ subsets (optionally with fixed endpoints); about 0.5 s at 24/8.
3. Swap local search on $L(S)$ started from $S_N$ plus 8 random starts, which guarantees $L(S_R) \ge L(S_N)$. Output $S_R$ (best-found).
4. Witnesses $U(\cdot)$: all $2^N$ corners, the split pattern, and L-BFGS-B refinement from the 3 worst corners; log the witness vectors.
5. Report certified dominance and the components.

Implementation: `idea-stage/pilots/a7_main.py` (frozen driver, **not yet run**), `a7_pilot.py` (helpers; `run_case` deprecated), `pass_lab.py`.

### Failure Modes and Diagnostics

- **Co-aligned receivers make the brackets conservative.** On the archived pilot, $U/L$ has median 1.021, 95th percentile 1.183, and maximum 1.729.
- **At large ε the Lemma-3 remainder becomes vacuous;** Proposition 1 validity also requires $\beta_D \le \pi/2$.
- **Negative certified comparisons are inconclusive, not failures,** and will be reported.
- **Model limits:** equal power split and isotropic radiation. One attenuation + directivity check is planned; coupled depletion is out of scope.

### Novelty and Elegance Argument

> We select multiple desired-phase-aligned pinching sites under independent bounded actuator errors, using nonlinear certificates to establish worst-case SLNR improvement over exhaustive nominal selection within a matched feasible family.

- **Credited as tools, not claimed:** sector/interval enclosures (Arnestad; Poli); nonlinear enclosures and all-error SINR (Zhang); interference-aware PASS activation (FullPASS); null fragility (Yang).
- **Elegance:** separable per-site certificates give an $O(NK)$ subset evaluation, and a single dominance test turns bounds into a design decision. There are no trainable parts.

## Claim-Driven Validation (summary; full plan in EXPERIMENT_PLAN.md)

- **C1 (primary):** certified dominance over exhaustive nominal selection in the matched family, identical-endpoint control included, with negative cases and desired/leakage components.
- **C2 (supporting):** why and when — the conditional fragility diagnostic, one paired mechanism analysis, the fixed-pair noise regime, and bracket tightness.

## Evidence So Far (pilot, not paper-final)

- Archived κ sweep (`a7_kappa.py`, `a7_kappa_results.csv`, 528 cases; local nominal comparator). **These pilot numbers must not be reused in the paper;** the paper uses `a7_main.py` outputs only.
- A reviewer-generated rerun against exhaustive nominal selection gives 359/528 certified positive and 247/528 above 5%.
- A reviewer rerun with identical endpoints (33 geometries × 4 settings) gives 16–22/33 above 5% (median 4–12%).
