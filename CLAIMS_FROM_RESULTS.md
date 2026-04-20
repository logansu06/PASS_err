# Claims From Results

Generated: 2026-04-17

## Claim Supported

`yes`

## Supported Claim

For the current constructive phase-aligned PASS placement in the studied symmetric setting:

- the deterministic lower bound accurately characterizes the bounded-error degradation inside the guaranteed small-error region;
- in the pre-null regime, the dominant harmful bounded-error pattern is an empirical left-right split-mode phase-spread pattern, while common-bias motion is nearly harmless;
- a second-order covariance / phase-variance predictor explains the observed stochastic degradation across the studied iid uniform, common-bias, and correlated Gaussian error models.

## Supported Evidence

- `epsilon_valid_norm = 0.17126776184398004` in `PASS_err/results/config.json`.
- Over the guaranteed region, the maximum absolute gap between `wc_norm` and `lb_full_norm` is about `3.40e-6`.
- Before `epsilon/lambda = 0.175`, the maximum split-versus-box-best-found gap is about `1.57e-5`.
- At `epsilon/lambda = 0.1`:
  - `box-best-found = 0.38172695`
  - `split-mode = 0.38174263`
  - `common-bias = 0.99993864`
- In the box-validation table, corner and continuous-box best-found match at `0.02, 0.05, 0.10, 0.15`, but differ at `0.175`, where the best-found box adversary reaches numerical zero.
- In the stochastic scenario table at `epsilon/lambda = 0.1`:
  - iid uniform mean `0.76980750`, quadratic approx `0.74416072`
  - common-bias mean `0.99997949`, quadratic approx `0.99997959`
  - correlated Gaussian mean `0.84576180`, quadratic approx `0.83094739`

## Not Supported

- No claim that the continuous-box adversary is globally solved.
- No theorem that split-mode is the exact optimizer for the box problem.
- No general design-optimality claim across placement families.
- No broad generalization across arbitrary `N`, `d`, `delta_p`, or arbitrary covariance structures.

## Missing Evidence

- `N` sweep.
- `d` or `delta_p` sweep.
- Stronger near-null continuous-box validation with more restarts or an independent global-search cross-check.
- Optional placement-family baseline section if the paper wants a comparative design claim.

## Recommended Wording

Claim only what the data clearly supports:

> For the current constructive phase-aligned PASS placement in the studied symmetric setting, the normalized gain under bounded position errors is accurately characterized in the guaranteed small-error regime by a deterministic lower bound; in the pre-null regime, degradation is dominated by an empirical left-right split-mode phase-spread pattern while common-bias motion is nearly harmless; and a second-order covariance / phase-variance predictor explains the observed stochastic degradation across the studied iid uniform, common-bias, and correlated Gaussian models. We do not claim a globally certified continuous-box worst-case or general design optimality.
