# Narrative Report: Robustness of Pinching-Antenna Systems to Pinching-Position Errors

> **Input for Workflow 3.** Run `/paper-writing "NARRATIVE_REPORT.md" — venue: IEEE_CONF` (6 pages including references).
>
> **Claim status: every claim below is `[unadjudicated]`.** `CLAIMS_FROM_RESULTS.md` is `verdict: REVIEW_UNAVAILABLE`; rerun `/result-to-claim` (Codex) before submission-grade writing. See the 2026-09-25 entry in `findings.md`.
>
> **Sources:** graduation report v7 (`fyp_report/latex/`), `findings.md`, `docs/THEORY_EXTENSIONS.md`, `fyp_report/review-stage/AUTO_REVIEW.md`, and `results/`. Every number below was recomputed from `results/` on 2026-09-25; the cited file and column are given next to each number.

## Venue Constraints

- **Venue:** IEEE ICC 2027 (Washington DC, 30 May – 3 June 2027). Paper submission deadline: 2 October 2026 via EDAS.
- **Length:** at most 6 printed pages (10-pt, two-column) including figures and references; longer initial submissions are rejected without review.
- **Format:** `\documentclass[conference]{IEEEtran}`, numeric `\cite{}`, `IEEEtran.bst`, `IEEEkeywords` after the abstract.
- **Candidate symposia:** Wireless Communications, or Signal Processing for Communications. Communication Theory also fits if the paper is framed mainly around the analysis.
- **Author block:** confirm the review policy on EDAS. ARIS `IEEE_CONF` defaults to non-anonymous. Do not generate author names.

## One-Sentence Contribution

For a phase-aligned pinching-antenna system (PASS), we show that pinching-position errors reduce the array gain, to second order, by the amplitude-weighted variance of the induced phase errors, where each antenna's phase sensitivity is $\xi_n = \sin\theta_n^\star + n_{\mathrm{eff}}$. This one quantity gives three results: a first-order lower bound with an explicit validity threshold; the identification of differential (split-mode) motion as the damaging error direction, with common drift nearly harmless; and a single covariance-based predictor for stochastic errors.

## Core Story

**Problem.** PASS radiates from points created by pinching dielectric particles onto a waveguide. The received phase of each activated antenna has two parts: the free-space phase $k_0 R_n$ and the guided-wave phase $k_0 n_{\mathrm{eff}} x_n$. Constructive placement aligns these phases so the element responses add coherently [ouyang2025array]. Existing PASS design work (array gain, rate maximization, NOMA activation, uplink fairness, sensing) assumes the pinching positions are exact. In hardware, fabrication tolerance, actuator limits, and calibration offsets all perturb those positions, and at mmWave the tolerance budget is tight. At 28 GHz ($\lambda \approx 10.7$ mm), a fixed 1 mm error per antenna ($\epsilon/\lambda \approx 0.093$) already lowers the box-best-found normalized gain of the constructive design to $0.441$ (`results/data_freq_sweep.csv`, `f_c = 28e9`, `eps_m = 0.001`, `wc_norm = 0.44105159`). The open questions are how a constructive PASS placement degrades, which error directions matter, and how much of the degradation can be predicted analytically.

**Key insight.** Linearizing the PASS phase law gives a per-antenna phase error $k_0 \xi_n \delta_n$ with $\xi_n = \sin\theta_n^\star + n_{\mathrm{eff}}$. For free-space movable antennas the corresponding sensitivity is $\sin\theta_n^\star \in (-1, 1)$, which is centered at zero. In PASS the guided-wave term shifts every sensitivity by the same amount, $n_{\mathrm{eff}}$, so most of the PASS-specific sensitivity acts as a common mode. For the studied design, $\xi_n \in [1.4203, 1.4597]$ and the weighted mean is exactly $n_{\mathrm{eff}} = 1.44$. A second-order expansion of the normalized coherent sum then gives normalized gain $\approx 1 - \mathrm{Var}_\alpha(k_0 \xi_n \delta_n)$: gain is lost only through the *centered* spread of phase errors across the aperture, not through their common rotation.

**Consequences tested in the paper.**
1. A first-order lower bound on the normalized gain holds whenever $k_0 \xi_{\max} \epsilon \le \pi/2$, which gives the explicit threshold $\epsilon_{\mathrm{valid}} = \pi / (2 k_0 \xi_{\max})$.
2. The box-feasible pattern that maximizes the centered spread is the split mode, $\delta_n = \epsilon\, \mathrm{sign}(\xi_n - \bar{\xi}_\alpha)$. In the symmetric geometry this is an outward left-right split. Common-bias drift, by contrast, is nearly harmless.
3. Taking the expectation gives $\mathbb{E}[\tilde{a}] \approx 1 - k_0^2\, \mathrm{tr}(M_\alpha D_\xi \Sigma_\delta D_\xi)$. This single covariance projection explains iid, common-bias, and spatially correlated errors.

**Evidence.** Studied configuration: $N = 16$, $d = 3$ m, $f_c = 28$ GHz, $n_{\mathrm{eff}} = 1.44$, $\Delta_p = 0.5$.
- The validity threshold is $\epsilon_{\mathrm{valid}}/\lambda = 0.1713$. Inside it, the lower bound stays within $3.40 \times 10^{-6}$ of the box-best-found adversary at all 35 grid points.
- Before the first null ($\epsilon/\lambda < 0.175$), the split mode stays within $1.57 \times 10^{-5}$ of the box-best-found adversary.
- At $\epsilon/\lambda = 0.10$, box-best-found gives $0.3817$ while common bias gives $0.99994$.
- The covariance predictor's mean absolute error over $0 \le \epsilon/\lambda \le 0.10$ is $5.7 \times 10^{-3}$ (iid uniform), $8.4 \times 10^{-8}$ (common bias), and $3.4 \times 10^{-3}$ (correlated Gaussian). It reproduces the ordering iid < correlated < common bias.
- Raising $n_{\mathrm{eff}}$ from $1.44$ to $1.99$ lowers the box-best-found gain at $\epsilon/\lambda = 0.10$ from $0.3817$ to $0.0992$, which confirms that the guided-wave term drives the sensitivity.

**Implication.** Tolerance and calibration effort for PASS should target differential error modes, which widen the centered phase spread, rather than whole-aperture drift. Larger $n_{\mathrm{eff}}$ and higher carrier frequency both tighten the placement-accuracy requirement.

## Claims

All claims are `[unadjudicated]`. Each claim lists its scope and the stored evidence. Derivation-type claims (C1 and the analytic part of C2) additionally need proof checking: `/paper-writing` Phase 4.5 or `/proof-checker`.

1. **C1 — PASS phase sensitivity is centered at $n_{\mathrm{eff}}$ (derivation + numerical profile).** Linearizing $\Phi_n(\Delta_n) = k_0(R_n(\Delta_n) + n_{\mathrm{eff}}\Delta_n)$ gives $\Delta\phi_n \approx k_0 \xi_n \delta_n$ with $\xi_n = \sin\theta_n^\star + n_{\mathrm{eff}}$. For the studied symmetric design, $\xi_{\max} = 1.4597026$ and the amplitude-weighted mean is $1.44$ (`results/config.json`: `xi_max`, `xi_mean`). The minimum is $\xi_{\min} = 1.4203$, derived as $2\,\xi_{\mathrm{mean}} - \xi_{\max}$ by symmetry; it is not stored separately. Scope: the formula holds for any nominal placement; the numbers are for the studied design.

2. **C2 — The first-order lower bound is tight inside its validity region.** The bound (Eq. B4 below) holds under the linearized phase model when $k_0 \xi_{\max} \epsilon \le \pi/2$. This gives $\epsilon_{\mathrm{valid}}/\lambda = 0.17126776$ (`results/config.json` `epsilon_valid_norm`). Over the 35 grid points with $\epsilon/\lambda \le \epsilon_{\mathrm{valid}}/\lambda$:
   - `lb_full_norm <= wc_norm` at every point;
   - the maximum gap is $3.398 \times 10^{-6}$ (`results/data_main.csv`, columns `lb_full_norm` and `wc_norm`).

   Scope: the studied configuration and the box-best-found adversary (not a certified global minimum).

3. **C3 — Split-mode motion dominates before the first null, and common bias is nearly harmless (empirical).**
   - For $\epsilon/\lambda < 0.175$, $\max|\text{split} - \text{box-best-found}| = 1.568 \times 10^{-5}$ (`results/data_main.csv`, `split_norm` vs `wc_norm`).
   - At $\epsilon/\lambda = 0.10$: box-best-found $0.38172695$, split $0.38174263$, common bias $0.99993864$ (`results/data_main.csv`).
   - Box validation (`results/data_box_validation.csv`): corner enumeration equals the continuous-box best-found value at $\epsilon/\lambda \in \{0.02, 0.05, 0.10, 0.15\}$. At $0.175$, local refinement reaches $1.88 \times 10^{-17}$, while the corner and split candidates stay at $1.58 \times 10^{-4}$.

   Scope: the split mode is an empirical near-adversarial pattern in the pre-null regime of the studied symmetric setting.

4. **C4 — One covariance projection predicts mean degradation under three stochastic error laws.** The predictor (Eq. B7) was tested against 2000-sample Monte Carlo at 21 levels over $0 \le \epsilon/\lambda \le 0.10$ (`results/data_error_scenarios.csv`, `mean` vs `quadratic_approx`):

   | Error law | MAE | Max abs. error (at $\epsilon/\lambda$) |
   |---|---|---|
   | iid uniform | $5.671 \times 10^{-3}$ | $2.565 \times 10^{-2}$ (0.100) |
   | Common bias | $8.413 \times 10^{-8}$ | $3.659 \times 10^{-7}$ (0.080) |
   | Correlated Gaussian | $3.387 \times 10^{-3}$ | $1.526 \times 10^{-2}$ (0.095) |

   The predictor reproduces the ordering iid < correlated < common bias. Scope: the studied design, $\epsilon/\lambda \le 0.10$, and these three covariance structures.

5. **C5 — The guided-wave index and the carrier frequency act as stress factors (supporting mechanism check).**
   - Box-best-found at $\epsilon/\lambda = 0.10$: $0.38173$, $0.20610$, $0.09921$ for $n_{\mathrm{eff}} = 1.44$, $1.75$, $1.99$ (`results/data_neff_sweep.csv`).
   - For a fixed 1 mm error: $0.96755$, $0.44105$, $3.75 \times 10^{-18}$ at $6$, $28$, $60$ GHz (`results/data_freq_sweep.csv`).

   Scope: sensitivity checks for the studied geometry; not a general scaling law.

6. **C6 — Same-aperture placement comparison (optional; lowest priority for 6 pages).** Raw array gain at $\epsilon/\lambda = 0.10$ (`results/data_baseline_summary.csv`):
   - Constructive aligned vs naive uniform aperture: nominal $+1.11\%$, box-best-found $+14.14\%$, iid mean $+0.90\%$.
   - Best-found same-aperture nominal-gain comparator vs constructive aligned: nominal $+1.69\%$, box-best-found $+11.09\%$, iid mean $+1.68\%$.

   The comparator leads on every reported metric. Scope: these three placements under matched span and spacing.

## Method and Analysis

Material for the system-model and analysis sections. Inherited from [ouyang2025array]: geometry, channel, array gain, and the phase-alignment idea. New in this work: the wavelength-snapped feasible construction, and everything from B1 onward.

**A1. System model [ouyang2025array].** The waveguide lies along $x$ at height $d$. The user is at $\mathbf{u} = [x_u, 0, 0]^T$. There are $N$ (even) pinching antennas at $\boldsymbol{\psi}_n = [x_n, 0, d]^T$, with $\Delta_n = x_n - x_u$ and $R_n(\Delta_n) = \sqrt{d^2 + \Delta_n^2}$. The channel is
$$h_n = \frac{\eta^{1/2}}{R_n} e^{-jk_0 R_n} e^{-jk_0 n_{\mathrm{eff}}(x_n - x_0)}.$$
With equal power allocation, the array gain is
$$a(\Delta) = \frac{\eta}{N}\Big|\sum_n \frac{e^{-j\Phi_n(\Delta_n)}}{R_n(\Delta_n)}\Big|^2, \qquad \Phi_n = k_0\big(R_n + n_{\mathrm{eff}}\Delta_n\big).$$

**A2. Constructive phase-aligned feasible placement (this work's reformulation).**
- Alignment target: $R_n + n_{\mathrm{eff}}\Delta_n = C' + m_n\lambda$, subject to symmetry ($\Delta_{-n} = -\Delta_n$) and minimum spacing ($|\Delta_n - \Delta_{n'}| \ge \Delta_p\lambda$).
- Initialize $\Delta_n^{(0)} = \Delta_p\lambda/2 + (n-1)\Delta_p\lambda$.
- Snap to $d_n = \lambda\lceil(\sqrt{d^2 + (\Delta_n^{(0)})^2} + n_{\mathrm{eff}}\Delta_n^{(0)})/\lambda\rceil$.
- Solve $\sqrt{d^2 + \Delta_n^2} + n_{\mathrm{eff}}\Delta_n = d_n$, whose closed-form feasible root is $\Delta_n = \big(d_n n_{\mathrm{eff}} - \sqrt{d_n^2 + d^2(n_{\mathrm{eff}}^2 - 1)}\big)/(n_{\mathrm{eff}}^2 - 1)$. If spacing is violated, increase $d_n$ by $\lambda$ and solve again.
- Mirror to the negative side. The result is denoted $\Delta^\star$.

This is a reproducible feasible design, not a global optimizer of $a(\Delta)$.

**A3. Normalized gain.** With the design phase reference $\phi_n^\star = \Phi_n(\Delta_n^\star)$,
$$\tilde{a}(\Delta;\Delta^\star) = \frac{\frac{\eta}{N}\big|\sum_n R_n^{-1} e^{-j(\Phi_n(\Delta_n) - \phi_n^\star)}\big|^2}{a_{\mathrm{ideal}}}, \qquad a_{\mathrm{ideal}} = \frac{\eta}{N}\Big(\sum_n R_n(\Delta_n^\star)^{-1}\Big)^2 = 1.7775.$$
Use $\tilde{a}$ for perturbation curves and raw $a$ for cross-placement comparison.

**B1. Error model.** $\Delta_n = \Delta_n^\star + \delta_n$ with $|\delta_n| \le \epsilon$. The adversarial target is $\tilde{a}_{\mathrm{wc}} = \min_{\|\delta\|_\infty \le \epsilon} \tilde{a}$, which is nonconvex and oscillatory. It is evaluated numerically as **box-best-found**: exhaustive corner enumeration ($N = 16 \le 20$) plus L-BFGS-B box-constrained refinement (6 restarts, 300 iterations). The refinement improves on the best corner only for $\epsilon/\lambda \ge 0.175$ (`method_used = enum+local` in `results/data_main.csv`).

**B2. Phase sensitivity.**
$$\Phi_n'(\Delta_n^\star) = k_0\xi_n, \qquad \xi_n = \frac{\Delta_n^\star}{\sqrt{d^2 + \Delta_n^{\star 2}}} + n_{\mathrm{eff}} = \sin\theta_n^\star + n_{\mathrm{eff}}, \qquad \Delta\phi_n \approx k_0\xi_n\delta_n.$$

**B3. Normalized coherent sum.**
$$\alpha_n = \frac{R_n(\Delta_n^\star)^{-1}}{\sum_m R_m(\Delta_m^\star)^{-1}}, \qquad \rho(\delta) = \sum_n \alpha_n e^{-jk_0\xi_n\delta_n},$$
under the phase-dominant approximation (amplitude perturbations neglected).

**B4. First-order lower bound.** If $k_0|\xi_n|\epsilon \le \pi/2$ for all $n$, each phasor keeps a nonnegative real projection, so
$$\tilde{a} \ge \left(\frac{\sum_n \cos(k_0|\xi_n|\epsilon)\big/\sqrt{d^2 + (|\Delta_n^\star| + \epsilon)^2}}{\sum_m 1/R_m(\Delta_m^\star)}\right)^2, \qquad \epsilon_{\mathrm{valid}} = \frac{\pi/2}{k_0\,\xi_{\max}}.$$
The bound uses the linearized phase error. The paper should call it a first-order bound; it is also checked numerically against box-best-found (C2).

**B5. Weighted phase-variance mechanism.** Expanding to second order with $\mu_\phi = \sum_n \alpha_n k_0\xi_n\delta_n$:
$$|\rho(\delta)|^2 \approx 1 - \sum_n \alpha_n (k_0\xi_n\delta_n)^2 + \mu_\phi^2 = 1 - \mathrm{Var}_\alpha(k_0\xi_n\delta_n).$$
A common phase rotation cancels; only the centered spread costs gain.

**B6. Split mode.** $\delta_n^{\mathrm{split}} = \epsilon\,\mathrm{sign}(\xi_n - \bar{\xi}_\alpha)$ with $\bar{\xi}_\alpha = \sum_n \alpha_n\xi_n$. With symmetric weights, $\bar{\xi}_\alpha = n_{\mathrm{eff}}$, so $\delta_n^{\mathrm{split}} = \epsilon\,\mathrm{sign}(\Delta_n^\star)$: an outward left-right split. This is a box-feasible, interpretable candidate, not a proven minimizer.

**B7. Covariance predictor.** For zero-mean $\delta$ with covariance $\Sigma_\delta$, define $M_\alpha = \mathrm{Diag}(\alpha) - \alpha\alpha^T$ and $D_\xi = \mathrm{Diag}(\xi)$. Then
$$\mathbb{E}[\tilde{a}] \approx 1 - k_0^2\,\mathrm{tr}(M_\alpha D_\xi \Sigma_\delta D_\xi).$$
- Common bias has $\Sigma_\delta \propto \mathbf{1}\mathbf{1}^T$, which $M_\alpha$ annihilates up to the small spread of $\xi_n$.
- iid errors put all covariance energy on the diagonal.
- Smooth correlated fields fall in between.

The same object drives B5 (deterministic) and B7 (stochastic).

## Experiments

### Setup
- **Models:** simulation of the PASS array-gain model in A1. No external dataset.
- **Configuration** (`results/config.json`):
  - $N = 16$, $d = 3.0$ m, $f_c = 28$ GHz, $\lambda = 10.714$ mm, $n_{\mathrm{eff}} = 1.44$, $\Delta_p = 0.5$, $\eta = 1$;
  - $k_0 = 586.43$ rad/m, $a_{\mathrm{ideal}} = 1.7775020$, $\xi_{\max} = 1.4597026$, $\epsilon_{\mathrm{valid}}/\lambda = 0.17126776$;
  - random seed `20260111`.
- **Error sweeps:**
  - Main curve: 41 levels over $0 \le \epsilon/\lambda \le 0.20$, with 1000 bounded iid Monte Carlo samples per level.
  - Stochastic scenarios: 21 levels over $0 \le \epsilon/\lambda \le 0.10$, 2000 samples per law.
  - Baselines: 31 levels over $0 \le \epsilon/\lambda \le 0.15$.
- **Stochastic laws** (`src/theory_extensions.py`):
  - iid uniform: $\delta_n \sim U[-\epsilon, \epsilon]$.
  - Common bias: one shared $b \sim U[-\epsilon, \epsilon]$.
  - Correlated Gaussian: exponential covariance $\sigma^2 e^{-|n-m|/L}$ in element-index distance, with $L = 4$ and $\sigma^2 = \epsilon^2/3$, matching the iid variance. This field is unbounded.
- **Hardware:** CPU only (NumPy/SciPy). Full run: `python src/main.py`.
- **Baselines** (C6 only):
  - Naive uniform aperture: same endpoints, uniform interior, mirrored.
  - Best-found same-aperture nominal-gain comparator: L-BFGS-B with 4 restarts, same span and spacing.

### Experiment 1: Bounded-error robustness (Figure 2, Table II) — supports C2, C3

Design-referenced normalized gain $\tilde{a}$ (`results/data_main.csv`; the corner column is from `results/data_box_validation.csv`):

| $\epsilon/\lambda$ | First-order LB | Box-best-found | Corner-restricted | Split mode | Common bias | iid MC mean [p05, p95] |
|---|---|---|---|---|---|---|
| 0.02 | 0.9676070 | 0.9676082 | 0.9676082 | 0.9676089 | 0.9999975 | 0.98981 [0.9858, 0.9937] |
| 0.05 | 0.8089142 | 0.8089171 | 0.8089171 | 0.8089240 | 0.9999847 | 0.93782 [0.9131, 0.9618] |
| 0.10 | 0.3817240 | 0.3817270 | 0.3817270 | 0.3817426 | 0.9999386 | 0.77036 [0.6876, 0.8494] |
| 0.15 | 0.0449403 | 0.0449408 | 0.0449408 | 0.0449452 | 0.9998619 | 0.54713 [0.4047, 0.6963] |
| 0.175 | (outside validity) | $1.88 \times 10^{-17}$ | $1.5787 \times 10^{-4}$ | $1.5790 \times 10^{-4}$ | 0.9998121 | 0.44100 [0.2732, 0.6172] |

**Interpretation.**
- Inside $\epsilon_{\mathrm{valid}}$, the first-order bound and the adversary agree to about $10^{-6}$.
- The split mode tracks the adversary before the null, and common drift costs almost nothing.
- Typical random box noise (MC mean $0.770$ at $0.10$) is far milder than structured split motion ($0.382$).
- The $0.175$ row is the only level where continuous refinement beats the corners. It marks the near-null regime, where the split mode is no longer near-adversarial.

### Experiment 2: Stochastic error laws (Figure 3) — supports C4

`results/data_error_scenarios.csv`:

| Law | $\epsilon/\lambda$ | MC mean | Predictor | [p05, p95] |
|---|---|---|---|---|
| iid uniform | 0.05 | 0.93770 | 0.93604 | [0.9135, 0.9610] |
| iid uniform | 0.10 | 0.76981 | 0.74416 | [0.6836, 0.8537] |
| Common bias | 0.05 | 0.999995 | 0.999995 | [0.99999, 1.00000] |
| Common bias | 0.10 | 0.99998 | 0.99998 | [0.99994, 1.00000] |
| Correlated Gaussian | 0.05 | 0.95889 | 0.95774 | [0.9107, 0.9859] |
| Correlated Gaussian | 0.10 | 0.84576 | 0.83095 | [0.6946, 0.9475] |

The aggregate error table is in C4.

**Interpretation.** The three laws share the same marginal variance but degrade very differently, and the predictor recovers both their scale and their ranking. Covariance structure, not error magnitude alone, decides the loss. The largest errors appear at the top of the tested range, where higher-order phase terms grow.

### Experiment 3: Guided-wave index and frequency sweeps (Figure 4, optional) — supports C5

Numbers are in C5. The $n_{\mathrm{eff}}$ sweep is the PASS-specific one and gets priority if only one sweep fits.

### Experiment 4 (optional): Same-aperture placements — supports C6

`results/data_baseline_summary.csv`, raw array gain at $\epsilon/\lambda = 0.10$:

| Quantity | Uniform aperture | Constructive aligned | Best-found nominal comparator |
|---|---|---|---|
| Nominal gain | 1.68249 | 1.70116 | 1.72994 |
| Box-best-found gain | 0.38857 | 0.44351 | 0.49270 |
| iid mean gain | 1.29981 | 1.31150 | 1.33358 |
| Common-bias mean gain | 1.68250 | 1.70108 | 1.72990 |
| Correlated-Gaussian mean gain | 1.43120 | 1.44299 | 1.46514 |

## Figures

Suggested budget for 6 pages. All data figures should be regenerated at IEEE column width (3.5 in) with `/paper-figure`; the existing PNG/PDF files in `results/` are sized for the A4 report.

1. **Figure 1 — System model** (schematic). Waveguide at height $d$, activated pinching antennas, user, and free-space plus guided-wave paths. Draft art is in `fyp_report/latex/figures/fig_pass_system_model_corrected.pdf` and `fig_pass_system_model_3d_minimal.pdf`, adapted from [ouyang2025array]. Redraw with `/figure-spec` if needed.
2. **Figure 2 — Main robustness curve (hero figure)**, line plot, from `results/data_main.csv`. Plot $\tilde{a}$ vs $\epsilon/\lambda \in [0, 0.2]$: first-order LB, box-best-found, split mode, common bias, iid MC mean with a [p05, p95] band, and a vertical line at $\epsilon_{\mathrm{valid}}/\lambda = 0.1713$. Existing version: `results/fig_main.pdf`.
3. **Figure 3 — Stochastic laws vs predictor**, line plot, from `results/data_error_scenarios.csv`. MC mean with a [p05, p95] band and dashed predictor for the three laws. Existing version: `results/fig_error_scenarios.pdf` (three panels; consider one combined panel to save space).
4. **Figure 4 (optional) — $n_{\mathrm{eff}}$ sweep**, line plot, from `results/data_neff_sweep.csv`. Existing version: `results/fig_neff_sweep.pdf`. Alternative: `results/fig_xi_distribution.pdf` as a small inset that illustrates C1.
5. **Table I — Simulation parameters** (from Setup).
6. **Table II — Bounded-error checkpoints** (Experiment 1). This replaces `fig_box_validation`, since a 6-page paper has no appendix.
7. **Table III (optional) — Same-aperture comparison** (Experiment 4).

**Do not use:** `fig_corr_length_sweep`. It has no generating code in `src/` and no data in `results/`; see `findings.md`, 2026-09-25.

## Known Weaknesses

- **Single configuration.** All evidence comes from one symmetric geometry ($N = 16$, $d = 3$ m, user under the array center). There is no $N$ sweep and no $d$ or $\Delta_p$ sweep; AUTO_REVIEW round 2 ranks this as the main generality gap.
- **Adversary not certified.** Box-best-found is not a certified global minimum. At $\epsilon/\lambda = 0.175$, local refinement beats all corners, and only 6 local restarts are used, with no independent global-search cross-check.
- **Split mode is empirical.** It is justified by the local variance argument, not proven optimal, and it stops being near-adversarial near the first null.
- **Bound relies on linearization.** The lower bound uses the linearized phase error $k_0\xi_n\delta_n$; the exact phase deviation carries higher-order terms. Numerically, it stays below box-best-found at all 35 grid points in the validity region.
- **Predictor scope.** The covariance predictor neglects amplitude perturbations and is validated only up to $\epsilon/\lambda = 0.10$, for one design and three covariance structures. The correlated-Gaussian law uses index distance rather than physical distance.
- **Constructive design is not the best tested placement.** The best-found nominal-gain comparator leads on all reported metrics (C6).
- **Novelty unchecked.** Novelty has not been checked against 2025–2026 PASS papers on imperfect pinching or robust PASS, or against classical array phase-error tolerance theory (see Related Work).
- **Citations unaudited.** The bibliography entries carry DOIs but have not been through `/citation-audit`.

## Claim Boundaries (writer guidance — not manuscript prose)

- **Terminology** (per `AGENTS.md`):
  - Say "box-best-found" or "best-found adversary", never "exact" or "global worst case".
  - Say "constructive phase-aligned feasible placement", never "optimal".
  - Describe the split mode as an "empirical near-adversarial pattern in the pre-null regime".
  - Call the bound a "first-order lower bound, valid for $\epsilon \le \epsilon_{\mathrm{valid}}$".
  - Scope the predictor to "validated for $0 \le \epsilon/\lambda \le 0.10$ for the studied design".
- **Gain scales:** use $\tilde{a}$ (design-referenced normalized gain) for perturbation curves and raw $a$ for cross-placement comparison. Never mix the two scales in one figure or table.
- **Monte Carlo sources:** Figure 2 and Table II use `results/data_main.csv` (1000 samples). Figure 3 and C4 use `results/data_error_scenarios.csv` (2000 samples). Do not quote one against the other.
- **Scope in claims, not disclaimers:** state scope positively inside each claim (`paper-write` Key Rules 3–6). Put generic caveats only in one Limitations paragraph, and do not write "we do not claim …" sentences.
- **Choose the contest the paper wins** (`paper-write` Key Rule 10): analytic accuracy and mechanism explanation, not placement superiority. If C6 is kept, report every number, including the comparator's lead, neutrally.
- **Inherited vs new:** credit [ouyang2025array] for the model, the channel, the array gain, and the phase-alignment idea. The new contributions are A2's feasible construction, B2–B7, and all numerical results.

## Related Work

Existing entries are in `fyp_report/latex/references.bib` (DOIs present, audit pending):
- **PASS foundations and tutorials:** fukuda2022pinching, ding2025perspective, liu2026tutorial.
- **PASS nominal design and applications:** ouyang2025array (base model, mandatory), xu2025downlink, wang2025noma, tegos2025uplink, ding2025isac. All of these treat pinching positions as exact.
- **Flexible antennas:** wong2021fluid, zhu2024movable, new2025tutorial, zhu2025tutorialma. Their sensitivity is geometric only; there is no guided-wave term.
- **Near-field and position-error robustness:** ouyang2024primer, su2025positionerror, yang2026nearfield. These are the closest analogues, but they study movable antennas whose sensitivity is centered at zero.
- **Numerical:** byrd1995lbfgsb (only if C6 is kept).

**Positioning gaps to close before writing** (not yet in the bibliography; verify before citing):
- Classical random-phase-error tolerance theory for arrays and reflectors (e.g., Ruze's antenna tolerance theory, Proc. IEEE, 1966) gives a similar variance-type gain-loss law. The paper must state what is PASS-specific: $\xi_n$ centered at $n_{\mathrm{eff}}$, the common-mode cancellation, the split-mode adversary, the deterministic bound with its validity threshold, and the covariance projection for bounded and correlated errors.
- 2025–2026 PASS papers on position errors or robust pinching placement: run `/comm-lit-review` and `/novelty-check`.

## Proposed Title

"Robustness of Pinching-Antenna Systems to Pinching-Position Errors: A Weighted Phase-Variance Analysis"

Alternative: "Which Pinching-Position Errors Hurt? Phase-Variance Analysis of Constructive PASS Placement"

## Target Venue

IEEE ICC 2027 — `IEEE_CONF`, 6 pages including references.

## Suggested Page Budget (for `/paper-plan`)

| Section | Pages |
|---|---|
| I. Introduction (gap, contributions C1–C4 as bullets, strongest result up front) | 0.9 |
| II. System and error model (A1–A3, B1) | 0.8 |
| III. Robustness analysis (B2–B7) | 1.5 |
| IV. Numerical results (Figs. 2–3, Tables I–II; Fig. 4 or Table III only if space allows) | 1.8 |
| V. Conclusion with one Limitations paragraph | 0.3 |
| References (about 15) | 0.6 |
| **Total** | **≈ 5.9** |

## Source Map

| Content | File |
|---|---|
| Full derivations | `fyp_report/latex/sections/02_materials_methods.tex`, `A_appendix_derivations.tex`; `docs/THEORY_EXTENSIONS.md` |
| Graduation-report results and discussion | `fyp_report/latex/sections/03_results.tex`, `04_discussion.tex` |
| Reviewer history | `fyp_report/review-stage/AUTO_REVIEW.md` (round 2: 5/10, not ready) |
| Evidence log | `findings.md` |
| Raw results | `results/*.csv`, `results/config.json`, `results/delta_wc.npz`, `results/run_log.txt` |
| Code | `src/` (entry point `src/main.py`) |
