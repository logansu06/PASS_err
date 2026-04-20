# Auto Review Log

Started: 2026-04-17

## Round 1

### Assessment (Summary)

- Score: 3/10
- Verdict: not ready
- Key criticisms:
  - The old `exact worst-case` wording was not justified because the implementation only searched box corners.
  - The old same-sign constructive upper bound was ineffective and did not match the observed degradation.
  - The project lacked multi-scenario evidence outside the single bounded-box setting.
  - The theorem-supported region and the empirical region were not clearly separated.

### Reviewer Raw Response

<details>
<summary>Click to expand full reviewer response</summary>

**Score:** `3/10` for strong-venue publication readiness.

**Verdict:** `NOT READY`

The strongest thing here is not the full current story. It is a much narrower one: a clean PASS sensitivity model plus a deterministic small-error lower bound that appears numerically very tight for the studied setting. Everything beyond that is currently under-supported.

1. **Your “exact worst-case” claim is not justified.**
The report defines
\[
a_{\mathrm{wc}}(\Delta^\*,\epsilon)=\min_{\|\delta\|_\infty\le \epsilon} a(\Delta^\*+\delta),
\]
but for `N=16` the implementation evaluates only corner patterns `δ_n ∈ {±ε}`. For a nonconvex trigonometric objective, that is not automatically the continuous-box minimum. Calling this “exact worst-case” is too strong unless corner optimality is proved.
**Minimum fix:** either prove corner optimality in the regime you use, or explicitly rename the result to a `corner-restricted adversary` and add continuous-box validation at representative `ε` via multistart coordinate descent / local search. Also check monotonicity: true worst-case vs `ε` cannot increase.

2. **The upper-bound story is not working.**
Your constructive test pattern is essentially useless as an upper bound in the current numerics. It stays near 1 while the worst-case gain collapses. So the paper currently promises “lower and upper bounds,” but only the lower-bound part is actually informative.
**Minimum fix:** remove the upper-bound claim from the main contribution, or replace it with a materially tighter adversarial construction. Do not center the paper around a bracket if you only have one useful side.

3. **The nominal placement is oversold as optimal / near-optimal.**
Section 3 frames an argmax problem, but the actual method is a constructive phase-alignment heuristic with wavelength snapping and spacing repair. That may be good, but it is not shown to be optimal or even near-optimal under the stated objective and constraints.
**Minimum fix:** narrow the claim to `constructive phase-aligned feasible placement`, or add a numerical comparison against direct nominal-gain optimization for small `N`.

4. **There are no meaningful baselines for the actual design question.**
You say the bound is placement-dependent and enables robustness comparison across placements, but the experiments only study one placement family. That does not support any design claim.
**Minimum fix:** add at least two baselines under the same spacing/aperture constraints:
`uniform symmetric placement` and one `alternative nominal design` or `robust-tuned design`. Show nominal gain vs worst-case gain tradeoff.

5. **The theorem-supported region and the empirical story are not cleanly separated.**
The lower bound is guaranteed only in the small-error regime `k0 |ξ_n| ε ≤ π/2`, but the narrative seems broader. If the bound stays tight beyond that, that is an empirical observation, not the theorem.
**Minimum fix:** clearly mark the guarantee region and report the bound gap outside it as empirical only.

6. **Experimental scope is too thin for a strong venue.**
`N=16`, one `d`, one spacing factor, one user geometry. The `f_c` and `n_eff` sweeps are useful sensitivity checks, but they are not enough to establish generality.
**Minimum fix:** add one `N` sweep and one geometry/spacing sweep. That is enough to materially improve credibility without exploding scope.

7. **The current writeup is still a progress report, not a paper argument.**
Placeholder references, limited related-work positioning, and no claims-to-evidence discipline.
**Minimum fix:** rewrite the contribution section around only what is actually supported.

**What the experiments support vs. what the paper claims**
There is a real mismatch:
- The experiments support a **tight deterministic lower bound** story.
- They do **not** support a meaningful upper-bound story.
- They do **not yet** support “exact worst-case over bounded continuous errors.”
- They do **not** support a design recommendation, because there are no placement baselines.

**Priority**
Prioritize, in this order:
1. `Narrower claim`
2. `Better theory / better worst-case validation`
3. `Better baselines`
4. `More experiments`

Do **not** spend the next round mainly adding more `f_c`/`n_eff` plots. That will not rescue the paper if the worst-case definition and the contribution framing are still loose.

</details>

### Actions Taken

- Replaced the old corner-only worst-case reporting with a continuous-box best-found adversary:
  - corner candidate generation;
  - multistart `L-BFGS-B` refinement under `|delta_n| <= epsilon`;
  - warm-starting from the previous best solution to avoid non-monotone artifacts.
- Added a validation experiment that explicitly compares:
  - corner-restricted adversary;
  - split-mode constructive adversary;
  - continuous-box best-found search.
- Replaced the old same-sign test pattern with a weighted-centered split-mode construction.
- Added a new theory note that reframes the mechanism in terms of weighted phase variance and covariance.
- Added multi-scenario validation for:
  - iid bounded uniform errors;
  - common-bias errors;
  - correlated Gaussian errors with matched marginal variance.
- Restricted the displayed lower bound to the guaranteed small-error region.

### Results

- The split-mode construction tracks the box-best-found adversary almost exactly before the first null.
- The old same-sign pattern is now explicitly shown to behave like a common-bias shift and stays close to 1.
- The continuous-box best-found curve removes the non-monotone tail that appeared in the corner-only implementation.

### Status

- Continuing to Round 2.

## Round 2

### Assessment (Summary)

- Score: 5/10
- Verdict: not ready
- Key criticisms:
  - The technical story is now coherent.
  - The highest-value missing piece is still a comparative design baseline section.
  - The continuous-box search is better, but still best-found rather than globally certified.
  - The stochastic predictor should be framed as a unified paper contribution, not an appendix-style add-on.

### Reviewer Raw Response

<details>
<summary>Click to expand full reviewer response</summary>

**Score**  
`5/10` for strong-venue readiness.

**Verdict**  
`NOT READY`

This is materially better than the previous version. The core story is now coherent: the old fake-upper-bound issue is gone, the worst-case search is no longer obviously wrong, and the stochastic extension adds real value. But it is still not at strong-venue level.

**Ranked Remaining Weaknesses**
1. There is still no comparative design story.
Minimum fix: add one compact baseline section with at least two alternative placement families under the same spacing/aperture constraints, and compare nominal gain, box-best-found worst-case curve, and stochastic mean degradation. Without this, you can characterize one placement, but you cannot make a design claim.

2. The continuous worst-case is still `best-found`, not certified global.
Minimum fix: keep the wording disciplined everywhere: `box-best-found` or `best-found adversary`, not exact worst case. Add a stronger validation table at a few representative `ε/λ` values with many random restarts / alternative solvers / seed sensitivity, especially around the first-null region.

3. Generality is still thin.
Minimum fix: add one `N` sweep and one geometry or spacing sweep (`d` or `Δ_p`). Right now the results are convincing for one setup, not yet for the problem class.

4. The split-mode adversary is strong empirically, but still mostly an empirical phenomenon.
Minimum fix: present it explicitly as an empirical near-adversarial pattern in the pre-null regime, not a theorem. A short first-order derivation or local argument for why weighted-centered sensitivity should matter would help.

5. The stochastic quadratic theory is useful, but still reads like an add-on rather than a paper-driving contribution.
Minimum fix: reframe it as a unified phase-variance predictor and report aggregate approximation error across scenarios, not just a few point comparisons.

6. The manuscript artifact is still behind the analysis.
Minimum fix: rewrite the paper around the new story. If the written report still says corner-only worst case and the old same-sign upper bound, reviewers will judge the old version, not the improved code/results.

**READY / ALMOST / NOT READY**  
`NOT READY`

**Most Important Next Step**  
Add the baseline section. That is the highest-value next move now.

If you do only one serious thing next, do this: compare the current phase-aligned nominal placement against `uniform symmetric` and one `alternative nominal/robust placement`, then evaluate all three with the new box-best-found search plus the stochastic scenarios. That is the missing piece that converts this from “nice robustness note for one design” into a paper with an actual design takeaway.

</details>

### Actions Taken

- Preserved the stronger worst-case search and split-mode theory.
- Added the phase-variance derivation note to make the split-mode mechanism explicit instead of purely empirical.
- Consolidated the new result artifacts so the manuscript can be rewritten around the revised story.

### Results

- Score improved from 3/10 to 5/10 under the same reviewer.
- The reviewer now treats the core robustness story as materially better, but still not submission-ready.
- The dominant remaining blocker is a missing baseline section, not a missing curve in the current setup.

### Status

- Loop terminated for this session with a clear next step:
  - add baseline placement families;
  - compare nominal gain, box-best-found robustness, and stochastic mean degradation;
  - then re-run the review loop.

## Method Description

The current method starts from a constructive phase-aligned PASS placement obtained by wavelength-grid snapping and spacing repair. Robustness is then evaluated under bounded position errors by combining a deterministic lower bound, a continuous-box best-found adversarial search, and a constructive split-mode perturbation derived from the weighted-centered phase sensitivity profile.

The revised theory interprets gain degradation through a weighted phase-variance object. This yields a unified second-order predictor for multiple error models through the covariance of the perturbation field, which is validated for iid uniform, common-bias, and correlated Gaussian scenarios. The present implementation therefore supports a coherent one-design robustness story, but not yet a full design-comparison story.
