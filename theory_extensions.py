from typing import Dict

import numpy as np

import robustness


def normalized_weights(delta_star: np.ndarray, d: float) -> np.ndarray:
    r = np.sqrt(d**2 + delta_star**2)
    w = 1.0 / r
    return w / np.sum(w)


def weighted_mean(values: np.ndarray, weights: np.ndarray) -> float:
    return float(np.sum(weights * values))


def split_error_vector(
    epsilon: float,
    xi: np.ndarray,
    weights: np.ndarray,
    delta_star: np.ndarray | None = None,
) -> np.ndarray:
    centered = xi - weighted_mean(xi, weights)
    signs = np.sign(centered)
    if delta_star is not None:
        zero_mask = signs == 0.0
        signs[zero_mask] = np.sign(delta_star[zero_mask])
    signs[signs == 0.0] = 1.0
    return epsilon * signs


def common_bias_vector(epsilon: float, size: int) -> np.ndarray:
    return np.full(size, epsilon, dtype=float)


def phase_variance(
    k0: float,
    xi: np.ndarray,
    delta_err: np.ndarray,
    weights: np.ndarray,
) -> float:
    phase_err = k0 * xi * delta_err
    mean_phase = np.sum(weights * phase_err)
    second_moment = np.sum(weights * phase_err**2)
    return float(second_moment - mean_phase**2)


def quadratic_gain_from_delta(
    k0: float,
    xi: np.ndarray,
    delta_err: np.ndarray,
    weights: np.ndarray,
) -> float:
    return float(np.clip(1.0 - phase_variance(k0, xi, delta_err, weights), 0.0, 1.0))


def quadratic_expected_gain(
    k0: float,
    xi: np.ndarray,
    weights: np.ndarray,
    cov_delta: np.ndarray,
) -> float:
    mixing = np.diag(weights) - np.outer(weights, weights)
    xi_mat = np.diag(xi)
    loss = (k0**2) * np.trace(mixing @ (xi_mat @ cov_delta @ xi_mat))
    return float(np.clip(1.0 - loss, 0.0, 1.0))


def exponential_covariance(size: int, sigma2: float, corr_len: float) -> np.ndarray:
    indices = np.arange(size, dtype=float)
    distance = np.abs(indices[:, None] - indices[None, :])
    return sigma2 * np.exp(-distance / corr_len)


def sample_iid_uniform(
    epsilon: float,
    size: int,
    samples: int,
    rng: np.random.Generator,
) -> np.ndarray:
    return rng.uniform(-epsilon, epsilon, size=(samples, size))


def sample_common_bias(
    epsilon: float,
    size: int,
    samples: int,
    rng: np.random.Generator,
) -> np.ndarray:
    bias = rng.uniform(-epsilon, epsilon, size=(samples, 1))
    return np.repeat(bias, size, axis=1)


def sample_correlated_gaussian(
    sigma2: float,
    corr_len: float,
    size: int,
    samples: int,
    rng: np.random.Generator,
) -> np.ndarray:
    cov = exponential_covariance(size, sigma2, corr_len)
    chol = np.linalg.cholesky(cov + 1e-15 * np.eye(size))
    z = rng.standard_normal(size=(samples, size))
    return z @ chol.T


def scenario_stats(
    delta_batch: np.ndarray,
    delta_star: np.ndarray,
    a_ideal: float,
    k0: float,
    d: float,
    n_eff: float,
    eta: float,
    phi_ref: np.ndarray | None,
) -> Dict[str, float]:
    gains = robustness.array_gain_batch(delta_star[None, :] + delta_batch, k0, d, n_eff, eta, phi_ref=phi_ref) / a_ideal
    return {
        "mean": float(np.mean(gains)),
        "p05": float(np.percentile(gains, 5)),
        "p50": float(np.percentile(gains, 50)),
        "p95": float(np.percentile(gains, 95)),
    }
