"""Table I (protocol) and Table II (results summary) as standalone LaTeX (booktabs), read from the stored results.

Sources: experiments/a7/a7_core.py constants, results/main_grid_meta.json, main_grid.csv (family sizes), main_summary.json,
m2m3_summary.json, m0_checks.json (R007 featured instance), r019_derived.json.
"""
import json

import pandas as pd

from paper_plot_style import FIG_DIR, RES
import a7_core as a

J = lambda f: json.loads((RES / f).read_text())
meta, ms, mm, m0, r9 = J('main_grid_meta.json'), J('main_summary.json'), J('m2m3_summary.json'), J('m0_checks.json'), J('r019_derived.json')
A = meta['args']
pc = lambda v, d=1: ('%.' + str(d) + 'f\\%%') % (100 * v)

# family sizes from the primary-filter rows (eps > 0, P != D); constant within each family
grid = pd.read_csv(RES / 'main_grid.csv')
grid = grid[(grid.eps_over_lambda > 0) & ~((grid.xP == 0) & (grid.yP == 0))]
FAM_SIZE = {}
for f, g in grid.groupby('control'):
    assert g.family_size.nunique() == 1, f
    FAM_SIZE[f] = int(g.family_size.iloc[0])

# ---------------------------------------------------------------- Table I
eps = [float(e) for e in A['eps'].split(',')]
t1 = r'''\begin{table}[t]
\centering
\caption{Simulation protocol (declared before the runs).}
\label{tab:protocol}
\footnotesize
\begin{tabular}{@{}p{0.24\columnwidth}p{0.70\columnwidth}@{}}
\toprule
Carrier, wavelength & $f_c = %g$ GHz, $\lambda = %.3f$ mm \\
Waveguide & $n_{\rm eff} = %g$, height $d = %g$ m, feed $x_f = %g$ m \\
Candidate family & $M = %d$ D-aligned sites, select $N = %d$, $d_{\min} = 0.5\lambda$ \\
Receivers & $D = (0,0)$; 33 positions $P$ ($x_P$: 11 values in $[-6, 6]$ m; $y_P \in \{1,2,4\}$ m) and the control $P = D$ \\
Tolerance & $\epsilon/\lambda \in \{%s\}$ \\
Reference SNR & $\{%s\}$ dB, relative to the central 8-site block toward $D$; fixed physical noise per SNR \\
Families & free; identical endpoints (sites 1 and $M$ forced) \\
Certificates & $K = %d$ with $\sec(\pi/K)$; $\beta_D \le \pi/2$ guard \\
Witnesses & $\le 2M$ family-wide endpoint templates (screening); for $S_{\rm N}$ / $\hat S$: all $2^N$ corners + %d / %d L-BFGS-B starts \\
Search & swap from $S_{\rm N}$ + %d random starts (seed %d); screening cap $%s$ evaluations \\
Main grid & %d cases (2 families $\times$ 4 SNR $\times$ 5 $\epsilon$ $\times$ 34 positions) \\
\bottomrule
\end{tabular}
\end{table}
''' % (a.FC / 1e9, 1e3 * a.LAM, a.NEFF, a.D_H, a.XF, A['M'], A['N'], ', '.join('%g' % e for e in eps), A['snr'].replace(',', ', '),
       A['K'], A['refine_nom'], A['refine_hat'], A['restarts'], A['seed'], '2\\times10^{5}' if A['cap'] == 200000 else A['cap'],
       meta['n_cases'])
(FIG_DIR / 'TABLE_I_protocol.tex').write_text(t1, encoding='utf-8')

# ---------------------------------------------------------------- Table II
o = ms['overall']
cnt = r9['counts']
bl = mm['baselines']
ni = mm['nonideal']
HEAD = r'\multicolumn{3}{@{}p{0.97\columnwidth}}{\emph{%s}} \\'
kn = lambda c: '%.2f\\%% (%d)' % (100 * c['k'] / c['n'], c['k'])  # exact k/n; 2 decimals avoid float half-even artefacts
rows = [HEAD % (r'Main grid, $\epsilon > 0$, $P \neq D$ ($n = %d$ per family), vs.\ exhaustive nominal $S_{\rm N}$' % o['free']['n'])]
for lab, key in ((r'$\Gamma > 0$ (cert.\ dominance)', 'gamma_pos'), (r'$\Gamma > 5\%$', 'gamma_above5')):
    rows.append(r'%s & %s & %s \\' % (lab, kn(cnt['free'][key]), kn(cnt['endpoints'][key])))
rows.append(r'Median $\Gamma$ [IQR] & %.1f [%.1f, %.1f]\%% & %.1f [%.1f, %.1f]\%% \\' % tuple(
    100 * v for f in ('free', 'endpoints') for v in (o[f]['median'], o[f]['q25'], o[f]['q75'])))
rows.append(r'Inconclusive ($\Gamma \le 0$) & %s & %s \\' % (pc(o['free']['inconclusive']), pc(o['endpoints']['inconclusive'])))
rows.append(r'Median nominal sacrifice & %s & %s \\' % (pc(o['free']['sacrifice_median'], 2), pc(o['endpoints']['sacrifice_median'], 2)))
rows.append(r'Unique robust optimum & %s & %s \\' % (pc(o['free']['unique']), pc(o['endpoints']['unique'])))
rows.append(r'Median $U^\star/L(\hat S) - 1$ & %s & %s \\' % (pc(o['free']['global_gap_median'], 2), pc(o['endpoints']['global_gap_median'], 2)))
rows.append(r'Median survivors / $|\mathcal{F}|$ & %d / %s & %d / %s \\' % (
    o['free']['survivors_median'], '{:,}'.format(FAM_SIZE['free']), o['endpoints']['survivors_median'], '{:,}'.format(FAM_SIZE['endpoints'])))
rows.append(r'Cap hit (bracket only) & %d & %d \\' % (o['free']['capped'], o['endpoints']['capped']))
rows.append(r'\midrule')
rows.append(HEAD % (r'Baseline slice: 20, 30 dB; $\epsilon/\lambda \in \{0.03, 0.05\}$; $n = %d$ per family' % bl['free|all']['n']))
rows.append(r'$\Gamma > 0$ vs.\ $S_{\rm N}$ & %s & %s \\' % (pc(bl['free|all']['nom_pos']), pc(bl['endpoints|all']['nom_pos'])))
rows.append(r'Cert.\ dominance vs.\ B-CR$^\dagger$ & %s & %s \\' % (pc(bl['free|all']['cr_pos']), pc(bl['endpoints|all']['cr_pos'])))
rows.append(r'Cert.\ dominance vs.\ B-GR & %s & %s \\' % (pc(bl['free|all']['gr_pos']), pc(bl['endpoints|all']['gr_pos'])))
rows.append(r'$\Gamma > 0$, 0.08 dB/m$^\ddagger$ & %s & %s \\' % (pc(ni['free|0.08 dB/m']['pos']), pc(ni['endpoints|0.08 dB/m']['pos'])))
rows.append(r'$\Gamma > 0$, 1 dB/m$^\ddagger$ & %s & %s \\' % (pc(ni['free|1 dB/m']['pos']), pc(ni['endpoints|1 dB/m']['pos'])))
rows.append(r'\midrule')
fc = m0['R007']['cases']
rows.append(HEAD % r'Featured instance: $P = (3, 2)$ m, $\epsilon = 0.05\lambda$, 30 dB. Float64 family certificate; selected decisive quantities (winner, float-ranked top rivals, $U(S_{\rm N})$) re-evaluated at 50 digits')
rows.append(r'$L(\hat S)$; rival margin & %.3f; %.4f & %.3f; %.4f \\' % (
    fc['free']['L_hat'][1], fc['free']['margin'][1], fc['endpoints']['L_hat'][1], fc['endpoints']['margin'][1]))
rows.append(r'Certified gain $\Gamma$ & %s & %s \\' % (pc(fc['free']['Gamma'][1], 2), pc(fc['endpoints']['Gamma'][1], 2)))
t2 = r'''\begin{table}[t]
\centering
\caption{Certified results. $\Gamma = L(\hat S)/U(S_{\rm N}) - 1$; $\Gamma > 0$ certifies a higher worst-case SLNR than the
exhaustive nominal layout in the same family. Certificates are analytical; all inequalities are evaluated in float64.
Rival margin: $L(\hat S) - \max_{S \neq \hat S} U_H(S)$. B-GR: desired-only, P-blind layout.
$^\dagger$Same-start shared-template swap heuristic (budgets not matched). $^\ddagger$Waveguide attenuation plus
$\cos^2\theta$ field directivity; both layouts redesigned under the model at a model-specific reference SNR.}
\label{tab:results}
\footnotesize
\setlength{\tabcolsep}{3pt}
\begin{tabular}{@{}lrr@{}}
\toprule
 & Free & Endpoints \\
\midrule
%s
\bottomrule
\end{tabular}
\end{table}
''' % '\n'.join(rows)
(FIG_DIR / 'TABLE_II_results.tex').write_text(t2, encoding='utf-8')
print(t1)
print(t2)
