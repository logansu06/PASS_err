"""Fig. 4: global screening yield and efficiency.

(a) survivor fraction after safe screening vs M (scaling.csv: 6 declared geometries x eps {0.03, 0.05} lam x 30 dB = 12 cases
    per family and M). Points = cases; line = median of the 8 cases with x_P != 0; x = the 4 cases with x_P = 0 (P behind D),
    where screening removes almost nothing (the minimum surviving share is printed from the data).
(b) wall time per case vs M, median of all 12 cases (bars: range):
    total = t_total (setup, family construction, endpoint-bank pass, nominal enumeration, GCS screening, nominal-witness
    refinement), and the GCS selection stage t_gcs. Capped scans (x_P = 0 at free M >= 24 and endpoints M = 32) are included
    as they ran, i.e. runtime of the capped procedure, not time to a completed certificate maximization.
(c) share of main-grid cases (eps > 0, P != D; 33 positions x 4 SNRs = 132 per point and family, M = 24) with a unique
    robust-optimality certificate within the respective finite family.
"""
import json

import numpy as np
import pandas as pd

from paper_plot_style import COL_W, FAMILY, FONT_SIZE, INK, INK_2, MUTED, RES, light_grid, plt, save_fig

sc = pd.read_csv(RES / 'scaling.csv')
ms = json.loads((RES / 'main_summary.json').read_text())
MS = sorted(sc.M.unique())
off = {'free': -0.35, 'endpoints': 0.35}
GCS_LS = (0, (1, 1.2))

fig, axes = plt.subplots(3, 1, figsize=(COL_W, 3.9), gridspec_kw=dict(hspace=0.55))
ax = axes[0]
for fam, st in FAMILY.items():
    d = sc[sc.control == fam]
    x0 = d.M.to_numpy() + off[fam]
    reg = (d.xP != 0).to_numpy()
    ax.scatter(x0[reg], d.survivor_frac[reg], s=6, marker=st['marker'], facecolor=st['mfc'], edgecolor=st['color'], lw=0.6, zorder=3)
    med = d[reg].groupby('M').survivor_frac.median()
    ax.plot(np.array(MS) + off[fam], med.to_numpy(), color=st['color'], ls=st['ls'], lw=1.0, label=st['label'] + ' (median)', zorder=2)
    ax.scatter(x0[~reg], d.survivor_frac[~reg], s=10, marker='x', color=MUTED, lw=0.7, zorder=3)
min_z = sc[sc.xP == 0].survivor_frac.min()
ax.annotate(r'$x_P = 0$: $\geq$%.3f%% survive' % (np.floor(1e5 * min_z) / 1e3), (MS[0] - 1.6, 1.0), xytext=(0, -2),
            textcoords='offset points', ha='left', va='top', fontsize=FONT_SIZE - 1, color=INK_2)
ax.set_yscale('log')
ax.set_ylabel(r'Survivors / $|\mathcal{F}|$')
ax.legend(loc='center', bbox_to_anchor=(0.5, 0.60), ncol=2, fontsize=FONT_SIZE - 1, handlelength=2.2, borderaxespad=0.1)
ax.set_ylim(1e-6, 3)

ax = axes[1]
for fam, st in FAMILY.items():
    x = np.array(MS) + off[fam]
    for col, ls_, ms_ in (('t_total', st['ls'], 3.5), ('t_gcs', GCS_LS, 2.8)):
        g = sc[sc.control == fam].groupby('M')[col]
        ax.vlines(x, g.min(), g.max(), color=st['color'], lw=0.8, alpha=0.6)
        ax.plot(x, g.median(), color=st['color'], ls=ls_, marker=st['marker'], mfc=st['mfc'], mec=st['color'], mew=0.8, ms=ms_)
ax.set_yscale('log')
ax.set_ylabel('Time (s)')
F, E = FAMILY['free'], FAMILY['endpoints']
h = [plt.Line2D([], [], color=F['color'], ls=F['ls'], marker=F['marker'], mfc=F['mfc'], ms=3, label='free: total'),
     plt.Line2D([], [], color=E['color'], ls=E['ls'], marker=E['marker'], mfc=E['mfc'], mec=E['color'], ms=3, label='endp.: total'),
     plt.Line2D([], [], color=F['color'], ls=GCS_LS, marker=F['marker'], mfc=F['mfc'], ms=2.6, label='free: GCS'),
     plt.Line2D([], [], color=E['color'], ls=GCS_LS, marker=E['marker'], mfc=E['mfc'], mec=E['color'], ms=2.6, label='endp.: GCS')]
ax.legend(handles=h, loc='upper left', ncol=2, fontsize=FONT_SIZE - 1, handlelength=2.2, columnspacing=0.8, borderaxespad=0.1)
ax.set_ylim(5e-3, 2e3)
for a in axes[:2]:
    a.set_xticks(MS)
    a.set_xticklabels(['M = %d' % m for m in MS])
    a.set_xlim(MS[0] - 2.5, MS[-1] + 2.5)
    light_grid(a)

ax = axes[2]
for fam, st in FAMILY.items():
    by = ms['by_eps'][fam]
    e = sorted(float(k) for k in by)
    u = [100 * by[str(k)]['unique'] for k in e]
    ax.plot(e, u, color=st['color'], ls=st['ls'], marker=st['marker'], mfc=st['mfc'], mec=st['color'], mew=0.8)
ax.set_xlabel(r'Tolerance $\epsilon/\lambda$ (main grid, $M = 24$)')
ax.set_ylabel('Unique cert. (%)')
ax.set_xticks([0.01, 0.03, 0.05, 0.08])
ax.set_ylim(0, 100)
light_grid(ax)
for a, t in zip(axes, 'abc'):
    a.text(-0.02, 1.02, '(%s)' % t, transform=a.transAxes, ha='right', va='bottom', fontsize=FONT_SIZE, color=INK)
save_fig(fig, 'fig4_screening')
