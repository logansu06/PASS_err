"""Reusable PASS pilot model: aligned design, attenuation/directivity, certificate, adversaries.

Geometry follows src/pass_model.py (user at x_u=0, waveguide at height d, feed at x_feed<0).
Received phasor of PA n: A_n * exp(-j k0 (R_n + n_eff (x_n - x_feed))) with
A_n = exp(-alpha (x_n - x_feed)) * pattern(theta_n) / R_n  (alpha in Np/m, power split equal).
"""
import itertools
import numpy as np
from scipy.optimize import brentq

C = 3e8


class PASS:
    def __init__(self, fc=28e9, d=3.0, n_eff=1.44, N=16, alpha_db_per_m=0.0, x_feed=-10.0, q=0.0):
        self.lam = C / fc
        self.k0 = 2 * np.pi / self.lam
        self.d, self.n, self.N = d, n_eff, N
        self.alpha = alpha_db_per_m * np.log(10) / 20.0  # amplitude Np/m
        self.x_feed, self.q = x_feed, q  # q: directional pattern cos(theta)^q about broadside

    # ---- geometry / channel -------------------------------------------------
    def R(self, x):
        return np.sqrt(self.d ** 2 + x ** 2)

    def phase(self, x):
        return self.k0 * (self.R(x) + self.n * (x - self.x_feed))

    def amp(self, x):
        cos_t = self.d / self.R(x)
        return np.exp(-self.alpha * (x - self.x_feed)) * cos_t ** self.q / self.R(x)

    def gain(self, x):
        """Raw array gain (eta=1) for positions x (..., N)."""
        s = np.sum(self.amp(x) * np.exp(-1j * self.phase(x)), axis=-1)
        return np.abs(s) ** 2 / self.N

    def xi(self, x):
        return self.n + x / self.R(x)

    # ---- aligned design (N0) -----------------------------------------------
    def aligned(self, center=0.0, levels=None):
        """N PAs on consecutive wavelength levels of R(x)+n x around `center`; unique root since xi>0."""
        f0 = lambda x: self.R(x) + self.n * x
        if levels is None:
            m0 = np.round(f0(center) / self.lam)
            levels = (m0 + np.arange(-(self.N // 2), self.N - self.N // 2)) * self.lam
        return np.array([brentq(lambda x, t=t: f0(x) - t, -1e3, 1e3, xtol=1e-14) for t in levels])

    # ---- certificate (N1) -----------------------------------------------------
    def certificate(self, x, eps):
        """Exact lower bound on min_{|delta|<=eps} gain(x+delta) (raw), valid if all beta<=pi/2.
        beta_n = max(|Phi(x+eps)-Phi(x)|, |Phi(x)-Phi(x-eps)|) (monotone phase), amp lower bound over the box."""
        ph = self.phase
        beta = np.maximum(ph(x + eps) - ph(x), ph(x) - ph(x - eps))
        a_min = self.amp_min(x, eps)
        if np.any(beta > np.pi / 2):
            return np.nan
        # nominal phases must be aligned (common mod 2pi); check
        res = np.angle(np.exp(1j * (ph(x) - ph(x)[0])))
        assert np.max(np.abs(res)) < 1e-6, "certificate requires an aligned design"
        return (np.sum(a_min * np.cos(beta))) ** 2 / self.N

    def amp_min(self, x, eps):
        """Exact min of amp over [x-eps, x+eps]: endpoints plus stationary points of
        log amp = -alpha x - (q+1)/2 log(d^2+x^2), i.e. roots of alpha x^2 + (q+1) x + alpha d^2 = 0."""
        cands = [x - eps, x + eps]
        if self.alpha > 0:
            disc = (self.q + 1) ** 2 - 4 * self.alpha ** 2 * self.d ** 2
            if disc >= 0:
                for r in [(-(self.q + 1) + np.sqrt(disc)) / (2 * self.alpha),
                          (-(self.q + 1) - np.sqrt(disc)) / (2 * self.alpha)]:
                    inside = np.abs(r - x) <= eps
                    cands.append(np.where(inside, r, x - eps))
        else:
            inside = np.abs(x) <= eps  # stationary point x=0 (a maximum when alpha=0)
            cands.append(np.where(inside, 0.0, x - eps))
        return np.min(np.stack([self.amp(c) for c in cands]), axis=0)

    def split(self, x, eps):
        a = self.amp(x); w = a / a.sum(); xi = self.xi(x)
        s = np.sign(xi - np.sum(w * xi)); s[s == 0] = 1
        return self.gain(x + eps * s), s

    def corner_min(self, x, eps, chunk=1 << 14):
        best = np.inf
        N = x.size
        for start in range(0, 1 << N, chunk):
            idx = np.arange(start, min(start + chunk, 1 << N))
            S = ((idx[:, None] >> np.arange(N)[None, :]) & 1) * 2.0 - 1.0
            best = min(best, self.gain(x[None, :] + eps * S).min())
        return best

    def mc(self, x, eps, samples=2000, rng=None, law="iid"):
        rng = rng or np.random.default_rng(0)
        if law == "iid":
            D = rng.uniform(-eps, eps, (samples, x.size))
        elif law == "common":
            D = np.repeat(rng.uniform(-eps, eps, (samples, 1)), x.size, axis=1)
        else:
            raise ValueError(law)
        g = self.gain(x[None, :] + D)
        return g.mean(), np.quantile(g, 0.05)
