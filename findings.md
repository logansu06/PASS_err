# PASS Result-to-Claim Evaluation (2026-04-17, updated after placement baselines)

- claim_supported: partial
- confidence: medium
- note: local judgment only; secondary reviewer delegation was unavailable in this session.

## Supported Scope

The updated experiments strongly support the narrow one-design robustness story for the current constructive phase-aligned PASS placement in the studied symmetric setting:

- The deterministic lower bound tightly characterizes normalized degradation inside the guaranteed small-error region.
- In the pre-null regime, the harmful bounded-error pattern is empirically a left-right split-mode phase-spread pattern, while common-bias motion is nearly harmless.
- The second-order covariance / phase-variance predictor explains the observed stochastic trends for the studied iid uniform, common-bias, and correlated Gaussian models over the tested small-error range.
- The results still do not support any globally certified continuous-box optimum claim or any general design-optimality claim.

The new baseline section supports only a narrower comparative design claim:

- The constructive aligned placement is better than the naive uniform-aperture baseline on the sampled robustness metrics, especially for box-best-found robustness.
- The constructive aligned placement is not the best same-aperture placement among the tested candidates, because the direct nominal optimizer is better on every reported metric in the new section.

## Key Evidence

- `PASS_err/results/config.json` logs `epsilon_valid_norm = 0.17126776184398004`.
- Over the guaranteed region, the maximum absolute gap between `wc_norm` and `lb_full_norm` in `PASS_err/results/data_main.csv` is about `3.40e-6`.
- Before `epsilon/lambda = 0.175`, the maximum split-versus-box-best-found gap in `PASS_err/results/data_main.csv` is about `1.57e-5`.
- At `epsilon/lambda = 0.1` for the aligned design:
  - `wc_norm = 0.38172695`
  - `split_norm = 0.38174263`
  - `common_bias_norm = 0.99993864`
- In `PASS_err/results/data_error_scenarios.csv` at `epsilon/lambda = 0.1`:
  - iid uniform mean `0.76980750`, quadratic approximation `0.74416072`
  - common-bias mean `0.99997949`, quadratic approximation `0.99997959`
  - correlated Gaussian mean `0.84576180`, quadratic approximation `0.83094739`
- In `PASS_err/results/data_baseline_summary.csv` at `epsilon/lambda = 0.10`:
  - aligned constructive vs uniform aperture:
    - nominal `1.70115737` vs `1.68249052` (`+1.1%`)
    - box-best-found `0.44350703` vs `0.38857314` (`+14.1%`)
    - iid mean `1.31150359` vs `1.29980612` (`+0.9%`)
  - direct nominal optimizer vs aligned constructive:
    - nominal `+1.69%`
    - box-best-found `+11.09%`
    - iid mean `+1.68%`
- In `PASS_err/results/data_baseline_curves.csv`, aligned constructive stays above uniform aperture on the sampled box-best-found and iid-mean curves, while the direct nominal optimizer stays above aligned constructive on those same sampled curves.

## Why The Verdict Is Not `yes`

The new design claim is not fully supported as currently phrased:

- `materially outperforms a naive uniform-aperture baseline` is too broad if it is read across all reported metrics. The only clearly material gain is box-best-found robustness; nominal gain and stochastic means improve only by about `1%`.
- The direct nominal optimizer beats the constructive aligned design on every reported same-aperture metric in the new section, so any near-optimal or generally preferable design language would be unsupported.

Because the intended claim bundle now includes this comparative design statement, the overall verdict should be `partial`, not `yes`.

## Limits

- Continuous-box search is still best-found, not globally certified.
- The split-mode construction is empirically near-adversarial in the current symmetric setting, not a theorem.
- The stochastic predictor is validated only for the studied placement and the tested range up to `epsilon/lambda = 0.1`.
- No `N` sweep or `d` / `delta_p` sweep yet, so comparative placement conclusions are not established beyond the current setup.

## Recommended Working Claim

For the current constructive phase-aligned PASS placement in the studied symmetric setting, the deterministic lower bound tightly characterizes normalized bounded-error degradation inside the guaranteed small-error region; in the pre-null regime, degradation is empirically dominated by a left-right split-mode phase-spread pattern while common-bias motion is nearly harmless; and a second-order covariance / phase-variance predictor explains the observed stochastic trends for the studied iid uniform, common-bias, and correlated Gaussian models. In the tested same-aperture comparison, the constructive aligned placement is more robust than a naive uniform-aperture baseline, especially in box-best-found robustness, but it is not the best placement among the tested candidates because the direct nominal optimizer performs better on all reported metrics. We do not claim a globally certified continuous-box optimum or any general design optimality.
