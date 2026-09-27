# Research Output Manifest

> Auto-maintained by ARIS skills. Tracks all generated artifacts across the research lifecycle.

| Timestamp | Skill | File | Stage | Description |
|-----------|-------|------|-------|-------------|
| 2026-09-27 14:32 | /experiment-bridge | refine-logs/EXPERIMENT_RESULTS_20260927_143216.md | implementation | A7 v2 results R001–R017 (M0–M3 + R017 extras) |
| 2026-09-27 14:32 | /experiment-bridge | refine-logs/EXPERIMENT_RESULTS.md | implementation | latest copy |
| 2026-09-27 14:35 | /experiment-bridge | refine-logs/EXPERIMENT_TRACKER.md | implementation | R001–R017 DONE with notes; R018–R020 (M4) TODO |
| 2026-09-27 13:42 | /experiment-bridge | experiments/a7/a7_core.py | implementation | GCS core (port of GPT-6 Pro bundle + non-ideal amplitude, batching, ε = 0 exact path) |
| 2026-09-27 13:43 | /experiment-bridge | experiments/a7/r001_port_check.py | implementation | R001 port check vs bundle featured results |
| 2026-09-27 13:50 | /experiment-bridge | experiments/a7/a7_checks.py | implementation | M0 checks R002–R008 (exit 1 on failure) |
| 2026-09-27 13:43 | /experiment-bridge | experiments/a7/run_main.py | implementation | M1 main-grid driver (also B4/B5 via flags) |
| 2026-09-27 13:58 | /experiment-bridge | experiments/a7/run_baselines.py | implementation | B2 baselines (B-NOM, B-CR, B-GR) |
| 2026-09-27 13:56 | /experiment-bridge | experiments/a7/run_scaling.py | implementation | B3 M-scaling (M = 16/24/32) |
| 2026-09-27 14:05 | /experiment-bridge | experiments/a7/run_m2m3.sh | implementation | M2–M3 run chain |
| 2026-09-27 13:57 | /experiment-bridge | experiments/a7/summarize_main.py | implementation | C1 gate + main summary |
| 2026-09-27 14:10 | /experiment-bridge | experiments/a7/summarize_m2m3.py | implementation | M2–M3 + R017 summary |
| 2026-09-27 14:20 | /experiment-bridge | experiments/a7/r017_mc_average.py | implementation | R017 Monte Carlo average SLNR |
| 2026-09-27 14:25 | /experiment-bridge | experiments/a7/r017_joint_box.py | implementation | R017 D.6 joint-box refinement |
| 2026-09-27 13:47 | /experiment-bridge | experiments/a7/results/r001_port_check.json | implementation | R001 PASS |
| 2026-09-27 14:03 | /experiment-bridge | experiments/a7/results/m0_checks.json | implementation | M0 8/8 PASS |
| 2026-09-27 14:03 | /experiment-bridge | experiments/a7/results/crosscheck_bundle/ | implementation | R008 rerun of GPT-6 Pro grid + unit checks |
| 2026-09-27 14:12 | /experiment-bridge | experiments/a7/results/main_grid.csv | implementation | 1,360-case main grid (+ _meta.json, .log) |
| 2026-09-27 14:13 | /experiment-bridge | experiments/a7/results/main_summary.json | implementation | C1 gate PASS (56.2%), tables by ε/SNR |
| 2026-09-27 14:13 | /experiment-bridge | experiments/a7/results/main_summary.md | implementation | human-readable main summary |
| 2026-09-27 14:17 | /experiment-bridge | experiments/a7/results/baselines.csv | implementation | B2 272-case slice |
| 2026-09-27 14:18 | /experiment-bridge | experiments/a7/results/limits.csv | implementation | B4 protection limits |
| 2026-09-27 14:20 | /experiment-bridge | experiments/a7/results/nonideal.csv | implementation | B5 0.08 dB/m + cos² |
| 2026-09-27 14:23 | /experiment-bridge | experiments/a7/results/scaling.csv | implementation | B3 M-scaling |
| 2026-09-27 14:27 | /experiment-bridge | experiments/a7/results/nonideal_1dB.csv | implementation | R017 1 dB/m |
| 2026-09-27 14:21 | /experiment-bridge | experiments/a7/results/r017_mc_average.json | implementation | R017 MC average (+ .csv) |
| 2026-09-27 14:30 | /experiment-bridge | experiments/a7/results/r017_joint_box.json | implementation | R017 joint-box (+ .log) |
| 2026-09-27 14:31 | /experiment-bridge | experiments/a7/results/m2m3_summary.md | implementation | M2–M3 + R017 summary (+ .json) |
| 2026-09-27 14:02 | /experiment-bridge | .aris/traces/experiment-bridge/2026-09-27_run01/ | implementation | GPT-6 Astra code-review traces (2 rounds) |
| 2026-09-27 14:45 | /experiment-bridge | HANDOFF.md | implementation | Handoff: status, results, next steps, environment, conventions |
