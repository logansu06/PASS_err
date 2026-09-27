# Round 1 Refinement

## Problem Anchor (verbatim from round 0, success condition 2 amended; see Anchor Check)

- **Bottom-line problem.**
  - A pinching-antenna system (PASS) steers energy *only* through where it pinches the waveguide: no phase shifters, a single feed.
  - Interference-aware PASS designs (e.g., FullPASS-style activation with leakage constraints) choose sites *nominally*.
  - Real actuators place pinches with bounded errors of a few percent of a wavelength. Because the PASS phase contains the guided-wave term $k_0 n_{\mathrm{eff}} x$, these errors break the nominal interference null.
  - A designer needs a site selection whose **signal-to-leakage-plus-noise ratio (SLNR) is guaranteed** for every actuator error in the tolerance box, and needs to know **when** such robust selection is worth using.
- **Must-solve bottleneck.** Nominal interference-aware selection has no worst-case guarantee, and its SLNR collapses under sub-wavelength actuator errors.
  - PASS robustness work has focused on user-location or CSI uncertainty. Pinching-position error has so far been treated only for a single radiator's secrecy (Pakravan et al.) and by electronic compensation with extra hardware (Chen et al., H-PASS).
  - Generic tolerance bounds give no PASS-specific selection guidance.
- **Non-goals.**
  - Learning-based selection.
  - Full-duplex or multi-user systems.
  - Hardware validation.
  - Globally optimal continuous placement.
  - Coupled downstream power depletion.
- **Constraints.** IEEE ICC 2027; 6 pages; 5 working days; CPU-only NumPy; single executor.
- **Success condition.**
  1. On a declared test grid, robust selection **certifiably dominates** the *exhaustive* nominal selection within the same aligned candidate family, including a fixed-aperture (identical-endpoint) control.
  2. *(Amended)* A rigorous, candidate-dependent condition certifies *when* the robust choice improves on the nominal one. A PASS-specific fragility lemma explains *why* nominal nulls degrade, and the observed mechanism is characterized. **No universal pre-search threshold is claimed.**
  3. The bounds are valid, and their tightness is reported honestly (median, quantiles, worst case).

## Anchor Check

- The task, the bottleneck, and the non-goals are unchanged.
- Success condition 2 is **weakened**, from "a closed-form κ predicts when robust selection helps" to "a candidate-dependent sufficient condition plus a fragility diagnostic." The round-1 review showed that κ is neither necessary nor sufficient:
  - there is a counterexample with $\kappa \approx 5\times10^{-6}$ and +2.3% certified gain;
  - 72/528 cases have a vacuous remainder.
- This is recorded as an acknowledged, evidence-driven narrowing, not as silent drift.

## Simplicity Check

- **Removed from the main paper:**
  - the κ threshold claim;
  - the "robust selection reduces $\sum|b_n|$" explanation;
  - the universal PASS-vs-free-space fragility claim;
  - the N0 / N2 / A8 comparators.
- **No new modules.** The new material (Lemma 0 and the directional radius) reuses quantities already computed.
- **Still one dominant contribution:** certificates plus the certified-dominance test within a matched feasible family.

## Changes Made

### 1. Proposition 3 → Lemma 3 (conditional fragility), plus directional mechanism

- Exact derivative:
$$b_n = e^{-j\psi_n}\Big[-\tfrac{t_n}{R_n^2} - jk_0\tfrac{n_{\mathrm{eff}} + t_n}{R_n}\Big], \qquad t_n = \sin\theta_{P,n}.$$
- Safe statement:
$$\max_\delta \frac{|h_P|^2}{N\sigma^2} \ge \big[\sqrt{\nu_0 + \kappa_b} - \bar\rho\big]_+^2.$$
- The mechanism is explained by the **directional first-order box radius**
$$T(S) = \epsilon\max_\theta\sum_n|\Re(e^{-j\theta}b_n)| \in \Big[\epsilon\sqrt{\textstyle\sum|b_n|^2},\ \epsilon\sum|b_n|\Big].$$
- Robust selection lowers $T(S)$ by spreading the derivative-phasor directions: $T^2$ fell 53% in the strongest case, while $\sum|b_n|$ rose 0.5%.

### 2. New Lemma 0 (PASS structural lemma; replaces the false free-space comparison)

- For $n_{\mathrm{eff}} > 1$, every site's phase map $x \mapsto \psi_r(x)$ is strictly increasing, with slope
$$\psi_r' = k_0(n_{\mathrm{eff}} + \sin\theta_r) \in [k_0(n_{\mathrm{eff}} - 1),\ k_0(n_{\mathrm{eff}} + 1)].$$
- Consequences:
  - (a) The feasible phase set of each site is exactly the endpoint interval. This is why Propositions 1–2 need only endpoint evaluations and closed-form amplitude extrema.
  - (b) There is a **positive sensitivity floor**: no PASS site's contribution is first-order invariant to actuator error, $|b_n| \ge k_0(n_{\mathrm{eff}} - 1)A_n$.
  - (c) The sensitivity is geometry-asymmetric. Sites downstream of the protected receiver (away from the feed) have $\xi_{P} \to n_{\mathrm{eff}} + 1$; sites upstream have $\xi_P \to n_{\mathrm{eff}} - 1$.
- Scope: a free-space array has along-axis sensitivity $|\sin\theta|$, which vanishes near broadside. The claim is restricted to "PASS has no insensitive sites and has broadside enhancement"; there is no universal "more fragile" statement.

### 3. Candidate-dependent certified-improvement condition (replaces κ as the "when")

Fix a robust subset $S_R$ and a nominal subset $S_N$ with a feasible witness $\hat\delta$. Define:
- $a = L_D(S_R)$ and $b = \bar I(S_R)$ (certified desired gain and leakage of the robust subset);
- $c = G_D(S_N, \hat\delta)$ and $d = I_P(S_N, \hat\delta)$ (exact desired gain and leakage of the nominal subset at the witness).

Then certified improvement holds iff
$$\frac{a}{\sigma^2 + b} > \frac{c}{\sigma^2 + d} \iff (a - c)\sigma^2 > cb - ad.$$
This yields the noise regime of certified benefit for each comparison. In the main figure it is shown against SNR, together with the fragility diagnostic $\kappa_b$ as an explanatory, not predictive, variable.

### 4. Evaluation repairs

- A frozen driver (`a7_main.py`, to be written) saves per-case inputs, subsets, $L$, $U$, witnesses, desired/leakage components, $T(S)$, and $\kappa_b$.
- Exhaustive nominal selection (done: 735,471 subsets in about 0.5 s).
- Endpoint-constrained robust search (done), **initialized with the exhaustive nominal subset** plus 8 random restarts.
- Clearance $d_{\min} + 2\epsilon$ enforced; the aligned-site spacing of about $0.687\lambda$ satisfies it for $\epsilon \le 0.09\lambda$ with $d_{\min} = 0.5\lambda$.
- $\epsilon = 0$ special-cased: no angular pad, exact nominal SLNR.
- Brackets reported by median, 95th percentile, and maximum.
- A small-instance exhaustive certificate optimum (12/4).
- One non-ideal check: 0.08 dB/m attenuation plus $\cos^2$ directivity.

### 5. Novelty statement narrowed

> We select multiple desired-phase-aligned pinching sites under independent bounded actuator errors, using nonlinear certificates to establish worst-case SLNR improvement over exhaustive nominal selection within a matched feasible family.

Related work adds Pakravan et al. and Chen et al. (H-PASS). Sector/interval bounds (Arnestad; Poli) and nonlinear enclosures (Zhang) are credited as tools.

## Revised Proposal

### Title
Certified Robust-SLNR Site Selection for Pinching-Antenna Systems Under Actuator Position Errors

### Method Thesis
Because the guided-wave term makes every PASS site's phase strictly monotone and never insensitive to actuator error (Lemma 0), cheap exact per-site enclosures yield a certified worst-case SLNR. Selecting sites to maximize it certifiably beats the best nominal selection in the same matched family, by making the leakage-derivative phasors directionally spread rather than by chasing deep nominal nulls.

### Contribution Focus
- **Dominant:** the certified robust-SLNR selection task and framework for PASS. Components:
  - Lemma 0 (monotone guided phase; sensitivity floor);
  - Proposition 1 (desired-gain lower bound);
  - Proposition 2 (sector-support leakage upper bound with exact angular-grid correction);
  - Corollary (SLNR bracket; certified dominance; candidate-dependent noise condition);
  - search initialized from the exhaustive nominal optimum.
- **Supporting:** Lemma 3 (conditional leakage fragility) plus the directional-radius mechanism $T(S)$, explaining why nominal nulls fail and what robust selection changes.
- **Rejected:** learning, calibration, full-duplex or multi-user systems, the κ threshold, and the N0/N2/A8 comparators in the main text.

### System, Error Model, and Objective
Unchanged from round 0.

### Algorithm

1. Precompute per-site tables ($c_n$; $s_n(\Theta_K)$; $A^+_{P,n}$).
2. Compute the exhaustive nominal optimum $S_N$ (optionally with fixed endpoints).
3. Run swap search on $L(S)$, starting from $S_N$ plus 8 random starts, and return the best subset $S_R$.
4. Compute the feasible witnesses $U(S_N)$ and $U(S_R)$ (all corners if $N \le 12$, plus continuous refinement).
5. Report certified dominance and the noise condition.

Cost: $O(MK)$ precomputation, $O(NK)$ per subset evaluation, and about 0.5 s for exhaustive nominal selection at 24/8.

### Claim-Driven Validation

- **Claim 1 (main): certified dominance within the matched family.**
  - Grid: 33 declared geometries × $\epsilon/\lambda \in \{0, 0.01, 0.03, 0.05, 0.08\}$ × reference SNR {10, 20, 30, 40} dB.
  - Comparator: exhaustive nominal selection.
  - Controls: common region vs identical endpoints.
  - Metrics:
    - fraction of cases with $L(S_R) > U(S_N)$;
    - fraction above 5%;
    - desired power and leakage separately;
    - bracket quantiles.
  - Anchor: at 12/4, compare the exhaustive certificate optimum with the search result.
- **Claim 2 (supporting): mechanism and fragility.**
  - $T(S_R)$ vs $T(S_N)$ and nominal leakage vs worst-case leakage.
  - The certified-gain region against SNR (the noise condition).
  - $\kappa_b$ as a diagnostic, with the positive and negative cases discussed.
  - The Lemma 0 asymmetry: fragility vs $x_P$ on the feed side and the far side.
- **Sensitivity:** one non-ideal channel check (attenuation + directivity).

### Failure Modes
Co-aligned receivers make the desired/leakage separation conservative (95th-percentile $U/L$ = 1.18; max 1.73). Remainder-vacuous regimes appear at large $\epsilon$. Validity requires $\beta_D \le \pi/2$.
