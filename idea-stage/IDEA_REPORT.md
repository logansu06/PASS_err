# Idea Discovery Report

**Direction**: Using the current results and the graduation-report content, find new ideas that raise the novelty of the ICC 2027 paper. Target the style of recent Globecom / ICC / WCNC / MobiCom papers: a strong task, a clear structure, and heavy mathematics. AI methods may be introduced. Give GPT-6 Astra more room.
**Date**: 2026-09-26
**Pipeline**: research-lit (comm-lit-review) → idea-creator → novelty-check → research-review → research-refine-pipeline
**Run state**: `.aris/runs/pass-icc27-novelty-20260926.json`
**Hard constraints**:
- ICC 2027 paper deadline is 2026-10-02 (6 days left).
- 6 pages including references.
- CPU-only NumPy/SciPy simulation; no GPU needed.

## Executive Summary

**Selected idea: A7, certified robust-SLNR site selection for pinching-antenna systems under actuator position errors, without learning.**

From 15 candidates (12 GPT-6 Astra `ultra` ideas plus Claude lens candidates), the cross-model jury piloted A7 and A2.
- **A7:** strong mechanism (certified SLNR gain over nominal selection that survives exhaustive-nominal and identical-endpoint controls in reviewer reruns). The learning component failed its gate and was dropped.
- **Novelty:** A7 6/10 PROCEED (closest: FullPASS; Zhang et al. 2609.23323 on MA enclosures).
- **External review:** proceed without learning; mock ICC 4/10 before repairs.
- **Two refinement rounds** raised it to **7.70/10**, with an estimated 60–70% ICC acceptance if the matched-endpoint result holds.

**Next step:** run the M0/M1 experiments in `refine-logs/EXPERIMENT_PLAN.md`. Experiments are on hold per the user's instruction.

### 🏆 Idea A7 — Certified Robust-SLNR Site Selection for PASS — RECOMMENDED

- **Method (what we actually do):**
  1. Build M candidate pinching positions that are all phase-aligned for the desired user D. These come from the graduation-report construction, corrected so that both sides are aligned.
  2. For any choice of N positions, compute in closed form a guaranteed lower bound on D's received power and a guaranteed upper bound on the power leaking to a protected user P, valid for **every** actuator error up to ±ε per antenna.
  3. Pick the N positions that maximize the guaranteed SLNR by swap search, started from the best error-free (nominal) choice.
  4. Prove the pick is better by showing that its guaranteed lower bound exceeds a feasible worst-case value of the best nominal choice.
- **Hypothesis:** nominal interference nulls in PASS are fragile under sub-wavelength actuator errors. Certified selection within the same candidate family gives certifiably higher worst-case SLNR.
- **Minimum experiment:** R001–R006 in `refine-logs/EXPERIMENT_TRACKER.md` — sanity checks plus the 1,320-case grid against exhaustive nominal selection, with identical endpoints.
- **Expected outcome:** certified dominance in a substantial reported fraction of the grid. If the gains vanish with identical endpoints, the claim is reframed as depending on aperture freedom (claims matrix).
- **Novelty:** 6/10 — closest: FullPASS (2607.19546), Zhang et al. (2609.23323), Arnestad et al. (JASA 2023).
- **Feasibility:** CPU-only, under 3 CPU-hours; driver `a7_main.py` ready.
- **Risk:** MEDIUM.
- **Contribution type:** method + theory (certificates, dominance) + design evaluation.
- **Pilot result:** POSITIVE for the mechanism; NEGATIVE for learning (dropped).
- **Reviewer's likely objection:** "established bounding tools". Answer: the audited PASS design result against the strongest matched comparator carries the paper.
- **Why we should do this:** it has the strongest task, structure, and mathematics among the candidates; the evidence is already positive under strong controls; and it fits 6 pages.

### Idea A2 — Power-Probe Calibration — BACKUP (not combined with A7)

- Mechanism positive: fixed DCT probes take normalized gain from 0.96 to 0.998 in 6 readings.
- Learned modes help only for stable device modes.
- Novelty 5/10, CAUTION.
- Missing its residual certificate.

## Literature Landscape

Builds on `idea-stage/LIT_REVIEW.md` (2026-09-25; full table and sources) and `idea-stage/NOVELTY_REPORT.md`. Sources for this run:
- Zotero and Obsidian: not configured; skipped.
- Local library: no `papers/` folder.
- Gemini CLI: installed but not authenticated (`GOOGLE_CLOUD_PROJECT` unset); skipped.
- Web search: IEEE, arXiv, and publisher pages.

### A. How PASS papers look at ICC / Globecom / WCNC in 2025–2026

- **The topic is hot and has a dedicated venue track.**
  - GLOBECOM 2026 has a PASS workshop (WS-17) and a tutorial (TUT-02).
  - WCNC 2026 had a PASS tutorial (T03) and PASS papers (e.g., movable-waveguide PASS).
- **Dominant paper template**, which is the "strong task, strong structure" style the user wants:
  - one concrete system task (rate, power, secrecy, ISAC, SWIPT);
  - a non-convex joint placement + beamforming problem;
  - structural decomposition (closed-form single-user optimum, alternating optimization, SCA, or BCD);
  - one to three propositions or theorems (closed forms, bounds, scaling laws);
  - simulations against fixed-antenna and heuristic baselines.
  - Examples: Ouyang et al., *Array Gain for PASS* (IEEE CL 2025); *Constrained Pinching Antenna Array Design for Sum-Rate Maximization in Multi-User PASS* (arXiv 2606.03830); *Dual-Scale Antenna Deployment* (arXiv 2510.27185); *PASS with Movable Waveguides* (arXiv 2609.16831).
- **Robust PASS work (all 2025–2026)** handles **user-location** or **CSI** uncertainty with robust optimization:
  - S-procedure / SDP (2604.09774);
  - outage-constrained designs (2507.12582, 2601.19704);
  - robust beamforming under channel error (2512.18075);
  - service-area robustness (2606.20133).
- **Pinching-position uncertainty itself** has only two treatments:
  - Pakravan et al. (2604.12156): a single radiating point, secrecy outage;
  - Chen–Qi–Dobre–Yuen, TWC 2026, *Hybrid PASS*: **simulated** multi-PA position-error degradation, mitigated with extra reconfigurable leaky-wave hardware.

### B. AI for PASS and spatially reconfigurable antennas

- **DRL:** joint beamforming and placement under user mobility (arXiv 2605.08039, DDPG).
- **LLM:** antenna partitioning for segmented PASS (arXiv 2604.10372).
- **GNN / attention:** two-state PASS activation (arXiv 2507.06222).
- **Learned beamforming:** PASS-ISAC for low-altitude networks (arXiv 2512.04293).
- **Graph transformer** for tri-beamforming (JSAC 2026; reported by search, *verify*).
- **Survey:** *AI for Spatially Reconfigurable Antennas: Movable, Fluid, and Pinching* (arXiv 2608.00255).
- **Movable antennas:** deep unfolding for position plus beamforming (two-timescale DUNN); gradient-based meta-learning for secure MA-ISAC (arXiv 2608.12870); DL position optimization with partial CSI (arXiv 2606.17543).
- **Pattern:** AI is used almost exclusively as a *fast approximate optimizer* for nominal (error-free) placement. None of these works gives a performance guarantee under hardware error. Guarantee-carrying learning exists outside PASS: worst-case certification of trained networks (e.g., MILP verification in *Learning Optimal Power Flow: Worst-Case Guarantees for Neural Networks*); safe or constrained RL for wireless (arXiv 2604.17032).

### C. Estimating and calibrating position errors

- **Movable antennas:** self-calibration DOA estimation with unknown antenna position errors, via alternating MUSIC and closed-form error estimates (arXiv 2605.23140); CRB-driven robust MA placement (2601.21997, 2606.23154).
- **PASS:** phase-aware **user** localization with a CRLB (arXiv 2602.21162). **No PASS paper found that estimates or calibrates the pinching positions themselves** from pilots or feedback. The PASS tutorial (arXiv 2508.07572) notes that closed-loop actuators with position sensors are needed and costly.

### D. Classical and array tolerance theory (from `LIT_REVIEW.md`)

- Ruze 1966 (statistical phase-error gain loss, including correlation).
- Rondinelli 1959 and Elliott 1958 (array tolerances).
- Poli et al. TAP 2015, Anselmi et al. TAP 2013, Arnestad et al. JASA 2023 (interval-arithmetic certified bounds plus back-tracking to the extremal pattern).
- Yang et al. TVT 2026 (movable antennas, per-element box, Taylor worst case).

### E. Structural gaps

1. **Analytic + certified** robustness for multi-PA coherent PASS under pinching-position errors. Chen et al. only simulate; Yang et al. are approximate and movable-antenna only.
2. **Tolerance-aware PASS placement.** Every robust PASS design targets user or CSI uncertainty, not the radiating positions.
3. **Pinching-position error estimation and closed-loop re-pinching.** This exists for movable antennas, not for PASS.
4. **AI under hardware error with guarantees.** PASS learning papers optimize nominal models; none certifies robustness or uses an analytic robustness object as a training signal or safety filter.
5. **Discrete PASS grids as structured position errors.** Discrete-activation papers report that very dense grids are needed (e.g., over 300 positions per meter, arXiv 2505.02864), but no closed-form grid-density law was found.

### F. Broad discovery by GPT-6 Astra (replacing the unavailable Gemini pass)

Thread `01a0dbc6-1722-74a3-87ba-1e6cac86eae8`; trace in `.aris/traces/idea-discovery/`. The reviewer reports every item below with high existence confidence (arXiv, publisher, or institutional record). **Claims about theorem-level content are the reviewer's reading and have not been re-checked.**

| # | Paper | ID / venue | Why it matters for us |
|---|---|---|---|
| F1 | Xu, Ding, Schober, Chang, *PASS with In-Waveguide Attenuation: Performance Analysis and Algorithm Design* | arXiv 2506.23966 (2025) | **The attenuation-optimal single-PA position already lies toward the feed.** N2 must isolate the *tolerance-induced* shift relative to an attenuation-aware nominal optimum. |
| F2 | Jiang, Schotten, *Switched-Feed PASS for Wideband THz* | arXiv 2607.12646; VTC 2026-Fall | Feed-side placement and feed switching under loss; recent neighbor to N2. |
| F3 | Luo, Zhou, Papanikolaou, Liu, Qiu, *CMT-Aware Channel Modeling and Transmit-Power Minimization for PASS* | arXiv 2608.03787 | Directional, lossy, coupling-length model with downstream power depletion. Upstream moves change the power left for later PAs. |
| F4 | Wang, Xu, Ouyang, Mu, Liu, *Multiport Network Modeling … Reconfigurable PASS* | npj Wireless Technol. 2026, DOI 10.1038/s44459-026-00071-w | Physically grounded model-validity reference. |
| F5 | Cui, Xiao, Wang, Su, Wu, *Movable-Signal and Pinching-Antenna for ISAC* | IEEE TWC 2026, DOI 10.1109/TWC.2026.3708419 | Worst-user gain guarantees and a QoS feasibility certificate. **Do not claim the "first certified PASS design".** |
| F6 | Tyrovolas et al., *Ergodic Rate Analysis of Two-State PASS* | arXiv 2511.01798; ICC Workshops 2026 | Closed-form discrete-PASS laws, with a single active PA. |
| F7 | Tyrovolas et al., *How Many Pinching Antennas Are Enough?* | arXiv 2512.18761 | Candidate-site count and spacing vs outage and rate; single active PA; **closest to the grid-density idea.** |
| F8 | Galanopoulou et al., *Viterbi State Selection for Discrete PASS* | arXiv 2512.20389 | Baseline for multi-active discrete selection. |
| F9 | Wu et al., *Sparse Fluid Antenna Arrays* | arXiv 2605.19455 | Sinc² loss under uniform position quantization (free-space steering). |
| F10 | Xie, Lu, Ding, *Graph Neural Network Enabled Pinching Antennas* | arXiv 2502.05447 | PASS GNN with a feasibility-preserving readout; nominal only. |
| F11 | Musri et al., *Adaptive Pinching Antenna Optimization via Meta-Learning* | arXiv 2601.00115 | Uncertainty-aware PASS learning (user uncertainty). |
| F12 | Xiu et al., *Distributed Distortion-Aware Robust Optimization for MA-aided Cell-Free ISAC* | arXiv 2508.13839 | **Robust learning (GNN) under MA hardware impairment already exists.** |
| F13 | Xiu et al., *Robust Optimization for MA-Aided Cell-Free ISAC With Time Synchronization Errors* | IEEE TWC 2026, DOI 10.1109/TWC.2026.3652128 | Worst-case plus meta-RL under a phase-related impairment. |
| F14 | Xiu et al., *Meta-RL for MA-aided FD CF-DFRC with CFO* | arXiv 2507.16132 | Same line. |
| F15 | Su et al., *Learning-Based Robust Jamming Suppression With MA Arrays* | IEEE CL 2026, DOI 10.1109/LCOMM.2026.3681607 | Robust learning under jammer-angle uncertainty. |
| F16 | Ouyang, Jiang, Wang, Liu, Ding, *Failure Detection for PASS* | arXiv 2602.17257 | **Tagged-pilot observability through a single RF chain**; a starting point for offset calibration. |
| F17 | Zhang et al., *Integrated Positioning and Communications for PASS: A Robust Approach* | arXiv 2605.26517 | Estimation-to-communication workflow (user positions). |
| F18 | Zhang et al., *Uplink Positioning for PASS in Multipath* | arXiv 2607.20069 | Multicarrier machinery reusable for offset estimation. |
| F19 | Shan, Ouyang, Popovski, Liu, *Access Protocols for SWANs* | arXiv 2606.04913 | Pilot-assisted acquisition in segmented PASS. |
| F20 | Ye et al., *Robust DOA Estimation for MA Arrays With Partial Gain and Phase Errors* | IEEE WCL 2026, DOI 10.1109/LWC.2025.3630221 | Flexible-array self-calibration baseline. |
| F21 | Zhao, Hu, Mishra, Ng, *Robust and Secure Blockage-Aware PA-assisted Wireless Communication* | arXiv 2601.06430 | Geometric uncertainty of the eavesdropper array. |
| F22 | Sun, Mu, Ouyang, Shang, Liu, *Robust Beamforming for PASS-Based Multi-User Communications* | IEEE WCL 2026, DOI 10.1109/LWC.2026.3688031 | Worst-case multi-user QoS under bounded CSI error. |
| F23 | Hong et al., *Sensing-Assisted Anti-Blockage PASS* | arXiv 2608.21859; IEEE MASS 2026 | Uncertainty-aware mechanical PASS operation. |
| F24 | Barzegar Astanjin et al., *FullPASS: Geometry Optimization for Full-Duplex PASS* | arXiv 2607.19546 | Nominal self-interference nulling; **nulls are more fragile than main-beam gain**, so tolerance matters here. |

**Updated collision assessment (reviewer):**
- *Nonlinear multi-PA position-box enclosure:* no duplicate found, but methodological proximity to interval analysis.
- *Broad "upstream placement" claim:* high risk (F1–F3). The *tolerance-induced shift* over the attenuation-aware nominal optimum remains open.
- *Coherent multi-active grid-density law:* plausible (F6–F9 are single-active or free-space).
- *AI with guarantees:* generic robust learning is occupied (F12–F15). A **verified lower gain bound under actuator boxes** is the narrow open property.
- *PASS offset calibration:* the strongest PASS-specific opportunity, via single-feed observability, guided phase, and tagged pilots (F16).

**Updated gaps.**
- E2 (tolerance-aware placement) must now be measured against attenuation-aware nominal placement.
- E4 (AI with guarantees) narrows to *verifier-backed learning under actuator boxes*.
- E5 (grid law) narrows to *coherent multi-active PAs*.
- New **E6**: position-tolerant **nulling / full-duplex / multi-user interference** tasks, where tolerance matters more than for main-beam gain.

## Ranked Ideas

**Summary of the ranking:**
- 15 deduplicated candidates.
- Cross-model jury (GPT-6 Astra `ultra`): 1 A7, 2 A2, 3 A12, 4 A1, 5 A10.
- Pilots: A7 mechanism POSITIVE, learning NEGATIVE; A2 mechanism POSITIVE, learning WEAK.
- Final selection after novelty check and external review: **A7 without learning** (RECOMMENDED); A2 as BACKUP.

Details follow.

### Candidate pool (Phase 2; generation, not verdicts)

- **Generator 1:** GPT-6 Astra at `ultra` (thread `01a0dbdd-9f51-75d3-9506-f811e9dc6602`; trace `.aris/traces/idea-creator/2026-09-26_run01/`). It produced 12 ideas, A1–A12: 7 learning-based and 5 analytical.
- **Generator 2:** Claude lens enumeration (Tier 3, no subagents) produced L1–L10. After mechanical dedup, L1/L2 merged into A4, L4 into A11, L7 into A12, L8 into A10, and L9 into A2. L5, L6, and L10 stay separate.
- Per the user's instruction, no gpt-5.5 second pass was run.
- **Feasibility gate (Type-A):** nothing dropped; all 15 candidates are CPU-only and take 1–3 days.
- Full annotated set: `idea-stage/codex_triage_bundle.md`.

| ID | Idea (one line) | Type | Learning role | Risk |
|---|---|---|---|---|
| A1 | Learned actuator map, with conformal residual boxes certified through N1 | learning / method | learns unknown command→position distortion | MED |
| A2 | Power-probe calibration: learned mechanical modes + symmetric dithers ($4u^TQ\delta$ identity), then re-pinching and a residual certificate (L9 REV-style variant) | learning / estimation | learns the low-rank harmful error subspace | HIGH |
| A3 | Error-covariance identification from activation-subset probes, then covariance-aware placement | learning / estimation | learns deployment error correlation | HIGH |
| A4 | Verified learned placement: shortlist, policy, or unfolding, checked by an N1 verifier with N2 fallback | learning / algorithm | amortized search | MED |
| A5 | Learned feasible adversaries for certified max–min pruning | learning / algorithm | learns counterexamples | MED |
| A6 | Learned actuator reliability plus sort-optimal certified subset selection | stats-learning / theory | learns per-actuator tolerance | MED |
| A7 | Learned robust nulling / interference suppression with leakage and gain certificates | learning / theory | branch-subset scoring | HIGH |
| A8 | Theorem: tolerance-induced upstream shift beyond the attenuation-aware optimum | theory | — | LOW |
| A9 | Actuator-precision allocation law | theory / optimization | — | LOW–MED |
| A10 | Certified DP on a finite actuator grid; coherent multi-active grid law | theory / algorithm | — | MED |
| A11 | Structured common + differential boxes; error-type mode theory | theory / diagnostic | — | LOW–MED |
| A12 | Tolerance-driven density–placement reversal; $N^*(\epsilon)$ | theory / mechanism | — | MED |
| L5 | Distributionally robust placement over the error covariance | method | — | MED |
| L6 | Joint user-location + pinching-error robust placement | method | — | MED |
| L10 | Certificate-shaped robust DRL under mobility | learning | online policy | HIGH |

### Phase-4 jury ranking (GPT-6 Astra, `ultra`; same thread; trace `.aris/traces/idea-creator/2026-09-26_run01/002-phase4-triage-ultra`)

The jury ran read-only numerical checks on `idea-stage/pilots/pass_lab.py` before ranking. Its checks changed four candidates materially:
- **A4 is demoted.** A vectorized scan of 4,096 heterogeneous-tolerance layouts takes about 2.6 ms, so learning is decorative for single-user placement.
- **A3 is demoted.** iid and split errors select the same offset, and the oracle gain is only about 0.14%.
- **A12's reversal is real.** It survives discrete phase levels and robust clearance ($N_{\max}=64$) and vanishes at a fixed $N=16$. Keep it as a separate analytic direction.
- **A7's certificate is useful, but its benefit is uneven.** In a 4-of-12 toy, the certified SLNR gain is +18.3% at $0.03\lambda$ and +26.5% at $0.05\lambda$. Only 4/31 and 7/31 geometries exceed 5%, and just 2/31 with identical endpoints.

| Rank | ID | Jury disposition |
|---:|---|---|
| 1 | **A7** learned robust nulling (robust **SLNR**) | Strongest task. Risk: deterministic robust search may already be enough, so learning must beat it at matched quality and runtime. Pilot today. |
| 2 | **A2 (+L9)** power-probe calibration | Clearest calibration task. Risk: actuator-mode assumptions. Learned PCA ties fixed DCT on smooth modes, helps on stable device modes (0.9729 vs 0.9448), and hurts when modes change. Pilot today. |
| 3 | A12 (+L7) density–placement reversal | Strongest new analytic finding. No learning role, so it stays a separate direction. |
| 4 | A1 learned actuator map | Learning-based reserve. Risk: data realism; benchmark it against simple bias correction. |
| 5 | A10 (+L8) certified grid DP | Rigorous, but the exact DP removes any role for learning. |
| 6 | A5 learned adversarial pruning | Better adversaries cannot fix a loose lower bound. |
| 7 | A3 covariance from subset probes | Low decision value (see above). |
| 8 | A8 attenuation-matched upstream theorem | Keep as **backbone and comparator**, not the headline. |
| 9 | A6 reliability plus subset selection | Too elementary to carry the paper. |
| 10 | L5 DRO placement | Modest method novelty. |
| 11 | A4 (+L1, L2) verified learned placement | Decorative learning (see above). |
| 12 | A11 (+L4) error-mode theory | Supporting only. **Correction:** longitudinal user error contributes about $-k_0 s_n u$; it is not harmless. |
| 13 | L6 joint location + pinching | Weak standalone novelty. |
| 14 | A9 precision allocation | Generic; no credible cost model. |
| 15 | L10 certificate-shaped DRL | Missing a sequential task. |

**Jury-proposed architecture:** an A7 paper with C1 / N0 / N1 / N2 as the analytic backbone.
- Thesis: *learning to select phase-equivalent pinching sites accelerates interference-aware robust PASS design, while nonlinear desired-gain and leakage bounds verify every returned placement under actuator errors.*
- Fallback: if A7 fails its learning gate and A2 passes, switch the whole paper to A2. Do not combine the two.

**Closeness to the graduation report** (user question, 2026-09-26):
- Close: A8, A11, A12 extend it directly.
- Far: A7 and A2 reuse the graduation-report model and C1/N1 as tools but add new tasks (a protected receiver; closed-loop calibration).
- Every candidate keeps the graduation report + N0–N2 as its comparison baseline.

### Pilot results (Phase 5 of idea-creator; CPU, 2026-09-26)

Scripts are in `idea-stage/pilots/`: `pass_lab.py`, `a7_pilot.py`, `a7_learn.py`, `a2_pilot.py`. All certificates use the exact model (endpoint phase excursions, exact amplitude extrema). The A7 leakage bound is a complex-plane **sector enclosure** with a θ-grid Lipschitz pad, not a Taylor expansion.

**A7, mechanism gate (robust vs nominal site selection; jury gate: >5% certified improvement in ≥20% of cases) — POSITIVE.**

Setup:
- Desired receiver D at the origin. Protected receiver P at 33 predefined positions: $x_P \in [-6, 6]$ m, $y_P \in \{1, 2, 4\}$ m.
- $N = 8$ of $M = 24$ D-aligned sites; equal power split.
- Certified improvement = $L_{\rm SLNR}(S_{\rm rob}) / U_{\rm SLNR}(S_{\rm nom}) - 1$, i.e., the robust design's lower bound over the nominal design's feasible-adversary upper bound.

| $\sigma^2$ | $\epsilon/\lambda$ | Common region: >5% | median | max | Identical endpoints: >5% | median |
|---|---|---|---|---|---|---|
| 1e-3 | 0.03 | 21/33 (64%) | +10.8% | +52% | 19/33 (58%) | +6.8% |
| 1e-3 | 0.05 | 26/33 (79%) | +14.0% | +93% | 20/33 (61%) | +9.5% |
| 1e-2 | 0.03 | 16/33 (48%) | +4.4% | +34% | 14/33 (42%) | +1.1% |
| 1e-2 | 0.05 | 20/33 (61%) | +5.8% | +75% | 20/33 (61%) | +8.9% |

Additional observations:
- Robust and nominal selections never coincided (0/33).
- The **median** upper-to-lower bound ratio of the robust design was 1.01–1.04.

> **Correction (external review, 2026-09-26):**
> - The ratio is **not** uniformly this tight. At $P = (0, 1)$ it reaches $U/L = 1.2226$ (all-corner witness $(1,1,1,1,-1,-1,-1,-1)$), where the desired and leakage responses are co-aligned. Report the median, upper quantiles, and maximum.
> - The identical-endpoint numbers above came from an **unarchived** inline driver; `a7_pilot.py`'s local-search path ignores `fix_ends`. The reviewer independently reran the study with exhaustive nominal selection (735,471 subsets), correctly constrained endpoints, and all 256 corners. Results (>5% cases; median):
>
>   | $\sigma^2$, $\epsilon/\lambda$ | Common region | Identical endpoints |
>   |---|---|---|
>   | 1e-3, 0.03 | 21/33; 14.0% | 17/33; 5.4% |
>   | 1e-3, 0.05 | 21/33; 20.2% | 18/33; 11.9% |
>   | 1e-2, 0.03 | 21/33; 8.3% | 16/33; 4.0% |
>   | 1e-2, 0.05 | 24/33; 14.0% | 22/33; 9.7% |
>
>   **The mechanism survives.** No archived sweep driver or per-case table exists yet; this is a Day-1 fix.
- Sanity check at $N = 4$, $M = 12$ (exhaustive, $y_P = 2$ m): 15/31 and 24/31 cases exceed 5%.

**A7, learning gate (≥95% of the reference certificate on 90% of held-out cases at ≥5× speed) — NEGATIVE (null for learning).**
- Setup: a NumPy MLP, geometry → site-inclusion logits, trained on 2,500 robust-search labels; every candidate is verified by the certificates.
- As a direct selector, it reaches a median of 0.669 of the reference; only 5% of cases reach ≥0.95. It is 147× faster (0.22 ms vs 32 ms). **Correction:** that timing gave the learner the certificate table for free; counting the setup, the ratio is about 28×. `candidates_from_scores` can also drop the top-N proposal (an `np.unique` truncation bug).
- As a warm start for one local-search pass, it scores 0.950 (49% of cases ≥0.95) vs 0.943 (44%) for a random start, at the same ~4.5 ms.
- The geometry→subset map is too phase-sensitive ($k_0 \approx 586$ rad/m) to learn smoothly, and deterministic robust search is already fast (32 ms).

**A2 (power-probe calibration; jury gate: learning ≥2× fewer observations than the best fixed probing at matched gain) — mechanism POSITIVE, learning WEAK.**
- Setup: $N = 16$, $\epsilon = 0.05\lambda$ with 3-mode errors, dither $0.01\lambda$, re-pinch jitter $0.005\lambda$.
- With 6 power readings, **fixed DCT probes** raise the normalized gain from about 0.96 to 0.998.
- Learned PCA beats DCT only for stable device-specific modes at low noise: 0.9980 with 6 readings vs 0.9933 with 12, which passes the 2× gate in this one case.
- At noise 0.01, DCT ≥ learned. When the modes change after training, learned < DCT (0.9780 vs 0.9821).
- Coordinatewise probing (32 readings) degrades badly under noise (about 0.69).

**Pilot conclusion.** Both top mechanisms are real and strong **without** learning. Learning is not necessary for A7 and only conditionally useful for A2. This matches the jury's "learning-necessity" risk.

## Novelty Verification

Records:
- `/novelty-check` on the two jury picks, by GPT-6 Astra at `ultra` (thread `01a0dbf2-c782-7e13-bd15-46ca66af82ae`);
- full review: `.aris/novelty/NOVELTY_REVIEW_A7_A2.md`;
- dossier: `.aris/novelty/NOVELTY_DOSSIER_A7_A2.md`;
- trace: `.aris/traces/novelty-check/`.

Existence of the cited papers was pre-checked with `verify_papers.py`; unverifiable items are marked in the dossier. Search cutoff: 2026-09-26.

| Idea | Score | Verdict | Precise delta (reviewer-verifiable) | Main risk |
|---|---:|---|---|---|
| **A7** | **6/10** | **PROCEED** | Select among desired-phase-aligned PASS sites and verify every returned subset with desired-gain and leakage bounds for the nonlinear guided/free-space channel under per-element actuator boxes. A learned proposer is optional. | Every broad ingredient has prior art. The contribution must come from a clear protected-receiver benefit under matched constraints. |
| **A2** | **5/10** | **PROCEED WITH CAUTION** | Learn recurring actuator-error modes, probe them with feasible physical position dithers in single-feed PASS, and turn a bounded post-correction error into a gain guarantee. | The quadratic modal sensing identity and power-only calibration are established (He et al. 2019; sensorless adaptive optics). PCA plus inversion is thin. |

**Collisions and corrections that bind the paper wording:**
- **Zhang et al., arXiv 2609.23323 (20 Sep 2026)** already gives affine nonlinear-phase decompositions, channel enclosures, and all-error SINR constraints for MA-ISAC. **Do not claim a "first nonlinear position-error certificate".**
- **FullPASS (2607.19546)** does interference-constrained PASS activation and explicitly leaves position-uncertainty robustness to future work. It is the closest PASS task neighbor.
- **Li et al. (2609.29200, 24 Sep 2026)** is concurrent nominal full-duplex PASS work.
- **GALR-Net** (SAGE journal, 7 Jul 2026) does learned PASS activation under user-location uncertainty. This blocks a broad claim of "first robust learned PASS selection".
- **Yang et al. (2601.17825)** already analyzes box-error null fragility for MA. Null fragility alone is not novel.
- **Classical position-only null steering:** Hejres, IEEE TAP 52(11), 2004, DOI 10.1109/TAP.2004.835128.
- **Measurement correction:** a higher certified lower bound does **not** mean a higher actual worst case. Dominance needs robust LB > comparator UB. The pilot metric already uses LB(S_rob)/UB(S_nom).
- **Safe wording (A7):** "exact" applies only to the affine box response; the random-sign fragility result is a sensitivity-based lower bound with a nontriviality condition.
- **A8** stays as a compact supporting comparator: the tolerance-induced shift beyond the attenuation-aware optimum (Xu et al. 2506.23966 covers generic upstream placement). Uniqueness and monotonicity still need proof with attenuation and movement boundaries.

**Stronger novelty bet: A7.** Keep A2 as a separate fallback; do not combine the two.

## External Critical Review

Reviewer: `/research-review` by GPT-6 Astra at `ultra` (thread `01a0dbfc-ccb0-7f11-a8e3-5687cc058061`). It was adversarial and read-only, and it ran independent A7 reruns. Trace: `.aris/traces/research-review/2026-09-26_run01/`. Brief: `.aris/review/RESEARCH_REVIEW_REQUEST.md`.

**Bottom line: PROCEED with the repaired, non-learning A7 for ICC; do not switch to A2.** The work is not yet submission-ready.

**Mock ICC review (current state): 4/10, weak reject, confidence 4/5.**
- Strengths:
  - a concrete, relevant hardware-error task;
  - sound guarantees under the stated assumptions;
  - the comparison of the robust lower bound against the nominal upper witness;
  - a benefit that survives matched endpoints.
- Weaknesses:
  - the ingredients are established (annular-sector / Minkowski-sum bounds in Arnestad et al.; nonlinear enclosures in Zhang et al.; interference-aware PASS in FullPASS);
  - a broken control, incomplete provenance, and overstated tightness;
  - an idealized equal-power model.
- What moves it toward accept:
  - reproducible, corrected controls;
  - exhaustive nominal and small-instance robust benchmarks;
  - *when* robust selection helps;
  - desired power and leakage reported separately;
  - one credible non-ideal channel sensitivity study.

**Verified correct:**
- amplitude ranges; endpoint phase excursions;
- the desired-gain bound (max $\beta_D \approx 0.461$ rad at $0.05\lambda$);
- the sector support function; the Lipschitz pad; feasible-adversary upper bounds;
- the certified-dominance metric: $L(S_{rob})/U(S_{nom}) - 1 > 0$ certifies improvement in true box-worst SLNR; a negative value is inconclusive.

216,576 feasible evaluations produced no bound violation.

**Defects to fix:**
1. The `fix_ends` path in local search.
2. The tightness overstatement.
3. No sweep driver or per-case results archived.
4. Graduation-report curves are phase-compensated, so they are not physical baselines (N0).
5. Wording: "exact support of the enclosing sector" is correct; "exact nonlinear uncertainty set" is not. The fragility floor is not yet implemented.
6. The learner comparison: timing and the candidate-generation bug.

**AI decision:** drop learning from the title, abstract, contributions, and main algorithm. Keep the negative pilot in the research record. Nothing in this known-model, small-search-space task *requires* learning.

**Claims matrix (reviewer):**

| Outcome | Defensible claim | Avoid |
|---|---|---|
| $L_{rob} > U_{nom}$ | Certified improvement in true box-worst SLNR for that comparison | Globally optimal robust placement |
| $L_{rob} > L_{nom}$, brackets overlap | Improved guaranteed lower bound only | Proven worst-case improvement |
| Gains survive exhaustive nominal + identical endpoints | Benefit within the aligned family at fixed aperture | Superiority over arbitrary continuous placement |
| Gains vanish after endpoint matching | Benefit depends on aperture freedom | Aperture-independent advantage |
| Small-instance search reaches the exhaustive certificate optimum | Strong optimization on tested instances | A general approximation guarantee |
| Brackets tight except near co-aligned receivers | Useful certification with quantified conservative cases | Uniform 1–4% tightness |
| Gains survive attenuation / directivity | Benefit persists in tested separable non-ideal models | Hardware validation; coupled depletion |
| A8 beats attenuation-aware nominal under matched constraints | Additional tolerance-induced placement benefit | Generic upstream optimality |
| Learner still inferior after correction | This learner is unnecessary here | Learning cannot solve it |

**Five-day package (reviewer):**
- **D1:** repair endpoints; N0 physics in every baseline; a runnable sweep with saved inputs, subsets, bounds, and witnesses; zero-error and θ-grid refinement checks.
- **D2:** 24/8 vs exhaustive nominal; 12/4 exhaustive certified optimum; restarts 1/8/32; all corners plus continuous refinement.
- **D3:** $\epsilon/\lambda \in \{0, .01, .03, .05, .08\}$ × reference SNR {10, 20, 30, 40} dB; desired power and leakage reported separately.
- **D4:** attenuation / directivity sensitivity; matched N0 / N1 / N2 / A8; $M \in \{16, 24, 32\}$ at $N = 8$; one relaxed-placement comparator.
- **D5:** freeze results; proofs; figures; reconcile every number with saved outputs.

**Outline (reviewer):**
- Title: *Certified SLNR-Based Site Selection for PASS Under Bounded Position Errors*.
- Prop. 1: per-site enclosure and desired-gain lower bound.
- Prop. 2: sector-support leakage upper bound with the angular-grid correction.
- Corollary: SLNR guarantee and certified dominance.
- Plus a finite-family verification bound.
- Page budget: 0.70 / 0.85 / 1.35 / 0.65 / 1.55 / 0.15 / 0.75.

## Eliminated Ideas

| Idea | Reason eliminated | Phase |
|---|---|---|
| A4 (+L1, L2) verified learned placement | Decorative learning: a vectorized scan of 4,096 layouts takes about 2.6 ms | Jury |
| A3 covariance from subset probes | Low decision value: same offset selected; 0.14% oracle gain | Jury (pre-check) |
| A12 (+L7) density–placement reversal | Real finding (vanishes at fixed N = 16) but no fit with the chosen task; kept as a separate analytic direction | Jury |
| A8 tolerance-induced upstream theorem | Kept only as supporting comparator material; generic upstream placement covered by Xu et al. 2506.23966 | Jury / novelty |
| A1 learned actuator map | Reserve; data-realism risk | Jury rank 4 |
| A5, A6, A9, A10, A11, L5, L6, L10 | Lower expected information within 6 days / 6 pages; reasons in the jury table | Jury |
| A7's learning component | Learning gate negative (selector 0.669 of reference; warm start ≈ random); reviewer: drop from paper | Pilot / review |
| A2 as the paper | Weaker novelty (5/10); residual certificate missing; not combined with A7 | Novelty / review |
| κ universal threshold (in A7) | Not necessary or sufficient (counterexample; remainder vacuous in 72/528 cases) | Refine round 1 |

## Refined Proposal

> **2026-09-27 upgrade (v2):** after the GPT-6 Pro deep verification (reply and Claude's check in `idea-stage/handoff/`), the paper is centered on **global witness screening and certification**. It uses at most 2M shared exact endpoint templates, giving safe screening, the exact certificate optimum, and a unique global robust-optimality test, plus a leakage converse/achievability bracket. The v1 swap search was not certificate-optimal on the featured case (53.42 vs the exact 56.56). New title: *Certified Robust Site Selection for Pinching-Antenna Systems: Global Screening Under Position Errors*.

- Proposal: `refine-logs/FINAL_PROPOSAL.md` (verdict REVISE, 7.70/10 after 2 rounds, GPT-6 Astra `ultra`, thread `01a0dc09-8626-7381-8ced-5aeb34168c36`)
- Review history: `refine-logs/REVIEW_SUMMARY.md`, `refine-logs/REFINEMENT_REPORT.md`, `refine-logs/round-*.md`
- Experiment plan: `refine-logs/EXPERIMENT_PLAN.md`
- Tracker: `refine-logs/EXPERIMENT_TRACKER.md`
- Pipeline summary: `refine-logs/PIPELINE_SUMMARY.md`
- Research contract: `idea-stage/docs/research_contract.md`

## Next Steps

- [ ] **(On hold per user instruction)** Run M0 sanity (R001–R004), then M1 (`python idea-stage/pilots/a7_main.py`, R005–R006) against the pre-declared go/no-go gate.
- [ ] M2/M3 baselines, ablations, mechanism, non-ideal check (R007–R016).
- [ ] `/result-to-claim` with GPT-6 Astra `ultra`; this replaces `CLAIMS_FROM_RESULTS.md` (currently `verdict: REVIEW_UNAVAILABLE`).
- [ ] Rewrite `NARRATIVE_REPORT.md` for A7, then run `/paper-writing — venue: IEEE_CONF, human checkpoint: true` (6 pages).
- [ ] Before submitting on 2026-10-02: `/paper-claim-audit` and `/citation-audit`.

## Sources (Phase 1 additions)

- https://arxiv.org/abs/2605.08039
- https://arxiv.org/pdf/2604.10372
- https://arxiv.org/pdf/2507.06222
- https://arxiv.org/pdf/2512.04293
- https://arxiv.org/pdf/2608.00255
- https://arxiv.org/pdf/2608.12870
- https://arxiv.org/html/2606.17543
- https://www.researchgate.net/publication/395908166_Two-Timescale_Deep-Unfolding_for_Joint_Optimization_of_Antenna_Position_and_Beamforming_in_Movable-Antenna_Arrays
- https://arxiv.org/abs/2605.23140
- https://arxiv.org/pdf/2601.21997
- https://arxiv.org/pdf/2606.23154
- https://arxiv.org/pdf/2602.21162
- https://arxiv.org/html/2508.07572v1
- https://arxiv.org/pdf/2606.03830
- https://arxiv.org/pdf/2510.27185
- https://arxiv.org/pdf/2609.16831
- https://globecom2026.ieee-globecom.org/events/ws-17-pinching-antenna-systems-pass-next-generation-wireless-communications-0
- https://globecom2026.ieee-globecom.org/events/tut-02-pinching-antenna-systems-pass-new-paradigm-wireless-transmission-6g
- https://wcnc2026.ieee-wcnc.org/ieee-wireless-communications-and-networking-conference-21/events/t03-pinching-antenna-systems-pass
- https://arxiv.org/pdf/2505.02864
- https://arxiv.org/pdf/2006.11029
- https://arxiv.org/html/2604.17032v1

<!-- ARIS_IDEA_DISCOVERY_EVIDENCE_GATE:START -->
## Evidence Gate
**Status:** PASS

All required stage records, review receipts, artifacts, and report sections are present.
<!-- ARIS_IDEA_DISCOVERY_EVIDENCE_GATE:END -->
