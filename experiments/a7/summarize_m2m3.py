"""Summaries for M2-M3: R011/R012 baselines, R014 M-scaling, R015 protection limits, R016 non-ideal control.

Writes results/m2m3_summary.json and results/m2m3_summary.md from the CSVs produced by run_m2m3.sh.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
RES = HERE / 'results'


def frac(x):
    return float(np.mean(x)) if len(x) else float('nan')


def baselines(lines, out):
    d = pd.read_csv(RES / 'baselines.csv')
    d = d[~((d.xP == 0) & (d.yP == 0))]
    out['baselines'] = {}
    lines += ['## B2 baselines (R011/R012): SNR {20,30} dB x eps {0.03,0.05} lam x 33 geometries (P = D excluded)', '',
              '| control | subset | n | vs NOM: Gamma>0 / >5% / median | vs CR: same layout / L_hat>L_CR / Gamma>0 / witness below U_H(S_CR) | vs GR: Gamma>0 / median | t_gcs / t_cr median (s) |',
              '|---|---|---|---|---|---|---|']
    for c in ('free', 'endpoints'):
        for sub, x in (('all', d[d.control == c]), ('x_P != 0', d[(d.control == c) & (d.xP != 0)])):
            r = dict(n=int(len(x)), nom_pos=frac(x.Gamma_NOM > 0), nom_5=frac(x.Gamma_NOM > 0.05), nom_med=float(x.Gamma_NOM.median()),
                     cr_same=frac(x.same_CR == 1), cr_L_strict=frac(x.L_hat > x.L_CR * (1 + 1e-12)), cr_pos=frac(x.Gamma_CR > 0),
                     cr_refuted=frac(x.U_CR < x.UH_CR * (1 - 1e-9)), cr_L_gain_med=float((x.L_hat / x.L_CR - 1).median()),
                     cr_L_gain_max=float((x.L_hat / x.L_CR - 1).max()), gr_pos=frac(x.Gamma_GR > 0), gr_med=float(x.Gamma_GR.median()),
                     t_gcs=float(x.t_gcs.median()), t_cr=float(x.t_cr.median()))
            out['baselines']['%s|%s' % (c, sub)] = r
            lines.append('| %s | %s | %d | %.2f / %.2f / %.3f | %.2f / %.2f / %.2f / %.2f | %.2f / %.2f | %.3f / %.3f |' % (
                c, sub, r['n'], r['nom_pos'], r['nom_5'], r['nom_med'], r['cr_same'], r['cr_L_strict'], r['cr_pos'],
                r['cr_refuted'], r['gr_pos'], r['gr_med'], r['t_gcs'], r['t_cr']))
    lines.append('')


def limits(lines, out):
    d = pd.read_csv(RES / 'limits.csv')
    out['limits'] = d[['control', 'xP', 'yP', 'eps_over_lambda', 'F_end', 'Ibar_hat', 'L_hat', 'U_star', 'Gamma', 'unique',
                       'nominal_sacrifice']].to_dict('records')
    lines += ['## B4 protection limits (R015): 30 dB', '',
              '| control | P | eps/lam | F_end | Ibar(S_hat) | Ibar/F_end | L(S_hat) | U* | Gamma | unique | sacrifice |',
              '|---|---|---|---|---|---|---|---|---|---|---|']
    for _, r in d.sort_values(['control', 'yP', 'xP', 'eps_over_lambda']).iterrows():
        lines.append('| %s | (%g,%g) | %.2f | %.3e | %.3e | %.2f | %.2f | %.2f | %.3f | %d | %.3f |' % (
            r.control, r.xP, r.yP, r.eps_over_lambda, r.F_end, r.Ibar_hat, r.Ibar_hat / r.F_end, r.L_hat, r.U_star, r.Gamma,
            r['unique'], r.nominal_sacrifice))
    lines.append('')


def nonideal(lines, out):
    d = pd.read_csv(RES / 'nonideal.csv')
    d1 = pd.read_csv(RES / 'nonideal_1dB.csv') if (RES / 'nonideal_1dB.csv').exists() else None
    ideal = pd.read_csv(RES / 'main_grid.csv')
    ideal = ideal[ideal.snr_db.isin([20, 30]) & ideal.eps_over_lambda.isin([0.03, 0.05])]
    out['nonideal'] = {}
    lines += ['## B5 non-ideal control (R016; 1 dB/m row = R017): cos^2 field directivity, same slice as B2 (P = D excluded)', '',
              '| control | model | n | Gamma>0 | Gamma>5% | median Gamma | unique | median U*/L-1 | capped |', '|---|---|---|---|---|---|---|---|---|']
    models = [('0.08 dB/m', d)] + ([('1 dB/m', d1)] if d1 is not None else []) + [('ideal', ideal)]
    for c in ('free', 'endpoints'):
        for tag, x in models:
            x = x[(x.control == c) & ~((x.xP == 0) & (x.yP == 0))]
            r = dict(n=int(len(x)), pos=frac(x.Gamma > 0), above5=frac(x.Gamma > 0.05), median=float(x.Gamma.median()),
                     unique=frac(x.unique == 1), gap=float(x.global_gap.median()), capped=int(x.capped.sum()))
            out['nonideal']['%s|%s' % (c, tag)] = r
            lines.append('| %s | %s | %d | %.2f | %.2f | %.3f | %.2f | %.2e | %d |' % (
                c, tag, r['n'], r['pos'], r['above5'], r['median'], r['unique'], r['gap'], r['capped']))
    lines.append('')


def scaling(lines, out):
    d = pd.read_csv(RES / 'scaling.csv')
    out['scaling'] = {}
    lines += ['## B3 M-scaling (R014): 6 declared geometries x eps {0.03,0.05} lam x 30 dB', '',
              '| M | control | family | median survivors (frac) | unique | capped | median Gamma | median / max total s | median / max GCS s |',
              '|---|---|---|---|---|---|---|---|---|']
    for (M, c), x in d.groupby(['M', 'control']):
        r = dict(n=int(len(x)), family=int(x.family_size.max()), survivors=float(x.survivors.median()),
                 survivor_frac=float(x.survivor_frac.median()), unique=frac(x.unique == 1), capped=int(x.capped.sum()),
                 gamma=float(x.Gamma.median()), t_med=float(x.t_total.median()), t_max=float(x.t_total.max()),
                 g_med=float(x.t_gcs.median()), g_max=float(x.t_gcs.max()))
        out['scaling']['%d|%s' % (M, c)] = r
        lines.append('| %d | %s | %d | %.0f (%.1e) | %.2f | %d | %.3f | %.1f / %.1f | %.2f / %.2f |' % (
            M, c, r['family'], r['survivors'], r['survivor_frac'], r['unique'], r['capped'], r['gamma'], r['t_med'], r['t_max'],
            r['g_med'], r['g_max']))
    lines.append('')


def extras(lines, out):
    if (RES / 'r017_mc_average.json').exists():
        mc = json.loads((RES / 'r017_mc_average.json').read_text())
        out['mc_average'] = mc
        lines += ['## R017 practitioner view: Monte Carlo SLNR of S_hat vs S_nom (1e4 uniform draws, B2 slice, P != D)', '',
                  '| control | subset | n | median mean-SLNR ratio | mean better | median p05 ratio | p05 better | sampled min better |',
                  '|---|---|---|---|---|---|---|---|']
        for k, r in mc.items():
            c, sub = k.split('|')
            lines.append('| %s | %s | %d | %.4f | %.2f | %.4f | %.2f | %.2f |' % (
                c, sub, r['n'], r['mean_ratio_median'], r['mean_better'], r['p05_ratio_median'], r['p05_better'], r['min_better']))
        lines.append('')
    if (RES / 'r017_joint_box.json').exists():
        jb = json.loads((RES / 'r017_joint_box.json').read_text())
        out['joint_box'] = [{k: v for k, v in r.items() if k != 'trace'} for r in jb]
        lines += ['## R017 joint-box refinement (D.6) on the 5 widest-gap cases (budget 300k boxes / 180 s each)', '',
                  '| control | P | eps/lam | SNR | L: Thm 1 -> refined | U(S_hat) | gap U/L-1: before -> after | log-gap closed | Gamma before -> after | valid | boxes / s |',
                  '|---|---|---|---|---|---|---|---|---|---|---|']
        for r in jb:
            lines.append('| %s | (%g,%g) | %.2f | %g | %.4f -> %.4f | %.4f | %.3f -> %.3f | %.0f%% | %.3f -> %.3f | %s | %d / %.0f |' % (
                r['control'], r['xP'], r['yP'], r['eps_over_lambda'], r['snr_db'], r['L_theorem1'], r['L_refined'], r['U_refined'],
                r['gap_before'], r['gap_after'], 100 * r['gap_closed'], r['Gamma_before'], r['Gamma_after'], r['valid'], r['n_eval'],
                r['seconds']))
        lines.append('')


def main():
    lines, out = ['# M2-M3 summary', ''], {}
    for f, name in ((baselines, 'baselines.csv'), (limits, 'limits.csv'), (nonideal, 'nonideal.csv'), (scaling, 'scaling.csv')):
        if (RES / name).exists():
            f(lines, out)
        else:
            lines += ['(%s missing)' % name, '']
    extras(lines, out)
    (RES / 'm2m3_summary.json').write_text(json.dumps(out, indent=2))
    (RES / 'm2m3_summary.md').write_text('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
