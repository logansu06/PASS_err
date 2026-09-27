"""R017 (nice-to-have): practitioner view - Monte Carlo average SLNR of S_hat vs S_nom under uniform box errors.

Uses the layouts stored in results/main_grid.csv on the B2 slice (SNR {20,30} dB, eps {0.03,0.05} lam, P != D).
1e4 i.i.d. uniform error vectors per case (seeded per case); reports mean and 5th percentile SLNR ratios.
"""
import json, zlib
from pathlib import Path

import numpy as np
import pandas as pd

import a7_core as a

HERE = Path(__file__).resolve().parent
M, N, NDRAW = 24, 8, 10000


def main():
    d = pd.read_csv(HERE / 'results/main_grid.csv')
    d = d[d.snr_db.isin([20, 30]) & d.eps_over_lambda.isin([0.03, 0.05]) & ~((d.xP == 0) & (d.yP == 0))]
    xs = a.aligned_sites(M)
    rows = []
    for _, r in d.iterrows():
        P, eps = (r.xP, r.yP), r.eps_over_lambda * a.LAM
        rng = np.random.default_rng(zlib.crc32(repr((r.control, r.snr_db, r.eps_over_lambda, r.xP, r.yP)).encode()))
        D = rng.uniform(-eps, eps, (NDRAW, N))
        out = {}
        for tag in ('S_hat', 'S_nom'):
            S = np.array([int(v) for v in r[tag].split()])
            v = a.exact_at(xs, S, D, P, N, r.sigma2)[0]
            out[tag] = (v.mean(), np.quantile(v, 0.05), v.min())
        rows.append(dict(control=r.control, snr_db=r.snr_db, eps=r.eps_over_lambda, xP=r.xP, yP=r.yP,
                         mean_ratio=out['S_hat'][0] / out['S_nom'][0], p05_ratio=out['S_hat'][1] / out['S_nom'][1],
                         min_ratio=out['S_hat'][2] / out['S_nom'][2]))
    x = pd.DataFrame(rows)
    x.to_csv(HERE / 'results/r017_mc_average.csv', index=False)
    summ = {}
    for c in ('free', 'endpoints'):
        for sub, y in (('all', x[x.control == c]), ('x_P != 0', x[(x.control == c) & (x.xP != 0)])):
            summ['%s|%s' % (c, sub)] = dict(n=len(y), mean_ratio_median=float(y.mean_ratio.median()),
                                             mean_better=float((y.mean_ratio > 1).mean()), p05_ratio_median=float(y.p05_ratio.median()),
                                             p05_better=float((y.p05_ratio > 1).mean()), min_better=float((y.min_ratio > 1).mean()))
    (HERE / 'results/r017_mc_average.json').write_text(json.dumps(summ, indent=2))
    print(json.dumps(summ, indent=2))


if __name__ == '__main__':
    main()
