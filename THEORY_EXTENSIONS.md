# Theory Extensions for PASS Position Errors

## Target

We want one theory line that explains three empirical facts at the same time:

1. why the original same-sign test pattern is not adversarial;
2. why a split-mode pattern tracks the worst-case curve much better;
3. how the degradation changes under different stochastic error structures.

The goal is not a full global theorem for the nonconvex box problem. The goal is a paper-ready local mechanism that remains meaningful across deterministic and stochastic scenarios.

## Invariant Object

For the aligned PASS design `Delta*`, define the normalized weighted coherent sum

```math
\rho(\delta)
= \sum_{n=1}^{N} \alpha_n e^{-j k_0 \xi_n \delta_n},
\qquad
\alpha_n = \frac{1 / R_n(\Delta_n^*)}{\sum_m 1 / R_m(\Delta_m^*)},
\qquad
\sum_n \alpha_n = 1.
```

Ignoring higher-order amplitude perturbations, the normalized array gain is approximated by

```math
\frac{a(\Delta^* + \delta)}{a_{\mathrm{ideal}}}
\approx |\rho(\delta)|^2.
```

This is the single object that survives across the deterministic box model and the stochastic error models.

## Assumptions and Notation

- `Delta*` is the constructive phase-aligned feasible placement produced by the snapped-target rule.
- `xi_n = sin(theta_n^*) + n_eff` is the first-order phase sensitivity at `Delta_n^*`.
- The small-error regime means `k_0 |xi_n| |delta_n| << 1`, or at least small enough for the second-order truncation to be informative.
- The derivation below is a phase-dominant approximation. It explains the mechanism, but it does not prove global optimality of any continuous-box adversary.

## Main Derivation

Expand the coherent sum at small phase error:

```math
e^{-j k_0 \xi_n \delta_n}
= 1 - j k_0 \xi_n \delta_n - \frac{1}{2} k_0^2 \xi_n^2 \delta_n^2 + O(\|\delta\|^3).
```

Let

```math
\mu_\phi = \sum_n \alpha_n k_0 \xi_n \delta_n.
```

Then

```math
\rho(\delta)
= 1 - j \mu_\phi - \frac{1}{2} \sum_n \alpha_n (k_0 \xi_n \delta_n)^2 + O(\|\delta\|^3),
```

which gives

```math
|\rho(\delta)|^2
\approx
1
- \sum_n \alpha_n (k_0 \xi_n \delta_n)^2
+ \mu_\phi^2.
```

Therefore,

```math
\frac{a(\Delta^* + \delta)}{a_{\mathrm{ideal}}}
\approx
1 - \operatorname{Var}_{\alpha}(k_0 \xi_n \delta_n),
```

where

```math
\operatorname{Var}_{\alpha}(z_n)
= \sum_n \alpha_n z_n^2 - \Big(\sum_n \alpha_n z_n\Big)^2.
```

## Interpretation

The local adversary is not the pattern that rotates all phasors in the same direction. A common rotation mainly changes the global phase, not the relative phase spread.

The harmful mechanism is the weighted phase variance:

- small weighted variance means the phasors remain coherent;
- large weighted variance means the phasors spread and the coherent sum collapses.

This immediately explains why the old same-sign construction was weak in the current symmetric PASS setting.

## Split-Mode Construction

The phase-variance view suggests the deterministic construction

```math
\delta_n^{\mathrm{split}}
= \epsilon \, \operatorname{sign}(\xi_n - \bar{\xi}_{\alpha}),
\qquad
\bar{\xi}_{\alpha} = \sum_n \alpha_n \xi_n.
```

For the symmetric PASS layout used here, `alpha_-n = alpha_n` and `xi_n = n_eff + sin(theta_n^*)`, so

```math
\bar{\xi}_{\alpha} = n_{\mathrm{eff}}.
```

Hence the split-mode adversary becomes

```math
\delta_n^{\mathrm{split}}
= \epsilon \, \operatorname{sign}(\sin(\theta_n^*))
= \epsilon \, \operatorname{sign}(\Delta_n^*),
```

which is an outward left-right split, not a common shift.

This construction is still only a feasible adversarial pattern, so it gives an upper bound on the true worst-case gain:

```math
a_{\mathrm{wc}}(\Delta^*, \epsilon)
\le
a(\Delta^* + \delta^{\mathrm{split}}).
```

Empirically, it is far tighter than the old same-sign pattern in the pre-null regime.

## Stochastic Extension

Let the error vector be random with covariance `Sigma_delta = E[\delta \delta^T]` and zero mean. Define

```math
M_{\alpha} = \operatorname{Diag}(\alpha) - \alpha \alpha^T,
\qquad
D_{\xi} = \operatorname{Diag}(\xi).
```

Taking expectation in the quadratic approximation gives

```math
\mathbb{E}\!\left[\frac{a(\Delta^* + \delta)}{a_{\mathrm{ideal}}}\right]
\approx
1 - k_0^2 \operatorname{tr}\!\left(M_{\alpha} D_{\xi} \Sigma_{\delta} D_{\xi}\right).
```

This is the unifying second-order formula used in the new scenario study.

### Special Case 1: IID Uniform Box Noise

If `delta_n` are independent and uniform on `[-epsilon, epsilon]`, then

```math
\Sigma_{\delta} = \frac{\epsilon^2}{3} I,
```

so

```math
\mathbb{E}\!\left[\frac{a}{a_{\mathrm{ideal}}}\right]
\approx
1 - \frac{k_0^2 \epsilon^2}{3}
\operatorname{tr}\!\left(M_{\alpha} D_{\xi}^2\right).
```

### Special Case 2: Common-Bias Error

If `delta = b 1` with `b` zero-mean and variance `sigma_b^2`, then

```math
\Sigma_{\delta} = \sigma_b^2 \, 11^T,
```

and

```math
\mathbb{E}\!\left[\frac{a}{a_{\mathrm{ideal}}}\right]
\approx
1 - k_0^2 \sigma_b^2 \operatorname{Var}_{\alpha}(\xi).
```

Because `Var_alpha(xi)` is small in the current design, common-bias motion is almost harmless even when iid noise is not.

### Special Case 3: Correlated Errors

For correlated zero-mean errors, the same formula shows that what matters is not only error power, but also how the covariance structure projects through `M_alpha D_xi`.

This is why smooth correlated perturbations can be materially less damaging than independent perturbations with matched marginal variance.

## Scope and Non-Claims

- The quadratic theory is a small-error mechanism, not a proof of the global continuous-box optimum.
- The split-mode construction is a strong constructive upper bound, not a universal exact minimizer theorem.
- The continuous-box best-found search improves the numerical evidence, but it is still a best-found result unless a global optimality proof is added later.
