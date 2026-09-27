# Research Proposal: Certified Robust-SLNR Site Selection for Pinching-Antenna Systems Under Actuator Position Errors

## Problem Anchor

- **Bottom-line problem.**
  - A pinching-antenna system (PASS) steers energy *only* through where it pinches the waveguide: no phase shifters, a single feed.
  - Interference-aware PASS designs (e.g., FullPASS-style activation with leakage constraints) choose sites *nominally*.
  - Real actuators place pinches with bounded errors of a few percent of a wavelength. Because the PASS phase contains the guided-wave term $k_0 n_{\mathrm{eff}} x$, these errors break the nominal interference null.
  - A designer needs a site selection whose **signal-to-leakage-plus-noise ratio (SLNR) is guaranteed** for every actuator error in the tolerance box, and needs to know **when** such robust selection is worth using.
- **Must-solve bottleneck.**
  - Nominal interference-aware selection has no worst-case guarantee, and its SLNR collapses under sub-wavelength actuator errors.
  - Existing PASS robustness work treats user-location or CSI uncertainty, not actuator errors.
  - Existing generic tolerance bounds (interval arithmetic, MA enclosures) give no PASS-specific rule for when robustness matters.
- **Non-goals.**
  - Learning-based selection (tested; not needed).
  - Full-duplex or multi-user systems.
  - Hardware validation.
  - Globally optimal continuous placement.
  - Coupled downstream power depletion.
- **Constraints.** IEEE ICC 2027; 6 pages; 5 working days; CPU-only NumPy; single executor. The graduation report and its C1 / N0 / N1 / N2 results form the analytic baseline.
- **Success condition.**
  1. On a declared test grid, robust selection **certifiably dominates** the *exhaustive* nominal selection within the same aligned candidate family, including a fixed-aperture (identical-endpoint) control.
  2. A closed-form, PASS-specific quantity predicts **when** robust selection helps.
  3. The bounds are valid, and their tightness is reported honestly (median, quantiles, worst case).

## Technical Gap

- **Nominal PASS interference suppression** (FullPASS 2607.19546; Li et al. 2609.29200) optimizes activation with leakage constraints but assumes exact positions. FullPASS explicitly leaves position uncertainty to future work.
- **Actuator-error analyses exist only for free-space movable antennas:**
  - Yang et al. 2601.17825: Taylor worst-case nulling;
  - Zhang et al. 2609.23323: nonlinear enclosures and robust SINR for MA-ISAC.
  Neither covers the guided-wave phase law, and both use generic flexible-array geometry.
- **Interval-arithmetic tolerance analysis** (Arnestad 2023; Poli 2015; Anselmi 2013) certifies generic array patterns. It says nothing about PASS site selection or when robustness pays.
- **What is missing:** a PASS-native answer to "which pinching sites should I activate so that the protected receiver stays protected under actuator tolerance ε, and when does it matter?"

## Method Thesis

The guided-wave term makes PASS leakage sensitivity $\xi_{P,n} = n_{\mathrm{eff}} + \sin\theta_{P,n}$ large and nearly receiver-independent. Nominal nulls are therefore fragile at a level set by the fragility-to-noise ratio
$$\kappa = \frac{\epsilon^2 k_0^2 \sum_n \xi_{P,n}^2 / R_{P,n}^2}{N\sigma^2}.$$
Separable nonlinear certificates for the desired gain and the leakage let us select phase-aligned pinching sites whose worst-case SLNR is **certified** higher than that of the nominally optimal selection, precisely in the $\kappa \gtrsim 1$ regime.

## Contribution Focus

- **Dominant contribution:** a certified robust-SLNR site-selection framework for PASS. It has three parts:
  - a per-site nonlinear enclosure;
  - a desired-gain lower bound and a sector-support leakage upper bound;
  - a certified-dominance test.
  
  Together with a PASS-specific **fragility law** ($\kappa$), it states when robust selection is needed and why the guided-wave term causes it.
- **Supporting:** the graduation-report sensitivity theory (C1: $\xi = n_{\mathrm{eff}} + \sin\theta$) reappears as the leakage-sensitivity law. The N0 aligned construction supplies the candidate family, and N1 supplies the desired-gain ingredient.
- **Explicitly rejected complexity:**
  - learning — pilot negative: 0.669 of the reference; warm start equal to a random start;
  - calibration loops (A2);
  - full-duplex or multi-user extensions;
  - a separate upstream-placement theorem (A8 stays a comparator);
  - continuous-position global optimization.

## Proposed Method

### Complexity Budget

- **Frozen:** the PASS channel model (Ouyang et al.) and the N0 aligned candidate family.
- **New:** two certificates (analytic), one fragility proposition, and one search routine (multistart swaps).
- **No trainable components.**

### System Overview

- **Geometry:** one waveguide along $x$ at height $d$, feed at $x_f$; desired receiver D at $(0, 0, 0)$; protected receiver P at $(x_P, y_P, 0)$.
- **Candidate sites:** M sites $\{x_m\}$ on consecutive D-aligned levels, $R_D(x_m) + n_{\mathrm{eff}} x_m \in \lambda\mathbb Z + C$ (N0; each root is unique because $\psi' > 0$).
- **Selection:** choose $S$ with $|S| = N$. Total power is $P$, split equally ($P/N$ per site).
- **Channels:** $h_r(S, \delta) = \sum_{n \in S} A_r(x_n + \delta_n)\, e^{-j\psi_r(x_n + \delta_n)}$ with $A_r = 1/R_r$ (optionally $e^{-\alpha(x - x_f)}$ and $\cos^q$ directivity) and $\psi_r = k_0(R_r + n_{\mathrm{eff}}(x - x_f))$.
- **Error model:** actuator errors $|\delta_n| \le \epsilon$. Robust clearance requires site spacing of at least $d_{\min} + 2\epsilon$.
- **Robust SLNR:**
$$W(S) = \min_{\delta} \frac{|h_D(S,\delta)|^2 / N}{\sigma^2 + |h_P(S,\delta)|^2 / N}.$$

### Core Mechanism

**Proposition 1 (per-site enclosure; desired-gain lower bound).**
- Since $\psi_r' = k_0(n_{\mathrm{eff}} + \sin\theta_r) > 0$ for $n_{\mathrm{eff}} > 1$, the feasible phase of site $n$ lies in $[\psi_r(x_n - \epsilon), \psi_r(x_n + \epsilon)]$, and its amplitude lies in $[A_r^-, A_r^+]$ (exact extrema: endpoints plus closed-form stationary points).
- For D-aligned sites with $\beta_{D,n} := \max(\text{endpoint excursions}) \le \pi/2$:
$$|h_D(S, \delta)|^2 \ge \Big(\sum_{n \in S} A_{D,n}^- \cos\beta_{D,n}\Big)^2 =: N L_D(S).$$

**Proposition 2 (sector-support leakage upper bound).**
- Let $s_n(\theta)$ be the support function of the annular sector $\{A e^{j\phi} : A \in [A^-_{P,n}, A^+_{P,n}],\ \phi \in [\phi_n - \beta_{P,n}, \phi_n + \beta_{P,n}]\}$, which has a closed form. Then
$$|h_P(S, \delta)| \le \max_\theta \sum_{n \in S} s_n(\theta) \le \max_{\theta \in \Theta_K} \sum_{n \in S} s_n(\theta) + \frac{\Delta\theta}{2}\sum_{n \in S} A^+_{P,n}.$$
- The last term is the grid correction; each $s_n$ is $A_n^+$-Lipschitz. Call the resulting bound $\sqrt{N \bar I(S)}$.
- **Wording:** this is the exact support of the *enclosing sector*, not of the curve-shaped true uncertainty set.

**Corollary (SLNR bracket and certified dominance).**
- $L(S) := L_D(S) / (\sigma^2 + \bar I(S)) \le W(S) \le U(S)$, where $U(S)$ is the minimum SLNR over feasible adversaries evaluated exactly (split pattern for D, leakage-aligned sign patterns, all corners when $N \le 12$, continuous refinement).
- Hence $L(S_{\rm rob}) > U(S_{\rm nom})$ **certifies** $W(S_{\rm rob}) > W(S_{\rm nom})$.
- Finite-family verification: $\max_{\mathcal F} L \le \max_{\mathcal F} W \le \max_{\mathcal F} U$.

**Proposition 3 (guided-wave fragility law).**
- Write $h_P(S, \delta) = h_0 + \sum_n b_n\delta_n + r(\delta)$ with $|r| \le \rho(\epsilon) = \tfrac12\sum_n \epsilon^2 \sup|h''_{P,n}|$.
- Averaging over random-sign corners gives $\max_\delta |h_P|^2 \ge \big[\sqrt{|h_0|^2 + \epsilon^2\sum_n|b_n|^2} - \rho\big]_+^2$.
- Moreover $b_n = -j k_0 \xi_{P,n} A_{P,n} e^{-j\psi_{P,n}}\,(1 + O((k_0 R_{P,n})^{-1}))$ with $\xi_{P,n} = n_{\mathrm{eff}} + \sin\theta_{P,n} \in [n_{\mathrm{eff}} - 1, n_{\mathrm{eff}} + 1]$.
- Consequently, **any** selection's worst-case leakage-to-noise ratio is at least about $\kappa(S) = \epsilon^2 k_0^2 \sum_{n \in S}\xi_{P,n}^2 A_{P,n}^2 / (N\sigma^2)$, whatever its nominal null depth.
- **Consequences:**
  - (i) For $\kappa \ll 1$, the nominal and robust selections coincide in value; robustness is unnecessary.
  - (ii) For $\kappa \gtrsim 1$, a nominal null gives no protection. The robust choice trades a shallower nominal null for smaller $\sum|b_n|$: sites with small $\xi_{P,n}/R_{P,n}$, i.e., far from P or on the feed side of P, where the guided and free-space phase changes partly cancel.
  - (iii) The $n_{\mathrm{eff}}^2$ scaling makes PASS nulls intrinsically more fragile than those of free-space arrays with the same geometry, whose along-axis sensitivity is $\sin\theta \in (-1, 1)$.

### Algorithm

- **Precompute per-site tables:**
  - $c_n = A^-_{D,n}\cos\beta_{D,n}$;
  - the vectors $s_n(\Theta_K)$;
  - $A^+_{P,n}$.
  
  Cost: $O(MK)$, with $K = 1440$.
- **Evaluating a subset:** $O(NK)$.
- **Search:** multistart swap local search (8 restarts) on $L(S)$; a fixed-endpoint variant for matched aperture.
- **Status:** best-found, reported against exhaustive search on small instances ($M = 12$, $N = 4$) and against exhaustive *nominal* selection at $M = 24$, $N = 8$.

### Failure Modes and Diagnostics

- **Co-aligned receivers.** When D and P respond similarly, the desired/leakage separation is conservative ($U/L$ up to 1.22 observed). Report bracket quantiles and flag such geometries.
- **Validity.** $\beta_{D,n} \le \pi/2$ limits $\epsilon$ (about $0.17\lambda$ here).
- **Regime.** For $\kappa \ll 1$, no benefit is expected (a declared negative control).
- **Scope.** Equal power split and isotropic radiation. Attenuation and directivity sensitivity are tested; coupled depletion is out of scope.

### Novelty and Elegance Argument

- **Genuinely new here:**
  - the PASS robust-SLNR selection task under actuator boxes;
  - the certified-dominance evaluation against exhaustive nominal selection;
  - the guided-wave fragility law ($\kappa$ with $\xi_{P,n} = n_{\mathrm{eff}} + \sin\theta$) explaining when and why.
- **Not claimed as new:** sector/interval enclosures, nonlinear phase enclosures, or swap search in general.
- **Elegance:** two separable certificates plus one proposition give both the algorithm (fast tables) and the design rule (κ). There are no trainable parts.

## Claim-Driven Validation Sketch

### Claim 1 (main): certified dominance within the aligned family

- **Test:**
  - $M = 24$, $N = 8$;
  - 33 declared geometries × $\epsilon/\lambda \in \{0, 0.01, 0.03, 0.05, 0.08\}$ × reference SNR {10, 20, 30, 40} dB;
  - robust selection vs **exhaustive** nominal selection;
  - common-region and identical-endpoint controls;
  - corner enumeration and continuous refinement for $U$.
- **Report:**
  - the fraction of the grid with $L(S_{\rm rob}) > U(S_{\rm nom})$ and with more than 5% gain;
  - desired power and leakage separately;
  - bracket quantiles.
- **Anchor check:** small instances with an exhaustive certified optimum.

### Claim 2 (supporting): the fragility law predicts when robust selection helps

- **Test:** certified gain vs $\log_{10}\kappa$ across all grid points, plus an $n_{\mathrm{eff}}$ sweep (1.2, 1.44, 1.75) at fixed geometry.
- **Pilot:** monotone medians of 0, +1.4%, +3.1%, +5.7%, +10.2%, +11.4% across the κ bins [<−2], [−2,−1), [−1,0), [0,1), [1,2), [≥2] (528 cases; `idea-stage/pilots/a7_kappa.py`, `a7_kappa_results.csv`).

## Experiment Handoff Inputs

- **Code:** `idea-stage/pilots/pass_lab.py`, `a7_pilot.py`, `a7_kappa.py`.
- **Required fixes:**
  - endpoint-constrained local search;
  - exhaustive nominal selection;
  - a saved per-case driver;
  - θ-grid refinement and zero-error checks.
- **Comparators:**
  - exhaustive nominal SLNR;
  - greedy + swap;
  - sampled-error robust selection;
  - N0 centered block (N consecutive sites);
  - N2 / A8 desired-gain-oriented tolerance-aware block.

## Compute & Timeline Estimate

- Every experiment runs on CPU in minutes.
- Exhaustive nominal selection at 24/8 takes 735k subsets per case in batches, a few seconds each.
- **Schedule:**
  - Day 1: fixes and the driver;
  - Day 2: Claim 1;
  - Day 3: Claim 2 and sensitivity;
  - Day 4: figures and proofs;
  - Day 5: writing and audit.
