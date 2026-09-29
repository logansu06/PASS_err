# Narrative Report: Certified Robust Site Selection for Pinching-Antenna Systems Under Actuator Position Errors

> **Input for Workflow 3.** Run `/paper-writing "NARRATIVE_REPORT.md" — venue: IEEE_CONF, human checkpoint: true` (6 pages including references). The paper is compiled in Overleaf, not locally: replace `/paper-compile` with the Overleaf round trip in `HANDOFF.md` §10.
>
> **Claim status.** Every claim below stays inside `CLAIMS_FROM_RESULTS.md`: the R020 jury verdict (partial / high, **provisional**, because `/experiment-audit` was skipped by user decision), plus the R019, R021 and auto-review round-1 updates. Sentences marked **[licensed]** are quoted from that file and may be used as written.
>
> **Sources.** Method and theorems: `refine-logs/FINAL_PROPOSAL.md` (v2). Results: `refine-logs/EXPERIMENT_RESULTS.md`, with raw files in `experiments/a7/results/` (`r019_numbers.md` maps quoted numbers to source keys; `ablation_summary.md` holds the R021 numbers). Figures, tables and draft captions: `figures/latex_includes.tex`. Review guidance: `review-stage/AUTO_REVIEW.md` (round 1: 7/10, almost). Positioning: `idea-stage/NOVELTY_TARGETED_A7v2.md`.
>
> This file replaces the graduation-project narrative, which is archived at `fyp_report/NARRATIVE_REPORT_FYP.md` and must not be used for this paper.

## Venue Constraints

- **Venue:** IEEE ICC 2027 (Washington DC, 30 May – 3 June 2027). Paper submission deadline: 2 October 2026 via EDAS; confirm the exact closing time and time zone on EDAS.
- **Length:** at most 6 printed pages (10-pt, two-column) including figures and references; longer initial submissions are rejected without review.
- **Format:** `\documentclass[conference]{IEEEtran}`, numeric `\cite{}`, `IEEEtran.bst`, `IEEEkeywords` after the abstract.
- **Candidate symposia:** Wireless Communications, or Signal Processing for Communications.
- **Author block:** confirm the review policy on EDAS. ARIS `IEEE_CONF` defaults to non-anonymous. Do not generate author names.

## One-Sentence Contribution

Within a finite, robust-clearance family of desired-phase-aligned pinching sites, one shared bank of at most 2M exact endpoint witnesses gives feasible worst-case SLNR upper bounds for every layout; together with a nonlinear sector certificate, this turns robust PASS site selection under actuator position errors into safe family-wide screening with exact certificate optimization, a global robust bracket, a uniqueness test and a leakage converse, and it certifies higher worst-case SLNR than exhaustive nominal selection in most cases of a declared grid.

## Core Story

**Problem.**
- A pinching-antenna system (PASS) radiates from pinches placed on a dielectric waveguide. It has no phase shifters; it shapes the field only through where it pinches.
- With a desired receiver D and a protected receiver P, nominal interference-aware site selection places a deep null toward P.
- Actuators place each pinch with a bounded position error of a few percent of a wavelength (at 28 GHz, 0.05λ ≈ 0.54 mm). Through the guided-wave phase $k_0 n_{\mathrm{eff}} x$, these errors break the nominal null.
- Featured case (Fig. 1; free family, $P = (3,2)$ m, $\epsilon = 0.05\lambda$, 30 dB): the exhaustive nominal layout $S_{\rm N}$ has nominal leakage field $|h_P| = 3.4\times10^{-4}$, a deep null, but its worst case over the error box is at least 0.3596. The GCS layout $\hat S$ is certified at most 0.3081 (bounds rounded outward).
- A designer needs a layout whose SLNR is guaranteed for every actuator error in the tolerance box, and a statement of how far that layout can be from the best robust layout in the family.

**Gap.**
- Robust PASS design treats user-location or CSI uncertainty, not errors in the pinch positions themselves.
- Pinch-position errors have been analysed for a single radiator's secrecy (Pakravan et al.), simulated for multi-antenna PASS and compensated with extra hardware (Chen et al., H-PASS), and characterized statistically for TDMA/NOMA (Jiang–Schotten).
- Movable-antenna work bounds position errors with Taylor models (Yang et al.) or nonlinear enclosures (Zhang et al.), for continuous positions. Interval tolerance analysis (Anselmi et al.; Poli et al.; Arnestad et al.) bounds the pattern of one given array.
- To our knowledge, no prior work combines finite PASS site selection, actuator-position error boxes, and family-wide certificates (safe screening, a global robust bracket, a uniqueness test). Each ingredient on its own has precedent; say so.

**Key idea.**
1. **Per-layout certificate (Theorem 1).** The PASS phase is strictly increasing in position ($\psi_r' \ge k_0(n_{\mathrm{eff}}-1) > 0$, Lemma 1), so each site's contribution over its error interval is an arc with known endpoints. An asymmetric phase sector around that arc, with a $\sec(\pi/K)$ angular correction, gives a certified SLNR lower bound $L(S) \le W(S)$.
2. **Shared witnesses (Theorem 2) — the technical centre of the paper.** For one layout, the endpoint-leakage maximum is a rank-2 binary quadratic maximum, attained within an auxiliary-angle candidate set; this is known (Karystinos–Pados; Karystinos–Liavas; Allemand et al.; Ferrez et al.) and is credited as an ingredient. The paper's own observation is that the candidate sign templates built **once from all M sites** serve **every** layout of the family, and that, applied as one physical error vector to both D and P, they are feasible SLNR witnesses: $U_H(S) \ge W(S)$ for every $S$. Its short proof (below) must appear in the paper.
3. **Family-wide consequences (Corollaries 1–2).** Safe screening (terminology from El Ghaoui et al.) discards every layout with $U_H(S) \le L(\hat S)$, so scanning the survivors returns the exact certificate optimum. The same bank gives a global bracket, a sufficient uniqueness test, and an exact endpoint leakage converse.

**What the experiments show.** On a declared grid of 1,360 cases:
- GCS certifies higher worst-case SLNR than exhaustive nominal selection in most nonzero-tolerance cases, including the identical-endpoint family (C1).
- It often certifies that its layout is the unique robust optimum of the family, and brackets the family optimum tightly in the median case (C2).
- Its certified leakage sits within 1.14% of the family-wide converse on the tested tolerance sweep (C3).
- Combined enclosure loss is at most 0.0934% on the primary fixed layouts; joint refinement establishes substantial D/P-dependency losses on the selected co-aligned stress panel (R021 ablation). On the full grid the remaining bracket mixes D/P dependency with unresolved witness slack, and in some off-axis layouts the enclosure is the larger part of a small gap.
- The honest negative region is P directly behind D ($x_P = 0$), where the certificate is inconclusive.

## Claims

Primary population throughout: $\epsilon > 0$, $P \ne D$, 528 cases per family (free; identical endpoints).

**C1 — Certified dominance over exhaustive nominal selection (primary).**
- **[licensed]** "On the declared nonzero-tolerance grid (ε > 0, P ≠ D; 528 cases per family), GCS certifies higher worst-case SLNR than exhaustive nominal selection in 87.5% (462/528) of free-family and 82.8% (437/528) of identical-endpoint cases, with certified gains above 5% in 61.9% (327/528) and 56.25% (297/528), respectively."
- Also report: inconclusive cases 66 / 91; median nominal sacrifice 0.16% / 0.32%. Median Γ is 11.3% [IQR 1.6, 27.6] / 6.9% [0.5, 19.4].
- The pre-declared go/no-go gate (Γ > 5% in at least 20% of endpoint cases) passed at 297/528 = 56.25%.
- The gain grows with SNR (leakage-limited regime): median Γ 1.6% / 1.1% at 10 dB, 27.6% / 17.2% at 40 dB.
- Evidence: `results/main_grid.csv`, `main_summary.json`; Fig. 2; Table II.

**C2 — Global certification yield and screening.**
- **[licensed]** "A shared bank of at most 2M endpoint witnesses enables safe family-wide screening and exact certificate maximization when the scan completes; on the main grid, a unique robust-optimal layout within the family is certified in 38.6%/45.3% of free/endpoint cases, with median global bracket gaps of 0.508%/0.489%."
- The uniqueness yield falls with ε: about 76–80% at 0.01λ, 9–15% at 0.08λ.
- Median survivors after screening: 70 of 735,471 (free) and 15 of 74,613 (endpoints) layouts.
- Global screening changes the selected layout, not only the certificate: the plain swap incumbent is strictly below the exact certificate optimum in 373/480 exact free cases and 312/528 exact endpoint cases (median 0.92% / 0.29%, max 24.3% / 25.9%). This is a gain in the certificate objective.
- Cost: the GCS selection stage takes 0.20 s / 0.12 s median. Inclusive of family construction, the bank pass, nominal enumeration and witness refinement, a case takes 3.9 s / 0.55 s median (max 11.5 s). At M = 32 (10,518,300 free layouts) a case takes about 35 s, dominated by the bank pass. The survivor fraction shrinks as M grows (free: 7.8e-4 at M = 16 to 5.8e-5 at M = 32).
- The screening cap ($2\times10^5$ evaluations) is hit in 48 free cases of the primary population, all at $x_P = 0$ (64 in the full 1,360-row grid; the other 16 are $P = D$ controls). Those report the bracket only, with no exact argmax.
- Failing the uniqueness test does not mean the scan failed: in 565 of the 1,056 primary cases the scan completes (exact certificate optimum) without a uniqueness certificate. Keep "exact certificate optimum", "unique", and "capped" distinct.
- Evidence: `main_summary.json`, `scaling.csv`; Fig. 4; Table II.

**C3 — Protection limits.**
- **[licensed]** "Across three pre-specified geometries, nine tolerances and both families at 30 dB, the leakage achievability bound lies within 1.14% of the exhaustive endpoint converse; at transmit power p, leakage ceilings below p·F_end are infeasible within the family, and any ceiling ≥ p·Ī(Ŝ) is met by Ŝ."
- The worst-case leakage floor $F_{\rm end}$ grows by ×67–71 from 0.01λ to 0.09λ at $P = (3,2)$ and $(6,1)$.
- At $P = (0,1)$, $F_{\rm end} \approx 0.80$ at every ε: within the family, no layout meets a leakage ceiling below about $0.80\,p$ for all errors.
- Evidence: `results/limits.csv`; Fig. 3.

**Supporting claims.**
- **S1 — Mechanism: certified lower worst-case leakage.** **[licensed]** "Among the 899 declared-grid cases with certified SLNR improvement, 893 (99.3%) also certify strictly lower worst-case leakage than exhaustive nominal selection. Across these 899 cases, the median certified upper bound on the worst-case leakage ratio is at most 0.800." At the best-found SLNR witnesses, the median desired-power ratio is 1.000 (descriptive). Evidence: `r019_derived.json` → `mechanism_gamma_pos`.
- **S2 — Baselines.** **[licensed]** "On the baseline slice, GCS certifiably outperforms the same-start shared-template swap heuristic in 68.9%/50.8% of free/endpoint cases and the P-blind desired-only baseline in 90.9% of cases for both families." The P-blind layout is the graduation-project-style design; with $x_P \ne 0$ it is certifiably beaten in 120/120 cases per family. Budgets are not matched. Evidence: `baselines.csv`; Table II.
- **S3 — Non-ideal channel.** **[licensed]** "After model-aware redesign at model-specific reference SNR, certified dominance persists in 81.8–88.6% (free) and 82.6–84.8% (endpoints) of cases under the two tested separable attenuation/directivity models." The median gain roughly halves. Evidence: `nonideal.csv`, `nonideal_1dB.csv`; Table II.
- **S4 — Co-aligned receivers ($x_P = 0$).**
  - All 96 primary cases at $x_P = 0$ are inconclusive. The other 61 inconclusive cases have median Γ −0.19%, but they are not uniformly marginal: 13 are below −5% (minimum −11.07%).
  - **[licensed]** "For five selected co-aligned endpoint cases, joint-box refinement closes 51–61% of the log bracket gap, but none becomes a certified improvement over nominal selection."
  - **[licensed]** "Additional joint-box verification certifies dominance in four of sixteen co-aligned stress pairs, all at P = (0,4), ε = 0.03λ, both families and 10/40 dB, with gains of at least 0.88%; the other twelve remain inconclusive."
- **S5 — Certificate-gap ablation (R021).**
  - **[licensed]** "On fixed primary GCS layouts, replacing the literal-v1 certificate with the production certificate increases certified-positive counts from 437 to 462 of 528 free cases and from 403 to 437 of 528 identical-endpoint cases."
  - Use the compact block in "Experiment 6" below.
- **S6 — Average and tail behaviour (descriptive).** **[licensed]** "With 10,000 iid-uniform error draws per case, the median estimated mean-SLNR ratio is 0.9968/0.9958 (free/endpoints), while the estimated fifth-percentile SLNR improves in 77.3%/54.5% of cases; individual mean losses can be much larger." Show the substantial-loss example in "Experiment 7" next to the median.

## Method and Analysis

### System and error model

- **Geometry:** waveguide along $x$ at height $d = 3$ m, feed at $x_f = -10$ m; $f_c = 28$ GHz ($\lambda = 10.714$ mm, $k_0 = 586.43$ rad/m); $n_{\mathrm{eff}} = 1.44$.
- **Receivers:** desired D at $(0, 0, 0)$; protected P at $(x_P, y_P, 0)$.
- **Channel:** $R_r(x) = \sqrt{(x - x_r)^2 + y_r^2 + d^2}$, $\psi_r(x) = k_0\big(R_r(x) + n_{\mathrm{eff}}(x - x_f)\big)$, $z_r(x) = A_r(x)e^{-j\psi_r(x)}$ with $A_r = 1/R_r$ (ideal isotropic, equal per-site power $1/N$). Separable in-waveguide attenuation and $\cos^q$ field directivity appear only in the non-ideal control.
- **Candidate family:** $M = 24$ sites on consecutive D-aligned levels ($R_D(x) + n_{\mathrm{eff}}x \in \lambda\mathbb Z + C$), so all sites share one nominal phase toward D; minimum spacing $0.68222\lambda$. This corrects the graduation-project construction, which mirrored one side and left the upstream half misaligned; state it as a system-construction step, not a contribution.
- **Selection:** $|S| = N = 8$. Robust clearance: adjacent selected sites satisfy $x_j - x_i \ge 0.5\lambda + 2\epsilon$ (necessary and sufficient). Every subset is feasible iff $\epsilon \le 0.0911\lambda$. The identical-endpoint subfamily forces the first and last sites.
- **Errors:** independent actuator position errors $|\delta_n| \le \epsilon$; D and P see the **same** physical error vector.
- **Objective:** $h_r(S,\delta) = \sum_{n\in S} z_r(x_n + \delta_n)$, $G_D = |h_D|^2/N$, $I_P = |h_P|^2/N$, and
  $$W(S) = \min_{\|\delta\|_\infty \le \epsilon} \frac{G_D(S,\delta)}{\sigma^2 + I_P(S,\delta)}, \qquad W^\star = \max_{S\in\mathcal F_\epsilon} W(S).$$
  The noise $\sigma^2 = A_{\rm ref}/\mathrm{SNR}_{\rm ref}$ is a fixed physical level ($A_{\rm ref}$: central 8-site block toward D), identical for all layouts.
- **Nominal baseline:** $S_{\rm N}$ maximizes the nominal SLNR over the same family (exhaustive enumeration).

### Theory (all statements proven with explicit assumptions; verified in `idea-stage/handoff/`)

**Lemma 1 (PASS phase and interval geometry).** For $n_{\mathrm{eff}} > 1$, $\psi_r' = k_0(n_{\mathrm{eff}} + t_r) \ge k_0(n_{\mathrm{eff}} - 1) > 0$ with $t_r = (x - x_r)/R_r$. So the unwrapped phase image of $[x_n - \epsilon, x_n + \epsilon]$ is exactly $\Psi_{r,n} = [\psi_r(x_n - \epsilon), \psi_r(x_n + \epsilon)]$. In the ideal amplitude model $A_r = 1/R_r$, the amplitude extrema $A^\pm_{r,n}$ over the interval lie at the endpoints or at the projection of the receiver onto the waveguide. (With attenuation or directivity, also check the stationary points; this applies only to the non-ideal control.)

**Theorem 1 (nonlinear SLNR bracket).**
- Desired power: the family is D-aligned, so every $\psi_D(x_n)$ equals a common phase $\bar\psi_D$ modulo $2\pi$. Define the desired-phase excursion $\beta_{D,n} = \max\{\psi_D(x_n + \epsilon) - \psi_D(x_n),\ \psi_D(x_n) - \psi_D(x_n - \epsilon)\}$. If every $\beta_{D,n} \le \pi/2$ (otherwise the tolerance is rejected), projecting $h_D$ onto $e^{-j\bar\psi_D}$ gives $G_D(S,\delta) \ge L_D(S) = \frac1N\big(\sum_{n\in S} A^-_{D,n}\cos\beta_{D,n}\big)^2$. (In floating point the sites carry a residual misalignment of at most about $2\times10^{-12}$ rad, which should be added to $\beta_{D,n}$; see Known Weaknesses.)
- Leakage: site $n$'s contribution lies in the asymmetric sector $\{a e^{j\phi} : a \in [A^-_{P,n}, A^+_{P,n}],\ |\phi - \phi_{c,n}| \le \beta_{c,n}\}$ with centre $\phi_{c,n} = -(\psi_P^+ + \psi_P^-)/2$ and half-width $\beta_{c,n} = (\psi_P^+ - \psi_P^-)/2$, where $\psi_P^\pm = \psi_P(x_n \pm \epsilon)$. Its support in direction $\theta$ is $s_n(\theta) = A^+_{P,n}\cos g_n(\theta)$ if $\cos g_n(\theta) \ge 0$ and $A^-_{P,n}\cos g_n(\theta)$ otherwise, with angular gap $g_n(\theta) = \max\{|\mathrm{wrap}(\theta - \phi_{c,n})| - \beta_{c,n},\ 0\}$. On the uniform grid $\theta_k = -\pi + 2\pi k/K$, $k = 0, \dots, K-1$:
  $$B_P(S) = \frac{\max_k \sum_{n\in S} s_n(\theta_k)}{\cos(\pi/K)} \ge \max_\delta |h_P|, \qquad \bar I(S) = B_P^2/N.$$
  With $K = 1440$ the angular power inflation is at most $\sec^2(\pi/K) - 1 \approx 4.76\times10^{-6}$.
- Bracket: for $\epsilon > 0$, $L(S) = L_D(S)/(\sigma^2 + \bar I(S)) \le W(S) \le U(S)$ for any feasible witness set evaluated with the same error vector for D and P.
- Zero tolerance: at $\epsilon = 0$ the formula above is still conservative (grid and sec factor), so $L(S)$ is **defined** as the exact nominal SLNR there. This explicit branch is what makes $\Gamma = 0$ and the zero global gap exact in the $\epsilon = 0$ control.

**Theorem 2 (shared endpoint witness bank).**
- Let $z_n^\pm = z_P(x_n \pm \epsilon)$ and $v_n = (z_n^+ - z_n^-)/2$. The breakpoints $\arg v_n \pm \pi/2$ over **all M sites** split the circle into cells; one angle per cell gives sign templates $s^{(1)},\dots,s^{(H)}$, $H \le 2M$ ($H = 2M$ in every case of the scaling study: 32, 48, 64 for $M = 16, 24, 32$).
- Exact endpoint cover: for every layout $S$ of the family,
  $$\max_{s\in\{\pm1\}^{|S|}} \Big|\sum_{n\in S} z_n^{s_n}\Big|^2 = \max_{q\le H} \Big|\sum_{n\in S} z_n^{s^{(q)}_n}\Big|^2.$$
- Witness bound: $U_H(S) = \min_q \mathrm{SLNR}(S, \epsilon s^{(q)}) \ge W(S)$ for every $S$, because each template is one feasible physical error vector applied to D and P.
- **Proof sketch (keep in the paper).** With $m_n = (z_n^+ + z_n^-)/2$, the endpoint leakage fields of $S$ are $w(s) = \sum_{n\in S} m_n + \sum_{n\in S} s_n v_n$, the vertices of a zonotope. $|w|^2$ is convex, so its maximum $w^\star$ is a vertex; with $\theta^\star = \arg w^\star$, $w^\star$ also maximizes $\mathrm{Re}(e^{-j\theta^\star}w)$, whose maximizing signs are $s_n = \mathrm{sign}\,\mathrm{Re}(e^{-j\theta^\star}v_n)$. These signs change only when $\theta$ crosses a breakpoint $\arg v_n \pm \pi/2$ with $n \in S$. The breakpoints of $S$ are a subset of those of all $M$ sites, so every cell of $S$'s arrangement contains a cell of the full arrangement, and the full-arrangement template for that cell restricted to $S$ gives the same signs. The offset $\sum m_n$ does not change the argument.
- **Credit and scope.** The per-layout statement is a rank-2 binary quadratic maximization (auxiliary-angle enumeration; zonotope vertices). The new parts are the family-wide sharing of one template set and its use as common D/P feasible witnesses. The theorem is exact for the endpoint-leakage maximum only; it does not claim that box leakage maxima or SLNR minima lie at the endpoints.

**Corollary 1 (global robust certification).**
- Safe screening: any $S$ with $U_H(S) \le L(\hat S)$ is discarded safely, so scanning the survivors returns $\max_{S\in\mathcal F} L(S)$ exactly when the scan completes.
- Global bracket: $L(\hat S) \le W^\star \le U^\star := \max_{S} U_H(S)$, hence $W(\hat S)/W^\star \ge L(\hat S)/U^\star$.
- Uniqueness: if $L(\hat S) > \max_{S \ne \hat S} U_H(S)$, then $\hat S$ is the unique robust-optimal layout of the family (a sufficient test).
- Certified dominance over nominal: $\Gamma = L(\hat S)/U(S_{\rm N}) - 1 > 0$, where $U(S_{\rm N})$ is the minimum over all $2^N$ corners plus L-BFGS-B refinement from the worst corners (best-found witnesses).

**Corollary 2 (protection limits).**
$$F_{\rm end} = \min_{S\in\mathcal F}\max_q \frac{|\sum_{n\in S} z_P(x_n + \epsilon s^{(q)}_n)|^2}{N} \le \min_S \max_\delta I_P(S,\delta) \le \bar I(\hat S).$$
With transmit power $p$, no layout of the family meets a leakage ceiling $I_{\max} < pF_{\rm end}$ for all errors, and $\hat S$ meets any $I_{\max} \ge p\,\bar I(\hat S)$.

### Algorithm: Global Certified Selection (GCS)

1. Enumerate the robust-clearance family (or its identical-endpoint subfamily); reject tolerances with any $\beta_{D,n} > \pi/2$.
2. Build per-site tables: $c_n = A^-_{D,n}\cos\beta_{D,n}$, sector supports $s_n(\theta_k)$, endpoint values, and the $H \le 2M$ templates.
3. Exhaustive nominal optimum $S_{\rm N}$ (baseline).
4. Incumbent: swap local search on $L$ from $S_{\rm N}$ plus 8 random starts (seed 2026).
5. Witness bank: $U_H(S)$ for every layout, in batches.
6. Safe screening: evaluate $L$ only on layouts with $U_H >$ incumbent, updating the incumbent; pre-declared cap $2\times10^5$ evaluations (above it, report the bracket only).
7. Certificates: global bracket, rival-dominance margin, certified dominance over $S_{\rm N}$, and $F_{\rm end}$ vs $\bar I(\hat S)$.

**Numerical wording.** "Certificates are analytical statements; all inequalities are evaluated numerically in float64, and decisive margins are reported." **[licensed]** The decisive margins of the featured case were recomputed with independent 50-digit code (free margin 0.3209, endpoints 0.0466), and the weakest positive margins on the grid kept their signs at 50 digits.

## Experiments

### Setup (Table I)

- Grid: 1,360 cases = 2 families × 4 reference SNRs {10, 20, 30, 40} dB × 5 tolerances $\epsilon/\lambda \in \{0, 0.01, 0.03, 0.05, 0.08\}$ × 34 receiver positions (33 positions of P with $x_P$ in 11 values over $[-6, 6]$ m and $y_P \in \{1, 2, 4\}$ m, plus the control $P = D$).
- Family sizes: 735,471 layouts (free), 74,613 (identical endpoints).
- Controls: $\epsilon = 0$ gives $\Gamma = 0$ and a zero global gap exactly, with $\hat S = S_{\rm N}$ in 272/272 cases; $P = D$ gives no certified gain, as expected.
- Sanity checks (M0, 8/8 passed): 0 bound violations in 1e5 random errors plus all corners per instance; bank identity verified on 1,600 layouts; GPT-6 Pro's independent 132-case grid reproduced exactly (108/132 positive, 79/132 above 5%).
- Compute: CPU only; the 1,360-case grid runs in 458 s on 7 workers.

### Experiment 1: Certified dominance (Fig. 2, Table II) — C1
- Γ distributions by tolerance and SNR for both families; inconclusive share per tolerance; the 5% level.
- Report the negative region (all $x_P = 0$ cases inconclusive) and the nominal sacrifice (median small; p90 13.5% pooled; max 88.5%).

### Experiment 2: Certification yield and screening (Fig. 4, Table II) — C2
- Survivor fraction vs M ∈ {16, 24, 32}; time per case (inclusive and GCS stage); uniqueness share vs tolerance.
- Report cap hits and the $x_P = 0$ cases separately. On the scaling slice of Fig. 4, at least 99.998% of the family survives in the $x_P = 0$ cases; on the main grid the co-aligned survivor fraction ranges from 53.35% to 100%, and the capped cases are there.
- State tractability only for the tested families; the bank pass scales with $|\mathcal F|$ and the method is not polynomial-time.

### Experiment 3: Protection limits (Fig. 3) — C3
- $F_{\rm end}$ vs $\bar I(\hat S)$ over 9 tolerances for $P \in \{(3,2), (6,1), (0,1)\}$, both families, 30 dB; SLNR bracket $[L(\hat S), U^\star]$ vs $U(S_{\rm N})$.

### Experiment 4: Baselines (Table II) — S2
- Slice: SNR {20, 30} dB × $\epsilon$ {0.03, 0.05}λ × 33 positions × 2 families.
- B-NOM: the exhaustive nominal optimum $S_{\rm N}$.
- B-CR: the same-start shared-template swap heuristic, which maximizes $U_H$ with the same starts and swap neighbourhood as the GCS incumbent step. Budgets are unmatched: B-CR's selection stage is faster (0.03 s vs 0.11–0.20 s) but uncertified.
- B-GR: the P-blind desired-only layout.

### Experiment 5: Non-ideal channel control (Table II) — S3
- Models: 0.08 dB/m and 1 dB/m in-waveguide loss, each with $\cos^2$ field directivity.
- Both layouts are redesigned under each model at a model-specific reference SNR. This is not a fixed-physical-noise transfer test.

### Experiment 6: Certificate-gap ablation (R021) — S5
Fixed stored layouts; no re-selection. For a layout $S$, $W/L_0$ = angular × P-sector × desired projection × D/P dependency. Values in percent, bound endpoints rounded outward (`results/ablation_summary.md`):

| Quantity | Result |
|---|---|
| Pad → sec gain: median / p95 / max (1,056 primary $\hat S$ rows) | 0.936 / 4.86 / ≤ 11.76 |
| Symmetric → asymmetric sector gain: max | ≤ 0.0183 |
| Angular / P-sector / desired-projection loss: max (2,112 primary layout-rows) | ≤ 0.000476 / ≤ 0.0797 / ≤ 0.0141 |
| Combined enclosure loss: max | ≤ 0.0934 |
| Median D/P dependency factor, stress panel: off-axis / co-aligned (32 layout-rows each) | [0.0359, 0.0436] / [13.71, 21.11] |
| Swap → completed GCS, improved exact cases: free / endpoints | 373/480 / 312/528 |

- The P-sector loss is measured against the true continuous per-site curve (exact by independence of the site errors). Minkowski addition introduces no relaxation.
- On the full grid, the remainder of the bracket mixes D/P dependency with unresolved witness slack; only the stress panel (joint-box refinement of both layouts) separates them. The enclosure is not negligible in every layout: for the free GCS layout at $P = (6,1)$, $\epsilon = 0.03\lambda$, 40 dB, it accounts for at least 98.4% of the (small, 0.074%) logarithmic gap (`results/narrative_checks.md`).
- Recommended placement: fold these rows into Table II or give them as two sentences; no new figure.

### Experiment 7: Average and tail behaviour (text only) — S6
- 10,000 iid-uniform error draws per case on the baseline slice; descriptive, no seed-uncertainty estimate.
- Substantial-loss example (verified in `results/main_grid.csv` and `results/r017_mc_average.csv`): identical endpoints, 30 dB, $\epsilon = 0.03\lambda$, $P = (-3.6, 2)$. The certified worst-case gain is +7.85%, while the nominal SLNR falls 39.17%, the estimated mean SLNR 14.95%, and the estimated 5th percentile 12.53%.

## Figures and Tables

All are generated by `figures/gen_*.py` from `experiments/a7/results/`, with draft captions in `figures/latex_includes.tex`.

| Item | Content | Width | Priority |
|---|---|---|---|
| Fig. 1 | Geometry and certificate construction (featured case): top view, one site's arc inside its asymmetric sector, leakage fields and endpoint zonotopes of $\hat S$ and $S_{\rm N}$ | full | Keep; shorten the caption |
| Fig. 2 | Certified gain Γ by tolerance and SNR, both families | full | Must keep |
| Fig. 3 | Tolerance sweep: $F_{\rm end}$ vs $\bar I(\hat S)$; SLNR bracket vs $U(S_{\rm N})$ | column | Must keep |
| Fig. 4 | Screening: survivor fraction vs M, time per case, uniqueness share | column | Keep; panel (b) can be cut if space is short |
| Table I | Protocol | column | Can move into the text if space is short |
| Table II | Results summary (C1, C2, baselines, non-ideal, featured instance) | column | Must keep; drop its featured-instance block (Fig. 1 already shows that case) and put the R021 rows in its place |

Captions round certificate bounds outward (upper bounds up, witnesses down); `figures/fig1_values.json` holds the rounded values.

## Known Weaknesses (state them in the paper)

- **Novelty is narrow** (main reviewer risk). Per-layout exact endpoint cover and sector bounds are established tools. The contribution rests on family-wide sharing, the resulting family-level guarantees, and the measured yield.
- **Finite family only.** The results concern one aligned candidate family and robust clearance; they say nothing about continuous-position optimality.
- **Co-aligned receivers** ($x_P = 0$): every primary case is inconclusive, and every screening-cap hit is there. On the stress panel, the certified D/P-dependency losses of co-aligned layouts have lower endpoints of 1.82%–28.3%; these are lower bounds, not the losses.
- **Uniqueness is rare at large ε** (9–15% at 0.08λ); those cases claim the bracket only.
- **Nominal and average-case cost:** the median nominal sacrifice is small, but the tail is large (max 88.5%), and the mean SLNR can drop substantially in individual cases (Experiment 7).
- **Baselines:** budgets are unmatched; B-CR is not an all-corner robust optimizer.
- **Screening is instance-dependent:** the bank pass scales with $|\mathcal F|$, and co-aligned cases keep almost the whole family.
- **Model scope:** one desired/protected pair, one waveguide, one aligned candidate aperture, equal site power, separable channels, position errors only (no activation errors, no coupled power depletion), no hardware validation.
- **Numerics:** float64 evaluation of analytical statements, not validated interval arithmetic. The production code (`a7_core.py`, `tables()`) omits the tiny nominal D-phase residual from $\beta_D$; the reviewers' replays of all 1,056 primary winners show $L$ lower by at most about 2.1e-12–2.7e-12 relative with the residual included, and no dominance or uniqueness sign changes. By the author's decision the production code is not changed before submission; the omission is disclosed.
- **Claim gate:** R020 is provisional (no `/experiment-audit`).

## Claim Boundaries (writer guidance — not manuscript prose)

- **Terminology.**
  - $\hat S$: "GCS layout"; $S_{\rm N}$: "exhaustive nominal layout".
  - "Best-found SLNR witnesses", never "SLNR-minimizing witnesses".
  - "Certificate inconclusive" for $\Gamma \le 0$, never "robust is worse".
  - B-CR: "same-start shared-template swap heuristic; budgets unmatched".
  - "Evaluated numerically in float64", never "machine-verified".
  - "Unique robust-optimal layout within the family" only when the test passes; "exact certificate optimum" only for uncapped cases.
- **Phrases that must not appear:** "always improves"; "universally superior"; "globally optimal PASS placement"; "optimal over continuous placements"; "no-cost robustness"; "robustness costs only 0.4%"; "machine-verified"; "exact continuous-box solver/adversary"; "polynomial-time global optimization"; "exact optimum" for capped cases; "all adversaries covered by 2M witnesses"; "within 1% in every case"; "every layout leaks 0.80"; "fundamentally unprotectable" (without $p$, $I_{\max}$ and family); "same compute budget"; "best robust heuristic"; "B-CR solves the worst-case problem"; "hardware validated"; "model-independent"; "same physical noise across models"; "negative cases are only a bound artifact"; "the negative region is repaired"; "the method still wins there"; "improves the lower tail" (unqualified); "Monte Carlo worst-case guarantee"; "dependency dominates the full-grid gap"; "Minkowski-sum relaxation"; "exact continuous worst case"; "sampling validates the bounds"; "screening delivers 38× speedup"; "dependency losses are at most 28%".
- **Absolute words:** test "all", "every", "never", "no" against every data row before using them.
- **Rounding:** round certificate bounds outward in captions and text.
- **Scope in claims:** state the population ($\epsilon > 0$, $P \ne D$, 528 per family; the baseline slice; the 54-case tolerance sweep; the 32-case stress panel) inside each claim. Keep generic caveats in one Limitations paragraph.
- **Choose the contest the paper wins:** certified guarantees and family-level statements over exhaustive nominal selection, not raw average performance.

## Related Work and Citations

Bibliography entries already in `fyp_report/latex/references.bib` (DOIs present; audit pending): fukuda2022pinching, ding2025perspective, liu2026tutorial, ouyang2025array (base array model), xu2025downlink, wang2025noma, tegos2025uplink, ding2025isac, zhu2024movable, new2025tutorial, yang2026nearfield, su2025positionerror, byrd1995lbfgsb. New entries must come from DBLP / CrossRef (the `/paper-write` chain); never write BibTeX from memory.

| Group | Works (identifiers from `idea-stage/`) | Use |
|---|---|---|
| PASS foundations | Fukuda et al. 2022; Ding et al. 2025; Liu et al. 2026 tutorial; Ouyang et al. 2025 (arXiv:2501.05657) | Background; base channel and array model |
| Nominal interference-aware PASS | FullPASS (arXiv:2607.19546); Li et al. (arXiv:2609.29200; verify) | Nominal selection that this paper robustifies |
| Robust PASS, other error sources | Feng et al. (arXiv:2604.09774, user location); Sun et al. (arXiv:2512.18075, CSI) | Contrast: uncertainty is not in the pinch positions |
| Pinch-position errors | **Jiang–Schotten (arXiv:2609.31088), must cite**; Pakravan et al. (arXiv:2604.12156); Chen et al., H-PASS, IEEE TWC 2026 (DOI 10.1109/TWC.2026.3664320) | Closest neighbours; statistical or hardware-compensation treatments |
| Movable-antenna position errors | Yang et al., IEEE TVT 2026 (arXiv:2601.17825; per-element box errors, Taylor model); Zhang et al. (arXiv:2609.23323; nonlinear enclosures) | Method neighbours for continuous positions |
| Interval / sector tolerance analysis | Anselmi et al., IEEE TAP 2013 (verify); Poli et al., IEEE TAP 2015; Arnestad et al., JASA 2023 (arXiv:2306.13106) | Credited tools for Theorem 1 |
| Rank-2 binary quadratic maximization | **Karystinos–Pados, IEEE TIT 2007 (DOI 10.1109/TIT.2007.903130); Karystinos–Liavas, ICASSP 2008 (DOI 10.1109/ICASSP.2008.4518425) / IEEE TIT 2010; Allemand et al., Math. Program. 2001 (DOI 10.1007/s101070100233); Ferrez et al., EJOR 2005 (DOI 10.1016/j.ejor.2003.04.011), must cite** | Credited per-layout basis of Theorem 2 |
| Safe screening | **El Ghaoui, Viallon, Rabbani (arXiv:1009.4219), must cite** (or say "safe pruning") | Terminology |
| Optimization tool | Byrd et al. 1995 (L-BFGS-B) | Witness refinement |

Target about 15–18 references.

## Proposed Title

"Certified Robust Site Selection for Pinching-Antenna Systems Under Actuator Position Errors"

Alternative: "Global Certified Site Selection for Pinching-Antenna Systems via Shared Endpoint Witnesses"

## Target Venue

IEEE ICC 2027 — `IEEE_CONF`, 6 pages including references. Build and compile in Overleaf (project `PASS-ICC2027`, `/overleaf-sync`).

## Suggested Page Budget (for `/paper-plan`)

| Section | Pages |
|---|---|
| I. Introduction (problem, gap, contributions as 3 bullets, strongest result up front) | 0.8 |
| II. System and error model (Table I or inline protocol) | 0.6 |
| III. Certificates and global screening (Lemma 1, Theorems 1–2, Corollaries 1–2, GCS; Fig. 1) | 1.7 |
| IV. Numerical results (Figs. 2–4, Table II with the R021 rows; baselines, non-ideal and tail example in text) | 2.0 |
| V. Conclusion with one Limitations paragraph | 0.3 |
| References (about 15–18) | 0.6 |
| **Total** | **≈ 6.0** |

The budget is tight with two full-width figures. Keep the shared-family proof sketch, the protection bracket, the compact R021 block and the substantial-loss example. If the draft runs over, cut in this order: the featured-instance block of Table II, Fig. 4(b) (keep inclusive runtimes and cap counts in the text), Table I (move into text), Corollary 2's interference-temperature sentence.

## Source Map

| Content | File |
|---|---|
| Method, theorems, algorithm | `refine-logs/FINAL_PROPOSAL.md` (v2) |
| Proofs and independent verification | `idea-stage/handoff/GPT6_PRO_REPLY.md`, `GPT6_PRO_VERIFICATION.md` |
| All results, with per-run notes | `refine-logs/EXPERIMENT_RESULTS.md`, `refine-logs/EXPERIMENT_TRACKER.md` |
| Licensed wording and forbidden phrases | `CLAIMS_FROM_RESULTS.md` |
| Number → source-key map | `experiments/a7/results/r019_numbers.md`; R021: `experiments/a7/results/ablation_summary.md` |
| Figures, tables, draft captions | `figures/latex_includes.tex`, `figures/TABLE_*.tex`, `figures/fig*.pdf` |
| Novelty positioning | `idea-stage/NOVELTY_TARGETED_A7v2.md`, `idea-stage/LIT_REVIEW.md` |
| Reviewer guidance | `review-stage/AUTO_REVIEW.md` |
| Code | `experiments/a7/` (`a7_core.py` = GCS) |
