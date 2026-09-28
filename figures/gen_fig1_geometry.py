"""Fig. 1: system geometry and certificate construction, computed for the featured case
(free family, P = (3, 2) m, eps = 0.05 lambda, reference SNR 30 dB; M = 24, N = 8).

(a) Top view: waveguide on the x axis (height d = 3 m, feed at x_f = -10 m), desired D, the 33 protected-receiver positions
    of the grid; inset: the 24 D-aligned candidate sites with the GCS layout S_hat and the exhaustive nominal layout S_N.
(b) One selected site in the complex plane: the true contribution z_P(x_n + delta), |delta| <= eps (monotone phase), its
    enclosing asymmetric sector (Theorem 1) and the endpoint chord [z_n^-, z_n^+] (zonotope generator, Theorem 2).
(c) Subset level: sampled leakage fields h_P(S, delta) for S_hat and S_N (uniform delta), the endpoint zonotope of each
    layout, the certified bound |h_P(S_hat)| <= B_P(S_hat) (Theorem 1) and the endpoint witness max |h_P(S_N)| (Theorem 2).
All quantities come from experiments/a7/a7_core.py; nothing is drawn by hand.
"""
import json

import numpy as np
from scipy.spatial import ConvexHull

from paper_plot_style import FAMILY, FIG_DIR, FONT_SIZE, GEOM, INK, INK_2, MUTED, TEXT_W, plt, save_fig
import a7_core as a
from a7_checks import instance
from run_main import GEOMS

P, EE, SNR_DB, FAM = (3.0, 2.0), 0.05, 30.0, 'free'
I = instance(P, FAM, SNR_DB, EE)
xs, eps, T, SN, Sh, N = I['xs'], I['eps'], I['T'], I['SN'], I['g']['S_hat'], 8
BLUE, NOMC = FAMILY['free']['color'], INK

fig = plt.figure(figsize=(TEXT_W, 2.45))
gs = fig.add_gridspec(2, 3, width_ratios=[1.55, 1, 1], height_ratios=[3.2, 1], wspace=0.34, hspace=0.62)

# ---------------------------------------------------------------- (a) geometry
ax = fig.add_subplot(gs[0, 0])
ax.axhline(0, color=INK_2, lw=1.6, zorder=1)
ax.annotate('', xy=(-7.3, 0), xytext=(-6.2, 0), arrowprops=dict(arrowstyle='->', color=INK_2, lw=0.8))
ax.text(7.3, -0.25, r'waveguide (height $d = 3$ m), feed at $x_f = -10$ m', ha='right', va='top', fontsize=FONT_SIZE - 1, color=INK_2)
gx = np.array([g for g in GEOMS if g != (0.0, 0.0)])
ax.scatter(gx[:, 0], gx[:, 1], s=6, color=MUTED, lw=0, zorder=2)
for Pg, st in GEOM.items():
    ax.scatter(*Pg, s=26, marker=st['marker'], facecolor='white' if Pg != P else st['color'], edgecolor=st['color'], lw=0.9, zorder=3)
ax.annotate(r'$P$ (featured)', P, xytext=(5, 3), textcoords='offset points', fontsize=FONT_SIZE - 1, color=INK)
ax.scatter(0, 0, s=45, marker='*', color=INK, zorder=4)
ax.annotate(r'$D$', (0, 0), xytext=(-5, 3), textcoords='offset points', ha='right', va='bottom', fontsize=FONT_SIZE, color=INK)
ax.set_xlim(-7.4, 7.4)
ax.set_ylim(-1.0, 4.6)
ax.set_yticks([0, 1, 2, 4])
ax.set_xlabel(r'$x$ (m)', labelpad=1)
ax.set_ylabel(r'$y$ (m)')
ax.text(-0.02, 1.02, '(a)', transform=ax.transAxes, ha='right', va='bottom', fontsize=FONT_SIZE)
ins = fig.add_subplot(gs[1, 0])
xm = 1e3 * (xs - xs.mean())
ins.scatter(xm, np.zeros_like(xm), s=5, marker='|', color=MUTED, lw=0.8)
ins.scatter(xm[Sh], np.full(N, 0.6), s=12, marker='o', color=BLUE, lw=0)
ins.scatter(xm[SN], np.full(N, -0.6), s=12, marker='o', facecolor='white', edgecolor=NOMC, lw=0.7)
ins.text(xm.max() + 5, 0.6, r'$\hat S$ (GCS)', va='center', fontsize=FONT_SIZE - 1, color=INK)
ins.text(xm.max() + 5, -0.6, r'$S_{\rm N}$ (nominal)', va='center', fontsize=FONT_SIZE - 1, color=INK)
ins.set_ylim(-1.2, 1.2)
ins.set_xlim(xm.min() - 5, xm.max() + 62)
ins.set_yticks([])
ins.spines['left'].set_visible(False)
ins.set_xlabel(r'24 D-aligned candidate sites, $x - \bar x$ (mm)', labelpad=1)

# ---------------------------------------------------------------- (b) one site
ax = fig.add_subplot(gs[:, 1])
n = int(Sh[len(Sh) // 2])
dd = np.linspace(-eps, eps, 400)
arc = a.z(xs[n] + dd, *P)
zp, zm = a.z(xs[n] + eps, *P), a.z(xs[n] - eps, *P)
pp, pm = a.psi(xs[n] + eps, *P), a.psi(xs[n] - eps, *P)
amin, amax = [float(v[0]) for v in a.amp_range(np.array([xs[n]]), eps, *P, None)]
for t in (-pp, -pm):  # sector edges: exact endpoint phases (monotone guided phase)
    ax.plot([0.6 * amax * np.cos(t), amax * np.cos(t)], [0.6 * amax * np.sin(t), amax * np.sin(t)], color=BLUE, lw=0.8, ls=(0, (2, 1.5)))
ax.plot(arc.real, arc.imag, color=BLUE, lw=4.0, alpha=0.25, solid_capstyle='butt')
ax.plot(arc.real, arc.imag, color=INK, lw=1.1)
ax.plot([zm.real, zp.real], [zm.imag, zp.imag], color=INK_2, lw=0.9, ls='--')
ax.scatter([zm.real, zp.real], [zm.imag, zp.imag], s=12, color=INK, zorder=4)
mid = (zp + zm) / 2
ax.scatter([mid.real], [mid.imag], s=14, marker='x', color=INK_2, lw=0.8, zorder=4)
ax.annotate(r'$z_n^{+}$', (zp.real, zp.imag), xytext=(4, -3), textcoords='offset points', fontsize=FONT_SIZE - 1, va='top')
ax.annotate(r'$z_n^{-}$', (zm.real, zm.imag), xytext=(-4, 3), textcoords='offset points', fontsize=FONT_SIZE - 1, ha='right')
ax.annotate(r'$m_n$', (mid.real, mid.imag), xytext=(-3, -3), textcoords='offset points', fontsize=FONT_SIZE - 1, ha='right', va='top')
ax.set_aspect('equal')
bx = np.r_[arc.real, 0.6 * amax * np.cos([-pp, -pm])]
by = np.r_[arc.imag, 0.6 * amax * np.sin([-pp, -pm])]
cx, cy, half = (bx.max() + bx.min()) / 2, (by.max() + by.min()) / 2, 0.58 * max(np.ptp(bx), np.ptp(by))
ax.set_xlim(cx - half, cx + half)
ax.set_ylim(cy - half, cy + half)
ax.set_xlabel(r'Re $z_P$')
ax.set_ylabel(r'Im $z_P$', labelpad=1)
h = [plt.Line2D([], [], color=INK, lw=1.1, label=r'true locus $z_P(x_n+\delta)$'),
     plt.Line2D([], [], color=BLUE, lw=4, alpha=0.3, label='sector, Thm 1 (radial width %.1e)' % ((amax - amin) / amax)),
     plt.Line2D([], [], color=INK_2, lw=0.9, ls='--', label='endpoint chord, Thm 2')]
ax.legend(handles=h, loc='upper center', bbox_to_anchor=(0.5, -0.3), fontsize=FONT_SIZE - 2, handlelength=1.6, borderaxespad=0.0)
ax.text(-0.02, 1.02, '(b)', transform=ax.transAxes, ha='right', va='bottom', fontsize=FONT_SIZE)

# ---------------------------------------------------------------- (c) subset leakage
ax = fig.add_subplot(gs[:, 2])
rng = np.random.default_rng(2026)
_, _, ZP = a.endpoint_bank(xs, eps, P)
B_hat = np.sqrt(N * a.leakage_upper(Sh, T, N))
for S, col, fill, lab in ((SN, NOMC, False, r'$S_{\rm N}$'), (Sh, BLUE, True, r'$\hat S$')):
    dl = rng.uniform(-eps, eps, (4000, N))
    hp = a.z(xs[S][None] + dl, *P).sum(1)
    ax.scatter(hp.real, hp.imag, s=0.6, color=col, alpha=0.25, lw=0, rasterized=True)
    V = ZP[np.asarray(S)].sum(0)
    hull = ConvexHull(np.c_[V.real, V.imag])
    poly = V[hull.vertices]
    ax.plot(np.r_[poly.real, poly.real[:1]], np.r_[poly.imag, poly.imag[:1]], color=col, lw=0.9)
    nom = a.z(xs[S], *P).sum()
    ax.scatter([nom.real], [nom.imag], s=16, marker='o', facecolor=col if fill else 'white', edgecolor=col, lw=0.8, zorder=5)
tt = np.linspace(0, 2 * np.pi, 400)
r_nom = np.abs(ZP[np.asarray(SN)].sum(0)).max()
ax.plot(B_hat * np.cos(tt), B_hat * np.sin(tt), color=BLUE, lw=0.8, ls=(0, (4, 2)))
ax.plot(r_nom * np.cos(tt), r_nom * np.sin(tt), color=NOMC, lw=0.8, ls=(0, (1, 1.2)))
ax.scatter(0, 0, s=14, marker='+', color=INK_2, lw=0.8)
ax.set_aspect('equal')
R = 1.12 * max(B_hat, r_nom)
ax.set_xlim(-R, R)
ax.set_ylim(-R, R)
ax.set_xlabel(r'Re $h_P$')
ax.set_ylabel(r'Im $h_P$', labelpad=1)
h = [plt.Line2D([], [], color=BLUE, lw=0.9, label=r'$\hat S$: samples, zonotope'),
     plt.Line2D([], [], color=NOMC, lw=0.9, label=r'$S_{\rm N}$: samples, zonotope'),
     plt.Line2D([], [], color=BLUE, lw=0.8, ls=(0, (4, 2)), label=r'$B_P(\hat S)$ (certified)'),
     plt.Line2D([], [], color=NOMC, lw=0.8, ls=(0, (1, 1.2)), label=r'endpoint max, $S_{\rm N}$')]
ax.legend(handles=h, loc='upper center', bbox_to_anchor=(0.5, -0.3), ncol=1, fontsize=FONT_SIZE - 2, handlelength=1.6, borderaxespad=0.0)
ax.text(-0.02, 1.02, '(c)', transform=ax.transAxes, ha='right', va='bottom', fontsize=FONT_SIZE)
vals = dict(case=dict(family=FAM, P=P, eps_over_lambda=EE, snr_db=SNR_DB), S_hat=[int(v) for v in Sh], S_nom=[int(v) for v in SN],
            B_P_S_hat=float(B_hat), endpoint_max_abs_hP_S_nom=float(r_nom),
            nominal_abs_hP_S_hat=float(abs(a.z(xs[Sh], *P).sum())), nominal_abs_hP_S_nom=float(abs(a.z(xs[SN], *P).sum())),
            site_n=n, sector_radial_width_rel=float((amax - amin) / amax), mc_draws_per_layout=4000,
            caption_upper_bound_rounded_up_4dp=float(np.ceil(1e4 * B_hat) / 1e4),
            caption_witness_rounded_down_4dp=float(np.floor(1e4 * r_nom) / 1e4))
(FIG_DIR / 'fig1_values.json').write_text(json.dumps(vals, indent=1))
print(vals)
save_fig(fig, 'fig1_geometry')
