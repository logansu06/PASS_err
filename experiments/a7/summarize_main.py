"""R010/R013: summary of the main grid (C1 go/no-go gate, Gamma distribution, GCS yield/efficiency).

Usage: python summarize_main.py [--csv results/main_grid.csv] [--out results/main_summary]
Writes <out>.json and <out>.md. The go/no-go gate is the one pre-declared in EXPERIMENT_PLAN.md v2:
Gamma > 5% in at least 20% of endpoint cases with eps > 0 and P != D.
"""
import argparse, json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent


def stats(d):
    g = d['Gamma'].to_numpy()
    sel = d['selection_gap'].dropna()  # undefined (None) when the screening cap was hit
    return dict(n=int(len(d)), pos=float(np.mean(g > 0)), above5=float(np.mean(g > 0.05)), inconclusive=float(np.mean(g <= 0)),
                median=float(np.median(g)), q25=float(np.quantile(g, 0.25)), q75=float(np.quantile(g, 0.75)),
                unique=float(d['unique'].mean()), global_gap_median=float(d['global_gap'].median()),
                global_gap_max=float(d['global_gap'].max()), n_exact=int(len(sel)),
                selection_gap_pos=float(np.mean(sel > 1e-12)) if len(sel) else float('nan'),
                selection_gap_median=float(sel.median()) if len(sel) else float('nan'),
                selection_gap_max=float(sel.max()) if len(sel) else float('nan'),
                sacrifice_median=float(d['nominal_sacrifice'].median()), survivors_median=float(d['survivors'].median()),
                survivor_frac_median=float((d['survivors'] / d['family_size']).median()), n_eval_max=int(d['n_eval'].max()),
                capped=int(d['capped'].sum()), gcs_seconds_median=float(d['gcs_seconds'].median()),
                gcs_seconds_max=float(d['gcs_seconds'].max()))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--csv', default='results/main_grid.csv')
    p.add_argument('--out', default='results/main_summary')
    args = p.parse_args()
    df = pd.read_csv(HERE / args.csv)
    df['PisD'] = (df.xP == 0) & (df.yP == 0)
    main_ = df[(df.eps_over_lambda > 0) & ~df.PisD]
    res = dict(n_cases=int(len(df)))
    gate = main_[main_.control == 'endpoints']
    frac = float(np.mean(gate.Gamma > 0.05))
    res['gate'] = dict(definition='Gamma > 5% in >= 20% of endpoint cases with eps > 0 and P != D', n=int(len(gate)),
                       fraction=frac, passed=bool(frac >= 0.20))
    res['overall'] = {c: stats(main_[main_.control == c]) for c in ('free', 'endpoints')}
    res['by_eps'] = {c: {str(e): stats(d) for e, d in main_[main_.control == c].groupby('eps_over_lambda')} for c in ('free', 'endpoints')}
    res['by_snr'] = {c: {str(s): stats(d) for s, d in main_[main_.control == c].groupby('snr_db')} for c in ('free', 'endpoints')}
    res['by_eps_snr'] = {c: {'%g/%g' % k: stats(d) for k, d in main_[main_.control == c].groupby(['eps_over_lambda', 'snr_db'])}
                         for c in ('free', 'endpoints')}
    ctrl = df[df.PisD & (df.eps_over_lambda > 0)]
    res['control_P_eq_D'] = {c: stats(ctrl[ctrl.control == c]) for c in ('free', 'endpoints')}
    zero = df[df.eps_over_lambda == 0]
    res['eps0'] = dict(n=int(len(zero)), max_abs_Gamma=float(zero.Gamma.abs().max()), unique=float(zero.unique.mean()),
                       max_global_gap=float(zero.global_gap.max()))
    out = HERE / args.out
    Path(str(out) + '.json').write_text(json.dumps(res, indent=2))
    lines = ['# Main grid summary (%d cases)' % len(df), '',
             '**Go/no-go (pre-declared):** %s -> fraction %.3f over %d cases: **%s**' % (
                 res['gate']['definition'], frac, len(gate), 'PASS' if res['gate']['passed'] else 'FAIL'), '',
             '| control | eps/lam | SNR | n | Gamma>0 | Gamma>5% | median Gamma [IQR] | unique | median U*/L-1 | swap gap>0 | median sacrifice | capped |',
             '|---|---|---|---|---|---|---|---|---|---|---|---|']
    for c in ('free', 'endpoints'):
        for k, s in res['by_eps_snr'][c].items():
            e, snr = k.split('/')
            lines.append('| %s | %s | %s | %d | %.2f | %.2f | %.3f [%.3f, %.3f] | %.2f | %.2e | %.2f | %.3f | %d |' % (
                c, e, snr, s['n'], s['pos'], s['above5'], s['median'], s['q25'], s['q75'], s['unique'],
                s['global_gap_median'], s['selection_gap_pos'], s['sacrifice_median'], s['capped']))
    for c in ('free', 'endpoints'):
        s = res['overall'][c]
        lines.append('| **%s all** | >0 | all | %d | %.2f | %.2f | %.3f [%.3f, %.3f] | %.2f | %.2e | %.2f | %.3f | %d |' % (
            c, s['n'], s['pos'], s['above5'], s['median'], s['q25'], s['q75'], s['unique'], s['global_gap_median'],
            s['selection_gap_pos'], s['sacrifice_median'], s['capped']))
    lines += ['', 'P = D control (eps > 0): ' + '; '.join('%s: Gamma>0 %.2f, median %.3f' % (c, s['pos'], s['median'])
                                                    for c, s in res['control_P_eq_D'].items()),
              'eps = 0: max |Gamma| = %.1e, unique %.2f, max U*/L-1 = %.1e' % (
                  res['eps0']['max_abs_Gamma'], res['eps0']['unique'], res['eps0']['max_global_gap'])]
    Path(str(out) + '.md').write_text('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
