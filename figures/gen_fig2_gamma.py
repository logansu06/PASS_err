"""Fig. 2: certified gain Gamma = L(S_hat)/U(S_nom) - 1 over the declared grid (eps > 0, P != D), free vs identical endpoints.

Data: experiments/a7/results/main_grid.csv. Per (eps, SNR) cell: 33 geometries. Boxes = IQR with median, whiskers 5-95%,
points = individual cases. Gamma <= 0 = certificate inconclusive (gray band); the inconclusive fraction per eps group
(132 cases) is printed under each group.
"""
import numpy as np
import pandas as pd
from matplotlib.colors import to_rgba

from paper_plot_style import (FAMILY, FONT_SIZE, INK, INK_2, MUTED, RES, SNR, SURFACE_SHADE, TEXT_W, light_grid, panel_tag,
                              plt, save_fig)

df = pd.read_csv(RES / 'main_grid.csv')
df = df[(df.eps_over_lambda > 0) & ~((df.xP == 0) & (df.yP == 0))]
EPS = sorted(df.eps_over_lambda.unique())
SNRS = sorted(df.snr_db.unique())
rng = np.random.default_rng(0)  # jitter only

fig, axes = plt.subplots(1, 2, figsize=(TEXT_W, 2.35), sharey=True, gridspec_kw=dict(wspace=0.06))
W = 0.19
YLO, YHI = -48, 122
for ax, fam, tag in zip(axes, ('free', 'endpoints'), ('(a) free family', '(b) identical endpoints')):
    d = df[df.control == fam]
    ax.axhspan(YLO, 0, color=SURFACE_SHADE, zorder=0, lw=0)
    ax.axhline(0, color=MUTED, lw=0.6, zorder=1)
    ax.axhline(5, color=INK_2, lw=0.6, ls=(0, (3, 2)), zorder=1)
    light_grid(ax)
    for i, e in enumerate(EPS):
        for j, s in enumerate(SNRS):
            g = 100 * d[(d.eps_over_lambda == e) & (d.snr_db == s)].Gamma.to_numpy()
            x0 = i + (j - 1.5) * W
            q05, q25, q50, q75, q95 = np.percentile(g, [5, 25, 50, 75, 95])
            ax.add_patch(plt.Rectangle((x0 - W * 0.42, q25), W * 0.84, q75 - q25, fc=to_rgba(SNR[s], 0.45), ec=INK_2, lw=0.5, zorder=2))
            ax.plot([x0, x0], [q05, q25], color=SNR[s], lw=0.7, zorder=2)
            ax.plot([x0, x0], [q75, q95], color=SNR[s], lw=0.7, zorder=2)
            ax.plot([x0 - W * 0.42, x0 + W * 0.42], [q50, q50], color=INK, lw=1.0, zorder=4)
            jit = x0 + rng.uniform(-W * 0.3, W * 0.3, len(g))
            neg = g <= 0
            ax.scatter(jit[~neg], g[~neg], s=2.2, color=SNR[s], lw=0, zorder=3)
            ax.scatter(jit[neg], g[neg], s=3.0, facecolor='white', edgecolor=SNR[s], lw=0.4, zorder=3)
    inc = [round(100 * (d[d.eps_over_lambda == e].Gamma <= 0).mean()) for e in EPS]
    ax.set_xticks(range(len(EPS)))
    ax.set_xticklabels(['%g\n%d%%' % (e, k) for e, k in zip(EPS, inc)])
    ax.set_xlabel(r'Tolerance $\epsilon/\lambda$  (second line: inconclusive share, $\Gamma\leq 0$)')
    ax.set_xlim(-0.55, len(EPS) - 0.45)
    ax.set_ylim(YLO, YHI)
    ax.text(0.01, 0.98, tag, transform=ax.transAxes, ha='left', va='top', fontsize=FONT_SIZE, color=INK)
    ax.text(-0.53, 6.0, '5%', ha='left', va='bottom', fontsize=FONT_SIZE - 1, color=INK_2)
    ax.text(-0.53, -2.0, 'inconclusive', ha='left', va='top', fontsize=FONT_SIZE - 1, color=INK_2, style='italic')
axes[0].set_ylabel(r'Certified gain $\Gamma$ (%)')
axes[0].tick_params(axis='y')
handles = [plt.Line2D([], [], marker='s', ls='', ms=5, mfc=SNR[s], mec=SNR[s], alpha=0.8, label='%g dB' % s) for s in SNRS]
axes[1].legend(handles=handles, title='Reference SNR', loc='upper right', ncol=4, handletextpad=0.2, columnspacing=0.9,
               fontsize=FONT_SIZE - 1, title_fontsize=FONT_SIZE - 1, borderaxespad=0.2)
save_fig(fig, 'fig2_gamma')
