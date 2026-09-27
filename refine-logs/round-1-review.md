# Round 1 Review (GPT-6 Astra, ultra)

- **Thread:** `01a0dc09-8626-7381-8ced-5aeb34168c36`
- **Trace:** `.aris/traces/research-refine/2026-09-26_run01/`
- **Verdict:** REVISE
- **Overall:** 7.40 / 10
- **Estimated acceptance:** 30–40% with the present claims; 55–65% after the focused repairs.

| Problem Fidelity | Method Specificity | Contribution Quality | Frontier Leverage | Feasibility | Validation Focus | Venue Readiness |
|---|---|---|---|---|---|---|
| 9 | 7 | 6 | 9 | 8 | 7 | 6 |

<details><summary>Condensed raw findings (full response is in the session transcript; condensed copy in trace)</summary>

**Proposition 3**
- The random-sign bound is correct.
- Exact derivative: $|b_n|^2 = t^2/R^4 + k_0^2 (n_{\mathrm{eff}} + t)^2/R^2$.
- Safe statement: $\max|h_P|^2/(N\sigma^2) \ge [\sqrt{\nu_0 + \kappa_b} - \bar\rho]_+^2$.
- The remainder makes the bound vacuous in 72/528 archived cases.
- $\kappa$ is not a sufficient "when it helps" predictor.
  - Counterexample: $\kappa \approx 4.9\times10^{-6}$, yet +2.32% certified gain through the desired side.
  - The first-order box radius is $T(S) = \epsilon\max_\theta\sum_n|\Re(e^{-j\theta}b_n)|$, not $\sum_n|b_n|^2$.
- The free-space comparison is false in general: PASS is larger only if $t > -n_{\mathrm{eff}}/2$.

**Pilot facts (reproduced)**
- All 528 $L_{\rm rob}$ values reproduce; $\kappa$ reproduces to $4.1\times10^{-8}$ relative error; every $U_{\rm nom}$ reproduces by all-corner enumeration.
- By regime:

  | Regime | Cases | Certified positive | Above 5% |
  |---|---|---|---|
  | $\kappa<1$ | 276 | 65.6% | 25.7% |
  | $\kappa\ge1$ | 252 | 69.8% | 58.3% |

- Against **exhaustive** nominal selection: 359/528 certified positive, 247/528 above 5%.
- In the strongest case (+103.55%), $\sum_n|b_n|$ rises by 0.48% while $T^2$ falls by 53.4%. **The mechanism is directional.**
- $U/L$: median 1.021, 95th percentile 1.183, maximum 1.729.
- At $\epsilon = 0$ the grid pad costs 2.78%, so $\epsilon = 0$ must be special-cased.

**Required fixes**
- Recast Proposition 3 as a conditional fragility lemma.
- Explain the mechanism through the directional support.
- Use the candidate-dependent sufficient condition $(a-c)\sigma^2 > cb - ad$.
- Build a frozen driver:
  - exhaustive nominal selection;
  - endpoint-constrained robust search initialized with the nominal subset;
  - clearance constraints;
  - saved witnesses and bracket statistics.
- Narrow the novelty claim (Pakravan; Chen H-PASS).
- Move N0/N2/A8 out of the main text.
- Keep one non-ideal-channel check.

**Other judgments**
- Modernization: NONE.
- Drift: NONE for the task. The change to success condition 2 must be acknowledged.

</details>
