#!/bin/bash
# M2-M3 runs (EXPERIMENT_PLAN.md v2): R011/R012 baselines, R015 protection limits, R016 non-ideal control, R014 M-scaling.
set -e
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
PY=${PY:-.venv/bin/python}
$PY run_baselines.py --workers 7 --out results/baselines.csv
$PY run_main.py --geoms "3,2;6,1;0,1" --eps 0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09 --snr 30 --refine-hat 8 --workers 7 --out results/limits.csv
$PY run_main.py --alpha-db 0.08 --q 2 --snr 20,30 --eps 0.03,0.05 --workers 7 --out results/nonideal.csv
$PY run_scaling.py --workers 3 --out results/scaling.csv
echo M2M3_DONE
