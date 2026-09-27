# AGENTS.md

Instructions for Codex and similar coding agents working in this repository.

## Scope

This file applies to the entire repository.

## Repository Purpose

This repository is a Python simulation and analysis project for PASS placement robustness under position errors. The main workflow:

1. builds the constructive phase-aligned nominal placement;
2. evaluates bounded-error robustness with Monte Carlo, lower bounds, and box-best-found adversaries;
3. validates stochastic error models and placement baselines;
4. writes figures and tables into `results/`.

The codebase is closer to a research artifact than an app. Be careful with terminology, reproducibility, and claim discipline.

## Environment And Main Command

- Use Python 3.10+.
- Expected dependencies are `numpy`, `scipy`, and `matplotlib`.
- Run the full experiment suite from the repository root with:

```powershell
python src/main.py
```

- Generated artifacts are written to `results/`.
- The default random seed is fixed in [config.py](src/config.py).

## Key Files

- [main.py](src/main.py): orchestration entry point.
- [config.py](src/config.py): experiment parameters and sweep settings.
- [design_delta_star.py](src/design_delta_star.py): constructive nominal placement design.
- [pass_model.py](src/pass_model.py): core gain and phase model.
- [robustness.py](src/robustness.py): Monte Carlo, corner search, coordinate descent, local search, lower bounds.
- [placement_baselines.py](src/placement_baselines.py): comparative placement families.
- [theory_extensions.py](src/theory_extensions.py): quadratic / covariance / phase-variance analysis helpers.
- [plotters.py](src/plotters.py): figure generation.
- [CLAIMS_FROM_RESULTS.md](CLAIMS_FROM_RESULTS.md): current evidence-backed wording.
- [AUTO_REVIEW.md](fyp_report/review-stage/AUTO_REVIEW.md): reviewer feedback and known weaknesses.
- [README.md](README.md): project overview and output descriptions.

## Editing Rules

- Preserve reproducibility unless the task explicitly requires changing it.
- Do not change `random_seed` casually.
- Keep code and docs in UTF-8. If a terminal displays mojibake, treat the file as an encoding/display issue before rewriting content.
- Prefer focused, minimal patches. This is a research codebase; avoid stylistic churn.
- Keep naming mathematically consistent with the existing code: `delta_star`, `phi_ref`, `xi`, `epsilon_valid`, `box`, `split`, `common_bias`, `iid`, `corr`.
- Preserve the current result file naming scheme inside `results/` unless the user asks for a format change.

## Validation Expectations

- If you change computation, configuration, plotting, or result-generation logic, rerun:

```powershell
python src/main.py
```

- If the full run is too expensive for the current task, make the best reasonable validation effort and state clearly what you did not rerun.
- If you change only documentation or prose files, no experiment rerun is required.
- When results-affecting code changes, update any stale statements in:
  - `README.md`
  - `CLAIMS_FROM_RESULTS.md`
  - `fyp_report/review-stage/AUTO_REVIEW.md`
  - files under `results/` that are meant to reflect current outputs

## Claim Discipline

Follow `CLAIMS_FROM_RESULTS.md` unless the user explicitly asks to investigate beyond it.

- Do not describe the continuous box search as an exact or globally certified worst case.
- Preferred wording is `box-best-found`, `best-found adversary`, or `continuous-box best found`.
- Do not describe the constructive placement as globally optimal or near-optimal unless new evidence is added.
- Do not claim the split-mode pattern is the exact optimizer; it is currently an empirical near-adversarial pattern in the pre-null regime.
- Do not generalize beyond the studied setting without new experiments.
- Keep the guaranteed small-error region separate from empirical observations outside that region.

If a task changes the scientific story, update the wording so it matches the evidence, not the aspiration.

## Results And Paper-Facing Artifacts

The repository contains paper-facing summaries. When touching research conclusions:

- cross-check `results/config.json` and generated CSVs before asserting numeric values;
- keep terminology aligned across plots, README text, and claims files;
- prefer conservative wording over strong publication-style claims unless the evidence is explicit in the generated artifacts.

## Practical Workflow

When working on code here, a good default sequence is:

1. inspect `src/config.py`, `src/main.py`, and the relevant module;
2. implement the smallest coherent change;
3. rerun `python src/main.py` if outputs may change;
4. inspect `results/` and `run_log.txt`;
5. update claim-facing markdown if the numerical story changed.


<!-- ARIS:BEGIN -->
## ARIS Skill Scope
For ARIS workflows in this project, use only the project-local ARIS skills under `.agents/skills/aris`.
Do not use global skills or non-ARIS project skills unless the user explicitly asks to mix them.
<!-- ARIS:END -->
