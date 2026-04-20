from typing import Dict

import numpy as np
from scipy.optimize import minimize

import pass_model as pm


def positive_side(delta: np.ndarray) -> np.ndarray:
    half = delta.size // 2
    return delta[half:].copy()


def mirror_symmetric(delta_pos: np.ndarray) -> np.ndarray:
    return np.concatenate([-delta_pos[::-1], delta_pos])


def uniform_aperture_from(delta_ref: np.ndarray) -> np.ndarray:
    delta_pos = positive_side(delta_ref)
    uniform_pos = np.linspace(delta_pos[0], delta_pos[-1], delta_pos.size)
    return mirror_symmetric(uniform_pos)


def _spacing_penalty(delta_pos: np.ndarray, min_spacing: float, weight: float) -> float:
    gaps = np.diff(delta_pos)
    violations = np.maximum(min_spacing - gaps, 0.0)
    return float(weight * np.sum(violations**2))


def optimize_nominal_same_aperture(config, delta_ref: np.ndarray, k0: float, logger=None) -> Dict[str, np.ndarray | float]:
    delta_pos_ref = positive_side(delta_ref)
    min_pos = float(delta_pos_ref[0])
    max_pos = float(delta_pos_ref[-1])
    min_spacing = config.delta_p * (config.c / config.f_c)
    free_dim = delta_pos_ref.size - 2

    if free_dim <= 0:
        delta_opt = delta_ref.copy()
        return {"delta": delta_opt, "gain": pm.array_gain(delta_opt, k0, config.d, config.n_eff, config.eta, None)}

    def unpack(y: np.ndarray) -> np.ndarray:
        z = 1.0 / (1.0 + np.exp(-y))
        delta_pos = np.empty(delta_pos_ref.size, dtype=float)
        delta_pos[0] = min_pos
        delta_pos[-1] = max_pos
        delta_pos[1:-1] = np.sort(min_pos + z * (max_pos - min_pos))
        return delta_pos

    def pack(delta_pos: np.ndarray) -> np.ndarray:
        free = delta_pos[1:-1]
        scaled = (free - min_pos) / np.maximum(max_pos - free, 1e-12)
        return np.log(np.maximum(scaled, 1e-12))

    def objective(y: np.ndarray) -> float:
        delta_pos = unpack(y)
        delta = mirror_symmetric(delta_pos)
        gain = pm.array_gain(delta, k0, config.d, config.n_eff, config.eta, None)
        penalty = _spacing_penalty(delta_pos, min_spacing, config.baselines.penalty_weight)
        return float(-gain + penalty)

    starts = [pack(np.linspace(min_pos, max_pos, delta_pos_ref.size))]
    starts.append(pack(delta_pos_ref))
    rng = np.random.default_rng(config.random_seed)
    for _ in range(config.baselines.optimizer_restarts - 2):
        random_pos = np.sort(rng.uniform(min_pos, max_pos, size=delta_pos_ref.size))
        random_pos[0] = min_pos
        random_pos[-1] = max_pos
        starts.append(pack(random_pos))

    best_gain = -np.inf
    best_delta = delta_ref.copy()
    for start_idx, y0 in enumerate(starts, start=1):
        result = minimize(objective, y0, method="L-BFGS-B", options={"maxiter": 400})
        delta_pos = unpack(result.x)
        gain = pm.array_gain(mirror_symmetric(delta_pos), k0, config.d, config.n_eff, config.eta, None)
        if gain > best_gain and np.all(np.diff(delta_pos) >= min_spacing - 1e-8):
            best_gain = float(gain)
            best_delta = mirror_symmetric(delta_pos)
        if logger is not None:
            logger.info(
                "Nominal optimizer restart %d: success=%s gain=%.6e",
                start_idx,
                result.success,
                gain,
            )

    return {"delta": best_delta, "gain": best_gain}
