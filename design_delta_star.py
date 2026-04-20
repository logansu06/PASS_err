from typing import Dict, Tuple, Optional

import numpy as np
from scipy.optimize import brentq

import pass_model as pm


def _solve_delta_for_dn(
    d: float,
    n_eff: float,
    d_target: float,
    lam: float,
    init_guess: float,
    logger,
) -> Tuple[float, int, float]:
    """
    Solve f(Delta)=0 where f(Delta)=sqrt(d^2+Delta^2)+n_eff*Delta-d_target.
    Returns (root, expansions, hi_used).
    """
    def f(x: float) -> float:
        return np.sqrt(d ** 2 + x ** 2) + n_eff * x - d_target

    hi = max(init_guess, 1e-9) + lam
    expansions = 0
    max_hi = 1e4 * lam
    while f(hi) <= 0.0 and hi < max_hi:
        hi *= 2.0
        expansions += 1
    if f(hi) <= 0.0:
        raise RuntimeError(
            f"Root bracket failed: d_target={d_target:.6e}, init={init_guess:.6e}, hi={hi:.6e}, f(hi)={f(hi):.3e}"
        )
    root = brentq(f, 0.0, hi, maxiter=200, xtol=1e-12, rtol=1e-10)
    if logger:
        logger.info(
            "Solved delta*: d_target=%.6e, root=%.6e, hi=%.6e, expansions=%d, f(root)=%.3e",
            d_target,
            root,
            hi,
            expansions,
            f(root),
        )
    return float(root), expansions, hi


def design_delta_star(config, logger=None) -> Dict[str, np.ndarray]:
    """Generate Delta* following the steps in fyp.pdf 3.2–3.3."""
    lam = pm.wavelength(config.c, config.f_c)
    k0 = pm.k0_from_lambda(lam)
    indices = pm.build_indices(config.N)
    half = config.N // 2
    delta_p_m = config.delta_p * lam

    delta_pos_init = delta_p_m / 2 + np.arange(half) * delta_p_m
    delta_pos = np.zeros(half, dtype=float)

    for i in range(half):
        delta0 = delta_pos_init[i]
        L0 = np.sqrt(config.d ** 2 + delta0 ** 2) + config.n_eff * delta0
        d_target = lam * np.ceil(L0 / lam)
        delta_i, expansions, hi = _solve_delta_for_dn(
            d=config.d,
            n_eff=config.n_eff,
            d_target=d_target,
            lam=lam,
            init_guess=delta0,
            logger=logger,
        )
        if i > 0:
            prev = delta_pos[i - 1]
            while delta_i - prev < delta_p_m - 1e-12:
                d_target += lam
                delta_i, expansions, hi = _solve_delta_for_dn(
                    d=config.d,
                    n_eff=config.n_eff,
                    d_target=d_target,
                    lam=lam,
                    init_guess=delta0,
                    logger=logger,
                )
                if logger:
                    logger.info(
                        "Adjusted d_target upward to enforce spacing: new d_target=%.6e, delta=%.6e",
                        d_target,
                        delta_i,
                    )
        delta_pos[i] = delta_i

    if not np.all(np.diff(delta_pos) > 0):
        if logger:
            logger.warning("Delta* positive side is not strictly increasing.")

    min_spacing = np.min(np.diff(delta_pos)) if half > 1 else delta_pos[0]
    if logger:
        logger.info(
            "Delta* spacing check: min_spacing=%.6e, required=%.6e",
            min_spacing,
            delta_p_m,
        )

    delta_star = np.concatenate([-delta_pos[::-1], delta_pos])
    xi = pm.xi_from_delta(delta_star, config.d, config.n_eff)
    phi_ref = pm.phase(k0, config.d, config.n_eff, delta_star)
    a_ideal = pm.compute_a_ideal(delta_star, k0, config.d, config.n_eff, config.eta)
    a_norm_check = pm.array_gain(delta_star, k0, config.d, config.n_eff, config.eta, phi_ref=phi_ref) / a_ideal
    if logger:
        logger.info("a_norm at Delta*: %.6e (should be ~1)", a_norm_check)

    return {
        "indices": indices,
        "delta_star": delta_star,
        "lambda_m": lam,
        "k0": k0,
        "xi": xi,
        "a_ideal": a_ideal,
        "a_norm_check": a_norm_check,
        "delta_p_m": delta_p_m,
        "phi_ref": phi_ref,
    }
