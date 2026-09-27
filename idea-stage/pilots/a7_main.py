"""Frozen main driver for the A7 paper (certified robust-SLNR site selection).
Per case: exhaustive nominal optimum S_N; robust S_R = swap search on certified L(S), started from S_N (+8 random);
feasible witnesses U(.) from all 2^N corners + split + continuous L-BFGS-B refinement; saves everything to CSV."""
import csv, itertools, sys, time
import numpy as np
from scipy.optimize import minimize
from a7_pilot import (aligned_sites, site_tables, cert_slnr, nominal_slnr, local_search, exhaustive_nominal,
                      z, R, LAM, K0, NEFF, TH, DTH)

M, N = 24, 8
GEOMS = [(xp, yp) for yp in (1.0, 2.0, 4.0) for xp in np.linspace(-6, 6, 11)]
EPS = (0.0, 0.01, 0.03, 0.05, 0.08)
SNR_DB = (10, 20, 30, 40)
XS = aligned_sites(M, 0.0)
D_MIN = 0.5 * LAM  # hardware minimum spacing; robust clearance requires spacing >= D_MIN + 2*eps
# fixed physical noise: reference = coherent gain of the central N-site block toward D
A_REF = np.abs(z(XS[(M - N) // 2:(M + N) // 2], 0, 0).sum()) ** 2 / N
CORNERS = np.array(list(itertools.product((-1.0, 1.0), repeat=N)))


def slnr_parts(x, dl, P):
    xx = x[None, :] + dl
    gD = np.abs(z(xx, 0, 0).sum(1)) ** 2 / N
    gP = np.abs(z(xx, P[0], P[1]).sum(1)) ** 2 / N
    return gD, gP


def witness(S, eps, P, s2):
    """Upper bound on worst-case SLNR: all corners, then continuous refinement from the 3 worst corners."""
    x = XS[S]
    if eps == 0:
        gD, gP = slnr_parts(x, np.zeros((1, N)), P); return gD[0] / (s2 + gP[0]), gD[0], gP[0], np.zeros(N)
    gD, gP = slnr_parts(x, eps * CORNERS, P); v = gD / (s2 + gP)
    best = int(np.argmin(v)); bv, bd = v[best], eps * CORNERS[best]
    f = lambda d: (lambda a, b: a[0] / (s2 + b[0]))(*slnr_parts(x, d[None, :], P))
    for k in np.argsort(v)[:3]:
        r = minimize(f, eps * CORNERS[k], method="L-BFGS-B", bounds=[(-eps, eps)] * N, options=dict(maxiter=60))
        if r.fun < bv:
            bv, bd = r.fun, r.x
    gD, gP = slnr_parts(x, bd[None, :], P)
    return bv, gD[0], gP[0], bd


def directional_radius(S, eps, P):
    x = XS[S]; b = (z(x + 1e-8, *P) - z(x - 1e-8, *P)) / 2e-8
    T = eps * np.max(np.abs(np.real(np.exp(-1j * TH)[:, None] * b[None, :])).sum(1))
    return T, np.sum(eps ** 2 * np.abs(b) ** 2) / N


def cert(S, T, s2, eps):
    if eps == 0:  # special case: exact nominal, no angular pad
        return nominal_slnr(S[None, :], T, N, s2)[0], None, None
    v, LD, Iup = cert_slnr(S[None, :], T, N, s2); return v[0], LD[0], Iup[0]


if __name__ == "__main__":
    out_path = sys.argv[1] if len(sys.argv) > 1 else "a7_main_results.csv"
    rng = np.random.default_rng(2026); rows = []; t0 = time.time()
    for ctrl, fixed in (("common", ()), ("endpoints", (0, M - 1))):
        for snr in SNR_DB:
            s2 = A_REF / 10 ** (snr / 10)
            for eps_l in EPS:
                eps = eps_l * LAM
                assert np.min(np.diff(XS)) >= D_MIN + 2 * eps, "robust clearance violated for this eps"
                for P in GEOMS:
                    T = site_tables(XS, eps, P)
                    if not T["valid"]:
                        continue
                    SN, _ = exhaustive_nominal(T, M, N, s2, fixed=fixed)
                    if eps == 0:
                        SR = SN
                    else:
                        SR, _ = local_search(lambda S: cert_slnr(S, T, N, s2)[0], M, N, rng, restarts=8, fixed=fixed, inits=[SN])
                    L_R, LD_R, I_R = cert(SR, T, s2, eps); L_N, _, _ = cert(SN, T, s2, eps)
                    U_R, gD_R, gP_R, w_R = witness(SR, eps, P, s2); U_N, gD_N, gP_N, w_N = witness(SN, eps, P, s2)
                    T_R, kb_R = directional_radius(SR, eps, P); T_N, kb_N = directional_radius(SN, eps, P)
                    rows.append(dict(control=ctrl, snr_db=snr, sigma2=s2, eps_over_lambda=eps_l, xP=P[0], yP=P[1],
                                     S_nom=" ".join(map(str, SN)), S_rob=" ".join(map(str, SR)),
                                     L_rob=L_R, U_rob=U_R, L_nom=L_N, U_nom=U_N,
                                     cert_gain=L_R / U_N - 1, bracket_rob=U_R / L_R,
                                     a_LD_rob=LD_R, b_Iup_rob=I_R, c_gD_nom_wit=gD_N, d_gP_nom_wit=gP_N,
                                     gD_rob_wit=gD_R, gP_rob_wit=gP_R, T_rob=T_R, T_nom=T_N,
                                     kappa_b_nom=kb_N / s2, kappa_b_rob=kb_R / s2,
                                     witness_rob_over_eps=" ".join(f"{v:.4f}" for v in (w_R / eps if eps else w_R)),
                                     witness_nom_over_eps=" ".join(f"{v:.4f}" for v in (w_N / eps if eps else w_N))))
        print(f"{ctrl} done, {len(rows)} rows, {time.time()-t0:.0f}s", flush=True)
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print("saved", out_path)
