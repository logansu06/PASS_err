from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
from cycler import cycler


_COLOR_CYCLE = [
    "#1b9e77",
    "#d95f02",
    "#7570b3",
    "#e7298a",
    "#66a61e",
    "#e6ab02",
    "#a6761d",
    "#666666",
]


def _apply_plot_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
            "mathtext.fontset": "dejavuserif",
            "axes.prop_cycle": cycler(color=_COLOR_CYCLE),
            "axes.linewidth": 1.0,
            "axes.labelsize": 11,
            "axes.titlesize": 12,
            "axes.titleweight": "semibold",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "xtick.direction": "in",
            "ytick.direction": "in",
            "xtick.major.size": 5,
            "ytick.major.size": 5,
            "xtick.minor.size": 3,
            "ytick.minor.size": 3,
            "xtick.major.width": 1.0,
            "ytick.major.width": 1.0,
            "xtick.minor.width": 0.8,
            "ytick.minor.width": 0.8,
            "grid.color": "0.85",
            "grid.linewidth": 0.8,
            "grid.alpha": 0.8,
            "legend.frameon": True,
            "legend.framealpha": 0.9,
            "legend.edgecolor": "0.8",
            "legend.fontsize": 9,
            "lines.linewidth": 2.2,
            "lines.markersize": 5,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.02,
        }
    )


def _finish_plot(fig: plt.Figure, out_base: str) -> None:
    fig.tight_layout()
    fig.savefig(out_base + ".png")
    fig.savefig(out_base + ".pdf")
    plt.close(fig)


def plot_main(
    data: Dict[str, np.ndarray],
    epsilon_valid_norm: float,
    xi_max: float,
    meta_text: str,
    out_base: str,
) -> None:
    _apply_plot_style()
    eps = data["eps_norm"]
    valid_mask = eps <= epsilon_valid_norm + 1e-12
    lb_full_plot = np.where(valid_mask, data["lb_full_norm"], np.nan)
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    ax.plot(eps, data["ideal_norm"], label="Ideal baseline")
    ax.plot(eps, data["wc_norm"], label="Box adversary (best found)")
    ax.plot(eps, data["split_norm"], label="Split-mode construction", linestyle=":")
    ax.plot(eps, data["common_bias_norm"], label="Common-bias shift", linestyle="--", linewidth=1.6)
    ax.plot(eps, lb_full_plot, label="Lower bound (full, guaranteed region)", linestyle="-.")
    ax.plot(eps, data["mc_mean"], label="Uniform-box MC mean", linewidth=1.8)
    ax.fill_between(eps, data["mc_p05"], data["mc_p95"], alpha=0.18, label="Uniform-box MC [p05, p95]")
    ax.axvline(
        epsilon_valid_norm,
        color="0.2",
        linestyle="--",
        linewidth=1.2,
        label="Guaranteed small-error region",
    )
    ax.set_xlabel("epsilon / lambda")
    ax.set_ylabel("normalized gain")
    ax.set_title("PASS gain degradation under bounded position errors")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.grid(True, which="minor", linestyle=":", alpha=0.25)
    ax.minorticks_on()
    ax.set_axisbelow(True)
    ax.text(
        0.02,
        0.97,
        meta_text + f", xi_max={xi_max:.3f}",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=9,
        bbox=dict(facecolor="white", alpha=0.85, edgecolor="0.8", boxstyle="round,pad=0.2"),
    )
    ax.legend(loc="lower left", bbox_to_anchor=(0.0, -0.03), ncol=2, handlelength=2.6)
    ax.set_ylim(bottom=0.0)
    _finish_plot(fig, out_base)


def plot_freq_sweep(curves: List[Dict[str, np.ndarray]], out_base: str) -> None:
    _apply_plot_style()
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    for entry in curves:
        label = f"f_c = {entry['f_c'] / 1e9:.0f} GHz"
        ax.plot(entry["eps_m"], entry["wc_norm"], label=label)
    ax.set_xlabel("epsilon (m)")
    ax.set_ylabel("normalized gain")
    ax.set_title("Carrier-frequency sensitivity sweep")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.grid(True, which="minor", linestyle=":", alpha=0.25)
    ax.minorticks_on()
    ax.set_axisbelow(True)
    ax.legend()
    _finish_plot(fig, out_base)


def plot_neff_sweep(curves: List[Dict[str, np.ndarray]], out_base: str) -> None:
    _apply_plot_style()
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    for entry in curves:
        label = f"n_eff = {entry['n_eff']:.2f}"
        ax.plot(entry["eps_norm"], entry["wc_norm"], label=label)
    ax.set_xlabel("epsilon / lambda")
    ax.set_ylabel("normalized gain")
    ax.set_title("Waveguide-index sensitivity sweep")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.grid(True, which="minor", linestyle=":", alpha=0.25)
    ax.minorticks_on()
    ax.set_axisbelow(True)
    ax.legend()
    _finish_plot(fig, out_base)


def plot_xi_distribution(indices: np.ndarray, xi: np.ndarray, xi_max: float, out_base: str) -> None:
    _apply_plot_style()
    fig, ax = plt.subplots(figsize=(6.5, 4.0))
    ax.plot(indices, xi, marker="o", linestyle="-")
    ax.axhline(xi_max, color="0.25", linestyle="--", linewidth=1.5, label="xi_max")
    ax.axhline(-xi_max, color="0.25", linestyle="--", linewidth=1.0, alpha=0.6)
    ax.set_xlabel("Index n")
    ax.set_ylabel("xi_n")
    ax.set_title("Phase-sensitivity profile")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.grid(True, which="minor", linestyle=":", alpha=0.25)
    ax.minorticks_on()
    ax.set_axisbelow(True)
    ax.legend()
    _finish_plot(fig, out_base)


def plot_box_validation(data: Dict[str, np.ndarray], out_base: str) -> None:
    _apply_plot_style()
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(data["eps_norm"], data["corner_norm"], label="Corner-restricted")
    ax.plot(data["eps_norm"], data["split_norm"], label="Split-mode construction", linestyle=":")
    ax.plot(data["eps_norm"], data["box_norm"], label="Continuous-box best found", linestyle="-.")
    ax.set_xlabel("epsilon / lambda")
    ax.set_ylabel("normalized gain")
    ax.set_title("Corner adversary vs continuous-box search")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.grid(True, which="minor", linestyle=":", alpha=0.25)
    ax.minorticks_on()
    ax.set_axisbelow(True)
    ax.legend()
    _finish_plot(fig, out_base)


def plot_error_scenarios(data: Dict[str, np.ndarray], out_base: str) -> None:
    _apply_plot_style()
    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    eps = data["eps_norm"]
    ax.plot(eps, data["iid_mean"], label="IID uniform mean")
    ax.plot(eps, data["iid_approx"], label="IID uniform quadratic", linestyle="--", linewidth=1.6)
    ax.plot(eps, data["common_mean"], label="Common-bias mean")
    ax.plot(eps, data["common_approx"], label="Common-bias quadratic", linestyle="--", linewidth=1.6)
    ax.plot(eps, data["corr_mean"], label="Correlated Gaussian mean")
    ax.plot(eps, data["corr_approx"], label="Correlated Gaussian quadratic", linestyle="--", linewidth=1.6)
    ax.set_xlabel("epsilon / lambda")
    ax.set_ylabel("normalized gain")
    ax.set_title("Cross-scenario validation of the quadratic theory")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.grid(True, which="minor", linestyle=":", alpha=0.25)
    ax.minorticks_on()
    ax.set_axisbelow(True)
    ax.legend(loc="lower left", bbox_to_anchor=(0.0, -0.02), ncol=2)
    _finish_plot(fig, out_base)


def plot_baseline_box_curves(curves: List[Dict[str, np.ndarray]], out_base: str) -> None:
    _apply_plot_style()
    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    for entry in curves:
        ax.plot(entry["eps_norm"], entry["box_abs"], label=entry["label"])
    ax.set_xlabel("epsilon / lambda")
    ax.set_ylabel("raw gain")
    ax.set_title("Baseline comparison under box-best-found errors")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.grid(True, which="minor", linestyle=":", alpha=0.25)
    ax.minorticks_on()
    ax.set_axisbelow(True)
    ax.legend()
    _finish_plot(fig, out_base)


def plot_baseline_iid_curves(curves: List[Dict[str, np.ndarray]], out_base: str) -> None:
    _apply_plot_style()
    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    for entry in curves:
        ax.plot(entry["eps_norm"], entry["iid_abs"], label=entry["label"])
    ax.set_xlabel("epsilon / lambda")
    ax.set_ylabel("raw gain")
    ax.set_title("Baseline comparison under iid uniform errors")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.grid(True, which="minor", linestyle=":", alpha=0.25)
    ax.minorticks_on()
    ax.set_axisbelow(True)
    ax.legend()
    _finish_plot(fig, out_base)


def plot_baseline_tradeoff(rows: List[Dict[str, float | str]], ref_eps_norm: float, out_base: str) -> None:
    _apply_plot_style()
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 4.0))

    x_nom = np.array([float(row["nominal_abs"]) for row in rows])
    y_box = np.array([float(row["box_abs_ref"]) for row in rows])
    y_iid = np.array([float(row["iid_mean_abs_ref"]) for row in rows])
    labels = [str(row.get("label", row["placement"])) for row in rows]

    axes[0].scatter(x_nom, y_box, s=60)
    axes[0].set_xlabel("nominal raw gain")
    axes[0].set_ylabel(f"box-best-found raw gain @ {ref_eps_norm:.2f}")
    axes[0].set_title("Nominal vs worst-case tradeoff")

    axes[1].scatter(x_nom, y_iid, s=60)
    axes[1].set_xlabel("nominal raw gain")
    axes[1].set_ylabel(f"iid mean raw gain @ {ref_eps_norm:.2f}")
    axes[1].set_title("Nominal vs stochastic tradeoff")

    for ax, y_values in zip(axes, [y_box, y_iid]):
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.grid(True, which="minor", linestyle=":", alpha=0.25)
        ax.minorticks_on()
        ax.set_axisbelow(True)
        for x_val, y_val, label in zip(x_nom, y_values, labels):
            ax.annotate(label, (x_val, y_val), xytext=(4, 4), textcoords="offset points", fontsize=8)

    _finish_plot(fig, out_base)
