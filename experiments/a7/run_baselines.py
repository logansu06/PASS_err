"""R011/R012 (B2): GCS vs baselines on the 272-case slice, all scored with the same certificate L and witness U.

Slice (EXPERIMENT_PLAN.md v2): SNR in {20, 30} dB x eps/lambda in {0.03, 0.05} x 34 geometries x 2 controls.
Systems:
  NOM  exhaustive nominal-SLNR optimum S_N (the B1 comparator);
  CR   same-budget corner-robust swap heuristic: maximizes U_H(S) (min exact SLNR over the shared endpoint templates),
       same starts (S_N + 8 random, seed 2026) and swap neighbourhood as the GCS incumbent step; uncertified;
  GR   graduation-report style: the desired-only (P-blind) layout maximizing |sum z_D| in the same family
       (the centered aligned block for `free`; sites 0, M-1 plus the most central sites for `endpoints`).
Gamma_X = L(S_hat) / U(S_X) - 1 > 0 means S_hat certifiably beats system X in worst-case SLNR.
"""
import argparse, csv, json, os, platform, time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

import a7_core as a
from run_main import GEOMS


def parse():
    p = argparse.ArgumentParser()
    p.add_argument('--M', type=int, default=24)
    p.add_argument('--N', type=int, default=8)
    p.add_argument('--controls', default='free,endpoints')
    p.add_argument('--snr', default='20,30')
    p.add_argument('--eps', default='0.03,0.05')
    p.add_argument('--alpha-db', type=float, default=0.0)
    p.add_argument('--q', type=float, default=0.0)
    p.add_argument('--seed', type=int, default=2026)
    p.add_argument('--restarts', type=int, default=8)
    p.add_argument('--refine', type=int, default=4)
    p.add_argument('--cap', type=int, default=200000)
    p.add_argument('--workers', type=int, default=6)
    p.add_argument('--out', default='results/baselines.csv')
    return p.parse_args()


def run_group(job):
    args, control, P, ee = job
    ch = a.Channel(args.alpha_db, args.q)
    M, N = args.M, args.N
    xs = a.aligned_sites(M)
    mid = (M - N) // 2
    A_ref = abs(a.z(xs[mid:mid + N], 0, 0, ch).sum()) ** 2 / N
    eps = ee * a.LAM
    forced = (0, M - 1) if control == 'endpoints' else ()
    T = a.tables(xs, eps, P, ch=ch)
    SS = a.family(xs, N, eps, forced)
    _, ZD, ZP = a.endpoint_bank(xs, eps, P, ch)
    SG = SS[np.argmax(np.abs(T['zD'][SS].sum(1)))]
    rows = []
    for snr in [float(v) for v in args.snr.split(',')]:
        s2 = A_ref / 10 ** (snr / 10)
        UU, _ = a.exact_bounds(SS, T, ZD, ZP, N, s2)
        SN = a.nominal_argmax(SS, T, N, s2)
        g = a.gcs(T, SS, UU, N, s2, SN, forced=forced, seed=args.seed, restarts=args.restarts, cap=args.cap)
        t0 = time.perf_counter()
        UH = lambda Q: a.bank_bounds(np.atleast_2d(Q), ZD, ZP, N, s2)[0]
        SC, _ = a.search(T, N, s2, SS, SN, seed=args.seed, restarts=args.restarts, forced=forced, objective=UH)
        t_cr = time.perf_counter() - t0
        row = dict(control=control, snr_db=snr, eps_over_lambda=ee, xP=P[0], yP=P[1], alpha_db_m=args.alpha_db, q=args.q,
                   L_hat=g['L_hat'], U_hat=a.witnesses(xs, g['S_hat'], eps, P, N, s2, refine=args.refine, ch=ch)[0],
                   unique=int(g['unique']), exact=int(g['exact']), t_gcs=g['seconds'], t_cr=t_cr, S_hat=' '.join(map(str, g['S_hat'])))
        for tag, S in (('NOM', SN), ('CR', SC), ('GR', SG)):
            U = a.witnesses(xs, S, eps, P, N, s2, refine=args.refine, ch=ch)[0]
            row.update({'S_' + tag: ' '.join(map(str, S)), 'L_' + tag: float(a.cert(S, T, N, s2)[0]), 'U_' + tag: U,
                        'UH_' + tag: float(UH(S)[0]), 'Gamma_' + tag: g['L_hat'] / U - 1,
                        'same_' + tag: int(np.array_equal(S, g['S_hat']))})
        rows.append(row)
    return rows


def main():
    args = parse()
    jobs = [(args, c, P, float(e)) for c in args.controls.split(',') for P in GEOMS for e in args.eps.split(',')]
    out = Path(__file__).parent / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.perf_counter()
    rows = []
    with Pool(args.workers) as pool:
        for k, rr in enumerate(pool.imap_unordered(run_group, jobs), 1):
            rows.extend(rr)
            if k % 20 == 0 or k == len(jobs):
                print('%d/%d groups, %d cases, %.0fs' % (k, len(jobs), len(rows), time.perf_counter() - t0), flush=True)
    rows.sort(key=lambda r: (r['control'], r['snr_db'], r['eps_over_lambda'], r['yP'], r['xP']))
    with open(out, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    meta = dict(args=vars(args), n_cases=len(rows), seconds=time.perf_counter() - t0, numpy=np.__version__,
                python=platform.python_version(), date=time.strftime('%Y-%m-%d %H:%M:%S'))
    Path(str(out).replace('.csv', '_meta.json')).write_text(json.dumps(meta, indent=2))
    print('saved', out, len(rows), 'cases', '%.0fs' % meta['seconds'])


if __name__ == '__main__':
    os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
    main()
