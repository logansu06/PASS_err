# Final Proposal: Certified Robust Site Selection for Pinching-Antenna Systems — Global Screening Under Position Errors

**Status:**
- **v2** (2026-09-27): upgraded with the GPT-6 Pro deep-verification review (`idea-stage/handoff/GPT6_PRO_REPLY.md`). Claude checked it (`idea-stage/handoff/GPT6_PRO_VERIFICATION.md`) and reproduced the global audit locally.
- **v1** (2026-09-26): refine rounds 1–2 with GPT-6 Astra `ultra` (REVISE, 7.70/10). Kept as `FINAL_PROPOSAL_20260926_130108.md`.

**Target:** IEEE ICC 2027 (Wireless Communications or Signal Processing for Communications symposium); 6 pages including references; deadline 2026-10-02.

**Estimated acceptance** (subjective, not calibrated):
- about 40–50% for v1 as it stood;
- about 60–70% for v2 once the matched-family evidence, the robust baseline, and the numerical audit are done (GPT-6 Pro).

## Problem Anchor (unchanged in substance)

- **Bottom-line problem.**
  - A pinching-antenna system (PASS) steers energy only through where it pinches the waveguide; there are no phase shifters.
  - Interference-aware PASS site selection is designed nominally.
  - Actuators place pinches with bounded **position** errors of a few percent of a wavelength. Through the guided-wave phase, these errors break nominal nulls toward a protected receiver.
  - A designer needs a selection whose SLNR is **guaranteed** for every actuator error in the tolerance box, and needs to know how far any selection in the design family can be from the best robust one.
- **Must-solve bottleneck.** Nominal selection has no worst-case guarantee.
  - PASS robustness work mostly addresses user-location or CSI uncertainty.
  - Pinching-position error has been treated for a single radiator's secrecy (Pakravan et al.) and compensated with extra hardware (Chen et al., H-PASS).
  - Generic interval/sector bounds (Arnestad et al.) give no family-level PASS selection guarantee.
- **Non-goals.**
  - Learning-based selection (tested negative; GPT-6 Pro concurs that it is not needed).
  - Activation errors (missed or stuck sites).
  - Full-duplex, multi-user, or secrecy as the main line.
  - Hardware validation.
  - Unrestricted continuous-position optimality.
  - Coupled downstream power depletion.
- **Constraints.** 6 pages; about 5 working days; CPU-only NumPy/SciPy; single author.
- **Success condition.**
  1. On a declared grid, the certified-optimal robust selection **certifiably dominates** the exhaustive nominal optimum within the same **robust-clearance, D-aligned family**, including identical endpoints. Negative and inconclusive cases, and the nominal sacrifice, are reported.
  2. For the whole family, the method yields a **global robust bracket** $L(\hat S) \le W^\star \le U^\star$ and, whenever the rival-dominance test passes, a **unique global robust-optimality certificate**.
  3. A leakage **converse/achievability** bracket states which protection levels no family member can guarantee.
  4. The bounds are valid. Their gaps are reported per source: angular, sector, D/P dependency, selection.

## Technical Gap

- **Nominal interference-aware PASS activation:** FullPASS (2607.19546) leaves position uncertainty to future work; Li et al. (2609.29200).
- **Actuator-error enclosures for movable antennas:** Yang et al. (2601.17825); Zhang et al. (2609.23323).
- **Interval / Minkowski tolerance geometry for arrays:** Arnestad et al. (JASA 2023); Poli et al. (TAP 2015).
- **Missing:** turning exact nonlinear PASS evaluations into **family-wide** adversarial witnesses. That would give safe screening, exact certificate optimization, and verifiable global robust-optimality statements for PASS site selection.

## Method Thesis

Within a robust-clearance, finite, D-aligned PASS family:
- nonlinear field enclosures give a per-layout certified SLNR lower bound;
- a bank of at most $2M$ shared **exact endpoint witnesses** gives feasible upper bounds for **every** layout;
- together they yield computable robust brackets, safe global screening, and verifiable layout-optimality certificates — so the chosen robust layout provably beats the exhaustive nominal optimum, and often provably beats every other layout in the family.

## Contribution Focus

- **Contribution 1 — Nonlinear robust certification (Theorem 1).**
  - The SLNR lower bound follows the PASS guided phase, independent actuator boxes, and the equal-power model.
  - It uses **asymmetric phase sectors** (centered on the true endpoint interval) and a **multiplicative $\sec(\pi/K)$ angular correction**. The power inflation is at most $4.76\times10^{-6}$ at $K = 1440$.
- **Contribution 2 — Global witness screening (Theorem 2 + Corollary 1).**
  - At most $2M$ shared endpoint sign templates exactly cover the endpoint-leakage maximum of every subset.
  - The resulting feasible-witness upper bounds support safe pruning and exact maximization of the certificate over the family.
  - They also give the global bracket $L(\hat S) \le W^\star \le U^\star$ and the **unique global robust-optimality test** $L(\hat S) > \max_{S \ne \hat S} U_H(S)$.
- **Contribution 3 — Protection limits (Corollary 2).**
  - An exact endpoint converse $F_{\rm end} \le \min_S \max_\delta I_P \le \bar I(\hat S)$.
  - An interference-temperature feasibility corollary: which leakage ceilings no layout can guarantee under tolerance ε.
- **Experimental contribution.** Matched-endpoint comparison against the **exhaustive** nominal optimum and a same-budget corner-robust heuristic, with nominal sacrifice, certification gaps, screening efficiency, and CPU cost.
- **Explicitly rejected complexity:**
  - learning;
  - A2 calibration;
  - secrecy as the main line;
  - the universal κ threshold;
  - the universal "directional spreading" story;
  - the full Taylor-remainder Lemma 3 (superseded by the exact endpoint converse);
  - N2/A8 upstream-placement optimization;
  - a Dinkelbach / per-angle-sorting "exact solver" (invalid min–max interchange);
  - validated interval arithmetic (out of time; wording adjusted instead).

## Role of the Graduation Report (baseline)

- **N0 (corrected aligned construction)** defines the D-aligned candidate family. It is a system-construction step, not a claimed contribution.
- **C1 sensitivity** is compressed to one or two sentences explaining why nominal nulls are sensitive to differential phase errors. Lemma 1 keeps the guided-phase monotonicity and sensitivity floor.
- **N1** is the desired-gain ingredient of Theorem 1.
- **Graduation-report-style design** (desired-only aligned centered block, blind to P, corrected physics) is one baseline in the experiments.
- **N2 upstream placement** is not in the main line. At most, one attenuation control shows that the effect is not mere upstream shifting.

## System and Error Model

- **Geometry:**
  - waveguide along $x$ at height $d = 3$ m; feed at $x_f = -10$ m;
  - $f_c = 28$ GHz ($\lambda = 10.714$ mm, $k_0 = 586.43$ rad/m); $n_{\mathrm{eff}} = 1.44$.
- **Receivers:** desired D at $(0, 0, 0)$; protected P at $(x_P, y_P, 0)$.
- **Channel:**
  - $R_r(x) = \sqrt{(x - x_r)^2 + y_r^2 + d^2}$;
  - $\psi_r(x) = k_0\big(R_r(x) + n_{\mathrm{eff}}(x - x_f)\big)$;
  - $z_r(x) = A_r(x)e^{-j\psi_r(x)}$ with $A_r = 1/R_r$ (ideal isotropic, equal per-site power).
  - Separable attenuation $e^{-\alpha(x - x_f)}$, with $\alpha = \frac{\ln 10}{20}\ell$ for $\ell$ in dB/m, and $\cos^q\theta$ field directivity appear only in the non-ideal control.
- **Candidate family (N0):**
  - M = 24 sites on consecutive D-aligned levels $R_D(x) + n_{\mathrm{eff}}x \in \lambda\mathbb Z + C$;
  - they share a common nominal phase $k_0(C - n_{\mathrm{eff}}x_f)$ modulo $2\pi$;
  - minimum spacing $0.68222\lambda$.
- **Selection:** $|S| = N = 8$; equal power; fixed physical noise $\sigma^2 = A_{\rm ref}/\mathrm{SNR}_{\rm ref}$, identical for all layouts.
- **Errors and robust-clearance family:**
  - actuator position errors $|\delta_n| \le \epsilon$, independent; D and P see the **same** physical error vector;
  - robust-clearance family $\mathcal F_\epsilon = \{S : x_j - x_i \ge d_{\min} + 2\epsilon$ for adjacent selected sites$\}$ with $d_{\min} = 0.5\lambda$. This is necessary and sufficient.
  - The whole unrestricted family is feasible iff $\epsilon \le 0.0911\lambda$.
  - The matched sub-family $\mathcal F_\epsilon^{\rm end}$ forces sites 0 and 23.
- **Objective:**
$$W(S) = \min_\delta \frac{|h_D|^2/N}{\sigma^2 + |h_P|^2/N}, \qquad W^\star = \max_{S \in \mathcal F_\epsilon} W(S).$$

## Mathematics (paper statements; all [PROVEN] in the GPT-6 Pro reply and checked by Claude)

**Lemma 1 (PASS phase and interval geometry).**
- For $n_{\mathrm{eff}} > 1$: $\psi_r' = k_0(n_{\mathrm{eff}} + t_r) > k_0(n_{\mathrm{eff}} - 1) > 0$, with $t_r = (x - x_r)/R_r$. So the unwrapped phase image of $[x_n - \epsilon, x_n + \epsilon]$ is exactly $[\psi_r(x_n - \epsilon), \psi_r(x_n + \epsilon)]$.
- Amplitude extrema: $A^- = 1/R_{\max}$ (endpoint) and $A^+ = 1/R_{\min}$ (projection of $x_r$). With attenuation or directivity, check the endpoints plus the roots of $\alpha v^2 + pv + \alpha b_r^2 = 0$.
- Remark (sensitivity floor): $|z_r'| \ge k_0(n_{\mathrm{eff}} - 1)A$. It concerns each complex contribution, not the power or the SLNR.

**Theorem 1 (nonlinear SLNR bracket).**
- Desired part: with common nominal phase and every $\beta_{D,n} \le \pi/2$ (otherwise the layout is rejected),
$$L_D(S) = \frac1N\Big(\sum_{n \in S} A^-_{D,n}\cos\beta_{D,n}\Big)^2.$$
- Leakage part: asymmetric sectors with center $\phi_{c,n} = -(\psi_P^+ + \psi_P^-)/2$ and half-width $\beta_{c,n} = (\psi_P^+ - \psi_P^-)/2$, support $s_n(\theta)$ (the $A^-$ branch where the cosine is negative), and
$$B_P(S) = \frac{\max_k \sum_{n \in S} s_n(\theta_k)}{\cos(\pi/K)}, \qquad \bar I = \frac{B_P^2}{N}.$$
- For $\epsilon = 0$: $B_P = |h_P|$ exactly.
- With $\sigma^2 > 0$:
$$L(S) = \frac{L_D}{\sigma^2 + \bar I} \le W(S) \le U(S)$$
for any nonempty feasible witness set, evaluated with the **same** error vector for D and P.

**Theorem 2 (shared endpoint bank and safe screening).**
- Setup: $z_n^\pm = z_P(x_n \pm \epsilon)$, $v_n = (z_n^+ - z_n^-)/2$; breakpoints $\arg v_n \pm \pi/2$ over all $M$ sites; one angle per cell gives templates $s^{(1..H)}$ with $H \le 2M$.
- Exact cover: for every $S$,
$$\max_{s \in \{\pm1\}^{|S|}}\Big|\sum_{n \in S} z_n^{s_n}\Big|^2 = \max_{q \le H}\Big|\sum_{n \in S} z_n^{s_n^{(q)}}\Big|^2.$$
  Proof sketch: zonotope; convexity of $|w|^2$; support-direction vertices.
- Witness bound: $U_H(S) = \min_q \mathrm{SLNR}(S, \epsilon s^{(q)}) \ge W(S)$.
- Safe screening: any $S$ with $U_H(S) \le L(\hat S)$ is discarded safely. Scanning the survivors therefore returns $\max_{S \in \mathcal F} L(S)$ **exactly**.
- Scope: exact for the **endpoint** leakage maximum. It does not claim that box maxima or SLNR minima lie at the endpoints.

**Corollary 1 (global robust certification).**
- Global bracket:
$$L(\hat S) \le W^\star \le U^\star := \max_{S \in \mathcal F} U_H(S), \qquad \frac{W(\hat S)}{W^\star} \ge \frac{L(\hat S)}{U^\star}.$$
- Uniqueness: if $L(\hat S) > \max_{S \ne \hat S} U_H(S)$, then $\hat S$ is the **unique global robust-optimal layout** in $\mathcal F$.
- Certified dominance over nominal: $L(\hat S) > U(S_N)$, with $S_N$ the exhaustive nominal optimum.

**Corollary 2 (protection limits).**
- Endpoint converse / achievability:
$$F_{\rm end} = \min_{S \in \mathcal F}\max_q \frac{|\sum_{n \in S} z_P(x_n + \epsilon s_n^{(q)})|^2}{N} \le \min_S \max_\delta I_P(S, \delta) \le \bar I(\hat S).$$
- Interference-temperature feasibility, with total power $p \in [0, p_{\max}]$, SNR target $\gamma$, and leakage ceiling $I_{\max}$:
  - the certificate constraints are feasible iff $\gamma\sigma_D^2/L_D \le \min\{p_{\max}, I_{\max}/\bar I\}$;
  - if $pF_{\rm end} > I_{\max}$, no family member meets the ceiling for all errors.
- A PASS-specific positive floor, from the sine identity $|v_n|^2 = (A_+ - A_-)^2/4 + A_+A_-\sin^2(\Delta\psi_n/2)$ and Lemma 1:
$$\min_S \max_\delta |h_P|^2 \ge \sin^2\big(k_0(n_{\mathrm{eff}} - 1)\eta\big)\,\min_S\sum_{n \in S}\underline A_n^2, \qquad \eta = \min\Big\{\epsilon,\ \frac{\pi}{2k_0(n_{\mathrm{eff}} + 1)}\Big\}.$$
  This is a remark only, if space allows.

**Remark (when robust selection wins; fixed pair).** With $A_q = a - c_q$ and $B_q = c_qb - ad_q$, the certified-dominance region in $s = \sigma^2 > 0$ is the union over witnesses of the half-lines $\{A_qs > B_q\}$. It is exact for the certificate test only. $S_N$ changes with σ², so every SNR point is recomputed.

**Dropped from the main text:**
- the Lemma 3 Taylor remainder (correct, but superseded by the exact endpoint converse);
- the κ diagnostic;
- the $(C_{\min}/C_{\max})^2$ approximation (optional remark).

## Algorithm (Global Certified Selection, GCS)

1. **Family.** Enumerate $\mathcal F_\epsilon$ (or $\mathcal F_\epsilon^{\rm end}$) with clearance filtering. Reject $\epsilon$ where any $\beta_{D,n} > \pi/2$.
2. **Tables** ($O(MK)$): $c_n$; asymmetric-sector supports $s_n(\theta_k)$; endpoint values $z_{D/P}(x_n \pm \epsilon)$; templates ($H \le 2M$).
3. **Nominal baseline.** Exhaustive nominal optimum $S_N$ over the family.
4. **Incumbent.** Swap local search on $L$ from $S_N$ plus 8 random starts, restricted to feasible swaps.
5. **Witness bank** ($O(|\mathcal F|NH)$, batched): compute $U_H(S)$ for all $S$.
6. **Safe screening.** Evaluate $L$ only on survivors with $U_H > $ incumbent, updating the incumbent. This returns $\hat S = \arg\max L$ exactly (subject to the pre-declared evaluation cap below).
7. **Certificates.**
   - global bracket $L(\hat S), U^\star$;
   - rival-dominance margin $L(\hat S) - \max_{S \ne \hat S} U_H$;
   - certified dominance over $S_N$ using $U(S_N)$ = all $2^N$ corners plus L-BFGS-B refinement;
   - $F_{\rm end}$ vs $\bar I(\hat S)$.
8. **Reporting.** Nominal sacrifice; desired power and leakage at witnesses; runtime; survivors.

**Pre-declared evaluation cap.** If the survivors exceed $2\times10^5$ certificate evaluations in a case, report the valid global bracket and incumbent without claiming the exact $\arg\max L$ for that case. Record the count.

**Numerical wording.** "Analytical certificates evaluated numerically in float64; margins reported." No claim of machine-verified interval arithmetic. For the featured instances, recompute the decisive margins independently (a second implementation, or higher precision on the winner plus the top rivals).

## Evidence So Far (pilot; paper-final numbers must come from the frozen driver)

**Reference instance:** $P = (3, 2)$, $\epsilon = 0.05\lambda$, SNR 30 dB. GPT-6 Pro produced these numbers; Claude reproduced them to machine precision.

| | Free family (735,471) | Identical endpoints (74,613) |
|---|---|---|
| Templates $H$ | 48 | 48 |
| $L(\hat S)$ | 56.5593 | 55.5740 |
| $U^\star$ (global upper bound) | 56.5828 (+0.042%) | 55.6040 (+0.054%) |
| Rival-dominance margin | 0.3209 → unique optimum | 0.0466 → unique optimum |
| Certified gain over exhaustive nominal | +34.17% | +2.79% |
| Nominal sacrifice (nominal SLNR) | 20.5% | 5.4% |
| $F_{\rm end}$ vs $\bar I(\hat S)$ | 0.011858 vs 0.011863 | 0.012070 vs 0.012076 |
| Runtime (whole family) | about 1.3 s total for both families | |

- The v1 swap search found $L = 53.42$, not the certificate optimum of 56.56. **Selection gap is real;** GCS removes it.
- GPT-6 Pro's independent matched grid (33 geometries × 4 settings; exhaustive nominal; swap robust; 256 corners): **108/132 certified positive, 79/132 above 5%**, with medians 5.1–11.8%. Claude has not yet rerun it; it is a cross-check run in the plan.
- **Do not reuse** the earlier 359/528 and 247/528 pilot counts; their protocol was incomplete.

## Failure Modes and Honest Limits

- **Four separate gaps.** Angular (tiny with sec); sector enclosure; D/P dependency (largest when D and P respond alike; the v1 pilot saw $U/L$ up to 1.73); selection (removed by GCS). Improving one does not shrink the others.
- **Screening efficiency is instance-dependent.** The worst case still scales with $|\mathcal F|$. It is not polynomial-time.
- **Inconclusive cases** ($L(\hat S) \le U(S_N)$) are reported as inconclusive, not as losses.
- **Scope:** ideal equal-power separable model; position errors only; one waveguide, one protected receiver.

## Novelty Statement

> Within a robust-clearance, D-aligned PASS family, we turn exact nonlinear endpoint evaluations into a family-wide shared adversarial witness bank (at most 2M templates). Together with sector-support certificates, it enables safe global screening, exact certificate optimization, unique robust-optimality certificates, and a leakage converse, and it establishes certified worst-case SLNR gains over exhaustive nominal selection under actuator position errors.

**Credited as tools:** sector/interval/Minkowski geometry (Arnestad; Poli); nonlinear all-error enclosures (Zhang); interference-aware PASS activation (FullPASS); null fragility (Yang); multi-PA position-error degradation (Chen H-PASS); attenuation-driven placement (Xu et al.).

## Claim-Driven Validation (summary; see `EXPERIMENT_PLAN.md`)

- **C1 (primary):** certified dominance over exhaustive nominal selection in the matched family, via GCS. Includes negative and inconclusive cases, and the nominal sacrifice.
- **C2 (supporting):** the global certification yield — how often the family-wide bracket is tight and uniqueness is certified — plus screening efficiency.
- **C3 (supporting):** protection limits — the converse/achievability bracket and interference-temperature thresholds across tolerance.
