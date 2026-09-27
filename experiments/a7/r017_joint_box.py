"""R017 (nice-to-have): dependency-aware joint-box refinement (GPT6_PRO_REPLY.md, D.6) on the 5 widest-gap cases.

The Theorem 1 certificate bounds the desired power and the leakage separately, which is loose when D and P respond
alike to the same error (co-aligned receivers, x_P = 0). D.6: partition the physical error box into sub-boxes Q_j;
on each sub-box a lower bound l_Q on the SLNR holds for every error in Q_j, so min_j l_Qj <= W(S).

Per sub-box (centre offsets c, half-widths w) we take the better of two valid bounds for each factor:
  desired  |h_D| >= max( projection onto angle h_D(c) with per-element phase/amplitude intervals,  |h_D(c)| - r_D )
  leakage  |h_P| <= min( Theorem 1 sector support on the sub-box intervals, sec(pi/K) corrected,   |h_P(c)| + r_P )
with r_r = sum_n D_rn w_n and D_rn >= sup |z_r'| on the element interval (mean-value bound of D.6).
Best-first branch and bound, children inherit max(parent, child); exact SLNR at box centres tightens U.
Fixed CPU budget per case (pre-declared here): 300,000 box evaluations or 180 s, whichever comes first.

Cases: the 5 largest U(S_hat)/L(S_hat) gaps in results/main_grid.csv over P != D, eps > 0, one row per distinct
(x_P, y_P, eps) (the row with the largest gap is kept). Validation: the refined bound is checked against 1e5
uniform draws + all corners (must not exceed the sampled minimum beyond 1e-10 relative).
"""
import heapq, itertools, json, time, zlib
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd

import a7_core as a

HERE = Path(__file__).resolve().parent
M, N, K = 24, 8, 1440
TH = np.linspace(-np.pi, np.pi, K, endpoint=False)
BUDGET, TMAX, BATCH = 300000, 180.0, 256


def wrap(t):
    return np.angle(np.exp(1j * t))


def amp_int(lo, hi, ux, uy):
    """min / max of 1/R over [lo, hi] (ideal channel)."""
    rl, rh = a.R(lo, ux, uy), a.R(hi, ux, uy)
    amax = np.where((lo <= ux) & (ux <= hi), 1 / a.R(ux, ux, uy), 1 / np.minimum(rl, rh))
    return 1 / np.maximum(rl, rh), amax


def deriv_bound(lo, hi, ux, uy):
    """D >= sup |z'(x)| on [lo, hi]; z = exp(-j psi)/R, |z'|^2 = (v/R^3)^2 + (K0 (v/R + NEFF) / R)^2."""
    b = np.sqrt(uy * uy + a.D_H ** 2)
    vl, vh = lo - ux, hi - ux
    vmin = np.where((vl <= 0) & (vh >= 0), 0.0, np.minimum(abs(vl), abs(vh)))
    rmin = np.sqrt(b * b + vmin * vmin)
    tl, th = vl / np.sqrt(vl * vl + b * b), vh / np.sqrt(vh * vh + b * b)
    tabs = np.maximum(abs(tl), abs(th))
    return np.sqrt((tabs / rmin ** 2) ** 2 + (a.K0 * (th + a.NEFF) / rmin) ** 2)


def box_eval(xS, C, W, P, s2):
    """Lower bound l_Q, exact SLNR at the centre, and a split score per dimension, for a batch of boxes (B, N)."""
    lo, hi, xc = xS + C - W, xS + C + W, xS + C
    zDc, zPc = a.z(xc, 0, 0), a.z(xc, *P)
    hD, hP = zDc.sum(1), zPc.sum(1)
    # desired: projection onto the centre direction
    pl, ph = a.psi(lo, 0, 0), a.psi(hi, 0, 0)
    mid = wrap(-(ph + pl) / 2 - np.angle(hD)[:, None])
    mc = np.cos(np.minimum(abs(mid) + (ph - pl) / 2, np.pi))
    amin, amax = amp_int(lo, hi, 0, 0)
    proj = np.where(mc >= 0, amin * mc, amax * mc).sum(1)
    dD = deriv_bound(lo, hi, 0, 0)
    dlb = np.maximum(np.maximum(proj, abs(hD) - (dD * W).sum(1)), 0)
    # leakage: sector support on the sub-box intervals
    ql, qh = a.psi(lo, *P), a.psi(hi, *P)
    phi, half = -(qh + ql) / 2, (qh - ql) / 2
    amin, amax = amp_int(lo, hi, *P)
    gap = np.maximum(abs(wrap(TH[None, None] - phi[..., None])) - half[..., None], 0)
    c = np.cos(gap)
    s = np.where(c >= 0, amax[..., None] * c, amin[..., None] * c).sum(1).max(1)
    dP = deriv_bound(lo, hi, *P)
    pub = np.minimum(np.maximum(s / np.cos(np.pi / K), 0), abs(hP) + (dP * W).sum(1))
    lq = dlb * dlb / (N * s2 + pub * pub)
    val = abs(hD) ** 2 / (N * s2 + abs(hP) ** 2)
    score = (dD + dP) * W
    return lq, val, score


def refine(xs, S, eps, P, s2, L0, U0):
    xS = xs[S][None]
    t0 = time.perf_counter()
    C, W = np.zeros((1, N)), np.full((1, N), eps)
    l, v, sc = box_eval(xS, C, W, P, s2)
    root = float(l[0])
    boxes = {0: (C[0], W[0], sc[0])}
    heap = [(max(root, L0), 0)]
    U, nid, n_eval, trace = min(U0, float(v[0])), 1, 1, []
    while n_eval < BUDGET and time.perf_counter() - t0 < TMAX:
        par = [heapq.heappop(heap) for _ in range(min(BATCH, len(heap)))]
        Cs, Ws, lp = [], [], []
        for lpar, i in par:
            c, w, s = boxes.pop(i)
            d = int(np.argmax(s))
            for sgn in (-1.0, 1.0):
                cc, ww = c.copy(), w.copy()
                ww[d] = w[d] / 2
                cc[d] = c[d] + sgn * ww[d]
                Cs.append(cc)
                Ws.append(ww)
                lp.append(lpar)
        Cs, Ws, lp = np.array(Cs), np.array(Ws), np.array(lp)
        l, v, sc = box_eval(xS, Cs, Ws, P, s2)
        l = np.maximum(l, lp)
        n_eval += len(l)
        U = min(U, float(v.min()))
        for k in range(len(l)):
            boxes[nid] = (Cs[k], Ws[k], sc[k])
            heapq.heappush(heap, (float(l[k]), nid))
            nid += 1
        if len(trace) == 0 or n_eval >= trace[-1][0] * 2:
            trace.append((n_eval, heap[0][0], U, time.perf_counter() - t0))
    Lr = heap[0][0]
    trace.append((n_eval, Lr, U, time.perf_counter() - t0))
    return dict(root_bound=root, L_refined=Lr, U_refined=U, n_eval=n_eval, seconds=time.perf_counter() - t0, trace=trace)


def run_case(r):
    xs = a.aligned_sites(M)
    P, eps, s2 = (float(r['xP']), float(r['yP'])), float(r['eps_over_lambda']) * a.LAM, float(r['sigma2'])
    S = np.array([int(v) for v in r['S_hat'].split()])
    res = refine(xs, S, eps, P, s2, float(r['L_hat']), float(r['U_hat']))
    rng = np.random.default_rng(zlib.crc32(repr((r['control'], r['snr_db'], r['eps_over_lambda'], P)).encode()))
    corners = np.array(list(itertools.product((-1., 1.), repeat=N)))
    D = np.vstack([rng.uniform(-eps, eps, (100000, N)), eps * corners])
    smin = float(a.exact_at(xs, S, D, P, N, s2)[0].min())
    res.update(control=r['control'], snr_db=float(r['snr_db']), eps_over_lambda=float(r['eps_over_lambda']), xP=P[0], yP=P[1],
               S_hat=r['S_hat'], S_nom=r['S_nom'], same_layout=bool(r['S_hat'] == r['S_nom']),
               L_theorem1=float(r['L_hat']), U_witness=float(r['U_hat']), U_nom=float(r['U_nom']), sampled_min=smin,
               gap_before=float(r['U_hat']) / float(r['L_hat']) - 1, gap_after=res['U_refined'] / res['L_refined'] - 1,
               Gamma_before=float(r['L_hat']) / float(r['U_nom']) - 1, Gamma_after=res['L_refined'] / float(r['U_nom']) - 1,
               valid=bool(res['L_refined'] <= smin * (1 + 1e-10)))
    res['gap_closed'] = 1 - np.log1p(res['gap_after']) / np.log1p(res['gap_before'])
    return res


def main():
    d = pd.read_csv(HERE / 'results/main_grid.csv')
    d = d[(d.eps_over_lambda > 0) & ~((d.xP == 0) & (d.yP == 0))].copy()
    d = d.sort_values('bracket_hat', ascending=False).drop_duplicates(['xP', 'yP', 'eps_over_lambda']).head(5)
    with Pool(5) as pool:
        out = pool.map(run_case, [r for _, r in d.iterrows()])
    (HERE / 'results/r017_joint_box.json').write_text(json.dumps(out, indent=2, default=float))
    for r in out:
        print('%s P=(%g,%g) eps=%.2f %gdB same=%d | L %.4f -> %.4f  U %.4f -> %.4f  gap %.3f -> %.3f (closed %.0f%%)  '
              'Gamma %.3f -> %.3f  valid=%s  %d boxes %.0fs' % (
                  r['control'], r['xP'], r['yP'], r['eps_over_lambda'], r['snr_db'], r['same_layout'], r['L_theorem1'],
                  r['L_refined'], r['U_witness'], r['U_refined'], r['gap_before'], r['gap_after'], 100 * r['gap_closed'],
                  r['Gamma_before'], r['Gamma_after'], r['valid'], r['n_eval'], r['seconds']))


if __name__ == '__main__':
    main()
