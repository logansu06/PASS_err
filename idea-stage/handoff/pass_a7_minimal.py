# Minimal standalone reproduction of the A7 certificate (numpy only).
import itertools, numpy as np
C, FC = 3e8, 28e9; LAM = C / FC; K0 = 2 * np.pi / LAM
D_H, NEFF, XF = 3.0, 1.44, -10.0          # waveguide height, effective index, feed position (m)
TH = np.linspace(-np.pi, np.pi, 1441)[:-1]; DTH = TH[1] - TH[0]

def R(x, ux, uy): return np.sqrt((x - ux) ** 2 + uy ** 2 + D_H ** 2)
def psi(x, ux, uy): return K0 * (R(x, ux, uy) + NEFF * (x - XF))          # strictly increasing if NEFF > 1
def z(x, ux, uy): return np.exp(-1j * psi(x, ux, uy)) / R(x, ux, uy)      # isotropic amplitude 1/R

def aligned_sites(M, center=0.0):                                          # N0: D-aligned consecutive levels
    f = lambda x: np.sqrt(x ** 2 + D_H ** 2) + NEFF * x
    m0 = np.round(f(center) / LAM); out = []
    for t in (m0 + np.arange(-(M // 2), M - M // 2)) * LAM:
        lo, hi = -50.0, 50.0
        for _ in range(200):
            mid = 0.5 * (lo + hi); lo, hi = (mid, hi) if f(mid) < t else (lo, mid)
        out.append(0.5 * (lo + hi))
    return np.array(out)

def amp_range(x, eps, ux, uy):                                              # exact extrema of 1/R on [x-eps, x+eps]
    e = np.stack([1 / R(x - eps, ux, uy), 1 / R(x + eps, ux, uy)])
    amax = np.where((x - eps <= ux) & (ux <= x + eps), 1 / R(ux, ux, uy), e.max(0))
    return e.min(0), amax

def tables(xs, eps, P):
    ux, uy = P
    bD = np.maximum(psi(xs + eps, 0, 0) - psi(xs, 0, 0), psi(xs, 0, 0) - psi(xs - eps, 0, 0))
    cD = amp_range(xs, eps, 0, 0)[0] * np.cos(np.minimum(bD, np.pi / 2))       # Prop. 1 per-site term
    bP = np.maximum(psi(xs + eps, ux, uy) - psi(xs, ux, uy), psi(xs, ux, uy) - psi(xs - eps, ux, uy))
    amin, amax = amp_range(xs, eps, ux, uy); phi0 = -psi(xs, ux, uy)
    gap = np.maximum(np.abs(np.angle(np.exp(1j * (TH[None] - phi0[:, None])))) - bP[:, None], 0)
    mc = np.cos(np.minimum(gap, np.pi))
    s = np.where(mc > 0, amax[:, None] * mc, amin[:, None] * mc)              # Prop. 2 sector support s_n(theta)
    return dict(cD=cD, s=s, amax=amax, valid=bool(np.all(bD <= np.pi / 2)), zD=z(xs, 0, 0), zP=z(xs, ux, uy))

def cert_L(S, T, N, s2):                                                   # certified SLNR lower bound L(S)
    LD = T["cD"][S].sum(-1) ** 2 / N
    Iup = np.maximum(T["s"][S].sum(-2).max(-1) + T["amax"][S].sum(-1) * DTH / 2, 0) ** 2 / N
    return LD / (s2 + Iup)

def nominal(S, T, N, s2):
    return (np.abs(T["zD"][S].sum(-1)) ** 2 / N) / (s2 + np.abs(T["zP"][S].sum(-1)) ** 2 / N)

def exhaustive_nominal(T, M, N, s2):
    allS = np.array(list(itertools.combinations(range(M), N)))
    return allS[np.argmax(nominal(allS, T, N, s2))]

def swap_search(f, M, N, init, rng, restarts=8):
    best, bv = None, -np.inf
    for S in [np.sort(init)] + [np.sort(rng.choice(M, N, replace=False)) for _ in range(restarts)]:
        v = f(S[None])[0]
        while True:
            cand = np.array([np.sort(np.where(np.arange(N) == i, j, S)) for i in range(N) for j in range(M) if j not in S])
            vals = f(cand); k = int(np.argmax(vals))
            if vals[k] <= v + 1e-15: break
            S, v = cand[k], vals[k]
        if v > bv: best, bv = S, v
    return best

def witness_U(xs, S, eps, P, N, s2):                                       # feasible upper bound: all 2^N corners
    x = xs[S]; Cn = np.array(list(itertools.product((-1.0, 1.0), repeat=N))) * eps
    gD = np.abs(z(x[None] + Cn, 0, 0).sum(1)) ** 2 / N; gP = np.abs(z(x[None] + Cn, *P).sum(1)) ** 2 / N
    return (gD / (s2 + gP)).min()

if __name__ == "__main__":
    M, N = 24, 8; xs = aligned_sites(M); A_REF = np.abs(z(xs[8:16], 0, 0).sum()) ** 2 / N
    P, eps, s2 = (3.0, 2.0), 0.05 * LAM, A_REF / 1e3                         # reference SNR 30 dB
    T = tables(xs, eps, P); SN = exhaustive_nominal(T, M, N, s2)
    SR = swap_search(lambda S: cert_L(S, T, N, s2), M, N, SN, np.random.default_rng(0))
    LR, UN = cert_L(SR[None], T, N, s2)[0], witness_U(xs, SN, eps, P, N, s2)
    print("S_nom", SN, "S_rob", SR, "L(S_rob)=%.3f  U(S_nom)=%.3f  certified gain=%+.1f%%" % (LR, UN, 100 * (LR / UN - 1)))
