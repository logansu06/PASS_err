import numpy as np


def build_indices(N: int) -> np.ndarray:
    if N % 2 != 0:
        raise ValueError("N must be even.")
    half = N // 2
    negative = np.arange(-half, 0, dtype=int)
    positive = np.arange(1, half + 1, dtype=int)
    return np.concatenate([negative, positive])


def wavelength(c: float, f_c: float) -> float:
    return c / f_c


def k0_from_lambda(lam: float) -> float:
    return 2.0 * np.pi / lam


def distance(d: float, delta: np.ndarray) -> np.ndarray:
    return np.sqrt(d ** 2 + delta ** 2)


def phase(k0: float, d: float, n_eff: float, delta: np.ndarray) -> np.ndarray:
    r = distance(d, delta)
    return k0 * (r + n_eff * delta)


def weights(d: float, delta: np.ndarray) -> np.ndarray:
    r = distance(d, delta)
    return 1.0 / r


def array_response(delta: np.ndarray, k0: float, d: float, n_eff: float, phi_ref: np.ndarray | None = None) -> complex:
    w = weights(d, delta)
    phi = phase(k0, d, n_eff, delta)
    if phi_ref is not None:
        phi = phi - phi_ref
    return np.sum(w * np.exp(-1j * phi), dtype=np.complex128)


def array_gain(delta: np.ndarray, k0: float, d: float, n_eff: float, eta: float = 1.0, phi_ref: np.ndarray | None = None) -> float:
    N = delta.size
    s = array_response(delta, k0, d, n_eff, phi_ref=phi_ref)
    return (eta / N) * np.abs(s) ** 2


def compute_a_ideal(delta_star: np.ndarray, k0: float, d: float, n_eff: float, eta: float = 1.0) -> float:
    N = delta_star.size
    w = weights(d, delta_star)
    return (eta / N) * (np.sum(w)) ** 2


def xi_from_delta(delta_star: np.ndarray, d: float, n_eff: float) -> np.ndarray:
    return delta_star / np.sqrt(d ** 2 + delta_star ** 2) + n_eff
