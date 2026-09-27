"""Pilot A7: certified robust SLNR site selection for PASS (desired D, protected P).

Sites are phase-aligned for D (N0 levels). Choose N of M sites (equal power split).
Certified quantities under per-element boxes |delta_n|<=eps (exact model, no Taylor):
  L_D(S) = (sum_{n in S} A-_{D,n} cos beta_{D,n})^2 / N                (N1, D aligned)
  I_up(S)= (max_theta sum_{n in S} s_n(theta) + pad)^2 / N              (sector enclosure)
  SLNR_lb(S) = L_D / (sigma2 + I_up)
Adversarial upper bound on worst-case SLNR via feasible perturbations (split for D,
leakage-maximizing signs for P, random corners) evaluated exactly.
"""
import itertools, time
import numpy as np
from scipy.optimize import brentq

C = 3e8; FC = 28e9; LAM = C / FC; K0 = 2 * np.pi / LAM
D_H = 3.0; NEFF = 1.44; XF = -10.0
TH = np.linspace(-np.pi, np.pi, 1441)[:-1]; DTH = TH[1] - TH[0]


def R(x, ux, uy):
    return np.sqrt((x - ux) ** 2 + uy ** 2 + D_H ** 2)


def z(x, ux, uy):  # complex channel of a PA at x toward receiver (ux,uy)
    r = R(x, ux, uy)
    return np.exp(-1j * K0 * (r + NEFF * (x - XF))) / r


def psi(x, ux, uy):  # monotone increasing phase (n_eff>1)
    return K0 * (R(x, ux, uy) + NEFF * (x - XF))


def amp_range(x, eps, ux, uy):
    lo, hi = x - eps, x + eps
    a_end = np.stack([1 / R(lo, ux, uy), 1 / R(hi, ux, uy)])
    a_max = np.where((lo <= ux) & (ux <= hi), 1 / R(ux, ux, uy), a_end.max(0))
    return a_end.min(0), a_max


def aligned_sites(M, center=0.0):
    f = lambda x: np.sqrt(x ** 2 + D_H ** 2) + NEFF * x
    m0 = np.round(f(center) / LAM)
    lv = (m0 + np.arange(-(M // 2), M - M // 2)) * LAM
    return np.array([brentq(lambda x, t=t: f(x) - t, -1e3, 1e3, xtol=1e-14) for t in lv])


def site_tables(xs, eps, P):
    """Per-site certificate ingredients."""
    ux, uy = P
    # desired D at (0,0): N1 terms
    bD = np.maximum(psi(xs + eps, 0, 0) - psi(xs, 0, 0), psi(xs, 0, 0) - psi(xs - eps, 0, 0))
    aD_min, _ = amp_range(xs, eps, 0, 0)
    cD = aD_min * np.cos(np.minimum(bD, np.pi / 2)); valid = np.all(bD <= np.pi / 2)
    # protected P: sector enclosure support function s_n(theta)
    phi0 = -psi(xs, ux, uy)  # z = A e^{j phi}
    bP = np.maximum(psi(xs + eps, ux, uy) - psi(xs, ux, uy), psi(xs, ux, uy) - psi(xs - eps, ux, uy))
    aP_min, aP_max = amp_range(xs, eps, ux, uy)
    dist = np.abs(np.angle(np.exp(1j * (TH[None, :] - phi0[:, None]))))  # angular distance to centre
    gap = np.maximum(dist - bP[:, None], 0.0)
    mc = np.cos(np.minimum(gap, np.pi))
    s = np.where(mc > 0, aP_max[:, None] * mc, aP_min[:, None] * mc)
    return dict(cD=cD, s=s, aPmax=aP_max, valid=valid,
                zD=z(xs, 0, 0), zP=z(xs, ux, uy))


def cert_slnr(Sidx, T, N, sigma2):
    """Vectorized certified SLNR lower bound for subsets Sidx (K,N)."""
    LD = T["cD"][Sidx].sum(1) ** 2 / N
    Ib = T["s"][Sidx].sum(1).max(1) + T["aPmax"][Sidx].sum(1) * DTH / 2  # Lipschitz pad
    Iup = np.maximum(Ib, 0) ** 2 / N
    return LD / (sigma2 + Iup), LD, Iup


def nominal_slnr(Sidx, T, N, sigma2):
    gD = np.abs(T["zD"][Sidx].sum(1)) ** 2 / N
    gP = np.abs(T["zP"][Sidx].sum(1)) ** 2 / N
    return gD / (sigma2 + gP)


def adv_upper(S, xs, eps, P, N, sigma2, rng, n_rand=256):
    """Feasible adversaries -> upper bound on worst-case SLNR of subset S (exact model)."""
    x = xs[S]; ux, uy = P
    def slnr(dl):
        xx = x[None, :] + dl
        gD = np.abs(z(xx, 0, 0).sum(1)) ** 2 / N
        gP = np.abs(z(xx, ux, uy).sum(1)) ** 2 / N
        return gD / (sigma2 + gP)
    cands = []
    xiD = NEFF + x / np.sqrt(x ** 2 + D_H ** 2); w = 1 / R(x, 0, 0); w = w / w.sum()
    sD = np.sign(xiD - (w * xiD).sum()); sD[sD == 0] = 1
    cands += [eps * sD, -eps * sD]
    zP = z(x, ux, uy); dz = (z(x + 1e-7, ux, uy) - z(x - 1e-7, ux, uy)) / 2e-7
    for th in TH[::8]:  # leakage-maximizing sign patterns
        sg = np.sign(np.real(np.exp(-1j * th) * dz)); sg[sg == 0] = 1
        cands.append(eps * sg)
    cands += list(eps * rng.choice([-1.0, 1.0], size=(n_rand, N)))
    return slnr(np.array(cands)).min()


def local_search(score_fn, M, N, rng, restarts=8, iters=400, fixed=(), inits=()):
    """Multistart swap search on score_fn over N-subsets of range(M); sites in `fixed` are always kept."""
    fixed = np.array(sorted(fixed), dtype=int); free = np.array([m for m in range(M) if m not in set(fixed.tolist())])
    k = N - fixed.size
    best_S, best_v = None, -np.inf
    starts = [np.sort(np.asarray(s)) for s in inits] + [None] * restarts
    for s0 in starts:
        S = s0 if s0 is not None else np.sort(np.r_[fixed, rng.choice(free, k, replace=False)])
        v = score_fn(S[None, :])[0]
        improved = True; it = 0
        while improved and it < iters:
            improved = False; it += 1
            cand = []
            for i in range(N):
                if S[i] in fixed:
                    continue
                for j in free:
                    if j in S:
                        continue
                    T2 = S.copy(); T2[i] = j; cand.append(np.sort(T2))
            cand = np.array(cand); vals = score_fn(cand); kk = int(np.argmax(vals))
            if vals[kk] > v + 1e-15:
                S, v, improved = cand[kk], vals[kk], True
        if v > best_v:
            best_S, best_v = S, v
    return best_S, best_v


def exhaustive_nominal(T, M, N, sigma2, fixed=(), batch=200000):
    """Exact nominal-SLNR optimum over all N-subsets (optionally containing `fixed`)."""
    fixed = sorted(fixed); free = [m for m in range(M) if m not in fixed]
    best, bv = None, -np.inf; buf = []
    def flush(buf):
        nonlocal best, bv
        A = np.array(buf); vals = nominal_slnr(A, T, N, sigma2); k = int(np.argmax(vals))
        if vals[k] > bv:
            best, bv = A[k], vals[k]
    for c in itertools.combinations(free, N - len(fixed)):
        buf.append(sorted(fixed + list(c)))
        if len(buf) >= batch:
            flush(buf); buf = []
    if buf:
        flush(buf)
    return np.array(best), bv


# DEPRECATED (round-2 review): the non-exhaustive branch ignores fix_ends and uses local nominal search.
# Use a7_main.py (exhaustive nominal, fixed endpoints, nominal-initialized robust search, eps=0 special case).
def run_case(M, N, eps_l, P, sigma2, rng, exhaustive, fix_ends=False, center=0.0):
    xs = aligned_sites(M, center); eps = eps_l * LAM; T = site_tables(xs, eps, P)
    if not T["valid"]:
        return None
    if fix_ends:
        inner = [i for i in range(1, M - 1)]
        mk = lambda sub: np.sort(np.concatenate([[0, M - 1], sub]))
    if exhaustive:
        if fix_ends:
            allS = np.array([mk(np.array(c)) for c in itertools.combinations(inner, N - 2)])
        else:
            allS = np.array(list(itertools.combinations(range(M), N)))
        nom = nominal_slnr(allS, T, N, sigma2); rob, _, _ = cert_slnr(allS, T, N, sigma2)
        S_nom, S_rob = allS[np.argmax(nom)], allS[np.argmax(rob)]
    else:
        def wrap(fn):
            if not fix_ends:
                return lambda S: fn(S, T, N, sigma2) if fn is nominal_slnr else fn(S, T, N, sigma2)[0]
            return None
        f_nom = lambda S: nominal_slnr(S, T, N, sigma2)
        f_rob = lambda S: cert_slnr(S, T, N, sigma2)[0]
        S_nom, _ = local_search(f_nom, M, N, rng); S_rob, _ = local_search(f_rob, M, N, rng)
    lb_rob = cert_slnr(S_rob[None, :], T, N, sigma2)[0][0]
    lb_nom = cert_slnr(S_nom[None, :], T, N, sigma2)[0][0]
    ub_nom = adv_upper(S_nom, xs, eps, P, N, sigma2, rng)
    ub_rob = adv_upper(S_rob, xs, eps, P, N, sigma2, rng)
    return dict(lb_rob=lb_rob, ub_rob=ub_rob, lb_nom=lb_nom, ub_nom=ub_nom,
                cert_gain=lb_rob / ub_nom - 1, same=np.array_equal(S_nom, S_rob),
                nom_nominal=nominal_slnr(S_nom[None, :], T, N, sigma2)[0])
