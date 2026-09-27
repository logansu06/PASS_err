# Experiment Tracker (v2, 2026-09-27)

Plan: `refine-logs/EXPERIMENT_PLAN.md` (v2). v1 tracker: `EXPERIMENT_TRACKER_20260926_130108.md`. **No runs started.**

| Run ID | Milestone | Purpose | System / Variant | Split | Metrics | Priority | Status | Notes |
|---|---|---|---|---|---|---|---|---|
| R001 | M0 | implement GCS driver | `a7_gcs.py`: clearance family, asymmetric sectors + sec, β guard, ε = 0 exact, shared endpoint bank, safe screening + cap, same-error witnesses, logging | — | bit-for-bit match with bundle `a7_global.py` on the featured case | MUST | TODO | port from `idea-stage/handoff/gpt6pro_bundle/.../a7_audit.py`, `a7_global.py` (attributed) |
| R002 | M0 | bound validity | L vs 1e5 random feasible δ + corners | 20 listed cases × 5 ε | violations (must be 0) | MUST | TODO | `a7_checks.py` |
| R003 | M0 | endpoint-bank identity | bank max vs 256-corner max | 40 random subsets | max abs diff | MUST | TODO | bundle `a7_unit_checks.py` |
| R004 | M0 | ε = 0 and angular K | exact at ε = 0; K ∈ {720, 1440, 5760} | featured + 10 cases | equality; ΔL within sec² bound | MUST | TODO | |
| R005 | M0 | clearance and β guard | artificial ε > 0.0911λ; β > π/2 | — | family shrinks; raise | MUST | TODO | |
| R006 | M0 | reproducibility | rerun driver | 20 cases | identical outputs | MUST | TODO | |
| R007 | M0 | featured margin audit | independent recompute (+ extended precision) of $L(\hat S)$, top-5 rival $U_H$, $U(S_N)$ | P = (3,2), ε = 0.05λ, 30 dB, both controls | margins | MUST | TODO | |
| R008 | M0 | cross-check | rerun GPT-6 Pro `a7_grid.py` parts 0–2 | its 132-case grid | reproduce 108/132, 79/132 | MUST | TODO | |
| R009 | M1 | **main: certified dominance (C1)** | GCS $\hat S$ vs exhaustive $S_N$ | 1,360 cases (free + endpoints) | Γ > 0, Γ > 5%, median / IQR, inconclusive, nominal sacrifice, desired/leak; GCS internals | MUST | TODO | **go/no-go:** Γ > 5% in ≥ 20% of endpoint cases (ε > 0, P ≠ D) |
| R010 | M1 | main figure and table | summary script | R009 | Fig. 2, Table II | MUST | TODO | |
| R011 | M2 | baseline B-CR | same-budget corner-robust swap (max $U_H$) | 272-case slice | L, U, dominance, runtime | MUST | TODO | |
| R012 | M2 | baseline B-GR | graduation-report-style desired-only centered block | 272-case slice | L, U, dominance | MUST | TODO | |
| R013 | M2 | yield and selection gap (C2) | GCS internals from R009 | 1,360 cases | uniqueness rate, $U^\star/L - 1$, survivors, runtime, swap-vs-exact gap, cap hits | MUST | TODO | analysis only |
| R014 | M2 | M-scaling | M ∈ {16, 24, 32}, N = 8 | 6 geometries × 2 ε × 30 dB | survivors, runtime, uniqueness | MUST | TODO | drop M = 32 if over budget |
| R015 | M3 | protection limits (C3) | $F_{\rm end}$ vs $\bar I(\hat S)$; SLNR bracket; interference-temperature thresholds | 3 geometries × ε 0.01–0.09 × 30 dB × 2 controls | brackets vs ε | MUST | TODO | Fig. 3 |
| R016 | M3 | non-ideal control | 0.08 dB/m + cos² field directivity, fixed per-site feed power | 272-case slice | as R009 / R013 | MUST | TODO | |
| R017 | M3 | extras | 1 dB/m; MC average SLNR; joint-box refinement on 5 widest gaps | subsets | — | NICE | TODO | only after M3 |
| R018 | M4 | figures | Fig. 1–4 | all | — | MUST | TODO | `/paper-figure` |
| R019 | M4 | number reconciliation | numbers table vs CSVs | all | — | MUST | TODO | |
| R020 | M4 | claim gate | `/result-to-claim` (GPT-6 Astra, ultra) | all | verdict | MUST | TODO | replaces `CLAIMS_FROM_RESULTS.md` |
