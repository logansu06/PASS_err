"""R009 (M1) / R016 (M3): certified dominance of GCS over exhaustive nominal selection on the declared grid.

Declared grid (refine-logs/EXPERIMENT_PLAN.md v2): 33 P geometries + P = D; eps/lambda in {0,.01,.03,.05,.08};
reference SNR in {10,20,30,40} dB; controls free / endpoints (sites 0 and M-1 forced). One CSV row per case.
"""
import argparse, csv, json, os, platform, subprocess, time
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import scipy

import a7_core as a

GEOMS = [(float(xp), float(yp)) for yp in (1.0, 2.0, 4.0) for xp in np.linspace(-6, 6, 11)] + [(0.0, 0.0)]


def parse():
    p = argparse.ArgumentParser()
    p.add_argument('--M', type=int, default=24)
    p.add_argument('--N', type=int, default=8)
    p.add_argument('--controls', default='free,endpoints')
    p.add_argument('--snr', default='10,20,30,40')
    p.add_argument('--eps', default='0,0.01,0.03,0.05,0.08')
    p.add_argument('--geoms', default='all', help="'all' or semicolon list like '3,2;6,1'")
    p.add_argument('--alpha-db', type=float, default=0.0, help='in-waveguide loss dB/m (non-ideal control)')
    p.add_argument('--q', type=float, default=0.0, help='cos^q field directivity exponent (non-ideal control)')
    p.add_argument('--K', type=int, default=1440)
    p.add_argument('--cap', type=int, default=200000)
    p.add_argument('--seed', type=int, default=2026)
    p.add_argument('--restarts', type=int, default=8)
    p.add_argument('--refine-nom', type=int, default=4)
    p.add_argument('--refine-hat', type=int, default=8)
    p.add_argument('--workers', type=int, default=4)
    p.add_argument('--out', default='results/main_grid.csv')
    return p.parse_args()


def run_group(job):
    """One (control, P, eps) group across all SNRs."""
    args, control, P, ee = job
    ch = a.Channel(args.alpha_db, args.q)
    M, N = args.M, args.N
    xs = a.aligned_sites(M)
    mid = (M - N) // 2
    A_ref = abs(a.z(xs[mid:mid + N], 0, 0, ch).sum()) ** 2 / N
    eps = ee * a.LAM
    forced = (0, M - 1) if control == 'endpoints' else ()
    t0 = time.perf_counter()
    T = a.tables(xs, eps, P, K=args.K, ch=ch)
    SS = a.family(xs, N, eps, forced)
    _, ZD, ZP = a.endpoint_bank(xs, eps, P, ch)
    setup = time.perf_counter() - t0
    snrs = [float(v) for v in args.snr.split(',')]
    rows = []
    for snr in snrs:
        tc = time.perf_counter()
        s2 = A_ref / 10 ** (snr / 10)
        UU, EE = a.exact_bounds(SS, T, ZD, ZP, N, s2)
        SN = a.nominal_argmax(SS, T, N, s2)
        g = a.gcs(T, SS, UU, N, s2, SN, forced=forced, seed=args.seed, restarts=args.restarts, cap=args.cap)
        Sh = g['S_hat']
        UN, dN, GDN, IPN = a.witnesses(xs, SN, eps, P, N, s2, refine=args.refine_nom, ch=ch)
        UR, dR, GDR, IPR = a.witnesses(xs, Sh, eps, P, N, s2, refine=args.refine_hat, ch=ch)
        LN = float(a.cert(SN, T, N, s2)[0])
        nomN = float(a.nominal(SN, T, N, s2)[0])
        nomR = float(a.nominal(Sh, T, N, s2)[0])
        rows.append(dict(
            control=control, snr_db=snr, sigma2=s2, eps_over_lambda=ee, xP=P[0], yP=P[1], alpha_db_m=args.alpha_db, q=args.q,
            family_size=len(SS), S_nom=' '.join(map(str, SN)), S_hat=' '.join(map(str, Sh)),
            L_hat=g['L_hat'], U_hat=UR, L_nom=LN, U_nom=UN, Gamma=g['L_hat'] / UN - 1,
            swap_L=g['swap_L'], swap_Gamma=g['swap_L'] / UN - 1, incumbent_improvement=g['L_hat'] / g['swap_L'] - 1,
            selection_gap=g['L_hat'] / g['swap_L'] - 1 if g['exact'] else None,  # vs exact max L; unknown if capped
            U_star=g['U_star'], rival_U=g['rival_U'], margin=g['margin'], unique=int(g['unique']),
            global_gap=g['U_star'] / g['L_hat'] - 1, bracket_hat=UR / g['L_hat'],
            survivors=g['survivors'], n_eval=g['n_eval'], capped=int(g['capped']), exact=int(g['exact']),
            nom_slnr_nom=nomN, nom_slnr_hat=nomR, nominal_sacrifice=1 - nomR / nomN,
            GD_nom_wit=GDN, IP_nom_wit=IPN, GD_hat_wit=GDR, IP_hat_wit=IPR,
            F_end=float(EE.min()), Ibar_hat=a.leakage_upper(Sh, T, N),
            gcs_seconds=g['seconds'], setup_seconds=setup, case_seconds=time.perf_counter() - tc,
            case_seconds_amortized=time.perf_counter() - tc + setup / len(snrs)))
    return rows, time.perf_counter() - t0


def main():
    args = parse()
    geoms = GEOMS if args.geoms == 'all' else [tuple(float(v) for v in g.split(',')) for g in args.geoms.split(';')]
    jobs = [(args, c, P, float(e)) for c in args.controls.split(',') for P in geoms for e in args.eps.split(',')]
    out = Path(__file__).parent / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.perf_counter()
    rows = []
    with Pool(args.workers) as pool:
        for k, (rr, dt) in enumerate(pool.imap_unordered(run_group, jobs), 1):
            rows.extend(rr)
            if k % 20 == 0 or k == len(jobs):
                print(f'{k}/{len(jobs)} groups done, {len(rows)} cases, {time.perf_counter() - t0:.0f}s', flush=True)
    rows.sort(key=lambda r: (r['control'], r['snr_db'], r['eps_over_lambda'], r['yP'], r['xP']))
    with open(out, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    try:
        commit = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, cwd=Path(__file__).parent).stdout.strip()
    except Exception:
        commit = None
    meta = dict(args=vars(args), n_cases=len(rows), seconds=time.perf_counter() - t0, numpy=np.__version__, scipy=scipy.__version__,
                python=platform.python_version(), git_commit=commit, date=time.strftime('%Y-%m-%d %H:%M:%S'))
    Path(str(out).replace('.csv', '_meta.json')).write_text(json.dumps(meta, indent=2))
    print('saved', out, len(rows), 'cases', f'{meta["seconds"]:.0f}s')


if __name__ == '__main__':
    os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
    main()
