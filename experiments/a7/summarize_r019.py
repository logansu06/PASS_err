"""R019 (M4): persist every derived statistic that refine-logs/EXPERIMENT_RESULTS.md quotes, from the stored CSVs only.

The /result-to-claim pre-check (R020, 2026-09-28) found 25 quoted numbers that no result file contained. This script
recomputes them with their original definitions, adds the corrections the R020 juries required, and re-verifies the
weakest decisive margins of the main grid in extended precision (independent scalar code from a7_checks.R007).

Usage: python summarize_r019.py [--no-audit] [--dps 50]
Writes results/r019_derived.json and results/r019_derived.md. No new simulation except the margin audit, which rebuilds
at most three main-grid cases deterministically and checks that they match the stored CSV rows first.
"""
import argparse, json, time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
RES = HERE / 'results'


def q(s, p):
    return float(np.quantile(np.asarray(s, float), p))


def count(mask):
    mask = np.asarray(mask, bool)
    return dict(k=int(mask.sum()), n=int(mask.size), frac=float(mask.mean()) if mask.size else float('nan'))


def not_pd(d):
    return d[~((d.xP == 0) & (d.yP == 0))]


def main_grid(out):
    df = pd.read_csv(RES / 'main_grid.csv')
    m = not_pd(df[df.eps_over_lambda > 0])  # primary filter: eps > 0, P != D (same as summarize_main.py)
    per = lambda d: {c: d[d.control == c] for c in ('free', 'endpoints')}
    both = lambda d: dict(pooled=d, **per(d))

    # counts behind the headline fractions (paper sentences quote k/n)
    out['counts'] = {c: dict(gamma_pos=count(x.Gamma > 0), gamma_above5=count(x.Gamma > 0.05), unique=count(x['unique'] == 1),
                             inconclusive=count(x.Gamma <= 0), capped=count(x.capped == 1),
                             median_L_over_Ustar=float((1 / (1 + x.global_gap)).median()))
                     for c, x in per(m).items()}
    out['counts']['by_eps_above5'] = {c: {str(e): count(g.Gamma > 0.05) for e, g in x.groupby('eps_over_lambda')}
                                      for c, x in per(m).items()}
    out['counts']['capped_full_grid'] = dict(total=int(df.capped.sum()), P_eq_D=int(df[(df.xP == 0) & (df.yP == 0)].capped.sum()))
    out['counts']['swap_below_exact'] = {c: count(x.selection_gap.dropna() > 1e-12) for c, x in per(m).items()}

    # x_P != 0 subgroup (exploratory; P not directly behind D)
    out['xP_nonzero'] = {c: dict(n=int(len(x)), gamma_pos=float((x.Gamma > 0).mean()), gamma_above5=float((x.Gamma > 0.05).mean()),
                                 gamma_median=float(x.Gamma.median()))
                         for c, x in per(m[m.xP != 0]).items()}

    # mechanism: exact desired power / leakage at the two SLNR witnesses (Gamma > 0 cases). These are values at the
    # witnesses, not independent worst cases. The certified leakage comparison uses Ibar(S_hat) >= max I_P(S_hat) and
    # IP_nom_wit <= max I_P(S_nom), so Ibar(S_hat) < IP_nom_wit certifies a lower worst-case leakage for S_hat.
    pos = m[m.Gamma > 0]
    mech = {}
    for k, x in both(pos).items():
        LD_hat = x.L_hat * (x.sigma2 + x.Ibar_hat)  # Theorem 1 desired lower bound L_D(S_hat)
        cert_leak = x.Ibar_hat / x.IP_nom_wit
        mech[k] = dict(n=int(len(x)), desired_ratio_at_witness_median=float((x.GD_hat_wit / x.GD_nom_wit).median()),
                       leakage_ratio_at_witness_median=float((x.IP_hat_wit / x.IP_nom_wit).median()),
                       certified_leakage_ratio_median=float(cert_leak.median()),
                       certified_leakage_lower=count(cert_leak < 1),
                       certified_desired_ratio_median=float((LD_hat / x.GD_nom_wit).median()))
    out['mechanism_gamma_pos'] = mech

    # nominal sacrifice 1 - SLNR_nom(S_hat)/SLNR_nom(S_nom)
    out['nominal_sacrifice'] = {k: dict(median=float(x.nominal_sacrifice.median()), p90=q(x.nominal_sacrifice, 0.9),
                                        max=float(x.nominal_sacrifice.max())) for k, x in both(m).items()}
    r = m.loc[m.nominal_sacrifice.idxmax()]
    out['nominal_sacrifice']['max_case'] = dict(control=r.control, snr_db=float(r.snr_db), eps_over_lambda=float(r.eps_over_lambda),
                                                xP=float(r.xP), yP=float(r.yP), nom_slnr_nom=float(r.nom_slnr_nom),
                                                U_nom=float(r.U_nom), nom_slnr_hat=float(r.nom_slnr_hat), L_hat=float(r.L_hat),
                                                Gamma=float(r.Gamma), sacrifice=float(r.nominal_sacrifice))

    # inconclusive (Gamma <= 0) breakdown
    inc = m[m.Gamma <= 0]
    oth = inc[inc.xP != 0]
    z0 = m[m.xP == 0]
    out['inconclusive'] = dict(
        total=int(len(inc)), at_xP0=int((inc.xP == 0).sum()), n_xP0=int(len(z0)), all_xP0_inconclusive=bool((z0.Gamma <= 0).all()),
        other=int(len(oth)), other_by_control={c: int(v) for c, v in oth.control.value_counts().items()},
        other_gamma_median=float(oth.Gamma.median()), other_gamma_min=float(oth.Gamma.min()),
        other_same_layout=float((oth.S_hat == oth.S_nom).mean()),
        other_by_eps={str(e): int(v) for e, v in oth.eps_over_lambda.value_counts().sort_index().items()},
        xP0_bracket_hat_median=float(z0.bracket_hat.median()), xP0_bracket_hat_max=float(z0.bracket_hat.max()),
        xP0_bracket_hat_argmax_eps=float(z0.loc[z0.bracket_hat.idxmax(), 'eps_over_lambda']),
        capped_all_at_xP0=bool((m[m.capped == 1].xP == 0).all()))

    # selection gap of the plain swap incumbent vs the exact certificate optimum, pooled over exact (uncapped) cases
    s = m.selection_gap.dropna()
    out['selection_gap_pooled'] = dict(n_exact=int(len(s)), positive=float((s > 1e-12).mean()), median=float(s.median()),
                                       p90=q(s, 0.9), max=float(s.max()))

    # runtime: selection stage (gcs_seconds) vs inclusive per case (family, bank, nominal, GCS, witnesses; setup amortized)
    out['runtime'] = {c: dict(gcs_median=float(x.gcs_seconds.median()), gcs_max=float(x.gcs_seconds.max()),
                              inclusive_median=float(x.case_seconds_amortized.median()),
                              inclusive_max=float(x.case_seconds_amortized.max())) for c, x in per(m).items()}


def limits(out):
    d = pd.read_csv(RES / 'limits.csv')
    d['ratio'] = d.Ibar_hat / d.F_end
    r = d.loc[d.ratio.idxmax()]
    growth = {}
    for (c, xp, yp), g in d.groupby(['control', 'xP', 'yP']):
        g = g.set_index('eps_over_lambda')
        growth['%s|(%g,%g)' % (c, xp, yp)] = float(g.F_end[0.09] / g.F_end[0.01])
    u01 = d[(d.xP == 0) & (d.yP == 1) & (d.eps_over_lambda == 0.05)]
    out['limits'] = dict(n=int(len(d)), ratio_max=float(r.ratio),
                         ratio_argmax=dict(control=r.control, xP=float(r.xP), yP=float(r.yP), eps_over_lambda=float(r.eps_over_lambda)),
                         n_ratio_above_1_01=int((d.ratio > 1.01).sum()), F_end_growth_001_to_009=growth,
                         P01_eps005={c: dict(L_hat=float(x.L_hat.iloc[0]), U_star=float(x.U_star.iloc[0]), Gamma=float(x.Gamma.iloc[0]))
                                     for c, x in u01.groupby('control')})


def nonideal(out):
    out['nonideal_xP_nonzero'] = {}
    for tag, fn in (('0.08 dB/m', 'nonideal.csv'), ('1 dB/m', 'nonideal_1dB.csv')):
        d = not_pd(pd.read_csv(RES / fn))
        d = d[d.xP != 0]
        out['nonideal_xP_nonzero'][tag] = dict(pooled=float((d.Gamma > 0).mean()),
                                               **{c: float((d[d.control == c].Gamma > 0).mean()) for c in ('free', 'endpoints')})


def mc(out):
    d = not_pd(pd.read_csv(RES / 'r017_mc_average.csv'))
    out['mc_mean_ratio'] = {c: dict(n=int(len(x)), median=float(x.mean_ratio.median()), p05=q(x.mean_ratio, 0.05), min=float(x.mean_ratio.min()),
                                    max_mean_loss=float(1 - x.mean_ratio.min()), median_mean_loss=float(1 - x.mean_ratio.median()))
                            for c, x in d.groupby('control')}


def margin_audit(out, dps):
    """Extended-precision re-evaluation of the weakest decisive margins on the main grid (float-selected rival only)."""
    import a7_core as a
    from a7_checks import Ext, M, N, instance, index_of
    X = Ext(dps)
    df = pd.read_csv(RES / 'main_grid.csv')
    m = not_pd(df[df.eps_over_lambda > 0])
    u = m[m['unique'] == 1]
    picks = {'min_positive_Gamma': m[m.Gamma > 0].Gamma.idxmin(),
             'min_relative_uniqueness_margin': (u.margin / u.L_hat).idxmin(),
             'min_absolute_uniqueness_margin': u.margin.idxmin()}
    res = dict(backend=X.name, scope='featured weakest cases; winner, float-selected strongest rival and S_nom witness only', cases={})
    done = {}
    for tag, idx in picks.items():
        row = m.loc[idx]
        key = (row.control, row.snr_db, row.eps_over_lambda, row.xP, row.yP)
        if key in done:
            res['cases'][tag] = dict(same_as=done[key])
            continue
        done[key] = tag
        t0 = time.perf_counter()
        P = (float(row.xP), float(row.yP))
        I = instance(P, row.control, float(row.snr_db), float(row.eps_over_lambda))
        xs, eps, s2, SS, UU, g, SN = I['xs'], I['eps'], I['s2'], I['SS'], I['UU'], I['g'], I['SN']
        Sh = g['S_hat']
        UN, dN, _, _ = a.witnesses(xs, SN, eps, P, N, s2, refine=4)
        match = dict(S_hat=' '.join(map(str, Sh)) == row.S_hat, S_nom=' '.join(map(str, SN)) == row.S_nom,
                     L_hat_rel=float(abs(g['L_hat'] - row.L_hat) / row.L_hat), U_nom_rel=float(abs(UN - row.U_nom) / row.U_nom))
        k_hat = index_of(SS, Sh)
        UUo = UU.copy()
        UUo[k_hat] = -np.inf
        rival = SS[int(np.argmax(UUo))]
        xe = [X.f(float(v)) for v in xs]
        epse = X.f(float(eps))
        mid = (M - N) // 2
        dr, di = X.zsum(xe[mid:mid + N], (0, 0))
        s2e = (dr * dr + di * di) / N / 10 ** (X.f(float(row.snr_db)) / 10)
        Le = X.lower([xe[n] for n in Sh], epse, P, N, s2e, 1440)
        UNe = X.slnr([xe[n] + X.f(float(v)) for n, v in zip(SN, dN)], P, N, s2e)
        UHe = X.bank_upper(xe, [int(n) for n in rival], epse, P, N, s2e)
        c = dict(control=row.control, snr_db=float(row.snr_db), eps_over_lambda=float(row.eps_over_lambda), xP=P[0], yP=P[1],
                 stored_row_match=match,
                 Gamma=dict(float64=float(row.Gamma), extended=float(Le / UNe - 1)),
                 margin=dict(float64=float(row.margin), extended=float(Le - UHe)) if row['unique'] == 1 else None,
                 L_hat=dict(float64=float(row.L_hat), extended=float(Le), rel=float(abs(Le - row.L_hat) / Le)),
                 seconds=time.perf_counter() - t0)
        c['sign_preserved'] = bool((c['Gamma']['float64'] > 0) == (c['Gamma']['extended'] > 0) and
                                   (c['margin'] is None or (c['margin']['float64'] > 0) == (c['margin']['extended'] > 0)))
        res['cases'][tag] = c
        print(tag, 'Gamma %.6e -> %.6e' % (c['Gamma']['float64'], c['Gamma']['extended']),
              '' if c['margin'] is None else 'margin %.6e -> %.6e' % (c['margin']['float64'], c['margin']['extended']),
              'match', match, '%.1fs' % c['seconds'], flush=True)
    res['all_signs_preserved'] = all(v.get('sign_preserved', True) for v in res['cases'].values())
    out['margin_audit'] = res


def pct(x, d=1):
    return '%.*f%%' % (d, 100 * x)


def markdown(o):
    c, mech, sac, inc = o['counts'], o['mechanism_gamma_pos'], o['nominal_sacrifice'], o['inconclusive']
    L = ['# R019 derived statistics (from stored CSVs)', '',
         'Primary filter: eps > 0, P != D; 528 cases per family. Generated by `summarize_r019.py`.', '',
         '## Counts behind headline fractions', '', '| family | Gamma>0 | Gamma>5% | unique | inconclusive | capped | median L/U* |', '|---|---|---|---|---|---|---|']
    for f in ('free', 'endpoints'):
        x = c[f]
        L.append('| %s | %d/%d = %s | %d/%d = %s | %d/%d = %s | %d/%d | %d | %s |' % (
            f, x['gamma_pos']['k'], x['gamma_pos']['n'], pct(x['gamma_pos']['frac'], 2), x['gamma_above5']['k'], x['gamma_above5']['n'],
            pct(x['gamma_above5']['frac'], 2), x['unique']['k'], x['unique']['n'], pct(x['unique']['frac'], 2), x['inconclusive']['k'],
            x['inconclusive']['n'], x['capped']['k'], pct(x['median_L_over_Ustar'], 2)))
    L += ['', 'Gamma > 5% by eps: ' + '; '.join('%s: ' % f + ', '.join('%s: %d/%d' % (e, v['k'], v['n']) for e, v in c['by_eps_above5'][f].items())
                                                for f in ('free', 'endpoints')),
          'Cap hits on the full 1,360-row grid: %d (of which P = D: %d).' % (c['capped_full_grid']['total'], c['capped_full_grid']['P_eq_D']),
          'Swap incumbent strictly below the exact max L (exact cases): ' + '; '.join(
              '%s %d/%d' % (f, c['swap_below_exact'][f]['k'], c['swap_below_exact'][f]['n']) for f in ('free', 'endpoints')) + '.', '',
          '## x_P != 0 subgroup (exploratory)', '', '| family | n | Gamma>0 | Gamma>5% | median Gamma |', '|---|---|---|---|---|']
    for f, x in o['xP_nonzero'].items():
        L.append('| %s | %d | %s | %s | %s |' % (f, x['n'], pct(x['gamma_pos']), pct(x['gamma_above5']), pct(x['gamma_median'])))
    L += ['', '## Mechanism (Gamma > 0 cases)', '',
          '| subset | n | desired ratio at witnesses | leakage ratio at witnesses | certified leakage ratio Ibar(S_hat)/I_P(S_nom, witness) | certified lower worst-case leakage | certified desired ratio L_D(S_hat)/G_D(S_nom, witness) |',
          '|---|---|---|---|---|---|---|']
    for k, x in mech.items():
        L.append('| %s | %d | %.4f | %.4f | %.4f | %d/%d = %s | %.4f |' % (
            k, x['n'], x['desired_ratio_at_witness_median'], x['leakage_ratio_at_witness_median'], x['certified_leakage_ratio_median'],
            x['certified_leakage_lower']['k'], x['certified_leakage_lower']['n'], pct(x['certified_leakage_lower']['frac']),
            x['certified_desired_ratio_median']))
    L += ['', 'Witness ratios are medians of exact values at the two SLNR-minimizing witnesses, not independent worst cases. '
              'A certified leakage ratio < 1 proves max_delta I_P(S_hat) < max_delta I_P(S_nom).', '',
          '## Nominal sacrifice', '', '| subset | median | p90 | max |', '|---|---|---|---|']
    for k in ('pooled', 'free', 'endpoints'):
        L.append('| %s | %s | %s | %s |' % (k, pct(sac[k]['median'], 2), pct(sac[k]['p90']), pct(sac[k]['max'])))
    mc_ = sac['max_case']
    L += ['', 'Largest sacrifice: %s, %g dB, eps = %gλ, P = (%g, %g): nominal SLNR %.0f -> %.0f; U(S_nom) = %.3f, L(S_hat) = %.3f, Gamma = %s.' % (
              mc_['control'], mc_['snr_db'], mc_['eps_over_lambda'], mc_['xP'], mc_['yP'], mc_['nom_slnr_nom'], mc_['nom_slnr_hat'],
              mc_['U_nom'], mc_['L_hat'], pct(mc_['Gamma'])), '',
          '## Inconclusive cases (Gamma <= 0)', '',
          '- total %d; at x_P = 0: %d of %d x_P = 0 cases (all inconclusive: %s); other %d %s.' % (
              inc['total'], inc['at_xP0'], inc['n_xP0'], inc['all_xP0_inconclusive'], inc['other'], inc['other_by_control']),
          '- other: median Gamma %s, min %s, S_hat = S_nom in %s; by eps %s.' % (
              pct(inc['other_gamma_median'], 2), pct(inc['other_gamma_min']), pct(inc['other_same_layout']), inc['other_by_eps']),
          '- x_P = 0 bracket U(S_hat)/L(S_hat): median %.3f, max %.3f (at eps = %gλ). All cap hits at x_P = 0: %s.' % (
              inc['xP0_bracket_hat_median'], inc['xP0_bracket_hat_max'], inc['xP0_bracket_hat_argmax_eps'], inc['capped_all_at_xP0']), '']
    s = o['selection_gap_pooled']
    L += ['## Selection gap (pooled exact cases)', '',
          '- n = %d; swap incumbent strictly below exact max L in %s; median %s, p90 %s, max %s.' % (
              s['n_exact'], pct(s['positive']), pct(s['median'], 2), pct(s['p90']), pct(s['max'])), '',
          '## Runtime per case (s)', '', '| family | GCS stage median / max | inclusive median / max |', '|---|---|---|']
    for f, x in o['runtime'].items():
        L.append('| %s | %.2f / %.2f | %.2f / %.2f |' % (f, x['gcs_median'], x['gcs_max'], x['inclusive_median'], x['inclusive_max']))
    li = o['limits']
    L += ['', '## Protection limits (54 cases)', '',
          '- max Ibar/F_end = %.6f at %s; rows above 1.01: %d.' % (li['ratio_max'], li['ratio_argmax'], li['n_ratio_above_1_01']),
          '- F_end(0.09λ)/F_end(0.01λ): ' + ', '.join('%s ×%.1f' % (k, v) for k, v in li['F_end_growth_001_to_009'].items()) + '.',
          '- P = (0,1), eps = 0.05λ: ' + '; '.join('%s [L, U*] = [%.4f, %.4f], Gamma %s' % (k, v['L_hat'], v['U_star'], pct(v['Gamma']))
                                                  for k, v in li['P01_eps005'].items()) + '.', '',
          '## Non-ideal control, x_P != 0', '']
    for k, v in o['nonideal_xP_nonzero'].items():
        L.append('- %s: Gamma > 0 pooled %s (free %s, endpoints %s).' % (k, pct(v['pooled']), pct(v['free']), pct(v['endpoints'])))
    L += ['', '## Monte Carlo mean-SLNR ratio S_hat/S_nom (B2 slice)', '', '| family | n | median | p05 | min (max loss) |', '|---|---|---|---|---|']
    for f, v in o['mc_mean_ratio'].items():
        L.append('| %s | %d | %.4f | %.4f | %.4f (%s) |' % (f, v['n'], v['median'], v['p05'], v['min'], pct(v['max_mean_loss'])))
    if 'margin_audit' in o:
        ma = o['margin_audit']
        L += ['', '## Weakest-margin extended-precision audit (%s)' % ma['backend'], '', 'Scope: %s.' % ma['scope'], '',
              '| case | setting | Gamma float64 -> extended | margin float64 -> extended | stored row reproduced | sign preserved |', '|---|---|---|---|---|---|']
        for tag, v in ma['cases'].items():
            if 'same_as' in v:
                L.append('| %s | same case as %s | | | | |' % (tag, v['same_as']))
                continue
            mg = '—' if v['margin'] is None else '%.6e -> %.6e' % (v['margin']['float64'], v['margin']['extended'])
            L.append('| %s | %s, %g dB, %gλ, P = (%g, %g) | %.6e -> %.6e | %s | %s | %s |' % (
                tag, v['control'], v['snr_db'], v['eps_over_lambda'], v['xP'], v['yP'], v['Gamma']['float64'], v['Gamma']['extended'], mg,
                all([v['stored_row_match']['S_hat'], v['stored_row_match']['S_nom'], v['stored_row_match']['L_hat_rel'] < 1e-12,
                     v['stored_row_match']['U_nom_rel'] < 1e-12]), v['sign_preserved']))
        L.append('')
        L.append('All signs preserved: %s.' % ma['all_signs_preserved'])
    return '\n'.join(L) + '\n'


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--no-audit', action='store_true')
    p.add_argument('--dps', type=int, default=50)
    args = p.parse_args()
    import platform, sys
    import scipy
    out = dict(date=time.strftime('%Y-%m-%d %H:%M:%S'),
               env=dict(platform=platform.platform(), python=sys.version.split()[0], numpy=np.__version__, scipy=scipy.__version__,
                        pandas=pd.__version__),
               note='Derived from CSVs produced on macOS (R001-R017); this summary may run on any platform.')
    main_grid(out)
    limits(out)
    nonideal(out)
    mc(out)
    if not args.no_audit:
        margin_audit(out, args.dps)
    (RES / 'r019_derived.json').write_text(json.dumps(out, indent=2))
    (RES / 'r019_derived.md').write_text(markdown(out))
    print(markdown(out))


if __name__ == '__main__':
    main()
