# Novelty Check Report

Generated: 2026-09-25 by `/novelty-check`.
- Cross-model reviewer: `gpt-6-astra` at xhigh reasoning (thread `01a0d8a1-0f6a-72c2-9226-549f077c32b3`).
- Reviewer trace: `.aris/traces/novelty-check/2026-09-25_run01/`.
- Dossier: `.aris/novelty/NOVELTY_DOSSIER.md`.
- Paper existence check: `.aris/novelty/verified.json`. All 15 plus 2 cited papers have been found. Anselmi 2013, Rondinelli 1959, and Poli 2015 were confirmed by web search only; their bibliographic details still need `/citation-audit`.

Claude independently re-checked the reviewer's three factual corrections before accepting them (see "Verification of Reviewer Claims").

## Proposed Method

Study a **truly phase-aligned** single-user PASS under per-antenna bounded pinching-position errors. The analysis has three parts:
- a lower bound valid for the full nonlinear phase-and-distance model, paired with an exactly evaluated feasible adversary (a certified worst-case enclosure);
- use of that certificate to show when placing the pinching aperture **upstream** of the user (between feed and user) beats centered placement in worst-case received gain, despite its nominal path-loss penalty;
- the sensitivity $\xi_n = n_{\mathrm{eff}} + \sin\theta_n$ as the mechanism.

## Core Claims

1. **C1 — Sensitivity and weighted-variance / covariance law.**
   - Closest: classical phase-error tolerance theory (Ruze 1966; Rondinelli 1959; JPL TMO 42-175) and the PASS channel of Ouyang et al. 2025.
   - Delta: substituting the guided-plus-free-space position derivative into the weighted phase covariance identifies which mechanical error modes degrade PASS.
   - Judgment: mostly established; use as supporting mechanism. Narrow the wording: the variance law is a *phase-dominant* approximation, and "the actuation direction is the most sensitive" needs a defined comparison.

2. **C2 — Linearized bound and split pattern (graduation report).**
   - Closest: Yang et al. 2026 (per-element box errors, Taylor analysis, sign-based extremal pattern); interval-phase bounds (Poli et al. 2015).
   - Delta: thin as a standalone contribution.
   - Judgment: absorb into N1; no separate section.

3. **N1 — Nonlinear certified worst-case enclosure.**
   - Closest: Poli et al. TAP 2015 (analytic bounds for interval phase errors); Arnestad et al. JASA 2023 (interval arithmetic with position errors plus back-tracking to the extremal pattern); Yang et al. 2026 (Taylor analysis).
   - Delta: a directly evaluable certificate bounds the full nonlinear PASS gain under position boxes and quantifies a feasible adversary's remaining optimality gap.
   - Judgment: defensible but specialized. It has **not** been shown to be stronger than a matched interval-arithmetic construction. Claim nonlinear-model validity plus an explicit gap, not methodological superiority.

4. **N2 — Tolerance-aware upstream placement.**
   - Closest: nominal PASS placement (Ouyang et al. 2025); robust PASS under user or CSI uncertainty (Feng 2026, Sun 2025); hardware mitigation of multi-PA position errors (Chen et al., TWC 2026).
   - Delta: under the single-user model, lowering guided-plus-free-space phase sensitivity justifies giving up nominal path gain through upstream placement, with a certified improvement.
   - Judgment: **strongest engineering contribution**. No paper found contains it.

5. **N3 — Waveguide-index drift as a phase ramp.**
   - Delta: a straightforward corollary of C1.
   - Judgment: drop.

## Closest Prior Work

| Paper | Year | Venue | Overlap | Key Difference |
|---|---|---|---|---|
| Ouyang, Wang, Liu, Ding, *Array Gain for PASS* | 2025 | IEEE Commun. Lett. | Channel, coherent gain, alignment through position | No position tolerance; no effect of tolerance on placement |
| Chen, Qi, Dobre, Yuen, *Hybrid Pinching Antenna Systems: Architecture and Beamforming Design* (DOI 10.1109/TWC.2026.3664320) | 2026 | IEEE TWC | **Simulates multi-PA position-error degradation** (Gaussian, variance about λ²) through phase misalignment; mitigates with electronically reconfigurable leaky-wave antennas | Simulation only; extra hardware. Ours is analytic, passive (placement-based), and gives a worst-case certificate |
| Pakravan, Trigui, Ajib, Zhu (arXiv 2604.12156) | 2026 | preprint | Pinching-activation position uncertainty | A single radiating point and a secrecy metric; no coherent multi-element analysis |
| Yang, Wei, Su, Mei, Chen, Ning (arXiv 2601.17825) | 2026 | IEEE TVT | **Per-element box** MA position errors; Taylor analysis; QCQP and sign solutions | Movable antennas (no guided-wave phase); approximate model; no nonlinear certificate; no placement rule |
| Poli, Rocca, Anselmi, Massa, *Dealing With Uncertainties on Phase Weighting of Linear Antenna Arrays by Means of Interval-Based Tolerance Analysis* (vol. 63, no. 7) | 2015 | IEEE TAP | Analytic power-pattern bounds for interval phase errors | Excitation-phase errors, not physical displacement with coupled phase and amplitude; no placement consequence |
| Arnestad et al., *Worst-case analysis of array beampatterns using interval arithmetic* (arXiv 2306.13106) | 2023 | JASA | IA with position errors; back-tracking to the extremal error pattern | Generic; no compact PASS formula; no placement benefit shown |
| Anselmi, Manica, Rocca, Massa, *Tolerance Analysis of Antenna Arrays Through Interval Arithmetic* | 2013 | IEEE TAP | Certified interval tolerance analysis | Excitation errors; not PASS |
| Feng et al. (2604.09774); Sun, Ouyang, Wu, Liu (2512.18075) | 2025–26 | preprints | Robust PASS placement or beamforming | Uncertainty in user location or CSI, not in the radiating positions |
| Zhang et al. (arXiv 2609.23323) | 2026 | preprint | Robust MA-ISAC under per-element position boxes, including clearance constraints | Movable antennas; concurrent work |
| Ruze, *Antenna Tolerance Theory — A Review* | 1966 | Proc. IEEE | Statistical gain loss vs rms phase error and correlation | Statistical only; reflector setting |

## Overall Novelty Assessment

- **Score: 6/10.** Anchor: 5/10 means clear neighbors but a defensible delta.
- **Recommendation: PROCEED WITH CAUTION.** The idea clears the novelty gate but is not yet submission-ready. No named published paper contains the complete result, so ABANDON is unwarranted.
- **Key differentiator:** a simple nonlinear certificate makes a concrete passive placement decision reviewable, including a *guaranteed* improvement over centered placement.
- **What makes the delta thin (and what would make it carry):**
  - The generic mathematics (Taylor expansion, real-part projection, sign patterns) is elementary and close to interval tolerance theory. Present it as a tool, not as the headline.
  - Two literature gaps asserted earlier do not survive:
    - Yang et al. already use per-element boxes;
    - Chen et al. already show multi-PA position-error degradation.
  - N2's practical strength depends on the radiation pattern, waveguide loss, and placement constraints. At least one directional-radiation and waveguide-loss check with matched nominal baselines is needed.
- **Risk (what a reviewer would cite):** Chen et al. TWC 2026; Yang et al. TVT 2026; Poli et al. TAP 2015 / Arnestad et al. JASA 2023; Ruze 1966.

## Suggested Positioning

> For phase-aligned single-user PASS, we derive nonlinear gain bounds under bounded pinching-position errors and use them to certify when upstream placement improves worst-case received gain despite its nominal path-loss penalty.

Suggested title (reviewer): *Certified Position-Tolerance Bounds and Upstream Placement for Pinching-Antenna Systems*.

Lead with N2's design consequence, supported immediately by N1's certificate. Present C1 as established tolerance analysis specialized to the PASS channel. Drop:
- N3;
- a standalone C2 section;
- the stale placement-comparator story (C6), which rests on the unaligned design;
- most stochastic-law and frequency plots.

## Technical Findings From the Review (must be fixed before writing)

1. **N0 is a prerequisite.** On an unaligned array, subtracting per-element nominal phases changes the physical model. The graduation-report normalized curves cannot be repaired by rescaling; the main pipeline must regenerate results with the aligned design.
2. **The N1 lower bound is sound.** It relies on $\Phi' > 0$ and $\Phi'' > 0$, a per-element phase bound, the amplitude bound, a common-phase real-part projection, and every $\beta_n \le \pi/2$.
   - Tighter phase bound: the exact endpoint excursion $\hat\beta_n = \Phi(D_n + \epsilon) - \Phi(D_n)$.
   - The validity threshold is implicit in $\epsilon$; the reviewer computes $\epsilon_{\mathrm{valid}}/\lambda \approx 0.1714834$ for the corrected centered design.
   - The enclosure width peaks at about $2.816 \times 10^{-4}$ near $\epsilon/\lambda \approx 0.125$. Report it as a numerical maximum, not "at most $2.8 \times 10^{-4}$".
3. **The dossier's split-mode quadratic-gap bound is false** for the asymmetric aligned design. The actual gap is $9.894 \times 10^{-5}$ vs the claimed bound $9.857 \times 10^{-5}$ (per $k_0^2\epsilon^2$); Claude reproduced this. The valid statement is $Q_{\max} - Q(\epsilon s) \le k_0^2\epsilon^2(\sum_n\alpha_n\xi_n s_n)^2$. The number-partitioning reduction itself is correct.
4. **N2 surrogate.** The stationary equation $s = -t(1 - s^2)\tan[t(n_{\mathrm{eff}} + s)]$ is correct, and $\log F$ is strictly concave on the pre-null branch, so the optimum is unique. Since $F'(0) < 0$, a small upstream shift always helps while $t\,n_{\mathrm{eff}} < \pi/2$.
5. **Certified N2 improvements.** These use the upstream lower bound divided by the centered upper bound, with raw gain:
   - $\epsilon/\lambda = 0.05$: at least $+1.916\%$;
   - $\epsilon/\lambda = 0.10$: at least $+37.6\%$;
   - $\epsilon/\lambda = 0.15$: at least $6.86\times$.
6. **`offset.py` labels post-null corner minima as worst cases.** They are only corner-restricted upper bounds. At the centered design and $\epsilon/\lambda = 0.20$, the corner minimum is 0.055, while continuous search reaches about $10^{-18}$.
7. **N2 comparisons re-synthesize the aperture.** The span grows from 0.1117 m (centered) to 0.1817 m (−2 m offset); state this, or compare matched apertures. Clearance under independent boxes requires nominal gaps of at least $d_{\min} + 2\epsilon$.

## Minimum Evidence for 6 Pages (reviewer list, in priority order)

1. Certified raw-gain sandwiches vs offset and tolerance.
2. A compact sweep over $N$ and aperture-to-height ratio.
3. One directional-radiation and waveguide-loss sensitivity check with matched nominal baselines.
4. Explicit feed, movement-region, power, and clearance constraints.
5. The stationary-rule placement compared with a numerical search inside the same placement family.

## Verification of Reviewer Claims (Claude, 2026-09-25)

- **Yang et al. use per-element boxes — confirmed.** Constraints (37b), (38b), and (52b) read $|\Delta d_n| \le \epsilon$ in arXiv 2601.17825 (HTML). The earlier "ℓ2" description in `LIT_REVIEW.md` was wrong and has been corrected.
- **Chen et al. study multi-PA position errors — confirmed.** The TWC 2026 PDF text says: "increasing σ² causes a pronounced performance degradation … due to phase misalignment induced by PA positioning inaccuracies" (Fig. 8), and H-PASS "mitigate[s] the performance loss caused by position errors in continuous-position PAs by up to 90%".
- **The split-gap bound fails — confirmed** by exhaustive enumeration of $2^{16}$ sign patterns (numbers above).

## Sources

- https://arxiv.org/html/2601.17825#S5
- https://signal.seu.edu.cn/_upload/tpl/0a/67/2663/template2663/JournalFiles/TWC2026HPAS.pdf
- https://arxiv.org/abs/2604.12156
- https://arxiv.org/abs/2306.13106
- https://iris.unitn.it/handle/11572/118173
- https://arxiv.org/abs/2604.09774
- https://arxiv.org/html/2512.18075
- https://arxiv.org/html/2609.23323
- https://arxiv.org/html/2501.05657
- https://ieeexplore.ieee.org/document/1446714/
- https://tmo.jpl.nasa.gov/progress_report/42-175/175G.pdf
- https://www.mdpi.com/2079-9292/15/13/2965
