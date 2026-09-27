from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any
import numpy as np


@dataclass
class MonteCarloConfig:
    samples: int = 1000


@dataclass
class WorstCaseConfig:
    enum_threshold_N: int = 20
    coord_grid_K: int = 21
    coord_max_iter: int = 30
    coord_restarts: int = 10
    coord_tol: float = 1e-6


@dataclass
class SweepConfig:
    f_c_list: List[float] = field(default_factory=lambda: [6e9, 28e9, 60e9])
    n_eff_list: List[float] = field(default_factory=lambda: [1.44, 1.75, 1.99])


@dataclass
class BoxSearchConfig:
    local_restarts: int = 6
    local_max_iter: int = 300
    validation_eps_norm_list: List[float] = field(default_factory=lambda: [0.02, 0.05, 0.10, 0.15, 0.175])


@dataclass
class ScenarioConfig:
    samples: int = 2000
    epsilon_norm_list: np.ndarray = field(default_factory=lambda: np.linspace(0.0, 0.10, 21))
    corr_length: float = 4.0


@dataclass
class BaselineConfig:
    epsilon_norm_list: np.ndarray = field(default_factory=lambda: np.linspace(0.0, 0.15, 31))
    reference_eps_norm_list: List[float] = field(default_factory=lambda: [0.05, 0.10, 0.15])
    summary_eps_norm: float = 0.10
    optimizer_restarts: int = 4
    penalty_weight: float = 1e6


@dataclass
class Config:
    # Physical constants
    c: float = 3e8
    f_c: float = 28e9
    d: float = 3.0
    n_eff: float = 1.44
    N: int = 16  # must be even
    delta_p: float = 0.5
    eta: float = 1.0

    epsilon_norm_list: np.ndarray = field(default_factory=lambda: np.linspace(0.0, 0.20, 41))
    # Absolute error sweep for frequency sensitivity (meters)
    eps_m_list: np.ndarray = field(default_factory=lambda: np.linspace(0.0, 0.002, 41))

    mc: MonteCarloConfig = field(default_factory=MonteCarloConfig)
    worst_case: WorstCaseConfig = field(default_factory=WorstCaseConfig)
    box_search: BoxSearchConfig = field(default_factory=BoxSearchConfig)
    scenarios: ScenarioConfig = field(default_factory=ScenarioConfig)
    baselines: BaselineConfig = field(default_factory=BaselineConfig)
    sweep: SweepConfig = field(default_factory=SweepConfig)

    random_seed: int = 20260111

    def to_serializable(self) -> Dict[str, Any]:
        """Convert config to a JSON-serializable dict."""
        data = asdict(self)
        data["epsilon_norm_list"] = [float(x) for x in self.epsilon_norm_list]
        data["eps_m_list"] = [float(x) for x in self.eps_m_list]
        data["scenarios"]["epsilon_norm_list"] = [float(x) for x in self.scenarios.epsilon_norm_list]
        data["baselines"]["epsilon_norm_list"] = [float(x) for x in self.baselines.epsilon_norm_list]
        return data


def get_config() -> Config:
    """Return default simulation configuration."""
    return Config()
