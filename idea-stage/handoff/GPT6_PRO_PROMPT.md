# Deep Verification & Innovation Request — Certified Robust Site Selection for Pinching-Antenna Systems (target: IEEE ICC 2027)

**Output language:** reply in Chinese. Keep all mathematics, variable names, paper titles, and technical terms in English.

## 0. Your Role and What I Need

Act as three people at once:
1. **A rigorous communication/signal-processing theorist** who checks every statement below line by line.
2. **A hostile but fair IEEE ICC Technical Program Committee member** (Wireless Communications or Signal Processing for Communications symposium).
3. **A senior co-author** whose job is to make this 6-page paper as likely to be accepted as possible by adding *correct, feasible* novelty.

Please think deeply and take your time. When you have a code sandbox, **run the reference code in §7 and check the numbers yourself**; do not trust my summaries. Label every mathematical statement you give as one of:
- **[PROVEN]** — with a complete proof;
- **[CORRECTED]** — my statement was wrong, and here is the right one with proof;
- **[CONJECTURE]**;
- **[NUMERICALLY OBSERVED]** — say what you ran.

**Citation rule:** never invent references. Give an arXiv ID or DOI only if you actually verified it (by browsing). Otherwise write "unverified".

## 1. Hard Constraints

- **Venue:** IEEE ICC 2027 symposium paper.
- **Length:** 6 pages in two-column IEEEtran, *including references*.
- **Deadline:** 2 October 2026. Today is 26 September 2026, so there are about 5 working days: roughly 2 for experiments, 2 for writing, 1 for audits.
- **Team:** one author.
- **Compute:** CPU only (NumPy/SciPy). No hardware, no GPUs, no new datasets.
- **Goal:** the highest acceptance probability, with a *strong task, clear structure, and strong mathematics*. AI/learning is optional; it should be used only if it is genuinely necessary.

## 2. Background: The Author's Graduation Project (the analytic baseline)

**Pinching-antenna system (PASS) model** (Ouyang–Wang–Liu–Ding, *Array Gain for PASS*, IEEE Commun. Lett. 2025, arXiv 2501.05657):
- A dielectric waveguide runs along the x-axis at height $d$, fed at $x_f$.
- Pinching antennas at positions $x_n$ radiate a signal that has travelled a guided path followed by a free-space path.
- Received phase: $\psi(x) = k_0\big(R(x) + n_{\mathrm{eff}}(x - x_f)\big)$.
- Amplitude: $1/R$.
- Alignment is achieved **only by where the pinches are placed**; there are no phase shifters.

**Results from the graduation project (and a follow-up) that we build on:**
- **C1 — sensitivity.** A position error $\delta_n$ causes a phase error $k_0\xi_n\delta_n$ with $\xi_n = n_{\mathrm{eff}} + \sin\theta_n$.
  - To second order, the normalized gain loss is $\mathrm{Var}_\alpha(k_0\xi_n\delta_n)$, a weighted phase variance: common-mode error is nearly harmless, differential error is harmful.
  - Covariance predictor: $1 - k_0^2\,\mathrm{tr}(M_\alpha D_\xi \Sigma D_\xi)$.
  - This is Ruze- or Rondinelli-type tolerance theory in form, so it is **not** novel by itself.
- **N0 — correctness fix.** The original construction mirrored the positive-side solution, which left the upstream half misaligned: residual phase up to 0.683 rad and only 95.7% of the ideal gain. The fix solves the alignment equation $R(x) + n_{\mathrm{eff}}x = (\text{integer})\lambda + C$ on both sides; each root is unique because $\psi' > 0$.
- **N1.** A nonlinear (mean-value / endpoint) certified lower bound on the single-user worst-case gain under per-element boxes $|\delta_n| \le \epsilon$. Paired with the "split-mode" feasible adversary, it pins the true worst case to within about $2.8\times10^{-4}$.
- **N2.** Tolerance-aware *upstream* placement (toward the feed) of the aligned aperture.
  - With 0.08 dB/m waveguide loss, the attenuation-aware nominal optimum shifts the aperture by only −0.10 m, whereas the certificate optimum shifts it by −1.4 m at $\epsilon = 0.1\lambda$, giving certified worst-case gain 1.35× the nominal optimum.
  - Generic upstream placement due to attenuation is already known (Xu–Ding–Schober–Chang, arXiv 2506.23966).

## 3. The Selected Paper Idea (A7)

**Title (working):** *Certified Robust-SLNR Site Selection for Pinching-Antenna Systems Under Actuator Position Errors.*

**System.**
- $f_c = 28$ GHz, $\lambda = 10.714$ mm, $k_0 = 586.43$ rad/m, $n_{\mathrm{eff}} = 1.44$.
- The waveguide lies at height $d = 3$ m along x (at $y = 0$); feed at $x_f = -10$ m.
- Desired receiver D at $(0, 0, 0)$; protected receiver P at $(x_P, y_P, 0)$.
- For receiver $r$: $R_r(x) = \sqrt{(x - x_r)^2 + y_r^2 + d^2}$, $\psi_r(x) = k_0\big(R_r(x) + n_{\mathrm{eff}}(x - x_f)\big)$, $z_r(x) = A_r(x)e^{-j\psi_r(x)}$ with $A_r = 1/R_r$ (ideal isotropic model).
- **Candidate family (N0).** $M = 24$ sites on consecutive D-aligned levels. They are all phase-aligned for D (a common phase mod $2\pi$); minimum spacing is $0.682\lambda$.
- **Selection.** Choose $|S| = N = 8$. Total power is split equally; the received powers are $|h_r|^2/N$ with $h_r(S, \delta) = \sum_{n \in S} z_r(x_n + \delta_n)$.
- **Noise.** Fixed physical noise $\sigma^2 = A_{\rm ref}/\mathrm{SNR}_{\rm ref}$, where $A_{\rm ref}$ is the coherent gain toward D of the central 8-site block. It is identical for every layout.
- **Actuator errors.** $|\delta_n| \le \epsilon$ independently. Robust clearance requires spacing $\ge d_{\min} + 2\epsilon$ with $d_{\min} = 0.5\lambda$.
- **Objective.** Robust SLNR:
$$W(S) = \min_\delta \frac{|h_D|^2/N}{\sigma^2 + |h_P|^2/N}.$$

**Claimed mathematics** (please verify each item and give corrected statements where needed).
- **Lemma 0 (monotone guided phase).**
  - For $n_{\mathrm{eff}} > 1$: $\psi_r'(x) = k_0(n_{\mathrm{eff}} + \sin\theta_r) \in [k_0(n_{\mathrm{eff}} - 1),\ k_0(n_{\mathrm{eff}} + 1)]$, where $\sin\theta_r = (x - x_r)/R_r$. Hence each site's feasible phase set over the box is exactly $[\psi_r(x_n - \epsilon), \psi_r(x_n + \epsilon)]$.
  - $|z_r'|^2 = A'^2 + A^2\psi'^2 \ge k_0^2(n_{\mathrm{eff}} - 1)^2A^2$: no PASS site's *complex contribution* is first-order insensitive to actuator error.
  - $\xi_P \to n_{\mathrm{eff}} + 1$ for sites downstream of P (away from the feed) and $\to n_{\mathrm{eff}} - 1$ for sites upstream of P.
- **Proposition 1 (desired-gain lower bound).** Let $\beta_{D,n} = \max\{\psi_D(x_n + \epsilon) - \psi_D(x_n),\ \psi_D(x_n) - \psi_D(x_n - \epsilon)\}$ and let $A^-_{D,n}$ be the exact minimum of $A_D$ on the box. If every $\beta_{D,n} \le \pi/2$ and the sites share a common nominal phase, then
$$|h_D|^2 \ge \Big(\sum_{n \in S} A^-_{D,n}\cos\beta_{D,n}\Big)^2.$$
- **Proposition 2 (sector-support leakage upper bound).**
  - Each P-contribution lies in the annular sector $\{Ae^{j\phi}: A \in [A^-_{P,n}, A^+_{P,n}],\ \phi \in [\phi_n - \beta_{P,n}, \phi_n + \beta_{P,n}]\}$, where $\phi_n = -\psi_P(x_n)$.
  - Its support function is $s_n(\theta) = A^\pm\cos(\max(\operatorname{dist}(\theta, \phi_n) - \beta_{P,n}, 0))$, using $A^+$ when the cosine is positive and $A^-$ otherwise.
  - Then
$$|h_P| \le \max_\theta\sum_n s_n(\theta) \le \max_{\theta \in \Theta_K}\sum_n s_n(\theta) + \frac{\Delta\theta}{2}\sum_n A^+_{P,n},$$
  where the last term is a Lipschitz grid correction with $K = 1440$.
  - Wording: this is the exact support of the *enclosing sector*, not of the true curve-shaped uncertainty set.
- **Corollary (bracket and certified dominance).**
  - $L(S) := L_D/(\sigma^2 + \bar I) \le W(S) \le U(S)$, where $U$ is the minimum SLNR over feasible witnesses evaluated exactly.
  - $L(S_R) > U(S_N) \Rightarrow W(S_R) > W(S_N)$.
  - For a fixed pair and witness, with $a = L_D(S_R)$, $b = \bar I(S_R)$, $c = G_D(S_N, \hat\delta)$, $d = I_P(S_N, \hat\delta)$, the test holds iff $(a - c)\sigma^2 > cb - ad$.
  - At $\epsilon = 0$ the grid pad must be switched off; otherwise it creates an artificial 2.78% loss.
- **Lemma 3 (conditional leakage fragility).**
  - $h_P(\delta) = h_0 + \sum_n b_n\delta_n + r$ with $|r| \le \rho = \tfrac12\sum_n\epsilon^2\sup|h''_{P,n}|$.
  - $b_n = e^{-j\psi_n}\big[-t_n/R_n^2 - jk_0(n_{\mathrm{eff}} + t_n)/R_n\big]$ with $t_n = \sin\theta_{P,n}$.
  - Random-sign averaging gives
$$\max_\delta \frac{|h_P|^2}{N\sigma^2} \ge \big[\sqrt{\nu_0 + \kappa_b} - \bar\rho\big]_+^2, \qquad \nu_0 = \frac{|h_0|^2}{N\sigma^2},\ \kappa_b = \frac{\epsilon^2\sum_n|b_n|^2}{N\sigma^2},\ \bar\rho = \frac{\rho}{\sqrt{N\sigma^2}}.$$

**Algorithm.**
1. Precompute the per-site tables ($O(MK)$); evaluating a subset then costs $O(NK)$.
2. Compute the exhaustive nominal-SLNR optimum $S_N$ over all $\binom{24}{8} = 735{,}471$ subsets (about 0.5 s).
3. Run swap local search on $L(S)$ started from $S_N$ plus 8 random starts.
4. Compute witnesses from all $2^8$ corners plus L-BFGS-B refinement.
5. Control: identical endpoints (sites 0 and 23 forced) for fixed aperture.

## 4. Evidence So Far (pilot-level; the paper-final runs have NOT been done yet)

**Positive.**
- The mechanism is real. In an independent rerun by an external reviewer (GPT-6 Astra) against **exhaustive** nominal selection:
  - **359/528** cases show a certified positive gain, and **247/528** exceed 5%;
  - the grid was 33 P-geometries × 4 noise levels × 4 tolerances;
  - with identical endpoints, 16–22/33 cases exceed 5% (median 4–12%) across the 4 settings tested.
- The strongest single case gave +103.6%.
- The certificates survived 216,576 feasible random checks with no violation.

**Negative / corrected** (please take these seriously).
1. **Learning was tested and failed.**
   - An MLP mapping geometry to the site subset reached a median of only 0.669 of the reference certificate.
   - A learned warm start ≈ a random warm start (0.950 vs 0.943).
   - Deterministic robust search already takes about 32 ms. AI was therefore dropped.
2. **κ is not a predictor of "when robust selection helps."**
   - We tried $\kappa = \epsilon^2k_0^2\sum\xi_P^2A_P^2/(N\sigma^2)$ as a universal threshold. Median certified gain did rise monotonically across κ bins (0 → +11%), but:
   - a counterexample exists ($\kappa \approx 4.9\times10^{-6}$ with +2.3% gain from the desired side);
   - large κ does not guarantee that a better subset exists;
   - the remainder $\rho$ makes Lemma 3 vacuous in 72/528 cases.
3. **"Directional spreading of leakage derivatives" is not universal.**
   - The first-order box radius $T(S) = \epsilon\max_\theta\sum_n|\Re(e^{-j\theta}b_n)|$ dropped by 53% in the strongest case.
   - But $T$ *increased* in 5 of 357 positive-gain comparisons.
4. **Brackets are not uniformly tight.** $U/L$ has median 1.021, 95th percentile 1.183, and maximum 1.729; they are loosest when D and P respond similarly.
5. **"PASS nulls are more fragile than free-space arrays" is false in general.** It holds only when $\sin\theta > -n_{\mathrm{eff}}/2$.

**Review history.**
- Novelty: 6/10, PROCEED.
- Mock ICC review before repairs: 4/10, weak reject — "established ingredients".
- Method refinement: 7.40 → 7.70/10, still REVISE; the missing piece is the principal matched-endpoint result.
- Estimated acceptance: 40–50% now; 60–70% if the matched-endpoint result holds.

## 5. Closest Literature (as known to us; please extend and correct)

- **FullPASS** (arXiv 2607.19546): nominal interference-constrained PASS activation. It explicitly leaves position uncertainty to future work.
- **Li et al.** (arXiv 2609.29200): nominal full-duplex PASS via WMMSE.
- **Zhang et al.** (arXiv 2609.23323, 20 Sep 2026): movable-antenna ISAC with nonlinear phase enclosures and all-error SINR constraints. This is the key collision for "nonlinear certificates".
- **Yang et al.** (arXiv 2601.17825 / IEEE TVT 2026): movable-antenna near-field nulling under per-element box errors (Taylor analysis, QCQP / closed forms).
- **Arnestad et al.** (JASA 2023, arXiv 2306.13106): interval-arithmetic worst-case beampatterns (annular sectors / Minkowski sums, backtracking). **Poli et al.** (IEEE TAP 2015): interval phase tolerance.
- **Chen–Qi–Dobre–Yuen**, *Hybrid PASS* (IEEE TWC 2026, DOI 10.1109/TWC.2026.3664320): simulated multi-PA position errors, mitigated with reconfigurable leaky-wave antennas.
- **Pakravan et al.** (arXiv 2604.12156): single-radiator pinching-position uncertainty (secrecy outage).
- **Robust PASS under user-location / CSI uncertainty:** 2604.09774, 2601.19704, 2507.12582, 2512.18075; also Sun et al., IEEE WCL 2026, *Robust Beamforming for PASS-Based Multi-User Communications*.
- **Learned PASS:** GNN PASS (2502.05447); DRL placement (2605.08039); GALR-Net (graph attention, user-location uncertainty, 2026).
- **Robust learning under movable-antenna hardware impairment:** Xiu et al., 2508.13839 / TWC 2026.
- **Classical tolerance theory:** Ruze 1966; Rondinelli 1959.

## 6. Tasks (please do all of them, in this order)

### Task A — Deep verification (the most important task)

For **each** of Lemma 0, Proposition 1, Proposition 2, the Corollary, and Lemma 3:
1. Give a complete proof, or a counterexample plus a corrected statement.
2. List every hidden assumption. Candidates to check:
   - common nominal phase modulo $2\pi$, including the feed-offset constant;
   - the $\pi/2$ condition;
   - that phase monotonicity makes the endpoint interval exact;
   - the amplitude extrema of $1/R$ (and with attenuation $e^{-\alpha(x - x_f)}$ and directivity $\cos^q\theta$);
   - the correctness of the sector support function, including the $A^-$ branch;
   - the Lipschitz constant of $s_n(\theta)$ and the grid correction;
   - the positivity of the denominators in the dominance test;
   - equal-power normalization;
   - clearance under independent boxes.
3. For Lemma 3, derive an **explicit, computable** $\sup_{|u| \le \epsilon}|h''_{P,n}(x_n + u)|$ bound, so $\rho$ is fully specified.
4. Tell me which statements are standard and must be cited, and which are genuinely specific to PASS.

### Task B — Hostile ICC review

Write a mock review from the Wireless Communications or Signal Processing for Communications symposium: summary, strengths, weaknesses, score (1–10), confidence, and a decision. Then list the **top 5 rejection risks**, each with the cheapest fix that fits the constraints. In particular, is "certified dominance over the exhaustive nominal optimum within a matched aligned family" a meaningful and fair comparison? What would a reviewer say about restricting to D-aligned sites?

### Task C — Collision search (browse if you can)

Search arXiv, IEEE Xplore, and Google Scholar for 2025–2026 work on:
- pinching-antenna / PASS robustness to antenna **position** or **activation** errors with multiple coherent antennas;
- certified or worst-case SLNR / leakage / nulling under **position** errors for movable, fluid, or pinching antennas;
- interval or sector enclosures used for antenna selection.

Report only papers you verified, with IDs. State plainly whether any paper already contains the A7 result.

### Task D — Innovation upgrades (think hard; this is where I want your creativity)

Propose **3–6 upgrades** that would raise acceptance probability. They must stay feasible: at most about 2 days of CPU work plus proofs, and they must fit in 6 pages. For each upgrade give:
- the idea;
- the precise theorem or proposition statement, with a proof or proof sketch;
- why it is PASS-specific or otherwise non-trivial;
- the minimal experiment;
- the risk;
- the expected acceptance lift.

Please at least evaluate these candidate directions (and add your own):

1. **A converse / achievability pair.** Is there a lower bound on $\min_{S \in \mathcal F}\max_\delta |h_P(S,\delta)|^2$ — i.e., "no selection in the family can protect P below X under tolerance ε" — that uses the guided-wave sensitivity floor from Lemma 0? A matching achievability would give a strong mathematical statement.
2. **Structural optimization of the certificate.** Can $\max_S L(S)$ be solved exactly or with a provable approximation ratio? For example: for a fixed angle θ the leakage support is additive in the sites, so consider Dinkelbach plus per-angle sorting or DP, plus an angle-grid argument. What complexity and what gap guarantee result?
3. **A correct "when does robust selection help" theorem** to replace the failed κ threshold. It could be necessary or sufficient, or a closed-form region in (geometry, ε, σ²) for a nominal-null subset to be certifiably beaten.
4. **Task reframing** that is more "strong task" for ICC, such as:
   - certified leakage-ceiling (interference-temperature) constrained power or SNR maximization;
   - *certified secrecy* with P as an eavesdropper;
   - which framing maximizes acceptance with the same mathematics?
5. **Is there any place where AI/learning would be genuinely necessary** — not decorative — within 5 days? Examples: amortized certified selection for a moving P, or learning-augmented branch-and-bound with certificates as a safety filter. Be honest: if the answer is no, say so.
6. Whether the graduation-report material (C1 sensitivity, N2 upstream placement) should appear in this paper at all, and in what form.

### Task E — Final recommendation

Give the **single best paper plan** you would bet on:
- title;
- one-sentence thesis;
- 3 contribution bullets;
- the exact theorem/lemma list (statements);
- a figure/table plan (at most 4 figures);
- the experiment list, marked must-run vs optional;
- a page budget;
- what to cut;
- your estimated acceptance probability, with reasoning.

Also give a **results → allowed-claims** table for the plausible outcomes of the main experiment.

## 7. Reference Code (numpy only; please run it)

Expected output on our machine:

```
S_nom [1 6 7 8 16 18 19 20] S_rob [3 4 7 8 9 13 14 17] L(S_rob)=53.422  U(S_nom)=42.154  certified gain=+26.7%
```

```python
# Minimal standalone reproduction of the A7 certificate (numpy only).
import itertools, numpy as np
C, FC = 3e8, 28e9; LAM = C / FC; K0 = 2 * np.pi / LAM
D_H, NEFF, XF = 3.0, 1.44, -10.0          # waveguide height, effective index, feed position (m)
TH = np.linspace(-np.pi, np.pi, 1441)[:-1]; DTH = TH[1] - TH[0]

def R(x, ux, uy): return np.sqrt((x - ux) ** 2 + uy ** 2 + D_H ** 2)
def psi(x, ux, uy): return K0 * (R(x, ux, uy) + NEFF * (x - XF))          # strictly increasing if NEFF > 1
def z(x, ux, uy): return np.exp(-1j * psi(x, ux, uy)) / R(x, ux, uy)      # isotropic amplitude 1/R

def aligned_sites(M, center=0.0):                                          # N0: D-aligned consecutive levels
    f = lambda x: np.sqrt(x ** 2 + D_H ** 2) + NEFF * x
    m0 = np.round(f(center) / LAM); out = []
    for t in (m0 + np.arange(-(M // 2), M - M // 2)) * LAM:
        lo, hi = -50.0, 50.0
        for _ in range(200):
            mid = 0.5 * (lo + hi); lo, hi = (mid, hi) if f(mid) < t else (lo, mid)
        out.append(0.5 * (lo + hi))
    return np.array(out)

def amp_range(x, eps, ux, uy):                                              # exact extrema of 1/R on [x-eps, x+eps]
    e = np.stack([1 / R(x - eps, ux, uy), 1 / R(x + eps, ux, uy)])
    amax = np.where((x - eps <= ux) & (ux <= x + eps), 1 / R(ux, ux, uy), e.max(0))
    return e.min(0), amax

def tables(xs, eps, P):
    ux, uy = P
    bD = np.maximum(psi(xs + eps, 0, 0) - psi(xs, 0, 0), psi(xs, 0, 0) - psi(xs - eps, 0, 0))
    cD = amp_range(xs, eps, 0, 0)[0] * np.cos(np.minimum(bD, np.pi / 2))       # Prop. 1 per-site term
    bP = np.maximum(psi(xs + eps, ux, uy) - psi(xs, ux, uy), psi(xs, ux, uy) - psi(xs - eps, ux, uy))
    amin, amax = amp_range(xs, eps, ux, uy); phi0 = -psi(xs, ux, uy)
    gap = np.maximum(np.abs(np.angle(np.exp(1j * (TH[None] - phi0[:, None])))) - bP[:, None], 0)
    mc = np.cos(np.minimum(gap, np.pi))
    s = np.where(mc > 0, amax[:, None] * mc, amin[:, None] * mc)              # Prop. 2 sector support s_n(theta)
    return dict(cD=cD, s=s, amax=amax, valid=bool(np.all(bD <= np.pi / 2)), zD=z(xs, 0, 0), zP=z(xs, ux, uy))

def cert_L(S, T, N, s2):                                                   # certified SLNR lower bound L(S)
    LD = T["cD"][S].sum(-1) ** 2 / N
    Iup = np.maximum(T["s"][S].sum(-2).max(-1) + T["amax"][S].sum(-1) * DTH / 2, 0) ** 2 / N
    return LD / (s2 + Iup)

def nominal(S, T, N, s2):
    return (np.abs(T["zD"][S].sum(-1)) ** 2 / N) / (s2 + np.abs(T["zP"][S].sum(-1)) ** 2 / N)

def exhaustive_nominal(T, M, N, s2):
    allS = np.array(list(itertools.combinations(range(M), N)))
    return allS[np.argmax(nominal(allS, T, N, s2))]

def swap_search(f, M, N, init, rng, restarts=8):
    best, bv = None, -np.inf
    for S in [np.sort(init)] + [np.sort(rng.choice(M, N, replace=False)) for _ in range(restarts)]:
        v = f(S[None])[0]
        while True:
            cand = np.array([np.sort(np.where(np.arange(N) == i, j, S)) for i in range(N) for j in range(M) if j not in S])
            vals = f(cand); k = int(np.argmax(vals))
            if vals[k] <= v + 1e-15: break
            S, v = cand[k], vals[k]
        if v > bv: best, bv = S, v
    return best

def witness_U(xs, S, eps, P, N, s2):                                       # feasible upper bound: all 2^N corners
    x = xs[S]; Cn = np.array(list(itertools.product((-1.0, 1.0), repeat=N))) * eps
    gD = np.abs(z(x[None] + Cn, 0, 0).sum(1)) ** 2 / N; gP = np.abs(z(x[None] + Cn, *P).sum(1)) ** 2 / N
    return (gD / (s2 + gP)).min()

if __name__ == "__main__":
    M, N = 24, 8; xs = aligned_sites(M); A_REF = np.abs(z(xs[8:16], 0, 0).sum()) ** 2 / N
    P, eps, s2 = (3.0, 2.0), 0.05 * LAM, A_REF / 1e3                         # reference SNR 30 dB
    T = tables(xs, eps, P); SN = exhaustive_nominal(T, M, N, s2)
    SR = swap_search(lambda S: cert_L(S, T, N, s2), M, N, SN, np.random.default_rng(0))
    LR, UN = cert_L(SR[None], T, N, s2)[0], witness_U(xs, SN, eps, P, N, s2)
    print("S_nom", SN, "S_rob", SR, "L(S_rob)=%.3f  U(S_nom)=%.3f  certified gain=%+.1f%%" % (LR, UN, 100 * (LR / UN - 1)))
```

## 8. Output Format

1. **Executive summary** (10 lines): what is correct, what is wrong, the best upgrade, and the final recommendation.
2. **Task A:** a table with one row per statement (status | corrected statement | proof), followed by the proofs.
3. **Task B:** the mock review and the top-5 risks.
4. **Task C:** verified collisions only.
5. **Task D:** the upgrades, ranked by acceptance lift per unit of effort.
6. **Task E:** the final paper plan and the claims table.
7. **Anything I did not ask about but should have.**
