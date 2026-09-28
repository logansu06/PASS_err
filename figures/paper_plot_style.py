"""Shared style for the A7 v2 paper figures (IEEE two-column: column 3.5 in, text width 7.16 in).

Colors come from the validated dataviz reference palette (light mode):
- families: free = slot 1 blue, endpoints = slot 2 orange (adjacent CVD dE 24.7); free is also drawn solid/filled and
  endpoints dashed/hollow, so print in grayscale keeps identity;
- geometries: violet / green / magenta (all-pairs CVD pass; magenta < 3:1 contrast -> curves are direct-labeled and
  carry distinct markers);
- reference SNR: one-hue blue ordinal ramp, steps 250/400/550/700 (monotone lightness, light end 2.06:1).
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / 'experiments' / 'a7' / 'results'
FIG_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'experiments' / 'a7'))

COL_W, TEXT_W = 3.5, 7.16
FONT_SIZE = 8

matplotlib.rcParams.update({
    'font.size': FONT_SIZE,
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'Times', 'STIXGeneral', 'DejaVu Serif'],
    'mathtext.fontset': 'stix',
    'axes.labelsize': FONT_SIZE,
    'axes.titlesize': FONT_SIZE,
    'xtick.labelsize': FONT_SIZE - 1,
    'ytick.labelsize': FONT_SIZE - 1,
    'legend.fontsize': FONT_SIZE - 1,
    'axes.linewidth': 0.6,
    'xtick.major.width': 0.6, 'ytick.major.width': 0.6,
    'xtick.minor.width': 0.4, 'ytick.minor.width': 0.4,
    'xtick.major.size': 2.5, 'ytick.major.size': 2.5,
    'lines.linewidth': 1.1,
    'lines.markersize': 3.5,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': False,
    'legend.frameon': False,
    'legend.handlelength': 1.8,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.02,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'text.usetex': False,
})

INK = '#0b0b0b'
INK_2 = '#52514e'
MUTED = '#8a8984'
GRID = '#e6e5e0'
SURFACE_SHADE = '#f0efec'   # diverging-neutral gray, used for the "inconclusive" band

FAMILY = {'free': dict(color='#2a78d6', ls='-', marker='o', mfc='#2a78d6', label='free family'),
          'endpoints': dict(color='#eb6834', ls='--', marker='s', mfc='white', label='identical endpoints')}
GEOM = {(3.0, 2.0): dict(color='#4a3aa7', marker='o', label='P = (3, 2)'),
        (6.0, 1.0): dict(color='#008300', marker='^', label='P = (6, 1)'),
        (0.0, 1.0): dict(color='#e87ba4', marker='s', label='P = (0, 1)')}
SNR = {10.0: '#86b6ef', 20.0: '#3987e5', 30.0: '#1c5cab', 40.0: '#0d366b'}


def light_grid(ax, axis='y'):
    ax.grid(True, axis=axis, color=GRID, lw=0.5, zorder=0)
    ax.set_axisbelow(True)


def panel_tag(ax, tag, x=-0.02, y=1.02):
    ax.text(x, y, tag, transform=ax.transAxes, ha='right', va='bottom', fontsize=FONT_SIZE, color=INK)


def save_fig(fig, name):
    for ext in ('pdf', 'png'):
        fig.savefig(FIG_DIR / f'{name}.{ext}')
    print(f'Saved: figures/{name}.pdf (+ .png preview)')
