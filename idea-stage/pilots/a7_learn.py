"""Pilot A7 learning gate: amortized site-inclusion MLP + certificate verification."""
import time
import numpy as np
from a7_pilot import aligned_sites, site_tables, cert_slnr, local_search, LAM

M, N = 24, 8
XS = aligned_sites(M, 0.0)


def sample_geoms(n, rng):
    return np.column_stack([rng.uniform(-6, 6, n), rng.uniform(0.5, 5.0, n),
                            rng.uniform(0.02, 0.06, n), rng.uniform(-3, -2, n)])  # xP, yP, eps/lam, log10 sigma2


def robust_ref(g, rng, restarts):
    T = site_tables(XS, g[2] * LAM, (g[0], g[1])); s2 = 10 ** g[3]
    f = lambda S: cert_slnr(S, T, N, s2)[0]
    S, v = local_search(f, M, N, rng, restarts=restarts)
    return S, v, T, s2


def feats(G):
    return np.column_stack([G[:, 0] / 6, (G[:, 1] - 2.75) / 2.25, (G[:, 2] - 0.04) / 0.02, G[:, 3] + 2.5,
                            np.sin(G[:, 0]), np.cos(G[:, 0]), G[:, 0] / np.sqrt(G[:, 0] ** 2 + G[:, 1] ** 2 + 9)])


class MLP:
    def __init__(self, din, dh, dout, rng):
        self.W = [rng.normal(0, np.sqrt(2 / din), (din, dh)), rng.normal(0, np.sqrt(2 / dh), (dh, dh)),
                  rng.normal(0, np.sqrt(1 / dh), (dh, dout))]
        self.b = [np.zeros(dh), np.zeros(dh), np.zeros(dout)]
        self.m = [np.zeros_like(p) for p in self.W + self.b]; self.v = [np.zeros_like(p) for p in self.W + self.b]; self.t = 0

    def fwd(self, X):
        h1 = np.maximum(X @ self.W[0] + self.b[0], 0); h2 = np.maximum(h1 @ self.W[1] + self.b[1], 0)
        return h1, h2, h2 @ self.W[2] + self.b[2]

    def step(self, X, Y, lr=3e-3):
        h1, h2, lo = self.fwd(X); p = 1 / (1 + np.exp(-lo)); gl = (p - Y) / len(X)
        gW2 = h2.T @ gl; gb2 = gl.sum(0); gh2 = gl @ self.W[2].T * (h2 > 0)
        gW1 = h1.T @ gh2; gb1 = gh2.sum(0); gh1 = gh2 @ self.W[1].T * (h1 > 0)
        gW0 = X.T @ gh1; gb0 = gh1.sum(0)
        grads = [gW0, gW1, gW2, gb0, gb1, gb2]; params = self.W + self.b; self.t += 1
        for i, (pa, gr) in enumerate(zip(params, grads)):
            self.m[i] = 0.9 * self.m[i] + 0.1 * gr; self.v[i] = 0.999 * self.v[i] + 0.001 * gr ** 2
            mh = self.m[i] / (1 - 0.9 ** self.t); vh = self.v[i] / (1 - 0.999 ** self.t)
            pa -= lr * mh / (np.sqrt(vh) + 1e-8)
        return -np.mean(Y * np.log(p + 1e-12) + (1 - Y) * np.log(1 - p + 1e-12))


def candidates_from_scores(sc, K):
    """Top-N plus single swaps (lowest included <-> highest excluded) -> K candidate subsets."""
    order = np.argsort(-sc); top = np.sort(order[:N]); cands = [top]
    inc = order[:N][::-1]; exc = order[N:]
    for i in inc[:4]:
        for j in exc[:max(1, K // 4)]:
            S = top.copy(); S[S == i] = j; cands.append(np.sort(S))
    return np.unique(np.array(cands), axis=0)[:K]


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    t0 = time.time(); Gtr = sample_geoms(2500, rng); Ytr = np.zeros((len(Gtr), M))
    for k, g in enumerate(Gtr):
        S, _, _, _ = robust_ref(g, rng, restarts=3); Ytr[k, S] = 1
    print(f"labels: {len(Gtr)} geometries in {time.time()-t0:.0f}s")
    net = MLP(7, 128, M, rng); X = feats(Gtr)
    for ep in range(4000):
        idx = rng.choice(len(X), 256); loss = net.step(X[idx], Ytr[idx])
    print(f"train BCE {loss:.3f}")
    Gte = sample_geoms(300, np.random.default_rng(99)); ratios = []; t_ref = t_learn = 0.0; fallback = 0
    for g in Gte:
        t = time.perf_counter(); S_ref, v_ref, T, s2 = robust_ref(g, rng, restarts=8); t_ref += time.perf_counter() - t
        t = time.perf_counter()
        sc = net.fwd(feats(g[None, :]))[2][0]; C = candidates_from_scores(sc, 16)
        vals = cert_slnr(C, T, N, s2)[0]; v_l = vals.max()
        t_learn += time.perf_counter() - t
        ratios.append(v_l / v_ref)
    r = np.array(ratios)
    print(f"held-out 300: median ratio {np.median(r):.3f}, >=0.95 in {np.mean(r>=0.95):.0%}, >=0.99 in {np.mean(r>=0.99):.0%}; "
          f"runtime ref {1e3*t_ref/300:.1f} ms vs learned+verify {1e3*t_learn/300:.2f} ms (x{t_ref/t_learn:.0f})")
