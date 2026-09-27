from typing import Dict, Tuple

import numpy as np
from scipy.optimize import minimize

import pass_model as pm
from utils import detect_reorder


def array_gain_batch(
    delta_batch: np.ndarray,
    k0: float,
    d: float,
    n_eff: float,
    eta: float,
    phi_ref: np.ndarray | None = None,
) -> np.ndarray:
    """
    Compute array gain for a batch of Delta arrays.
    delta_batch: shape (B, N)
    Returns: shape (B,)
    """
    r = np.sqrt(d ** 2 + delta_batch ** 2)
    w = 1.0 / r
    phi = k0 * (r + n_eff * delta_batch)
    if phi_ref is not None:
        phi = phi - phi_ref
    s = np.sum(w * np.exp(-1j * phi), axis=1, dtype=np.complex128)
    N = delta_batch.shape[1]
    gains = (eta / N) * np.abs(s) ** 2
    return gains.real


def detect_reorder_batch(delta_batch: np.ndarray) -> bool:
    diffs = np.diff(delta_batch, axis=1)
    return np.any(diffs <= 0)


def monte_carlo_stats(
    epsilon: float,
    delta_star: np.ndarray,
    a_ideal: float,
    k0: float,
    d: float,
    n_eff: float,
    eta: float,
    M: int,
    rng: np.random.Generator,
    phi_ref: np.ndarray | None,
) -> Tuple[Dict[str, float], bool]:
    N = delta_star.size
    deltas = rng.uniform(-epsilon, epsilon, size=(M, N))
    delta_total = delta_star + deltas
    gains = array_gain_batch(delta_total, k0, d, n_eff, eta, phi_ref=phi_ref) / a_ideal
    stats = {
        "mean": float(np.mean(gains)),
        "p05": float(np.percentile(gains, 5)),
        "p50": float(np.percentile(gains, 50)),
        "p95": float(np.percentile(gains, 95)),
    }
    reorder_flag = detect_reorder_batch(delta_total)
    return stats, reorder_flag


def _enumerate_corners(
    epsilon: float,
    delta_star: np.ndarray,
    a_ideal: float,
    k0: float,
    d: float,
    n_eff: float,
    eta: float,
    logger,
    phi_ref: np.ndarray | None,
) -> Tuple[float, np.ndarray, bool]:
    N = delta_star.size
    total = 1 << N
    batch = 1 << 14  # 16384
    best_val = np.inf
    best_delta = None
    reorder_flag = False
    shifts = np.arange(N, dtype=np.uint64)
    for start in range(0, total, batch):
        end = min(start + batch, total)
        ids = np.arange(start, end, dtype=np.uint64)
        bits = ((ids[:, None] >> shifts) & 1).astype(np.int8)
        delta = np.where(bits == 0, -epsilon, epsilon)
        delta_total = delta_star + delta
        vals = array_gain_batch(delta_total, k0, d, n_eff, eta, phi_ref=phi_ref) / a_ideal
        idx = np.argmin(vals)
        if vals[idx] < best_val:
            best_val = float(vals[idx])
            best_delta = delta[idx].copy()
        reorder_flag = reorder_flag or detect_reorder_batch(delta_total)
    if logger is not None:
        logger.info("Corner enumeration completed: checked=%d", total)
    return best_val, best_delta, reorder_flag


def _coord_descent(
    epsilon: float,
    delta_star: np.ndarray,
    a_ideal: float,
    k0: float,
    d: float,
    n_eff: float,
    eta: float,
    config,
    rng: np.random.Generator,
    logger,
    phi_ref: np.ndarray | None,
) -> Tuple[float, np.ndarray, bool]:
    N = delta_star.size
    grid = np.linspace(-epsilon, epsilon, config.worst_case.coord_grid_K)
    best_val = np.inf
    best_delta = None
    reorder_flag = False

    for r_idx in range(config.worst_case.coord_restarts):
        delta = rng.uniform(-epsilon, epsilon, size=N)
        prev = np.inf
        for it in range(config.worst_case.coord_max_iter):
            for i in range(N):
                candidates = np.repeat(delta[None, :], grid.size, axis=0)
                candidates[:, i] = grid
                vals = array_gain_batch(delta_star + candidates, k0, d, n_eff, eta, phi_ref=phi_ref) / a_ideal
                best_idx = int(np.argmin(vals))
                delta[i] = grid[best_idx]
            val = array_gain_batch(delta_star + delta[None, :], k0, d, n_eff, eta, phi_ref=phi_ref)[0] / a_ideal
            if prev - val < config.worst_case.coord_tol:
                break
            prev = val
        if val < best_val:
            best_val = float(val)
            best_delta = delta.copy()
        reorder_flag = reorder_flag or detect_reorder(delta_star + delta)
        if logger is not None:
            logger.info(
                "Coord descent restart %d: val=%.6e, iters=%d",
                r_idx + 1,
                val,
                it + 1,
            )
    return best_val, best_delta, reorder_flag


def _local_search(
    epsilon: float,
    delta_star: np.ndarray,
    a_ideal: float,
    k0: float,
    d: float,
    n_eff: float,
    eta: float,
    config,
    rng: np.random.Generator,
    phi_ref: np.ndarray | None,
    starts: list[np.ndarray],
) -> Tuple[float, np.ndarray]:
    bounds = [(-epsilon, epsilon)] * delta_star.size
    best_val = np.inf
    best_delta = np.zeros_like(delta_star)

    def objective(delta_err: np.ndarray) -> float:
        return float(pm.array_gain(delta_star + delta_err, k0, d, n_eff, eta, phi_ref=phi_ref) / a_ideal)

    run_starts = [np.clip(np.asarray(s, dtype=float), -epsilon, epsilon) for s in starts]
    for _ in range(config.box_search.local_restarts):
        run_starts.append(rng.uniform(-epsilon, epsilon, size=delta_star.size))

    for start in run_starts:
        result = minimize(
            objective,
            start,
            method="L-BFGS-B",
            bounds=bounds,
            options={"maxiter": config.box_search.local_max_iter},
        )
        cand_delta = np.clip(result.x, -epsilon, epsilon) if result.success else start
        cand_val = objective(cand_delta)
        if cand_val < best_val:
            best_val = cand_val
            best_delta = cand_delta.copy()

    return best_val, best_delta


def corner_worst_case_gain(
    epsilon: float,
    delta_star: np.ndarray,
    a_ideal: float,
    k0: float,
    d: float,
    n_eff: float,
    eta: float,
    logger,
    phi_ref: np.ndarray | None,
) -> Tuple[float, np.ndarray, bool]:
    return _enumerate_corners(
        epsilon,
        delta_star,
        a_ideal,
        k0,
        d,
        n_eff,
        eta,
        logger,
        phi_ref,
    )


def worst_case_gain(
    epsilon: float,
    delta_star: np.ndarray,
    a_ideal: float,
    k0: float,
    d: float,
    n_eff: float,
    eta: float,
    config,
    rng: np.random.Generator,
    logger,
    phi_ref: np.ndarray | None,
    extra_starts: list[np.ndarray] | None = None,
) -> Tuple[float, np.ndarray, str, bool]:
    N = delta_star.size
    if N <= config.worst_case.enum_threshold_N:
        wc_norm, delta_wc, reorder_flag = _enumerate_corners(
            epsilon, delta_star, a_ideal, k0, d, n_eff, eta, logger, phi_ref
        )
        method_used = "enum"
    else:
        wc_norm, delta_wc, reorder_flag = _coord_descent(
            epsilon, delta_star, a_ideal, k0, d, n_eff, eta, config, rng, logger, phi_ref
        )
        method_used = "coord"

    starts = [delta_wc]
    if extra_starts:
        starts.extend(extra_starts)
    local_val, local_delta = _local_search(
        epsilon,
        delta_star,
        a_ideal,
        k0,
        d,
        n_eff,
        eta,
        config,
        rng,
        phi_ref,
        starts,
    )
    local_reorder = detect_reorder(delta_star + local_delta)
    if local_val < wc_norm:
        wc_norm = local_val
        delta_wc = local_delta
        method_used += "+local"
        reorder_flag = reorder_flag or local_reorder

    return wc_norm, delta_wc, method_used, reorder_flag


def delta_test_vector(epsilon: float, xi: np.ndarray) -> np.ndarray:
    signs = np.sign(xi)
    signs[signs == 0] = 1.0
    return epsilon * signs


def lower_bounds(
    epsilon: float,
    delta_star: np.ndarray,
    xi: np.ndarray,
    a_ideal: float,
    k0: float,
    d: float,
    n_eff: float,
    eta: float,
) -> Dict[str, float]:
    w_minus = 1.0 / np.sqrt(d ** 2 + (np.abs(delta_star) + epsilon) ** 2)
    lb_full = (eta / delta_star.size) * (np.sum(w_minus * np.cos(k0 * np.abs(xi) * epsilon))) ** 2
    xi_max = np.max(np.abs(xi))
    lb_simpl = np.cos(k0 * xi_max * epsilon) ** 2
    return {
        "lb_full": float(lb_full),
        "lb_full_norm": float(lb_full / a_ideal),
        "lb_simpl_norm": float(lb_simpl),
        "xi_max": float(xi_max),
    }
