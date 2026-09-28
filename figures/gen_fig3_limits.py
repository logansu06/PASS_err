"""Fig. 3: tolerance sweep at 30 dB for the three pre-specified geometries (R015, limits.csv; 54 cases).

Top row: leakage converse F_end = min_S max_q I_P (line) and the achievable certified leakage Ibar(S_hat) (hollow markers).
Bottom row: certified robust SLNR bracket [L(S_hat), U*] (line + band) and the exhaustive-nominal upper witness U(S_nom)
(dotted); where L(S_hat) > U(S_nom), GCS certifiably dominates.
"""
import numpy as np
import pandas as pd

from paper_plot_style import COL_W, FONT_SIZE, GEOM, INK, INK_2, RES, light_grid, plt, save_fig

d = pd.read_csv(RES / 'limits.csv')
db = lambda v: 10 * np.log10(v)

fig, axes = plt.subplots(2, 2, figsize=(COL_W, 3.3), sharex=True, sharey='row', gridspec_kw=dict(hspace=0.12, wspace=0.08))
for col, (fam, tag) in enumerate((('free', 'free'), ('endpoints', 'endpoints'))):
    top, bot = axes[0, col], axes[1, col]
    for P, st in GEOM.items():
        x = d[(d.control == fam) & (d.xP == P[0]) & (d.yP == P[1])].sort_values('eps_over_lambda')
        e = x.eps_over_lambda.to_numpy()
        top.plot(e, x.F_end, color=st['color'], lw=1.0, zorder=3)
        top.plot(e, x.Ibar_hat, ls='', marker=st['marker'], mfc='white', mec=st['color'], mew=0.7, ms=3.2, zorder=4)
        bot.fill_between(e, db(x.L_hat), db(x.U_star), color=st['color'], alpha=0.35, lw=0, zorder=2)
        bot.plot(e, db(x.U_star), color=st['color'], lw=0.6, zorder=3)
        bot.plot(e, db(x.L_hat), color=st['color'], lw=1.0, marker=st['marker'], ms=2.6, zorder=3)
        bot.plot(e, db(x.U_nom), color=st['color'], lw=0.8, ls=(0, (1, 1.3)), zorder=3)
    top.set_yscale('log')
    top.set_ylim(5e-5, 30)
    bot.set_ylim(-4.5, 33)
    light_grid(top)
    light_grid(bot)
    top.text(0.03, 0.97, '(%s) %s' % ('ab'[col], tag), transform=top.transAxes, ha='left', va='top', fontsize=FONT_SIZE - 1, color=INK)
    bot.text(0.97, 0.97, '(%s) %s' % ('cd'[col], tag), transform=bot.transAxes, ha='right', va='top', fontsize=FONT_SIZE - 1, color=INK)
    bot.set_xlabel(r'$\epsilon/\lambda$')
    bot.set_xticks([0.01, 0.03, 0.05, 0.07, 0.09])
    off = d[(d.control == fam) & (d.xP != 0)]
    gap = float((db(off.U_star) - db(off.L_hat)).max())
    bot.text(0.97, 0.33, 'off-axis gap\n' + r'$\leq %.2f$ dB' % (np.ceil(100 * gap) / 100), transform=bot.transAxes,
             ha='right', va='top', fontsize=FONT_SIZE - 1, color=INK_2)
axes[0, 0].set_ylabel(r'Leakage $I_P$')
axes[1, 0].set_ylabel('Robust SLNR (dB)')
# direct labels for geometries (right panels, right end), identity never color-alone
for P, st in GEOM.items():
    x = d[(d.control == 'endpoints') & (d.xP == P[0]) & (d.yP == P[1])].sort_values('eps_over_lambda')
    axes[0, 1].annotate('(%g,%g)' % P, (x.eps_over_lambda.iloc[-1], x.F_end.iloc[-1]), xytext=(3, 0), textcoords='offset points',
                        va='center', ha='left', fontsize=FONT_SIZE - 1, color=INK_2, annotation_clip=False)
    axes[1, 1].annotate('(%g,%g)' % P, (x.eps_over_lambda.iloc[-1], db(x.L_hat.iloc[-1])), xytext=(3, 0), textcoords='offset points',
                        va='center', ha='left', fontsize=FONT_SIZE - 1, color=INK_2, annotation_clip=False)
h = [plt.Line2D([], [], color=INK_2, lw=1.0, label=r'converse $F_{\rm end}$'),
     plt.Line2D([], [], color=INK_2, ls='', marker='o', mfc='white', ms=3.2, label=r'achievable $\bar I(\hat S)$')]
axes[0, 0].legend(handles=h, loc='upper left', bbox_to_anchor=(0.0, 0.74), fontsize=FONT_SIZE - 1, handlelength=1.4, borderaxespad=0.1)
h = [plt.Line2D([], [], color=INK_2, lw=1.0, marker='o', ms=2.6, label=r'$L(\hat S)$, certified'),
     plt.Line2D([], [], color=INK_2, lw=0.6, label=r'$U^\star$, family bound'),
     plt.Line2D([], [], color=INK_2, lw=0.8, ls=(0, (1, 1.3)), label=r'$U(S_{\rm N})$, nominal')]
fig.legend(handles=h, loc='upper center', bbox_to_anchor=(0.52, 0.0), ncol=3, fontsize=FONT_SIZE - 1, handlelength=1.6,
           columnspacing=0.9, handletextpad=0.4, borderaxespad=0.0)
save_fig(fig, 'fig3_limits')
