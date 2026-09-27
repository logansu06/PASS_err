# Idea-Generation Bundle — PASS Robustness Paper for IEEE ICC 2027

You are a senior wireless-communications and signal-processing researcher brainstorming research ideas. You have **broad creative latitude**:
- surprising connections are welcome;
- inverted assumptions are welcome;
- AI methods are welcome where they reveal something the analysis alone cannot.

Read these files for context (read-only):
- `/Users/logansu/Documents/PASS/NARRATIVE_REPORT.md` — graduation-report story and numbers.
- `/Users/logansu/Documents/PASS/idea-stage/LIT_REVIEW.md` — prior-art table (2026-09-25).
- `/Users/logansu/Documents/PASS/idea-stage/NOVELTY_REPORT.md` — novelty verdict on the current baseline (6/10, PROCEED WITH CAUTION).
- `/Users/logansu/Documents/PASS/idea-stage/IDEA_REPORT.md`, section "Literature Landscape" — the 2025–2026 landscape, including AI-for-PASS work, and the structural gaps E1–E5.
- `/Users/logansu/Documents/PASS/.aris/novelty/proto.py` and `offset.py` — working prototypes (aligned design, certificate, upstream offset). They import `/Users/logansu/Documents/PASS/src/pass_model.py`.

## Research Direction (from the user)

Using the current results and the graduation-report content, find new ideas that raise the novelty of the ICC 2027 paper.
- **Style:** recent GLOBECOM / ICC / WCNC / MobiCom papers — a strong task, a clear structure, and heavy mathematics.
- **AI:** AI methods may be introduced.
- **Baseline:** the ideas must build on the existing baseline below. That baseline is the reference the new contribution is measured against and extends; it is not to be replaced.

**User-confirmed main thread (2026-09-26):** AI methods for PASS and movable-antenna optimization, plus robust and **learning-based robust design** under hardware (pinching-position) errors. The paper should read as a strong-task, strong-math robust-design paper in which learning plays a central, justified role. The analytic baseline (C1, N0, N1, N2) supplies the structure, the certificates, and the comparison baselines.

## Baseline (what already exists)

- **Model** (Ouyang et al., IEEE CL 2025):
  - single-user PASS; waveguide at height $d$;
  - $N$ pinching antennas at offsets $\Delta_n$;
  - phase $\Phi_n = k_0(R_n + n_{\mathrm{eff}}\Delta_n)$;
  - gain $a = \frac{\eta}{N}\big|\sum_n e^{-j\Phi_n}/R_n\big|^2$;
  - alignment is achieved **by placement only** (no phase shifters).
- **C1 (graduation report):**
  - sensitivity $\xi_n = n_{\mathrm{eff}} + \sin\theta_n$;
  - weighted phase-variance loss $1 - \mathrm{Var}_\alpha(k_0\xi_n\delta_n)$;
  - covariance predictor $1 - k_0^2\,\mathrm{tr}(M_\alpha D_\xi\Sigma D_\xi)$, validated for iid, common-bias, and correlated errors;
  - common mode is nearly harmless, the differential mode is damaging;
  - the split-mode pattern tracks the best-found box adversary.
- **N0 (fix):** solve the alignment equation on both sides of the user (the graduation report mirrored and was misaligned, 95.7% of ideal gain).
- **N1:** a nonlinear certified worst-case enclosure under per-element boxes $|\delta_n| \le \epsilon$:
  - lower bound $\big(\sum_n w_n^-\cos\beta_n / W\big)^2$ with $\beta_n = k_0\epsilon\,\xi_n^+(\epsilon)$ (or the endpoint excursion);
  - upper bound: the split mode evaluated exactly;
  - enclosure width about $2.8 \times 10^{-4}$.
- **N2:** tolerance-aware upstream placement.
  - Surrogate: $F(s) = (1 - s^2)\cos^2[k_0\epsilon(n_{\mathrm{eff}} + s)]$ with $s = \sin\theta_c$.
  - Stationary point: $s = -k_0\epsilon(1 - s^2)\tan[k_0\epsilon(n_{\mathrm{eff}} + s)]$.
  - Certified improvement over centered placement: $+1.9\%$ / $+37.6\%$ / $6.86\times$ at $\epsilon/\lambda = 0.05$ / $0.10$ / $0.15$.
- **Novelty review of the baseline:**
  - C1 is established (Ruze-type).
  - C2 is thin.
  - N1 is defensible but close to interval-arithmetic tolerance analysis (Poli 2015, Arnestad 2023).
  - N2 is the strongest.
  - Closest prior work: Chen et al., TWC 2026 (Hybrid PASS; simulated multi-PA position errors, mitigated with extra hardware); Yang et al., TVT 2026 (movable antennas; box errors; Taylor analysis).

## New Landscape Facts (from your own broad-discovery pass; see IDEA_REPORT.md § F)

- **Upstream placement already has a nominal justification.** In-waveguide attenuation already pushes the optimum toward the feed (Xu et al., 2506.23966; switched-feed PASS 2607.12646; the CMT-aware lossy/directional model 2608.03787). Any placement contribution must isolate the *tolerance-induced* shift beyond the attenuation-aware nominal optimum.
- **Discrete-PASS closed forms exist**, but only for single-active PAs (Tyrovolas et al., 2511.01798 and 2512.18761).
- **Certified PASS QoS guarantees exist** (Cui et al., TWC 2026), so do not claim the "first certified PASS design".
- **Robust learning under movable-antenna hardware impairments exists** (Xiu et al., GNN / meta-RL under distortion, synchronization error, and CFO). An AI contribution must deliver a more specific property; for example, a *verified gain lower bound under actuator boxes*.
- **PASS hardware-state observability** through tagged pilots and a single RF chain exists (failure detection, 2602.17257). Pinching-offset calibration remains open.
- **Nulling, full-duplex, and interference tasks** (FullPASS 2607.19546) are more tolerance-fragile than main-beam gain.

## Hard Constraints

- **Deadline:** 2 October 2026 (6 days from now).
- **Length:** 6 pages in two-column IEEE format, including references.
- **Compute:** CPU-only NumPy/SciPy simulation.
- **Implementation:** a single executor; each idea must be implementable in about 1–2 days.
- **Structure expected by ICC reviewers:** system model → a well-posed optimization or estimation *task* → structural analysis (lemmas, theorems, closed forms, complexity, optimality gap) → algorithm → simulations against meaningful baselines, including the graduation-report baseline and yesterday's N1/N2.

## Request

Generate **12–14 concrete research ideas**. Mix them deliberately:
- ideas that turn N1/N2 into a full **task** (a well-posed max–min, outage, or estimation problem with provable structure);
- ideas that add a **new mechanism or finding**;
- **at least half of the ideas (6 or more) should be learning-based robust designs** for PASS under pinching-position or hardware errors. Examples of the kind of thing meant (not a list to copy):
  - learned placement or beamforming policies trained against the certified or analytic robustness objects;
  - deep unfolding of a robust algorithm;
  - meta-learning or amortization across user positions or tolerances;
  - learning-based calibration or error estimation with closed-loop re-pinching;
  - DRL / Bayesian optimization with physics priors;
  - generative or diffusion models of error fields;
  - certified or verified neural policies.

  The AI must be *necessary*, not decorative: the analysis alone cannot do it (multi-user, lossy or directional radiation, unknown error statistics, online adaptation, amortized speed), and the analysis certifies, explains, or regularizes what the AI learns. Each such idea must name what the closed form or the N2 rule can **not** do that the learner can;
- at least 2 **high-risk / high-upside** ideas.

For each idea, give:
1. A one-sentence summary.
2. The core hypothesis: what you expect, and why.
3. The task formulation: an explicit optimization or estimation problem, in math.
4. The theorem or structural result you expect to prove (state it; sketch why it should hold).
5. The minimum viable experiment on CPU in NumPy, and what it takes to implement.
6. Contribution type: theory / method / algorithm / diagnostic / system.
7. Risk: LOW / MEDIUM / HIGH.
8. Effort, in days.
9. How it uses and extends the baseline (C1, N0, N1, N2).
10. The closest prior work you know, and the likely delta.

Prioritize ideas that are:
- **simple at the core** — one mechanism a colleague could restate after hearing it once;
- **likely to give a clear answer either way.**

"Apply X to Y" is legitimate when it reveals something non-obvious. Be genuinely creative; filters come later and are strict. A bold idea with a named risk beats a hedged, complicated one.

Finish with your own top 3 for a 6-page ICC 2027 paper and the one-sentence paper thesis each would support.
