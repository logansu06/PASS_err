"""Pilot A2: power-probe calibration of pinching-position errors with learned vs fixed modes.
Exact-model received power; symmetric dithers; LS in the C1 quadratic model; re-pinching with fresh jitter."""
import numpy as np
from pass_lab import PASS

S = PASS(N=16); X0 = S.aligned(0.0); N = X0.size; LAM = S.lam
g0 = S.gain(X0)
a = 1 / S.R(X0); al = a / a.sum(); xi = S.xi(X0)
Q = S.k0 ** 2 * np.diag(xi) @ (np.diag(al) - np.outer(al, al)) @ np.diag(xi)


def gain_norm(dl):
    return S.gain(X0 + dl) / g0


def dct_modes(r):
    n = np.arange(N); B = np.stack([np.cos(np.pi * (n + 0.5) * k / N) for k in range(1, r + 1)], 1)
    return B / np.linalg.norm(B, axis=0)


def smooth_random_modes(r, rng, L=4.0):
    idx = np.arange(N); K = np.exp(-np.abs(idx[:, None] - idx[None, :]) / L)
    B = np.linalg.cholesky(K + 1e-9 * np.eye(N)) @ rng.normal(size=(N, r))
    B, _ = np.linalg.qr(B); return B


def draw_errors(Btrue, n, eps, rng, resid=0.1):
    Z = rng.uniform(-1, 1, (n, Btrue.shape[1]))
    D = Z @ Btrue.T
    D = D / np.max(np.abs(D), axis=1, keepdims=True) * eps * rng.uniform(0.6, 1.0, (n, 1))
    return D + resid * eps * rng.uniform(-1, 1, D.shape)


def calibrate(delta, Bhat, dither, noise, jitter, rng, reps=1):
    """Probe along columns of Bhat (+/-), LS for coefficients, re-pinch; returns gain after, #measurements."""
    U = dither * Bhat / np.max(np.abs(Bhat), axis=0, keepdims=True)  # probe directions (per-column max = dither)
    y = []
    for k in range(U.shape[1]):
        m = lambda d: np.mean(gain_norm(d) + noise * rng.normal(size=reps))
        y.append(m(delta - U[:, k]) - m(delta + U[:, k]))
    A = 4 * U.T @ Q @ Bhat
    zhat = np.linalg.lstsq(A, np.array(y), rcond=None)[0]
    corr = -Bhat @ zhat
    after = delta + corr + jitter * rng.uniform(-1, 1, N)
    return gain_norm(after), 2 * U.shape[1] * reps


if __name__ == "__main__":
    rng = np.random.default_rng(3); eps = 0.05 * LAM; dither = 0.01 * LAM; jitter = 0.005 * LAM
    r_true = 3
    scen = {}
    Bdev = smooth_random_modes(r_true, rng)                  # device-specific stable modes
    scen["smooth-DCT modes"] = (dct_modes(r_true), dct_modes(r_true))
    scen["stable device modes"] = (Bdev, Bdev)
    scen["modes changed"] = (Bdev, smooth_random_modes(r_true, np.random.default_rng(77)))
    for noise in [0.002, 0.01]:
        print(f"--- power noise {noise} (x nominal), dither {dither/LAM:.3f}λ, re-pinch jitter {jitter/LAM:.3f}λ, eps {eps/LAM}λ")
        for name, (Btrain, Btest) in scen.items():
            hist = draw_errors(Btrain, 300, eps, rng)
            U_, s_, Vt = np.linalg.svd(hist - hist.mean(0), full_matrices=False)
            tests = draw_errors(Btest, 200, eps, rng)
            res = {}
            for label, B, in [("before", None), ("learned PCA r=3", Vt[:3].T), ("learned PCA r=6", Vt[:6].T),
                              ("DCT r=3", dct_modes(3)), ("DCT r=6", dct_modes(6)),
                              ("random r=6", np.linalg.qr(rng.normal(size=(N, 6)))[0]),
                              ("coordinatewise r=16", np.eye(N))]:
                if B is None:
                    res[label] = (np.mean([gain_norm(d) for d in tests]), 0); continue
                out = [calibrate(d, B, dither, noise, jitter, rng) for d in tests]
                res[label] = (np.mean([o[0] for o in out]), out[0][1])
            print(f"  {name:22s} " + " | ".join(f"{k}: {v[0]:.4f} ({v[1]} meas)" for k, v in res.items()))
