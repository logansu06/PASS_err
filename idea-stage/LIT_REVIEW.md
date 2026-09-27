# Literature Review: Robustness of PASS to Pinching-Position Errors

Generated: 2026-09-25 by `/comm-lit-review`. Sources searched:
- Zotero and Obsidian: not configured; skipped.
- Local library: no `papers/` or `literature/` folder in the project.
- Web search: IEEE Xplore and arXiv pages, reached through web search.

Metadata marked *verify* comes from secondary pages and must pass `/citation-audit` before it is cited.

## Literature Table

| Paper | Venue | Year | Layer | Scenario | Method | Key Result | Limitation | Relevance | Source |
|---|---|---:|---|---|---|---|---|---|---|
| Ouyang, Wang, Liu, Ding, *Array Gain for Pinching-Antenna Systems (PASS)* | IEEE Commun. Lett. | 2025 | PHY | Single user; N pinching antennas on one waveguide | Closed-form array-gain upper bound for fixed spacing; position refinement | Optimal number of antennas exists; placement near the bound | Pinching positions assumed exact | Base model we inherit | web (arXiv 2501.05657) |
| Pakravan, Trigui, Ajib, Zhu, *Impact of Position Uncertainty on the Secrecy Performance of Pinching Antenna Systems* (v2 title: *Secrecy Performance Analysis of PASS Under Pinching-Position Uncertainty*) | preprint | 2026 | PHY security | **Single** radiating point with an activation-position error; Bob and Eve | Marginal SNR distributions; Gaussian copula; approximate secrecy outage probability | PAS stays more secure than fixed antennas under activation uncertainty | Single antenna, so no multi-element phase coherence and no array-gain analysis | Closest prior work on **pinching-position** errors; must be cited and distinguished | web (arXiv 2604.12156) |
| Sun, Ouyang, Wu, Liu, *Robust Beamforming for Pinching-Antenna Systems* | preprint | 2025 | PHY | Multi-user; lossy and lossless waveguides | Robust beamforming (SOCP / MRT) plus Gauss–Seidel position optimization under CSI error | PASS is more robust to CSI error than fixed arrays | Uncertainty is in the **channel**, not in PA positions | Robust PASS design line; different error source | web (arXiv 2512.18075) |
| Feng, Bedeer, Zeng, Li, Hao, Wen, *Robust Single- and Multi-Pinching Antenna Systems Under User Location Uncertainty* | preprint | 2026 | PHY / RA | Bounded user-location regions | S-procedure SDP (single PA); worst-case channel-gain evaluation plus BCD (multi-PA) | Reliable QoS under location error | **User** position uncertain; PA positions exact | Worst-case robust PASS placement; different error source | web (arXiv 2604.09774) |
| *Joint Power Allocation and Antenna Placement for PASS under User Location Uncertainty* (authors *verify*) | preprint | 2026 | RA | Gaussian user-localization error | Outage-constrained robust design | PASS energy efficiency degrades faster than fixed antennas as uncertainty grows | User location only | Motivates why PASS is location-sensitive | web (arXiv 2601.19704) |
| *Robust Resource Allocation for PASS under Imperfect CSI* (authors *verify*) | preprint | 2025 | RA | User position within a circular uncertainty region | Outage-constrained power minimization; bisection / PSO placement | Reliability kept for location errors up to 6 m | User location only | Same | web (arXiv 2507.12582) |
| Hadzi-Velkov, Poposka, Pejoski, Nallanathan, *Spatially Robust Near-Field SWIPT Using Pinching Antennas* | preprint | 2026 | PHY | Service-area coverage for SWIPT | Antenna selection for area-wide guarantees | Rate–energy trade-off bounds | User displacement, not PA errors | Adjacent robustness notion | web (arXiv 2606.20133) |
| Jiang, Xu, Lam, Liu, Nallanathan, *Discrete Coupling and Localized Motion for PASS* | preprint | 2026 | PHY | PAs moving among discrete positions; quantized coupling | Joint position / coupling / beamforming optimization | Practical hardware constraints handled by the optimizer | Optimizes within the discrete set; no error or degradation analysis | Position quantization is a structured position error | web (arXiv 2609.16293) |
| Wang, So, Ding, *PASS: From Antenna Placement to Antenna Roaming* | preprint | 2026 | PHY / RA | Finite PA movement speed | Dynamic programming; placement vs roaming | Trade-off between channel quality and usable time | No position-error analysis | Actuation-limited PASS | web (arXiv 2608.10136) |
| Yang, Wei, Su, Mei, Chen, Ning, *Movable Antenna-Enhanced Near-Field Flexible Beamforming: Performance Analysis and Optimization* | IEEE Trans. Veh. Technol. | 2026 | PHY | Near-field MA beam nulling and multi-beam | Taylor expansion plus **per-element box** position errors $|\Delta d_n| \le \epsilon$ (Sec. V, eqs. 37b/38b/52b); worst case via non-convex QCQP or closed form, with sign-based extremal patterns | Closed-form worst-case multi-beam gain under position error | Free-space MA (no guided-wave phase); Taylor-approximate model | Closest methodological analogue to our worst-case analysis. (Corrected 2026-09-25: an earlier version wrongly said ℓ2 ball.) | web (arXiv 2601.17825) |
| Chen, Qi, Dobre, Yuen, *Hybrid Pinching Antenna Systems: Architecture and Beamforming Design* | IEEE Trans. Wireless Commun., vol. 25, pp. 12129–12144 | 2026 | PHY | Multi-user PASS with reconfigurable leaky-wave antennas added | Sum-rate beamforming; **simulates multi-PA position errors** (Gaussian, variance about λ²) | Position errors cause pronounced degradation through phase misalignment; the hybrid design recovers up to 90% | Simulation only; mitigation needs extra hardware | **Closest multi-PA position-error work** (added 2026-09-25 from the novelty check) | web (DOI 10.1109/TWC.2026.3664320) |
| Su, Mei, Wei, Chen, Ning, *Movable Antenna-Enhanced Near-Field Beamforming: Impact of Antenna Position Errors* | FCN (conf.) | 2025 | PHY | Near-field MA | Position-error impact analysis | Degradation of nulling and beam gain | Conference version of the line above | Same | bib |
| Zhang et al., *Robust Beamforming and Antenna Position Optimization for MA-Assisted ISAC with Imperfectly Positioned MAs* | preprint | 2026 | PHY / ISAC | MA-ISAC with position errors | Worst-case robust design; common phase-response decomposition | Robust SINR / CRB design | Optimization-centric; MA, not PASS | Shows the field treats MA position error as a first-class issue | web (arXiv 2609.23323) |
| Ruze, *Antenna Tolerance Theory — A Review* | Proc. IEEE, vol. 54, pp. 633–640 | 1966 | Antenna | Reflector surface errors with spatial correlation | Statistical phase-error theory | Gain loss ≈ exp(−σ²) in rms phase error; correlation-radius effects; ≈ λ/16 rms rule | Statistical only (no deterministic worst case); reflector phase ∝ surface error | **Classical anchor** for our variance and covariance laws | web (IEEE Xplore 1446714) |
| Rondinelli, *Effects of Random Errors on the Performance of Antenna Arrays of Many Elements* | IRE Int. Conv. Rec. | 1959 | Antenna | Large arrays with random excitation errors | Statistical analysis | Mean gain loss and sidelobe rise | iid errors; statistical | Classical array tolerance | web (*verify*) |
| Elliott, *Mechanical and Electrical Tolerances for Two-Dimensional Scanning Antenna Arrays* | IRE Trans. Antennas Propag. | 1958 | Antenna | Scanning arrays | Tolerance analysis | Position and phase tolerance budgets | Statistical | Classical array tolerance | web (*verify*) |
| Poli, Rocca, Anselmi, Massa, *Dealing With Uncertainties on Phase Weighting of Linear Antenna Arrays by Means of Interval-Based Tolerance Analysis* | IEEE Trans. Antennas Propag., vol. 63, no. 7 | 2015 | Antenna | Interval phase errors | Analytic upper and lower power-pattern bounds | Certified bounds for phase uncertainty | Excitation phase, not physical displacement | Prior art for N1 (added 2026-09-25) | web |
| Arnestad et al., *Worst-case analysis of array beampatterns using interval arithmetic* | J. Acoust. Soc. Am. | 2023 | Array | Position, phase, amplitude, and coupling errors | Interval arithmetic plus back-tracking to the extremal error pattern | Certified bounds and the pattern that realizes them | Generic; not PASS | Prior art for N1's "bound plus realizing pattern" (added 2026-09-25) | web (arXiv 2306.13106) |
| Anselmi, Manica, Rocca, Massa, *Tolerance Analysis of Antenna Arrays Through Interval Arithmetic* | IEEE Trans. Antennas Propag. | 2013 | Antenna | Bounded excitation errors | Interval arithmetic giving **certified** pattern bounds | Guaranteed inclusion intervals for power patterns | Bounds usually conservative; no achievability; excitation errors, not position errors | Prior art for **certified deterministic** tolerance bounds | web (*verify* vol./pages) |
| JPL TMO Progress Report 42-175, *Combining Loss of a Transmitting Array due to Phase Errors* | tech. report | ~2008 | Antenna | Arrayed transmitters | Statistical combining-loss analysis | Loss vs phase-error variance | Tech report | Supports the variance-law background | web |

Also relevant, already in `fyp_report/latex/references.bib`: ding2025perspective, liu2026tutorial, xu2025downlink, wang2025noma, tegos2025uplink, ding2025isac, ouyang2024primer, and the fluid- and movable-antenna tutorials.

## Synthesis

1. **What the field solves.** PASS work in 2025–2026 is dominated by nominal design: placement, activation, and resource allocation. The robustness studies that exist almost all treat **user-location** or **CSI** uncertainty and solve robust optimization problems (S-procedure, outage constraints, BCD). Uncertainty in the pinching positions themselves appears in Pakravan et al. (a single radiating point) and in Chen et al., TWC 2026. Chen et al. show multi-PA position-error degradation **by simulation** and mitigate it with extra hardware. (Corrected 2026-09-25: an earlier version said only the single-antenna paper existed.)

2. **Clusters.**
   - (a) Robust PASS optimization under user or CSI uncertainty: 2507.12582, 2601.19704, 2604.09774, 2512.18075, 2606.20133.
   - (b) Performance analysis under PA activation error, single antenna: 2604.12156.
   - (c) Movable-antenna position-error analysis: Taylor expansion with per-element box errors and robust design (Yang et al. TVT 2026, Su et al. FCN 2025, 2609.23323).
   - (d) Classical tolerance theory: statistical (Ruze, Rondinelli, Elliott) and certified interval bounds (Anselmi et al.).

3. **What was already known in the project vs newly surfaced.** The graduation-report bibliography already had the PASS base papers and the MA position-error line. Newly surfaced here:
   - Pakravan et al. (pinching-position uncertainty) — must be cited;
   - four robust-PASS papers on user or CSI uncertainty;
   - classical tolerance theory (Ruze and the array-tolerance papers);
   - interval-arithmetic certified bounds.

4. **Strength of evidence.** Almost all 2026 PASS items are arXiv preprints, so the evidence is strong for the *landscape* but weak for venue status. Classical tolerance theory is mature. For iid errors, our variance law is essentially Ruze- or Rondinelli-type small-error theory with a PASS-specific sensitivity, so it **cannot be claimed as new by itself**.

5. **Remaining gap.** No paper found gives an *analytic, certified* account of how pinching-position errors break coherent phase alignment in multi-antenna PASS, or turns that account into a passive placement rule. Chen et al. show the degradation numerically. In particular, none of them:
   - identifies the guided-wave term making the actuation direction the most sensitive one ($\xi_n = n_{\mathrm{eff}} + \sin\theta_n$);
   - separates common and differential error modes;
   - gives a certified deterministic worst case under per-element (box) tolerances;
   - turns the sensitivity into a placement rule.

## Positioning Against Prior Art

| Our element | Closest prior art | What is PASS-specific or new |
|---|---|---|
| Variance loss law $1-\mathrm{Var}_\alpha(k_0\xi_n\delta_n)$ | Ruze 1966; Rondinelli 1959 | Not new as a law. New: the PASS mapping $\xi_n = n_{\mathrm{eff}} + \sin\theta_n$, which is centered at $n_{\mathrm{eff}}$, and the resulting common/differential split. |
| Covariance predictor for correlated errors | Ruze (correlation radius) | Weakly new: an explicit $M_\alpha D_\xi$ projection for per-element PASS errors. Present it as a tool, not a headline. |
| Deterministic first-order lower bound | Yang et al. 2026 (per-element box, Taylor, MA); Poli 2015 and Arnestad 2023 (interval bounds plus realizing pattern) | New if made **exact** (non-linearized) and paired with an achieving pattern; see N1. |
| Split-mode adversary | Yang et al. 2026 also use sign-based extremal patterns | Thin on its own. The quadratic model reduces to weighted number partitioning; the valid split gap bound is $k_0^2\epsilon^2(\sum\alpha\xi s)^2$. (The earlier $(\sum\alpha|\sin\theta|)^2$ bound was false for the aligned design.) |
| Tolerance-aware placement | Robust PASS designs target user or CSI error, not PA error | New; see N2. |

## Practical Takeaway

- **Dominant current approach:** robust optimization of PASS under user-location or CSI uncertainty.
- **Likely saturated:** another robust power-allocation or placement algorithm under user-location error.
- **Promising open direction:** analysis-driven robustness to the **pinching positions themselves**, meaning certified worst-case characterization and tolerance-aware placement. The guided-wave phase is what makes this problem distinct from the movable-antenna case.

## Candidate Novelty Additions (numerically prototyped 2026-09-25; scratchpad only, not yet in `results/`)

- **N0 (correctness prerequisite).** The graduation-report construction mirrors the positive-side solution to the negative side. Because the PASS phase is not even in $\Delta$, the upstream half is **not** phase-aligned: residual phases reach 0.68 rad and the raw nominal gain is 95.7% of $a_{\mathrm{ideal}}$. Solving the alignment equation on both sides (it has a unique root per wavelength level, since $\sin\theta + n_{\mathrm{eff}} > 0$) gives raw gain = $a_{\mathrm{ideal}} = 1.7775$. That exceeds the graduation report's best-found nominal comparator (1.7299, under that report's span constraint), so the "constructive loses on every metric" finding (C6) is likely an artifact.
- **N1 (certified worst-case sandwich).** An exact lower bound replaces $\xi_n$ with $\xi_n^+(\epsilon) = n_{\mathrm{eff}} + (\Delta_n^\star + \epsilon)/\sqrt{d^2 + (\Delta_n^\star + \epsilon)^2}$ (mean-value theorem). Evaluating the split mode exactly gives an upper bound. On the aligned $N = 16$ design, the true box worst case lies in an interval whose width peaks at about $2.82 \times 10^{-4}$ (numerically, near $\epsilon/\lambda \approx 0.125$) over the validity region (e.g., $[0.38230, 0.38253]$ at $\epsilon/\lambda = 0.10$), and exhaustive corner search always falls inside it. This removes the "best-found, not certified" weakness inside the validity region. By contrast, the graduation report's linearized bound is not guaranteed; it sits about $2 \times 10^{-4}$ above the exact bound.
- **N2 (tolerance-aware upstream placement).** Worst-case raw gain $\approx a_{\mathrm{nom}}(\theta_c)\cos^2(k_0\epsilon(n_{\mathrm{eff}} + \sin\theta_c))$, with $a_{\mathrm{nom}} \propto \cos^2\theta_c$. Shifting the aperture upstream (between feed and user) lowers $\xi$, so the optimum offset satisfies $\sin\theta^\star = -k_0\epsilon\cos^2\theta^\star\tan(k_0\epsilon(n_{\mathrm{eff}} + \sin\theta^\star))$. Prototype worst-case raw gain vs a centered placement:
  - $\epsilon/\lambda = 0.05$: $+1.9\%$;
  - $\epsilon/\lambda = 0.10$: $+38\%$ (0.936 vs 0.680);
  - $\epsilon/\lambda = 0.15$: $6.9\times$ (0.555 vs 0.081).
  Downstream offsets are always worse.
- **N3 (optional remark).** Drift of the waveguide index $\delta n_{\mathrm{eff}}$ produces the phase ramp $k_0\,\delta n_{\mathrm{eff}}\,\Delta_n$ (a differential mode), with loss $\approx k_0^2\,\delta n^2\,\mathrm{Var}_\alpha(\Delta)$. The same projection covers it, and the loss scales with aperture size.

## Sources

- https://arxiv.org/abs/2604.12156
- https://arxiv.org/abs/2512.18075
- https://arxiv.org/abs/2604.09774
- https://arxiv.org/abs/2601.19704
- https://arxiv.org/html/2507.12582
- https://arxiv.org/abs/2606.20133
- https://arxiv.org/abs/2609.16293
- https://arxiv.org/abs/2608.10136
- https://arxiv.org/abs/2601.17825
- https://arxiv.org/abs/2609.23323
- https://arxiv.org/abs/2501.05657
- https://ieeexplore.ieee.org/document/1446714/
- https://ui.adsabs.harvard.edu/abs/1966IEEEP..54..633R/abstract
- https://ieeexplore.ieee.org/iel6/8242/25880/01150784.pdf
- https://journals.sagepub.com/doi/abs/10.3233/JAE-150170
- https://www.researchgate.net/publication/255995629_Tolerance_Analysis_of_Antenna_Arrays_Through_Interval_Arithmetic
- https://tmo.jpl.nasa.gov/progress_report/42-175/175G.pdf
