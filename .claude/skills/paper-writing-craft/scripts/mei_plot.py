#!/usr/bin/env python3
"""mei_plot.py - matplotlib helpers that reproduce the curve-plot template of profiles/weidong-mei.

  from mei_plot import use, fig_single, curve, finish, save
  use()
  fig, ax = fig_single()
  curve(ax, x, y_prop, "Proposed", proposed=True)
  curve(ax, x, y_bl,  "Benchmark 1", ls="--")
  finish(ax, "Number of Sampling Points", "Received SNR (dB)", xticks=x, legend_loc="lower right")
  save(fig, "fig_snr_vs_points")          # writes .pdf (vector) and .png

Run `python mei_plot.py demo out.pdf` to render a demo figure.

Conventions encoded (see profiles/weidong-mei/figures_tables.md section 3):
single column 3.5 in, 4:3; boxed axes, grey grid, inward ticks; line + hollow marker on every data
point; no in-plot title (the LaTeX caption is the title); axis label "Quantity (unit)";
x ticks on the swept values; y limits fitted to the data with round ticks; legend inside the axes,
framed, single column, proposed / optimal entry first (or last when you name benchmarks
"Benchmark 1..n" then "Proposed"); legend labels equal the names used in the text.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

STYLE = Path(__file__).resolve().parent.parent / "assets" / "mei_ieee.mplstyle"
MARKERS = ["*", "v", "o", "^", ">", "s", "d", "x"]
_state = {"i": 0}


def use():
    """Activate the style (call once per script)."""
    plt.style.use(str(STYLE))
    _state["i"] = 0


def fig_single(aspect: float = 4 / 3, width: float = 3.5):
    """IEEE single column (3.5 in). `aspect` = width / height (4:3 default, 1.0 for beam-gain plots)."""
    fig, ax = plt.subplots(figsize=(width, width / aspect))
    _state["i"] = 0
    return fig, ax


def fig_double(aspect: float = 3.2, width: float = 7.16):
    fig, ax = plt.subplots(figsize=(width, width / aspect))
    _state["i"] = 0
    return fig, ax


def curve(ax, x, y, label, proposed: bool = False, ls: str | None = None, marker: str | None = None, color: str | None = None):
    """One series. `proposed=True` -> black, solid, '*' marker (the optimal / proposed scheme).
    Others take the next colour and marker of the cycle (red v, blue o, magenta ^, ...)."""
    if proposed:
        c, m, l = "black", "*", "-"
    else:
        cyc = mpl.rcParams["axes.prop_cycle"].by_key()
        k = (_state["i"] + 1) % len(cyc["color"])  # index 0 is reserved for black
        c, m, l = cyc["color"][k], cyc["marker"][k], "-"
        _state["i"] += 1
    ax.plot(x, y, label=label, color=color or c, marker=marker or m, linestyle=ls or l)


def round_limits(lo: float, hi: float, n: int = 8):
    """Fit y limits to the data with round tick values (what the MATLAB exports look like)."""
    if hi == lo:
        hi = lo + 1.0
    raw = (hi - lo) / max(n - 1, 1)
    mag = 10 ** math.floor(math.log10(raw))
    step = next(s * mag for s in (1, 2, 2.5, 5, 10) if s * mag >= raw)
    return math.floor(lo / step) * step, math.ceil(hi / step) * step, step


def finish(ax, xlabel: str, ylabel: str, xticks=None, legend_loc: str = "best", legend_anchor=None, fit_y: bool = True):
    """Axis labels ('Quantity (unit)'), x ticks on the sweep values, fitted y range, legend inside."""
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if xticks is not None:
        ax.set_xticks(list(xticks))
        ax.set_xlim(min(xticks), max(xticks))
    if fit_y:
        ys = np.concatenate([np.asarray(l.get_ydata(), float) for l in ax.get_lines()])
        lo, hi, step = round_limits(float(np.nanmin(ys)), float(np.nanmax(ys)))
        ax.set_ylim(lo, hi)
        ax.set_yticks(np.arange(lo, hi + step / 2, step))
    ax.legend(loc=legend_loc, bbox_to_anchor=legend_anchor)
    ax.set_title("")  # the caption is the title


def save(fig, stem: str, png: bool = True):
    """Vector PDF for the paper (+ PNG preview)."""
    fig.savefig(f"{stem}.pdf")
    if png:
        fig.savefig(f"{stem}.png", dpi=200)


def demo(path: str = "mei_demo.pdf"):
    """Synthetic data, only to show the style (no data from any paper)."""
    use()
    fig, ax = fig_single()
    x = np.array([10, 20, 30, 40, 50])
    curve(ax, x, 5.0 + 3.0 * (1 - np.exp(-x / 18.0)), "Proposed", proposed=True)
    curve(ax, x, 5.0 + 2.8 * (1 - np.exp(-x / 18.0)), "Suboptimal")
    curve(ax, x, np.full(x.shape, 6.2), "Benchmark 1")
    curve(ax, x, np.full(x.shape, 4.6), "Benchmark 2")
    finish(ax, "Number of Sampling Points", "Received SNR (dB)", xticks=x, legend_loc="lower right", legend_anchor=(0.98, 0.14))
    save(fig, str(Path(path).with_suffix("")))


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "demo":
        demo(sys.argv[2] if len(sys.argv) > 2 else "mei_demo.pdf")
    else:
        print(__doc__)
