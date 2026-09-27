# Experiment Results (A7 v2: certified robust PASS site selection, GCS)

**Date:** 2026-09-27
**Plan:** `refine-logs/EXPERIMENT_PLAN.md` (v2); per-run status is in `refine-logs/EXPERIMENT_TRACKER.md`.
**Code:** `experiments/a7/`. `a7_core.py` is the GCS port of the GPT-6 Pro bundle, which the plan calls `a7_gcs.py`. The drivers are `run_main.py`, `run_baselines.py`, `run_scaling.py`, `run_m2m3.sh`, `r017_*.py`; checks are in `a7_checks.py`, summaries in `summarize_*.py`.
**Results:** `experiments/a7/results/`:
- `main_grid.csv` and `main_summary.{json,md}`;
- `baselines.csv`, `limits.csv`, `nonideal.csv`, `nonideal_1dB.csv`, `scaling.csv`;
- `m2m3_summary.{json,md}`;
- `m0_checks.json`;
- `r017_mc_average.*` and `r017_joint_box.*`.

**Environment:**
- Local CPU (8 cores); Python 3.13.4, NumPy 2.3.0, SciPy 1.15.3; mpmath 1.4.1 for the extended-precision audit.
- The venv at `experiments/a7/.venv` uses the system site-packages plus mpmath, pandas and matplotlib.
- No GPU was needed. Total wall time was about 25 min on 6–7 workers (≈ 2.5 CPU-hours), within the plan's 4 CPU-hour budget.

**Code review:**
- GPT-6 Astra (ultra) ran 2 rounds, with no CRITICAL finding.
- Two MAJOR reporting defects were fixed and verified:
  - ε = 0 used different arithmetic paths, which could show ±1e-16 "gains";
  - the selection gap was reported even when the screening cap was hit.
- Three MINOR items were also fixed.
- Traces: `.aris/traces/experiment-bridge/2026-09-27_run01/`.

All numbers are float64 evaluations of exact-arithmetic statements. Margins on the featured instances were audited at 50 digits (R007). Nothing is claimed as "machine-verified".

## M0 — Sanity and numerical audit: PASSED (8/8)

| Run | Check | Result |
|---|---|---|
| R001 | Port vs bundle (featured P = (3,2), ε = 0.05λ, 30 dB) | All 18 fields match `a7_global_results.json` to ≤ 1e-12 relative |
| R002 | Bound validity | 120 instances (20 listed ideal cases + 4 non-ideal cases, × 5 ε) × 4 layouts; 1e5 uniform draws + 256 corners each. **0 violations** of SLNR ≥ L, G_D ≥ (Σc)²/N, I_P ≤ Ī, L ≤ U_H (worst 3.7e-16 relative) |
| R003 | Endpoint-bank identity (Theorem 2) | 1,600 layouts, ideal and non-ideal: bank max = 256-corner max to 1.0e-15; at most 48 = 2M templates |
| R004 | ε = 0 exactness; angular K | 272 cases: L = U_H = U = nominal **exactly**, Γ = U\*/L − 1 = 0, Ŝ = S_N in 272/272. K ∈ {720, 1440, 5760}: max L ratio 1.0000187 ≤ sec²(π/720) = 1.0000190 |
| R005 | Clearance and guards | Threshold 0.091110λ. Family 735,471 → 660,858 at 0.0912λ. The β_D guard raises above 0.1704λ. A misaligned family raises |
| R006 | Reproducibility | Two CLI runs (36 cases, multiprocessing) are identical on every non-timing field |
| R007 | Featured margin audit (independent scalar code, mpmath 50 digits) | **Free:** L(Ŝ) = 56.559334; rival margin 0.320874 (6th rival 0.813); Γ = +34.17%. **Endpoints:** L(Ŝ) = 55.574007; margin 0.046616; Γ = +2.79%. float64 vs 50 digits: ≤ 2.7e-12 relative |
| R008 | Cross-check against GPT-6 Pro's independent 132-case grid | All 264 rows reproduced: identical layouts, 1.5e-15 relative. Matched family **108/132 positive, 79/132 > 5%**. Bundle unit checks identical |

## M1 — Main result C1: certified dominance over exhaustive nominal selection (R009/R010)

**Grid:** 1,360 cases = 2 controls × 4 SNR × 5 ε × 34 geometries (33 + P = D). Wall time 458 s on 7 workers.

**Pre-declared go/no-go:** Γ = L(Ŝ)/U(S_N) − 1 > 5% in ≥ 20% of endpoint cases with ε > 0 and P ≠ D.
**Result: 56.2% of 528 → PASS.**

| Control (ε > 0, P ≠ D) | n | Γ > 0 (certified) | Γ > 5% | Median Γ [IQR] | Inconclusive | Median nominal sacrifice |
|---|---|---|---|---|---|---|
| free | 528 | 87.5% | 61.9% | 11.3% [1.6, 27.6] | 12.5% | 0.2% |
| endpoints (sites 0 and 23 forced) | 528 | 82.8% | 56.3% | 6.9% [0.5, 19.4] | 17.2% | 0.3% |
| free, x_P ≠ 0 | 480 | 96.3% | 68.1% | 14.2% | 3.7% | — |
| endpoints, x_P ≠ 0 | 480 | 91.0% | 61.9% | 8.9% | 9.0% | — |

**By ε** (all SNR; free / endpoints):

| ε/λ | Γ > 0 | Γ > 5% | Median Γ | Unique | Median U\*/L − 1 |
|---|---|---|---|---|---|
| 0.01 | 86% / 77% | 42% / 30% | 2.5% / 1.1% | 76% / 80% | 0.02% / 0.02% |
| 0.03 | 89% / 86% | 64% / 60% | 12.9% / 7.8% | 42% / 51% | 0.30% / 0.43% |
| 0.05 | 89% / 86% | 71% / 70% | 15.9% / 11.6% | 28% / 36% | 1.6% / 1.5% |
| 0.08 | 85% / 82% | 72% / 66% | 14.4% / 9.8% | 9% / 15% | 8.8% / 7.7% |

**By SNR** (free / endpoints):
- The effect grows with SNR, i.e. as the regime becomes leakage-limited:
  - 10 dB: Γ > 5% in 25% / 27%; median 1.6% / 1.1%. This is the noise-dominated control, where the effect is small as expected.
  - 40 dB: Γ > 5% in 83% / 75%; median 27.6% / 17.2%.
- The nominal sacrifice also grows with SNR (median at 40 dB: 3.7% / 9.2%).

**Controls:**
- **P = D:** 0% certified positive (median Γ ≈ −12%). This is expected; there is nothing to protect.
- **ε = 0:** Γ = 0 and U\*/L − 1 = 0 exactly. Uniqueness holds in 272/272 cases.

**Mechanism** (at the witnesses, Γ > 0 cases):
- desired power is unchanged (median ratio Ŝ/S_N = 1.000);
- worst-case leakage is 21% lower (median ratio 0.79).

**Trade-off:**
- The nominal sacrifice has median 0.2–0.3%, p90 13.5%, and max 88.5%.
- The maximum is at free, 40 dB, ε = 0.08λ, P = (−3.6, 2):
  - S_N has a deep nominal null, with nominal SLNR 9,997, but its worst case is ≤ 2.09;
  - Ŝ has nominal SLNR 1,147 and a certified worst case ≥ 3.02, so Γ = +44%.

**Honest negative region:**
- Of the 157 inconclusive P ≠ D cases, **96 are at x_P = 0** (P directly behind D), and every x_P = 0 case is inconclusive. There the D-aligned sites are nearly phase-aligned toward P as well (co-aligned receivers).
- In that region the decoupled Theorem 1 bracket is loose: median U(Ŝ)/L(Ŝ) = 1.09, and up to 1.73 at ε = 0.08λ.
- The other 61 inconclusive cases (43 endpoints, 18 free) are marginal:
  - median Γ = −0.19%, minimum −11%;
  - in 46% of them Ŝ = S_N, so Γ ≤ 0 is just the width of that layout's own bracket;
  - they cluster at the smallest and largest ε (24 at 0.01λ, 20 at 0.08λ).
- Every screening-cap hit (48 free cases) is also at x_P = 0.
- R017 (below) shows the looseness is the bound's, not the method's: joint-box refinement closes about half of the log-gap there.

## C2 — Global certification yield and screening efficiency (R013, R014)

**From the main grid** (ε > 0, P ≠ D; free / endpoints):
- **Uniqueness certificate:** L(Ŝ) > max_{S≠Ŝ} U_H holds in 38.6% / 45.3% of cases. It falls with ε, from about 76–80% at 0.01λ to 9–15% at 0.08λ.
- **Global bracket:** median U\*/L(Ŝ) − 1 = 0.51% / 0.49%, so the certified performance ratio is ≥ 99.5% of the family-wide robust optimum in the median case. The maximum is 74.5% / 73.9%, at x_P = 0.
- **Screening:** median survivors are 70 / 15 of 735,471 / 74,613 layouts (≤ 0.02%). Median GCS time is 0.20 s / 0.12 s; the maximum is 7.3 s.
- **Swap search vs the exact certificate optimum:**
  - Over 1,008 exact cases, the plain swap incumbent is **strictly below the exact max L in 68%**, with median 0.6%, p90 7.6% and max 25.9%.
  - So global screening changes the selected layout, not just the certificate.
- **Cap hits:** 48 cases, all free with x_P = 0. There the bracket is loose, so no layout can be screened out; these are reported as bracket-only.

**M-scaling (R014).** Six geometries declared before running: (−6,1), (−3,2), (0,1), (3,2), (6,1), (0,4). ε ∈ {0.03, 0.05}λ, 30 dB.

| M | Control | Family | Median survivors (fraction) | Unique | Capped | Median / max total time | Median GCS time |
|---|---|---|---|---|---|---|---|
| 16 | endpoints | 3,003 | 4 (1.3e-3) | 50% | 0 | 0.1 / 0.1 s | 0.02 s |
| 16 | free | 12,870 | 10 (7.8e-4) | 42% | 0 | 0.1 / 0.2 s | 0.03 s |
| 24 | endpoints | 74,613 | 20 (2.7e-4) | 33% | 0 | 0.3 / 1.3 s | 0.06 s |
| 24 | free | 735,471 | 276 (3.8e-4) | 33% | 4 | 1.8 / 4.5 s | 0.11 s |
| 32 | endpoints | 593,775 | 42 (7.2e-5) | 33% | 4 | 3.2 / 6.0 s | 0.10 s |
| 32 | free | 10,518,300 | 608 (5.8e-5) | 25% | 4 | 35.3 / 36.9 s | 0.36 s |

- The survivor fraction shrinks as M grows.
- At M = 32, time is dominated by the O(|F|·H) bank pass. The GCS scan itself stays under 3 s.
- Every cap hit is again at x_P = 0 (4 = 2 geometries × 2 ε).

## M2 — Baselines (R011/R012)

The slice is SNR {20, 30} dB × ε {0.03, 0.05}λ × 33 geometries × 2 controls, with P = D excluded. All systems are scored with the same L and U.

| Control | Subset | vs B-NOM: Γ > 0 / > 5% / median | vs B-CR: same layout / L(Ŝ) > L(S_CR) / certified Γ_CR > 0 / witness < U_H(S_CR) | vs B-GR: Γ > 0 / median | Time: GCS / CR |
|---|---|---|---|---|---|
| free | all | 89% / 78% / 17.6% | 8% / 92% / 69% / 33% | 91% / 60% | 0.20 / 0.03 s |
| free | x_P ≠ 0 | 98% / 86% / 20.2% | 8% / 92% / 76% / 37% | 100% / 68% | |
| endpoints | all | 86% / 73% / 13.1% | 22% / 78% / 51% / 36% | 91% / 146% | 0.11 / 0.03 s |
| endpoints | x_P ≠ 0 | 94% / 80% / 14.7% | 24% / 76% / 56% / 39% | 100% / 159% | |

- **B-CR is the same-budget corner-robust swap that maximizes U_H.**
  - It lands on Ŝ in only 8–22% of cases.
  - Ŝ has a strictly higher certificate in 78–92% of cases and certifiably beats it (L(Ŝ) > U(S_CR)) in 51–69%.
  - In 33–36% of cases a refined witness drives S_CR's worst case below its own template value U_H. So the heuristic's apparent robustness is refuted there.
  - B-CR is about 4–7× faster (0.03 s vs 0.11–0.20 s), but it is uncertified.
- **B-GR is the graduation-report-style desired-only (P-blind) layout.** Ŝ certifiably beats it in every x_P ≠ 0 case, with median gain 68% (free) and 159% (endpoints).

## M3 — Protection limits C3 (R015) and non-ideal control (R016)

**Protection limits** (30 dB; both controls). The leakage bracket F_end ≤ min_S max_δ I_P ≤ Ī(Ŝ) is **tight to within 1%** (Ī/F_end ≤ 1.01) for every geometry and every ε ∈ {0.01, …, 0.09}λ. The converse and achievability therefore essentially coincide, and Ŝ is nearly leakage-optimal as well.

| P | Control | F_end at ε = 0.01 / 0.05 / 0.09 λ | SLNR bracket [L, U\*] at 0.05λ | Γ at 0.05λ |
|---|---|---|---|---|
| (3,2) | free | 5.08e-4 / 1.19e-2 / 3.57e-2 | [56.56, 56.58] | +34.2% |
| (3,2) | endpoints | 5.08e-4 / 1.21e-2 / 3.59e-2 | [55.57, 55.60] | +2.8% |
| (6,1) | free | 1.06e-4 / 2.39e-3 / 7.50e-3 | [219.0, 220.5] | +22.1% |
| (6,1) | endpoints | 1.18e-4 / 2.56e-3 / 7.84e-3 | [208.5, 208.6] | +40.7% |
| (0,1) | both | 0.80 at every ε | [0.90, 1.10] | −17% (inconclusive) |

- **Reading as an interference-temperature test.** With transmit power p:
  - no layout in the family can meet a ceiling I_max < p·F_end under tolerance ε;
  - Ŝ meets any I_max ≥ p·Ī(Ŝ).
- **The worst-case leakage floor grows roughly quadratically with ε** (about ×70 from 0.01 to 0.09λ at (3,2) and (6,1)).
- **At (0,1)** every layout leaks about 0.80 (normalized) at every ε. P behind D is fundamentally unprotectable within this family.

**Non-ideal control** (B2 slice, P = D excluded). Field directivity is cos²θ; the per-site feed power is fixed (each site carries 1/N of the feed, attenuated along the waveguide; no depletion coupling); phase is unchanged.

| Control | Model | Γ > 0 | Γ > 5% | Median Γ | Unique | Median U\*/L − 1 |
|---|---|---|---|---|---|---|
| free | ideal | 89% | 78% | 17.6% | 38% | 0.66% |
| free | 0.08 dB/m + cos² | 89% | 60% | 7.7% | 33% | 0.42% |
| free | 1 dB/m + cos² (R017) | 82% | 58% | 9.4% | 42% | 0.32% |
| endpoints | ideal | 86% | 73% | 13.1% | 46% | 1.00% |
| endpoints | 0.08 dB/m + cos² | 83% | 55% | 6.5% | 41% | 0.61% |
| endpoints | 1 dB/m + cos² (R017) | 85% | 61% | 8.0% | 42% | 0.52% |

The certified-positive rate persists under the tested separable attenuation and directivity. The typical gain roughly halves. Excluding x_P = 0, the 0.08 dB/m model is positive in 94% of cases.

## R017 — Nice-to-have extras

**Monte Carlo average SLNR** (practitioner view; 1e4 uniform draws per case; B2 slice):

| Metric | free | endpoints |
|---|---|---|
| Median mean-SLNR ratio Ŝ/S_N | 0.997 | 0.996 |
| Ŝ better on the 5th percentile | 77% | 55% |
| Ŝ better on the sampled minimum | 85% | 79% |

Worst-case robustness costs about 0.4% of average SLNR, while it improves the lower tail.

**Joint-box refinement (D.6)** on the 5 widest-gap cases. These are all endpoints at 40 dB with x_P = 0. The fixed budget is 300k sub-boxes / 180 s per case. Every refined bound was validated against 1e5 draws plus corners.

| P | ε/λ | L: Theorem 1 → refined | Gap U/L − 1: before → after | Log-gap closed | Γ before → after |
|---|---|---|---|---|---|
| (0,1) | 0.08 | 0.633 → 0.839 | 0.730 → 0.305 | 51% | −0.415 → −0.224 |
| (0,2) | 0.08 | 0.822 → 1.090 | 0.676 → 0.264 | 55% | −0.380 → −0.178 |
| (0,4) | 0.08 | 1.581 → 2.092 | 0.578 → 0.192 | 61% | −0.312 → −0.089 |
| (0,1) | 0.05 | 0.903 → 1.000 | 0.220 → 0.102 | 51% | −0.174 → −0.086 |
| (0,2) | 0.05 | 1.174 → 1.300 | 0.199 → 0.082 | 56% | −0.147 → −0.056 |

- The co-aligned looseness is a decoupling artifact of the bound, and a dependency-aware refinement recovers about half of it.
- Within this budget, none of these cases turns certifiably positive. They stay inconclusive.
- The refinement is a targeted repair, as GPT-6 Pro anticipated. It is not part of the main algorithm.

## Results → claims (pre-declared matrix)

| Outcome observed | Allowed claim (from the plan) |
|---|---|
| L(Ŝ) > U(S_N) in 83–88% of cases (both controls; 91–96% for x_P ≠ 0); gate passed | **C1:** certified worst-case SLNR improvement over exhaustive nominal selection within the matched robust-clearance family, including identical endpoints. Report free and endpoints separately (median 11.3% vs 6.9%) |
| L(Ŝ) > max_{S≠Ŝ} U_H in 39–45% of cases | A unique global robust-optimal layout within the stated family, model and float64 margins, **in those cases** |
| Otherwise, the median bracket is 0.5% | A global bracket, with performance ratio ≥ L/U\* |
| Cap hit in 48 free cases (x_P = 0) | Bracket-only there; no exact argmax claimed |
| Inconclusive: 96 cases at x_P = 0, 61 marginal elsewhere | "Certificate inconclusive", not "robust is worse". x_P = 0 is explained by co-alignment and partly repaired by D.6 |
| Ī/F_end ≤ 1.01 | **C3:** quantified protection limits; converse ≈ achievability within 1% on the tested geometries |
| B-CR ≠ Ŝ in 78–92% of cases; certified dominance 51–69% | The certified global selection matters for selection, not only for verification |
| Non-ideal control holds (Γ > 0 in 82–89%) | Persists under the tested separable attenuation and directivity. Not a hardware validation |
| Nominal sacrifice up to 88% at high SNR | An explicit nominal–robust trade-off. Never "no-cost robustness" |

## Summary

- **Must-run experiments:** 16/16 done (R001–R016). The M4 items R018–R020 (figures, number reconciliation, claim gate) belong to the next stage.
- **Nice-to-have:** R017 all 3 done (1 dB/m; Monte Carlo average; joint-box refinement).
- **Main result: positive.** The C1 gate passes with a wide margin (56.2% vs 20%). C2 and C3 are supported. The negative region (x_P = 0, co-aligned P) is identified, explained and partly repaired; the remaining inconclusive cases are marginal.
- **Ready for Workflow 2: YES.**

## Next steps

1. `/result-to-claim` (GPT-6 Astra, ultra). This is R020; it replaces `CLAIMS_FROM_RESULTS.md`.
2. R018 figures (Fig. 2–4 from the CSVs; `/paper-figure`) and R019 number reconciliation.
3. Optional: `/ablation-planner` (skill Phase 5.6). Candidate ablations: asymmetric vs symmetric sectors; sec vs additive pad; screening vs swap-only (already covered by the selection gap).
4. A limited `/auto-review-loop`. Then rewrite `NARRATIVE_REPORT.md` for A7 v2, then `/paper-writing — venue: IEEE_CONF, human checkpoint: true`.

## Reproduce

```bash
cd experiments/a7
OPENBLAS_NUM_THREADS=1 .venv/bin/python r001_port_check.py           # R001
OPENBLAS_NUM_THREADS=1 .venv/bin/python a7_checks.py --workers 6     # R002–R008 (exit 1 on any failure)
OPENBLAS_NUM_THREADS=1 .venv/bin/python run_main.py --workers 7      # R009: results/main_grid.csv
.venv/bin/python summarize_main.py                                   # R010/R013
./run_m2m3.sh                                                        # R011/R012, R015, R016, R014
.venv/bin/python run_main.py --alpha-db 1.0 --q 2 --snr 20,30 --eps 0.03,0.05 --out results/nonideal_1dB.csv   # R017
.venv/bin/python r017_mc_average.py && .venv/bin/python r017_joint_box.py                                      # R017
.venv/bin/python summarize_m2m3.py
```
