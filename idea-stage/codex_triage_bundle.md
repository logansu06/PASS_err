# Idea-Triage Bundle (Phase 4 jury)

This is the full annotated candidate set after merging and deduplication. Sources:
- your 12 ideas A1–A12 (thread `01a0dbdd…`);
- 10 Claude lens candidates L1–L10 (`idea-stage/lens_candidates.json`).

Merging was mechanical: clustered by hypothesis only; nothing was dropped for being "weak". No candidate failed the feasibility gate, since all are CPU-only and take 1–3 days.

## Context the Jury Must Respect

- **User-confirmed main thread:** AI methods for PASS and movable-antenna optimization, plus robust and **learning-based robust design** under hardware (pinching-position) errors.
  - **Baseline:** the graduation report plus yesterday's C1 / N0 / N1 / N2. It stays the comparison anchor and the analytic backbone.
  - **Style:** ICC / GLOBECOM / WCNC / MobiCom — a strong task, a clear structure, heavy mathematics.
- **Constraints:** ICC 2027 deadline 2026-10-02 (**6 days**); 6 pages including references; CPU-only NumPy/SciPy; one executor.
- **Pilot infrastructure (ready):** `idea-stage/pilots/pass_lab.py`. It includes:
  - the aligned design;
  - in-waveguide attenuation (dB/m, feed at −10 m) and a cos^q radiation pattern;
  - an exact certificate (endpoint phase excursion, plus an amplitude minimum from endpoints and closed-form stationary points; this fixes the issue you flagged);
  - the split-mode upper bound, corner enumeration, and Monte Carlo.
- **Pilot fact (verified):**
  - At 0.08 dB/m, the attenuation-aware nominal optimum sits at −0.10 m and the certificate optimum at −1.40 m for ε = 0.1λ; certified worst-case gain is 1.35× the nominal optimum's split upper bound.
  - At 1 dB/m: −1.2 m vs −2.6 m, 1.15×.
  - The aperture widens (0.114 → 0.158 m), so matched-aperture comparisons are still needed.

## Candidates (with annotations)

Each candidate lists `prior_work`, `so_what`, and `effort_note`.

**A1 — Learned actuator map plus a conformal residual certificate.**
- Learn a command→position distortion (backlash, drift) and compensate it.
- Certify the gain with N1 on conformal residual boxes (one simultaneous score).
- prior_work:
  - conformal prediction (established);
  - PASS meta-learning under *user* uncertainty (2601.00115);
  - MA robust learning under distortion, synchronization, and CFO (Xiu et al. 2508.13839, TWC 2026 DOI 10.1109/TWC.2026.3652128, 2507.16132).
- so_what: turns "tolerance ε" from a datasheet guess into a learned, calibrated quantity with a received-gain guarantee.
- effort_note: 1.5–2 days. The actuator distortion model must be *simulated*, so realism is the reviewer risk.

**A2 (+L9) — Power-probe calibration.** Learned harmful mechanical modes, symmetric dithers $g(\delta-u)-g(\delta+u) = 4u^TQ\delta$, then re-pinching, then an N1 residual certificate.
- L9 variant: REV-style sliding of each pinch by fractions of λ_g, with three power samples per element; a closed form.
- prior_work:
  - REV power-only calibration (Mano–Katagi line; IEEE 9445668);
  - PASS failure detection with tagged pilots (2602.17257);
  - MA self-calibration DOA (2605.23140);
  - MA-ISAC position-error estimation (2609.23323);
  - robust MA DOA with gain/phase errors (WCL 2026).
- so_what: a closed-loop fix PASS needs, since PASS has one RF chain per waveguide and cannot measure per-element CSI. The sensing math is clean.
- effort_note: 2 days. Your pilot used supplied modes; the learned-mode benefit needs actuator statistics that are genuinely low-rank. **Your own note: PASS physics alone gives Q nearly isotropic**, so low rank must come from the actuator.

**A3 — Learn the error covariance from activation-subset probes** (half-array activation separates iid from split), then plan placement for that covariance.
- prior_work: PASS failure detection (observability); covariance / tolerance theory (Ruze).
- so_what: identifies whether a deployment's errors are harmful-differential or benign-common before choosing placement.
- effort_note: 1.5–2 days. Assumes switchable activation and stationarity during probing.

**A4 (+L1, L2) — Verified learned placement.**
- A learned shortlist, amortized policy, or deep-unfolded optimizer proposes N0-aligned layouts.
- An N1 verifier accepts or rejects each; N2 is the fallback.
- Guarantee: $L(x_{\rm out}) \ge L(x_{\rm N2})$.
- prior_work: PASS GNN with a feasibility readout (Xie–Lu–Ding 2502.05447); DRL placement (2605.08039); MA deep unfolding.
- so_what: learning supplies speed; the verifier supplies the hardware-error guarantee.
- effort_note: 1 day. **Risk:** single-user placement may be cheap enough to scan exhaustively, which would make the learning decorative unless the family is rich (heterogeneous tolerances, blocked sites, multi-user).

**A5 — Learned feasible adversaries for certified pruning** of a finite placement family.
- prior_work: Arnestad et al. (interval arithmetic plus back-tracking), JASA 2023.
- so_what: faster certified max–min search when heterogeneous errors break the split pattern.
- effort_note: 1–1.5 days. The homogeneous N2 family is a negative control, since its enclosure is already tight.

**A6 — Learned actuator reliability plus certified subset selection.**
- Sort by $b_i = A_i^-\cos\beta_i$, giving $O(N\log N)$.
- Removal rule: drop element $j$ if $b_j/\sum b < 1-\sqrt{(m-1)/m}$.
- prior_work: Viterbi discrete PASS selection (2512.20389); two-state PASS laws (Tyrovolas).
- so_what: a clean theorem; learning estimates per-actuator tolerance.
- effort_note: 1 day. The effect may need strong heterogeneity.

**A7 — Learned robust interference suppression (nulling).**
- Select N of M phase-equivalent sites.
- Leakage upper certificate $(B+R)^2$, plus a desired-gain lower certificate.
- prior_work: FullPASS (2607.19546); Yang et al., movable-antenna nulling under box errors (TVT 2026); Chen et al., hybrid PASS (TWC 2026).
- so_what: nulls are far more tolerance-fragile than main-beam gain, which fits the E6 gap.
- effort_note: 2 days, with a day-1 gate on how tight the leakage certificate is. Requires a multi-receiver model (desired plus protected user).

**A8 — Theorem: the tolerance-induced upstream shift beyond the attenuation-aware optimum.**
- Log-concavity; a unique maximizer that moves upstream monotonically as ε grows; directivity parameter q ≥ 0.
- prior_work: Xu et al. 2506.23966 (attenuation-aware nominal placement); switched-feed PASS 2607.12646; CMT-aware 2608.03787.
- so_what: makes N2 a complete, lossy, provable design rule, and our pilot already supports it.
- effort_note: 1 day. Analytic only; not AI-centered.

**A9 — Actuator-precision allocation.** $\epsilon_n \propto (c_n/(A_n\xi_n^2))^{1/(p+2)}$, a convex program.
- prior_work: interval tolerance allocation; general tolerance design.
- so_what: a hardware-budget design law.
- effort_note: 1 day. Generic tolerance allocation is not new.

**A10 (+L8) — Certified dynamic programming on a finite actuator grid** (interval scheduling per projection angle); also yields a coherent multi-active grid-density law.
- prior_work: Viterbi discrete PASS; Tyrovolas et al. (single active PA); sparse fluid-antenna arrays (2605.19455, sinc² quantization loss).
- so_what: global optimization of the certified objective for discrete PASS.
- effort_note: 1.5–2 days.

**A11 (+L4) — Structured common + differential error boxes; error-type mode theory.** Explains why PASS is "robust" to CSI or user-location errors (common-mode) but "fragile" to pinching errors (guided-term differential). Also relaxes the clearance requirement.
- prior_work: correlated-error tolerance theory; C1 itself.
- so_what: resolves an apparent contradiction in the PASS literature and changes placement and packing.
- effort_note: 1–1.5 days.

**A12 (+L7) — Density–placement reversal and tolerance-limited scaling.** Under a fixed aperture length, the sign of the optimal shift reverses near ε/λ ≈ 0.072; tolerance-limited $N^*(\epsilon)$.
- prior_work: Ouyang et al. (optimal antenna count, nominal).
- so_what: a surprising mechanism that fixed-N N2 does not have.
- effort_note: 1–2 days. The reversal may vanish under integer spacing constraints.

**L5 — Distributionally robust placement** (Wasserstein or moment ambiguity on the error covariance, via the covariance predictor).
- prior_work: Wasserstein DRO beamforming (2506.01154); robust MA placement under CSI error (2505.07035).
- so_what: sits between box-conservative N2 and optimistic nominal placement.
- effort_note: 2 days.

**L6 — Joint user-location and pinching-error robust placement.**
- prior_work: robust PASS under user location (2604.09774, 2601.19704).
- so_what: shows which uncertainty dominates at mmWave.
- effort_note: 2 days.

**L10 — Certificate-shaped robust DRL for mobile users,** with N2 as warm start and safety fallback.
- prior_work: DRL PASS with mobility (2605.08039); safe RL (2604.17032).
- so_what: online adaptation with a certificate.
- effort_note: 2–3 days; high risk under the deadline.

## Your Job (rank; do not rewrite)

For each candidate:
- make the strongest case **for** it (what would make it the paper people cite);
- state the strongest reviewer objection;
- state the most likely failure mode;
- say whether its prior_work note is a real novelty problem or differentiable.

Then rank by expected information and upside **within 6 days and 6 pages**. Name the 2–3 you would actually pilot today, with a **concrete CPU pilot and decision criterion** for each: what positive, negative, and null outcomes would teach.

Constraints on the ranking:
- Answer each objection or record it as a named risk; never absorb it by adding modules.
- Complexity added since the brainstorm is a red flag.
- If your top set is all low-risk, name the high-upside idea that deserves a pilot slot.

Finally, propose **the paper architecture** that best combines the baseline with the chosen idea(s) into one ICC paper with a single thesis. The main thread must stay learning-based robust design, with the analytic baseline as backbone and comparator.
