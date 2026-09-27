"""Global Certified Selection (GCS) core for certified robust PASS site selection.

Ported from the GPT-6 Pro verification bundle (idea-stage/handoff/gpt6pro_bundle/bundle/
a7_verification_bundle: a7_reference.py, a7_audit.py, a7_global.py; 2026-09-26) with the
arithmetic of the ideal isotropic path preserved, so the featured case reproduces the bundle's
a7_global_results.json. Additions: separable non-ideal amplitude (in-waveguide attenuation +
cos^q field directivity), a pre-declared screening cap, and extra logged quantities.

Model (see refine-logs/FINAL_PROPOSAL.md, v2): waveguide along x at height D_H, feed at XF;
receiver r at (ux, uy, 0); phase psi = K0 (R + NEFF (x - XF)); amplitude
A = exp(-ALPHA (x - XF)) (b/R)^Q / R with b = sqrt(uy^2 + D_H^2). Equal power split 1/N.
All certificates are exact-arithmetic statements evaluated in float64.
"""
import itertools
import time

import numpy as np
from scipy.optimize import minimize

C, FC = 3e8, 28e9
LAM = C / FC
K0 = 2 * np.pi / LAM
D_H, NEFF, XF = 3.0, 1.44, -10.0
D_MIN = 0.5 * LAM


class Channel:
    """Separable amplitude model. alpha_db_m: in-waveguide power loss (dB/m); q: field directivity exponent."""

    def __init__(self, alpha_db_m=0.0, q=0.0):
        self.alpha = np.log(10) / 20 * alpha_db_m  # field attenuation (Np/m)
        self.q = float(q)

    @property
    def ideal(self):
        return self.alpha == 0 and self.q == 0


def R(x, ux, uy):
    return np.sqrt((x - ux) ** 2 + uy ** 2 + D_H ** 2)


def psi(x, ux, uy):
    return K0 * (R(x, ux, uy) + NEFF * (x - XF))


def amp(x, ux, uy, ch=None):
    """Field amplitude A_r(x)."""
    r = R(x, ux, uy)
    if ch is None or ch.ideal:
        return 1 / r
    b = np.sqrt(uy * uy + D_H ** 2)
    return np.exp(-ch.alpha * (x - XF)) * (b / r) ** ch.q / r


def z(x, ux, uy, ch=None):
    if ch is None or ch.ideal:
        return np.exp(-1j * psi(x, ux, uy)) / R(x, ux, uy)  # bundle arithmetic (ideal path)
    return np.exp(-1j * psi(x, ux, uy)) * amp(x, ux, uy, ch)


def aligned_sites(M, center=0.0):
    """N0: M sites on consecutive D-aligned levels R_D(x) + NEFF x in LAM*Z (bisection, as in the bundle)."""
    f = lambda x: np.sqrt(x ** 2 + D_H ** 2) + NEFF * x
    m0 = np.round(f(center) / LAM)
    out = []
    for t in (m0 + np.arange(-(M // 2), M - M // 2)) * LAM:
        lo, hi = -50.0, 50.0
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            lo, hi = (mid, hi) if f(mid) < t else (lo, mid)
        out.append(0.5 * (lo + hi))
    return np.array(out)


def amp_range(x, eps, ux, uy, ch=None):
    """Exact min/max of A over [x-eps, x+eps]: endpoints + interior stationary points.
    Stationary points of log A satisfy alpha v^2 + p v + alpha b^2 = 0, v = x - ux, p = q + 1."""
    if ch is None or ch.ideal:  # bundle arithmetic
        e = np.stack([1 / R(x - eps, ux, uy), 1 / R(x + eps, ux, uy)])
        amax = np.where((x - eps <= ux) & (ux <= x + eps), 1 / R(ux, ux, uy), e.max(0))
        return e.min(0), amax
    lo, hi = x - eps, x + eps
    cands = [amp(lo, ux, uy, ch), amp(hi, ux, uy, ch)]
    b = np.sqrt(uy * uy + D_H ** 2)
    p = ch.q + 1
    roots = []
    if ch.alpha == 0:
        roots = [0.0]
    else:
        disc = p * p - 4 * ch.alpha ** 2 * b * b
        if disc >= 0:
            roots = [(-p + np.sqrt(disc)) / (2 * ch.alpha), (-p - np.sqrt(disc)) / (2 * ch.alpha)]
    for v in roots:
        xv = ux + v
        inside = (lo <= xv) & (xv <= hi)
        cands.append(np.where(inside, amp(np.full_like(x, xv), ux, uy, ch), cands[0]))
    cands = np.stack(cands)
    return cands.min(0), cands.max(0)


def feasible(S, xs, eps, dmin=D_MIN):
    """Robust clearance: adjacent selected sites separated by >= dmin + 2 eps (necessary and sufficient)."""
    S = np.atleast_2d(S)
    return np.all(np.diff(xs[S], axis=1) >= dmin + 2 * eps - 1e-14, axis=1)


def combos(M, N):
    """All N-subsets of range(M) as int16 rows, in the same lexicographic order as itertools.combinations."""
    C = np.arange(M - N + 1, dtype=np.int16)[:, None]
    for k in range(1, N):
        last = C[:, -1].astype(np.int64)
        cnt = M - N + k - last
        rep = np.repeat(np.arange(len(C)), cnt)
        start = np.repeat(np.cumsum(cnt) - cnt, cnt)
        nxt = np.repeat(last + 1, cnt) + (np.arange(len(rep)) - start)
        C = np.hstack([C[rep], nxt[:, None].astype(np.int16)])
    return C


def family(xs, N, eps, forced=(), batch=1 << 20):
    allS = combos(len(xs), N)
    keep = np.empty(len(allS), dtype=bool)
    for st in range(0, len(allS), batch):
        keep[st:st + batch] = feasible(allS[st:st + batch], xs, eps)
    for f in forced:
        keep &= np.any(allS == f, axis=1)
    return allS[keep]


def tables(xs, eps, P, K=1440, asymmetric=True, ch=None):
    """Per-site certificate tables (Theorem 1). Raises if the family is not D-aligned or beta_D > pi/2."""
    xs = np.asarray(xs, dtype=float)
    phase0 = psi(xs, 0, 0)
    if np.max(np.abs(np.angle(np.exp(1j * (phase0 - phase0[0]))))) > 1e-8:
        raise ValueError('desired certificate requires a D-aligned candidate family')
    if eps < 0 or K < 3:
        raise ValueError('require eps >= 0 and K >= 3')
    th = np.linspace(-np.pi, np.pi, K, endpoint=False)
    pp = psi(xs + eps, 0, 0)
    pm = psi(xs - eps, 0, 0)
    p0 = psi(xs, 0, 0)
    bd = np.maximum(pp - p0, p0 - pm)
    if np.any(bd > np.pi / 2 + 1e-12):
        raise ValueError('desired projection certificate needs beta_D <= pi/2')
    c = amp_range(xs, eps, 0, 0, ch)[0] * np.cos(bd)
    p0 = psi(xs, *P)
    pp = psi(xs + eps, *P)
    pm = psi(xs - eps, *P)
    if asymmetric:
        phi = -(pp + pm) / 2
        bp = (pp - pm) / 2
    else:
        phi = -p0
        bp = np.maximum(pp - p0, p0 - pm)
    amin, amax = amp_range(xs, eps, *P, ch)
    gap = np.maximum(np.abs(np.angle(np.exp(1j * (th[None] - phi[:, None])))) - bp[:, None], 0)
    mc = np.cos(gap)
    s = np.where(mc >= 0, amax[:, None] * mc, amin[:, None] * mc)
    return dict(cD=c, s=s, amax=amax, zD=z(xs, 0, 0, ch), zP=z(xs, *P, ch), K=K, eps=eps, xs=xs.copy(), ch=ch)


def cert(S, T, N, s2, mode='sec'):
    """Certified SLNR lower bound L(S) = (sum c)^2 / (N s2 + B^2); eps = 0 uses the exact leakage."""
    if T['eps'] == 0:  # exact: one arithmetic path shared with nominal(), exact_at() and exact_bounds()
        return nominal(S, T, N, s2)
    S = np.atleast_2d(S)
    c = T['cD'][S].sum(1)
    m = T['s'][S].sum(1).max(1)
    if mode == 'sec':
        B = m / np.cos(np.pi / T['K'])
    elif mode == 'pad':
        B = m + T['amax'][S].sum(1) * np.pi / T['K']
    else:
        raise ValueError(mode)
    B = np.maximum(B, 0)
    return c * c / (N * s2 + B * B)


def nominal(S, T, N, s2, batch=1 << 18):
    """Nominal SLNR |h_D|^2 / (N s2 + |h_P|^2), batched."""
    S = np.atleast_2d(S)
    out = np.empty(len(S))
    for st in range(0, len(S), batch):
        B = S[st:st + batch]
        out[st:st + len(B)] = np.abs(T['zD'][B].sum(1)) ** 2 / (N * s2 + np.abs(T['zP'][B].sum(1)) ** 2)
    return out


def nominal_argmax(SS, T, N, s2):
    return SS[np.argmax(nominal(SS, T, N, s2))]


def search(T, N, s2, allS, init, seed=0, restarts=8, forced=(), mode='sec', objective=None):
    """Multistart swap search (bundle a7_audit.search). `objective(S2d) -> values` overrides the certificate."""
    f = objective if objective is not None else (lambda SS: cert(SS, T, N, s2, mode))
    rng = np.random.default_rng(seed)
    best, bestv = None, -np.inf
    starts = [np.sort(init)] + [allS[k] for k in rng.integers(0, len(allS), size=restarts)]
    M = len(T['cD'])
    for S in starts:
        S = S.copy()
        v = f(S)[0]
        while True:
            outsiders = np.setdiff1d(np.arange(M), S)
            cand = []
            for i in range(N):
                if int(S[i]) in forced:
                    continue
                for j in outsiders:
                    Q = S.copy()
                    Q[i] = j
                    Q = np.sort(Q)
                    cand.append(Q)
            if not cand:
                break
            cand = np.asarray(cand)
            cand = cand[feasible(cand, T['xs'], T['eps'])]
            if not len(cand):
                break
            vv = f(cand)
            k = np.argmax(vv)
            if vv[k] <= v + 1e-12:
                break
            S, v = cand[k], vv[k]
        if v > bestv:
            best, bestv = S, v
    return best, float(bestv)


def exact_at(xs, S, delta, P, N, s2, ch=None):
    D = np.atleast_2d(delta)
    hD = z(xs[S][None] + D, 0, 0, ch).sum(1)
    hP = z(xs[S][None] + D, *P, ch).sum(1)
    dd, pp = np.abs(hD) ** 2, np.abs(hP) ** 2
    return dd / (N * s2 + pp), dd / N, pp / N


def witnesses(xs, S, eps, P, N, s2, refine=0, ch=None):
    """Feasible upper bound U(S): all 2^N corners, then L-BFGS-B from the `refine` worst corners.
    Same physical error vector for D and P. Returns (U, delta, GD, IP) at the witness."""
    corners = np.array(list(itertools.product((-1., 1.), repeat=N)))
    vv, _, _ = exact_at(xs, S, eps * corners, P, N, s2, ch)
    k = np.argmin(vv)
    U = float(vv[k])
    delta = eps * corners[k]
    if eps > 0:
        for k in np.argsort(vv)[:refine]:
            res = minimize(lambda u: exact_at(xs, S, eps * u, P, N, s2, ch)[0][0], corners[k], method='L-BFGS-B',
                           bounds=[(-1, 1)] * N, options={'maxiter': 150, 'ftol': 1e-12})
            u = np.clip(res.x, -1, 1)
            val = exact_at(xs, S, eps * u, P, N, s2, ch)[0][0]
            if val < U:
                U = float(val)
                delta = eps * u
    _, GD, IP = exact_at(xs, S, delta, P, N, s2, ch)
    return U, delta, float(GD[0]), float(IP[0])


def endpoint_bank(xs, eps, P, ch=None):
    """Theorem 2: at most 2M shared endpoint sign templates (bundle a7_global.endpoint_bank)."""
    zp = z(xs + eps, *P, ch)
    zm = z(xs - eps, *P, ch)
    d = (zp - zm) / 2
    angles = np.mod(np.r_[np.angle(d) + np.pi / 2, np.angle(d) - np.pi / 2], 2 * np.pi)
    breaks = np.unique(angles)
    th = (breaks + np.r_[breaks[1:], breaks[0] + 2 * np.pi]) / 2
    signs = np.where(np.real(d[:, None] * np.exp(-1j * th[None])) >= 0, 1., -1.)
    ZP = z(xs[:, None] + eps * signs, *P, ch)
    ZD = z(xs[:, None] + eps * signs, 0, 0, ch)
    return signs, ZD, ZP


def bank_bounds(SS, ZD, ZP, N, s2, batch=4096):
    """U_H(S) (min SLNR over templates) and endpoint worst leakage EE(S) for all layouts in SS."""
    UU = np.empty(len(SS))
    EE = np.empty(len(SS))
    for start in range(0, len(SS), batch):
        B = SS[start:start + batch]
        hp = ZP[B].sum(1)
        hd = ZD[B].sum(1)
        pp = abs(hp) ** 2
        dd = abs(hd) ** 2
        UU[start:start + len(B)] = np.min(dd / (N * s2 + pp), axis=1)
        EE[start:start + len(B)] = np.max(pp, axis=1) / N
    return UU, EE


def exact_bounds(SS, T, ZD, ZP, N, s2):
    """(U_H, E_end) for every layout; at eps = 0 U_H is the exact nominal SLNR on the same arithmetic path as cert()."""
    UU, EE = bank_bounds(SS, ZD, ZP, N, s2)
    if T['eps'] == 0:
        UU = nominal(SS, T, N, s2)
    return UU, EE


def gcs(T, SS, UU, N, s2, SN, forced=(), seed=0, restarts=8, cap=200000, batch=128):
    """Global Certified Selection: incumbent by swap search, then safe screening (Theorem 2 / Corollary 1).
    Returns a dict with the certificate optimum (exact unless the cap is hit), bracket and uniqueness margin."""
    t0 = time.perf_counter()
    SR, inc = search(T, N, s2, SS, SN, seed=seed, restarts=restarts, forced=forced)
    swap_S, swap_L = SR.copy(), inc
    survivors = np.flatnonzero(UU > inc)
    n_eval = 0
    capped = False
    for start in range(0, len(survivors), batch):
        ii = survivors[start:start + batch]
        active = ii[UU[ii] > inc]
        if not len(active):
            continue
        if n_eval + len(active) > cap:
            capped = True
            break
        vv = cert(SS[active], T, N, s2)
        n_eval += len(active)
        k = np.argmax(vv)
        if vv[k] > inc:
            inc = float(vv[k])
            SR = SS[active[k]]
    rivals = np.any(SS != SR, axis=1)
    rival_U = float(UU[rivals].max()) if rivals.any() else -np.inf
    return dict(S_hat=SR, L_hat=inc, swap_S=swap_S, swap_L=swap_L, U_star=float(UU.max()), rival_U=rival_U,
                margin=inc - rival_U, unique=bool(inc > rival_U), survivors=int(len(survivors)), n_eval=n_eval,
                capped=capped, exact=not capped, seconds=time.perf_counter() - t0)


def leakage_upper(S, T, N):
    """Ibar(S) = B_P(S)^2 / N (Theorem 1 leakage bound)."""
    if T['eps'] == 0:
        return float(np.abs(T['zP'][np.asarray(S)].sum()) ** 2 / N)
    m = T['s'][np.asarray(S)].sum(0).max()
    B = max(m / np.cos(np.pi / T['K']), 0)
    return float(B * B / N)
