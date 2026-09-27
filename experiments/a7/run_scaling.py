"""R014 (B3): screening yield and cost of GCS vs the number of candidate sites M (N = 8).

Geometries declared in refine-logs/EXPERIMENT_TRACKER.md before running: (-6,1), (-3,2), (0,1), (3,2), (6,1), (0,4).
eps/lambda in {0.03, 0.05}, 30 dB, both controls (endpoints = sites 0 and M-1 forced). M = 32 is about 10.5 M
subsets, so the family, nominal search and bank bounds are all evaluated in batches.
"""
import argparse, csv, json, os, platform, time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

import a7_core as a

GEOMS6 = [(-6., 1.), (-3., 2.), (0., 1.), (3., 2.), (6., 1.), (0., 4.)]


def parse():
    p = argparse.ArgumentParser()
    p.add_argument('--Ms', default='16,24,32')
    p.add_argument('--N', type=int, default=8)
    p.add_argument('--eps', default='0.03,0.05')
    p.add_argument('--snr', type=float, default=30.0)
    p.add_argument('--controls', default='free,endpoints')
    p.add_argument('--cap', type=int, default=200000)
    p.add_argument('--seed', type=int, default=2026)
    p.add_argument('--workers', type=int, default=3)
    p.add_argument('--out', default='results/scaling.csv')
    return p.parse_args()


def run_job(job):
    args, M, control, P, ee = job
    N = args.N
    t = {}
    t0 = time.perf_counter()
    xs = a.aligned_sites(M)
    mid = (M - N) // 2
    s2 = abs(a.z(xs[mid:mid + N], 0, 0).sum()) ** 2 / N / 10 ** (args.snr / 10)
    eps = ee * a.LAM
    forced = (0, M - 1) if control == 'endpoints' else ()
    T = a.tables(xs, eps, P)
    SS = a.family(xs, N, eps, forced)
    t['family'] = time.perf_counter() - t0
    t1 = time.perf_counter()
    signs, ZD, ZP = a.endpoint_bank(xs, eps, P)
    UU, EE = a.exact_bounds(SS, T, ZD, ZP, N, s2)
    t['bank'] = time.perf_counter() - t1
    t1 = time.perf_counter()
    SN = a.nominal_argmax(SS, T, N, s2)
    t['nominal'] = time.perf_counter() - t1
    g = a.gcs(T, SS, UU, N, s2, SN, forced=forced, seed=args.seed, cap=args.cap)
    UN = a.witnesses(xs, SN, eps, P, N, s2, refine=4)[0]
    return dict(M=M, control=control, xP=P[0], yP=P[1], eps_over_lambda=ee, snr_db=args.snr,
                min_gap_over_lambda=float(np.diff(xs).min() / a.LAM), family_size=len(SS), templates=signs.shape[1],
                survivors=g['survivors'], survivor_frac=g['survivors'] / len(SS), n_eval=g['n_eval'], capped=int(g['capped']),
                exact=int(g['exact']),
                unique=int(g['unique']), margin=g['margin'], L_hat=g['L_hat'], U_star=g['U_star'],
                global_gap=g['U_star'] / g['L_hat'] - 1, incumbent_improvement=g['L_hat'] / g['swap_L'] - 1,
                selection_gap=g['L_hat'] / g['swap_L'] - 1 if g['exact'] else None, U_nom=UN,
                Gamma=g['L_hat'] / UN - 1, S_hat=' '.join(map(str, g['S_hat'])), S_nom=' '.join(map(str, SN)),
                t_family=t['family'], t_bank=t['bank'], t_nominal=t['nominal'], t_gcs=g['seconds'],
                t_total=time.perf_counter() - t0)


def main():
    args = parse()
    jobs = [(args, int(M), c, P, float(e)) for M in args.Ms.split(',') for c in args.controls.split(',')
            for P in GEOMS6 for e in args.eps.split(',')]
    jobs.sort(key=lambda j: -j[1])  # largest M first
    out = Path(__file__).parent / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.perf_counter()
    rows = []
    with Pool(args.workers) as pool:
        for r in pool.imap_unordered(run_job, jobs):
            rows.append(r)
            print('M=%d %s P=(%g,%g) eps=%.2f: family %d, survivors %d, unique %d, %.1fs' % (
                r['M'], r['control'], r['xP'], r['yP'], r['eps_over_lambda'], r['family_size'], r['survivors'],
                r['unique'], r['t_total']), flush=True)
    rows.sort(key=lambda r: (r['M'], r['control'], r['eps_over_lambda'], r['yP'], r['xP']))
    with open(out, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    meta = dict(args=vars(args), n=len(rows), seconds=time.perf_counter() - t0, numpy=np.__version__,
                python=platform.python_version(), date=time.strftime('%Y-%m-%d %H:%M:%S'))
    Path(str(out).replace('.csv', '_meta.json')).write_text(json.dumps(meta, indent=2))
    print('saved', out, len(rows), 'rows', '%.0fs' % meta['seconds'])


if __name__ == '__main__':
    os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
    main()
