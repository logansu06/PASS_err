"""Archived driver: certified robust-vs-nominal SLNR gain vs fragility-to-noise ratio kappa.
kappa = (sum_n eps^2 |b_n|^2 / N) / sigma2 on the nominal subset (b_n = d z_P / d x at site n),
i.e. the first-order random-sign expected leakage floor over noise. Outputs a7_kappa_results.csv."""
import csv
import numpy as np
from a7_pilot import aligned_sites, site_tables, cert_slnr, nominal_slnr, local_search, adv_upper, z, LAM

M, N = 24, 8
if __name__ == "__main__":
    rng = np.random.default_rng(7); xs = aligned_sites(M, 0.0); out = []
    for s2 in [1e-4, 1e-3, 1e-2, 1e-1]:
        for e in [0.01, 0.03, 0.05, 0.08]:
            for yp in [1.0, 2.0, 4.0]:
                for xp in np.linspace(-6, 6, 11):
                    P = (xp, yp); eps = e * LAM; T = site_tables(xs, eps, P)
                    if not T["valid"]:
                        continue
                    Sn, _ = local_search(lambda S: nominal_slnr(S, T, N, s2), M, N, rng, restarts=4)
                    Sr, _ = local_search(lambda S: cert_slnr(S, T, N, s2)[0], M, N, rng, restarts=4)
                    x = xs[Sn]; b = (z(x + 1e-7, xp, yp) - z(x - 1e-7, xp, yp)) / 2e-7
                    kappa = np.sum(eps ** 2 * np.abs(b) ** 2) / N / s2
                    L_rob = cert_slnr(Sr[None, :], T, N, s2)[0][0]
                    U_nom = adv_upper(Sn, xs, eps, P, N, s2, rng, n_rand=128)
                    out.append(dict(sigma2=s2, eps_over_lambda=e, xP=xp, yP=yp, kappa=kappa, L_rob=L_rob, U_nom=U_nom,
                                    cert_gain=L_rob / U_nom - 1, S_nom=" ".join(map(str, Sn)), S_rob=" ".join(map(str, Sr))))
    with open("a7_kappa_results.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
    k = np.log10([r["kappa"] for r in out]); g = np.array([r["cert_gain"] for r in out])
    for lo, hi in zip([-9, -2, -1, 0, 1, 2], [-2, -1, 0, 1, 2, 9]):
        m = (k >= lo) & (k < hi)
        if m.sum():
            print(f"log10 kappa [{lo},{hi}): n={m.sum()} median {np.median(g[m]):+.3f} frac>5% {np.mean(g[m] > .05):.0%}")
