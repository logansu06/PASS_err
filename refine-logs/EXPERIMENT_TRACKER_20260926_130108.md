# Experiment Tracker

Plan: `refine-logs/EXPERIMENT_PLAN.md`. Status legend: TODO / RUNNING / DONE / BLOCKED. **No runs started** (per user instruction, 2026-09-26).

| Run ID | Milestone | Purpose | System / Variant | Split | Metrics | Priority | Status | Notes |
|---|---|---|---|---|---|---|---|---|
| R001 | M0 | sanity: bound validity | L/U vs 1e5 random feasible δ | 20 fixed grid cases | violations (must be 0) | MUST | TODO | `a7_checks.py` (to write) |
| R002 | M0 | sanity: ε = 0 | $S_R$ vs $S_N$, L = U = exact | all ε = 0 rows | equality; gain = 0 | MUST | TODO | ε = 0 special case in `a7_main.py` |
| R003 | M0 | sanity: angular grid | K = 720 / 1440 / 5760 | 20 cases | ΔL < 0.5% | MUST | TODO | |
| R004 | M0 | sanity: reproducibility and clearance | rerun driver | 20 cases | identical CSV; clearance assert | MUST | TODO | |
| R005 | M1 | main: certified dominance | $S_R$ vs exhaustive $S_N$ | full grid, 1,320 cases, common + endpoints | frac $L_R > U_N$; frac > 5%; median; desired/leak | MUST | TODO | `a7_main.py` → `a7_main_results.csv`; **go/no-go gate** |
| R006 | M1 | main table and figure | summary script | R005 CSV | Table I, Fig. 2 | MUST | TODO | |
| R007 | M2 | baseline B-GR | graduation-report-style desired-only centered block (N0 physics) | 30 dB, ε ∈ {.03, .05}, 33 geoms, 2 controls | L, U, dominance | MUST | TODO | `a7_baselines.py` |
| R008 | M2 | baseline B-SAMP | sampled-error robust heuristic (64 corners) | same slice | L, U, dominance, runtime | MUST | TODO | selection-vs-verification framing |
| R009 | M2 | search adequacy | swaps (1 / 8 / 32 restarts) vs exhaustive certificate optimum | 12/4, 33 geoms × ε ∈ {.03, .05} | optimality gap | MUST | TODO | `a7_ablate.py` |
| R010 | M2 | deletion: leakage certificate | desired-only N1 objective | B2 slice | certified-SLNR loss | MUST | TODO | |
| R011 | M2 | deletion: Taylor bound | first-order leakage bound, no remainder | B2 slice | violations; selection diff | NICE | TODO | |
| R012 | M3 | mechanism (paired) | $S_R$ vs $S_N$: $\|h_0\|$, directional response, desired gain | R005 CSV | fraction of favorable moves; examples | MUST | TODO | `a7_analyze.py` |
| R013 | M3 | noise regime | pointwise fixed-pair condition | R005 CSV | benefit map over (ε, SNR) | MUST | TODO | |
| R014 | M3 | fragility and tightness | $\kappa_b$ scatter; U/L quantiles by class | R005 CSV | median / p95 / max | MUST | TODO | |
| R015 | M3 | non-ideal channel | 0.08 dB/m + cos² directivity | B2 slice | as R005 | MUST | TODO | channel switch in `a7_main.py` |
| R016 | M3 | scale and average view | M ∈ {16, 32}; MC average SLNR | B2 slice | as R005 | NICE | TODO | |
| R017 | M4 | figures and number reconciliation | — | all CSVs | figures; numbers table | MUST | TODO | |
| R018 | M4 | claim gate | `/result-to-claim` (GPT-6 Astra, ultra) | all | verdict | MUST | TODO | replaces `CLAIMS_FROM_RESULTS.md` |
