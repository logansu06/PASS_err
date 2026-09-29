"""Ablation (ablation-planner, 2026-09-29): certificate-gap accounting on fixed layouts.

Design: GPT-6 Astra (ultra), trace .aris/traces/ablation-planner/2026-09-29_run01/ (001-design, 002-feasibility).
No layout is re-selected: every quantity is evaluated on the stored S_hat / S_nom of results/main_grid.csv, with the
row's geometry, tolerance, family and physical noise sigma2.

A1  fixed-subset certificate replay: symmetric sector + additive pad (literal v1), symmetric + sec, asymmetric + sec
    (production), plus asymmetric + pad for the 2x2 factorial; eps = 0 rows report the literal-v1 penalty only.
A2  references for the multiplicative accounting, for a fixed subset S (SLNR = G_D / (sigma2 + I_P), both /N):
        L0 = D0 / (s2 + I_A) <= D0 / (s2 + I_S) <= D0 / (s2 + p) <= Q = d / (s2 + p) <= W(S) <= U(S)
    I_A  production leakage bound (asymmetric sectors, K = 1440, sec correction);
    I_S  continuous-angle asymmetric-sector maximum, bracketed with the radius theorem at K_REF;
    p    max leakage over the continuous error box: independence gives p = (max_theta sum_n h_n(theta))^2 / N with
         h_n the support of site n's true curve; bracketed by a G-point grid (lower) plus the interpolation
         remainder C_n Delta^2 / 8 (upper) and the radius theorem at K_REF;
    D0   desired projection bound with beta_D enlarged by the residual nominal D-phase misalignment (the production
         numerator omits it); d = min G_D is bracketed by [D0, min over the 2^N corners];
    factors: angular (s2+I_A)/(s2+I_S), P-sector (s2+I_S)/(s2+p), desired d/D0, dependency W/Q, each as an interval.
A3  witness ladder U_H >= U_C >= U_8 (template bank, all corners, 8 refinement starts for both layouts) on every
    positive-error row; on the 32-case stress panel also U_+ (40 corner starts + 16 uniform starts) and the D.6
    joint-box lower bound (r017_joint_box.refine, both layouts). The refinement budget is 100k boxes (deterministic;
    checked per batch of 256, so a run stops at 100,351); a 3600 s safety cap is recorded if it ever binds.
    P = D rows: W = d / (s2 + d).
    On the full grid, U_8 / (enclosure factors x Q) mixes D/P dependency with unresolved witness slack; only the
    stress panel separates them.
A4  selection accounting from main_grid.csv and a no-screening exhaustive audit on the M = 16 scaling slice
    (correctness only: its two timing paths use different batch sizes, so their ratio is not a screening speedup).

All bounds are analytical statements evaluated in float64; radii carry a relative allowance REL on both sides.
"""
import argparse, itertools, json, os, platform, sys, time, zlib
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd
import scipy
from scipy.optimize import minimize

import a7_core as a
import r017_joint_box as jb

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'idea-stage' / 'handoff' / 'gpt6pro_bundle' / 'bundle' / 'a7_verification_bundle'))
import a7_reference as v1  # noqa: E402  literal v1 certificate (symmetric sector + additive pad)

M, N, K = 24, 8, 1440
K_REF, G = 11520, 1025
REL = 1e-12
CORNERS = np.array(list(itertools.product((-1., 1.), repeat=N)))
STRESS_P = [(6.0, 1.0), (2.4, 2.0), (0.0, 1.0), (0.0, 4.0)]
STRESS_EPS, STRESS_SNR = (0.03, 0.08), (10.0, 40.0)
GEOMS6 = [(-6., 1.), (-3., 2.), (0., 1.), (3., 2.), (6., 1.), (0., 4.)]


def parse():
    p = argparse.ArgumentParser()
    p.add_argument('--stage', default='all', help='gaps, stress, screen or all')
    p.add_argument('--limit', type=int, default=0, help='smoke test: only the first LIMIT (P, eps) groups')
    p.add_argument('--workers', type=int, default=7)
    p.add_argument('--refine-boxes', type=int, default=100000)
    p.add_argument('--refine-seconds', type=float, default=3600.0, help='safety cap only; the box count is the budget')
    p.add_argument('--tag', default='')
    return p.parse_args()


def subset(txt):
    return np.array([int(v) for v in str(txt).split()])


# ---------------------------------------------------------------- references (per geometry and tolerance)

def curve_support(xs, eps, P):
    """h^-, h^+ (M, K_REF): lower / upper bounds on the support of each site's true P-contribution curve
    {z_P(x): |x - x_n| <= eps} in the directions theta_k (ideal channel, z = exp(-j psi) / R)."""
    th = np.linspace(-np.pi, np.pi, K_REF, endpoint=False)
    cth, sth = np.cos(th), np.sin(th)
    u = np.linspace(-1.0, 1.0, G)
    delta = 2 * eps / (G - 1)
    ux, uy = P
    b2 = uy * uy + a.D_H ** 2
    hlo = np.empty((len(xs), K_REF))
    C = np.empty(len(xs))
    for n, x in enumerate(xs):
        zz = a.z(x + eps * u, ux, uy)
        for st in range(0, K_REF, K):
            hlo[n, st:st + K] = (np.outer(zz.real, cth[st:st + K]) + np.outer(zz.imag, sth[st:st + K])).max(0)
        lo, hi = x - eps - ux, x + eps - ux
        vmin = 0.0 if lo <= 0 <= hi else min(abs(lo), abs(hi))
        vmax = max(abs(lo), abs(hi))
        rmin = np.sqrt(vmin * vmin + b2)
        amax, a1, a2 = 1 / rmin, vmax / rmin ** 3, (2 * vmax * vmax + b2) / rmin ** 5  # sup A, |A'|, |A''|
        p1 = a.K0 * (a.NEFF + vmax / np.sqrt(vmax * vmax + b2))  # sup |psi'|
        p2 = a.K0 * b2 / rmin ** 3  # sup |psi''|
        C[n] = a2 + 2 * a1 * p1 + amax * p2 + amax * p1 * p1  # sup |f''|, f = A cos(psi + theta)
    return hlo, hlo + (C * delta * delta / 8)[:, None], C


def desired_tables(xs, eps):
    """Projection coefficients with beta_D enlarged by the residual nominal D-phase misalignment."""
    p0, pp, pm = a.psi(xs, 0, 0), a.psi(xs + eps, 0, 0), a.psi(xs - eps, 0, 0)
    bd = np.maximum(pp - p0, p0 - pm)
    ref = np.angle(np.exp(1j * p0).sum())
    resid = np.abs(np.angle(np.exp(1j * (p0 - ref))))
    if np.any(bd + resid > np.pi / 2):
        raise ValueError('beta_D + residual > pi/2')
    amin = a.amp_range(xs, eps, 0, 0)[0]
    return amin * np.cos(bd + resid), float(resid.max())


def radius_bracket(tab, S):
    """[R^-, R^+] of the Minkowski sum from per-site support values on the uniform K_REF grid."""
    m = tab[S].sum(0).max()
    return max(m, 0.0) * (1 - REL), max(m, 0.0) * (1 + REL) / np.cos(np.pi / K_REF)


def leak(S, T, mode):
    m = T['s'][S].sum(0).max()
    B = m / np.cos(np.pi / T['K']) if mode == 'sec' else m + T['amax'][S].sum() * np.pi / T['K']
    return max(B, 0.0) ** 2 / N


# ---------------------------------------------------------------- stage 1: fixed-subset gap accounting

def gap_group(job):
    (P, ee), rows = job
    xs = a.aligned_sites(M)
    eps = ee * a.LAM
    t0 = time.perf_counter()
    out = []
    if ee == 0:
        T = a.tables(xs, 0.0, P)
        Tv1 = v1.tables(xs, 0.0, P)
        for r in rows:
            for role in ('hat', 'nom'):
                S = subset(r['S_' + role])
                nom = float(a.nominal(S, T, N, r['sigma2'])[0])
                Lv1 = float(v1.cert_L(S[None], Tv1, N, r['sigma2'])[0])
                out.append(dict(key(r), role=role, S=' '.join(map(str, S)), L_prod=float(a.cert(S, T, N, r['sigma2'])[0]),
                                nominal=nom, L_v1=Lv1, v1_zero_error_penalty=1 - Lv1 / nom))
        return out, time.perf_counter() - t0
    Ta = a.tables(xs, eps, P)
    Ts = a.tables(xs, eps, P, asymmetric=False)
    Tr = a.tables(xs, eps, P, K=K_REF)
    Tv1 = v1.tables(xs, eps, P)
    hlo, hhi, Cn = curve_support(xs, eps, P)
    cD, resid = desired_tables(xs, eps)
    _, ZD, ZP = a.endpoint_bank(xs, eps, P)
    cache = {}
    for r in rows:
        s2 = float(r['sigma2'])
        for role in ('hat', 'nom'):
            S = subset(r['S_' + role])
            L = {f'L_{g}_{m}': float(a.cert(S, T, N, s2, m)[0]) for g, T in (('sym', Ts), ('asym', Ta)) for m in ('pad', 'sec')}
            Lv1 = float(v1.cert_L(S[None], Tv1, N, s2)[0])
            IA = leak(S, Ta, 'sec')
            IS_lo, IS_hi = (v * v / N for v in radius_bracket(Tr['s'], S))
            rlo = max(hlo[S].sum(0).max(), 0.0) * (1 - REL)
            rhi = max(hhi[S].sum(0).max(), 0.0) * (1 + REL) / np.cos(np.pi / K_REF)
            p_lo, p_hi = rlo * rlo / N, rhi * rhi / N
            D0raw = float(Ta['cD'][S].sum() ** 2 / N)
            D0 = float(cD[S].sum() ** 2 / N)
            GDc = np.abs(a.z(xs[S][None] + eps * CORNERS, 0, 0).sum(1)) ** 2 / N
            IPc = np.abs(a.z(xs[S][None] + eps * CORNERS, *P).sum(1)) ** 2 / N
            d_up = float(GDc.min())
            # witness ladder (U_H >= U_C >= U_8), same physical error for D and P
            UH = float(a.bank_bounds(S[None], ZD, ZP, N, s2)[0][0])
            UC = float(a.witnesses(xs, S, eps, P, N, s2, refine=0)[0])
            U8, d8, _, _ = a.witnesses(xs, S, eps, P, N, s2, refine=8)
            Q_lo, Q_hi = D0 / (s2 + p_hi), d_up / (s2 + p_lo)
            L0 = D0 / (s2 + IA)
            rec = dict(key(r), role=role, S=' '.join(map(str, S)), same_layout=int(r['S_hat'] == r['S_nom']),
                       **L, L_v1=Lv1, v1_rel_diff=abs(Lv1 / L['L_sym_pad'] - 1),
                       L_stored=float(r['L_' + role]), U_stored=float(r['U_' + role]), U_nom_stored=float(r['U_nom']),
                       g_pad_to_sec=L['L_sym_sec'] / L['L_sym_pad'] - 1, g_sym_to_asym=L['L_asym_sec'] / L['L_sym_sec'] - 1,
                       g_v1_to_prod=L['L_asym_sec'] / L['L_sym_pad'] - 1,
                       I_A=IA, I_sym_pad=leak(S, Ts, 'pad'), I_S_lo=IS_lo, I_S_hi=IS_hi, p_lo=p_lo, p_hi=p_hi,
                       I_corner_max=float(IPc.max()), D0_raw=D0raw, D0=D0, d_up=d_up, resid_D_phase=resid,
                       interp_rel=float((hhi - hlo)[S].sum(0).max() / max(rlo, 1e-300)),
                       ang_lo=(s2 + IA) / (s2 + IS_hi) - 1, ang_hi=(s2 + IA) / (s2 + IS_lo) - 1,
                       sec_lo=max(0.0, (s2 + IS_lo) / (s2 + p_hi) - 1), sec_hi=(s2 + IS_hi) / (s2 + p_lo) - 1,
                       secI_lo=max(0.0, IS_lo / p_hi - 1), secI_hi=IS_hi / p_lo - 1,
                       des_lo=0.0, des_hi=d_up / D0 - 1, Q_lo=Q_lo, Q_hi=Q_hi, L0=L0,
                       U_H=UH, U_C=UC, U_8=U8, delta8=' '.join(repr(float(v)) for v in d8 / eps),
                       dep_lo=max(0.0, Q_lo / Q_hi - 1), dep_hi=U8 / Q_lo - 1, total_hi=U8 / L0 - 1,
                       prod_gap=L['L_asym_sec'] / D0raw * (s2 + IA) - 1)
            if P == (0.0, 0.0):  # P = D: W = d / (s2 + d) exactly, so W / Q = (s2 + p) / (s2 + d)
                rec.update(W_lo=D0 / (s2 + D0), W_hi=d_up / (s2 + d_up),
                           dep_lo=max(0.0, (s2 + p_lo) / (s2 + d_up) - 1), dep_hi=(s2 + p_hi) / (s2 + D0) - 1)
            # validity checks (must hold for any valid enclosure)
            rec['check_sector_contains_curve'] = int(IS_hi >= p_lo)
            rec['check_curve_contains_corners'] = int(p_hi >= IPc.max() * (1 - 1e-12))
            rec['check_production_ge_sector'] = int(IA >= IS_lo * (1 - 1e-12))
            rec['check_nested_witness'] = int(UH >= UC * (1 - 1e-12) and UC >= U8 * (1 - 1e-12))
            rec['check_Q_le_U'] = int(Q_lo <= U8 * (1 + 1e-12))
            out.append(rec)
    return out, time.perf_counter() - t0


def key(r):
    return dict(control=r['control'], snr_db=float(r['snr_db']), sigma2=float(r['sigma2']),
                eps_over_lambda=float(r['eps_over_lambda']), xP=float(r['xP']), yP=float(r['yP']))


# ---------------------------------------------------------------- stage 2: stress panel (dependency brackets)

def stress_one(job):
    rec, boxes, seconds = job
    xs = a.aligned_sites(M)
    P, eps, s2 = (rec['xP'], rec['yP']), rec['eps_over_lambda'] * a.LAM, rec['sigma2']
    S = subset(rec['S'])
    t0 = time.perf_counter()
    f = lambda u: a.exact_at(xs, S, eps * np.atleast_2d(u), P, N, s2)[0]
    vv = f(CORNERS)
    order = np.argsort(vv)
    U, best = rec['U_8'], np.array([float(v) for v in rec['delta8'].split()])
    rng = np.random.default_rng(zlib.crc32(repr((rec['control'], rec['snr_db'], rec['eps_over_lambda'], P, rec['S'])).encode()))
    starts = list(CORNERS[order[:40]]) + list(rng.uniform(-1, 1, (16, N)))
    for u0 in starts:
        res = minimize(lambda u: f(u)[0], u0, method='L-BFGS-B', bounds=[(-1, 1)] * N,
                       options={'maxiter': 150, 'ftol': 1e-12})
        u = np.clip(res.x, -1, 1)
        v = float(f(u)[0])
        if v < U:
            U, best = v, u
    t_wit = time.perf_counter() - t0
    Uplus = float(f(best)[0])  # reproducible from delta_plus; refinement centre values are reported separately
    jb.BUDGET, jb.TMAX = boxes, seconds
    ref = jb.refine(xs, S, eps, P, s2, rec['L0'], Uplus)
    Wlo = max(ref['L_refined'], rec['Q_lo'])
    D = np.vstack([rng.uniform(-eps, eps, (20000, N)), eps * CORNERS])
    smin = float(a.exact_at(xs, S, D, P, N, s2)[0].min())
    return dict({k: rec[k] for k in ('control', 'snr_db', 'eps_over_lambda', 'xP', 'yP', 'role', 'S', 'L0', 'Q_lo', 'Q_hi', 'U_8')},
                U_plus=Uplus, delta_plus=' '.join(repr(float(v)) for v in best), U_refine_centres=ref['U_refined'],
                L_joint=ref['L_refined'], W_lo=Wlo,
                n_boxes=ref['n_eval'], box_budget_reached=int(ref['n_eval'] >= boxes), refine_seconds=ref['seconds'],
                witness_seconds=t_wit, sampled_min=smin,
                valid=int(ref['L_refined'] <= smin * (1 + 1e-10)),
                ladder_8_to_plus=rec['U_8'] / Uplus - 1,
                dep_lo=max(0.0, Wlo / rec['Q_hi'] - 1), dep_hi=Uplus / rec['Q_lo'] - 1,
                bracket_before=rec['U_8'] / rec['L0'] - 1, bracket_after=Uplus / Wlo - 1)


# ---------------------------------------------------------------- stage 3: no-screening exhaustive audit (M = 16)

def screen_one(job):
    Mx, control, P, ee = job
    xs = a.aligned_sites(Mx)
    mid = (Mx - N) // 2
    s2 = abs(a.z(xs[mid:mid + N], 0, 0).sum()) ** 2 / N / 10 ** (30.0 / 10)
    eps = ee * a.LAM
    forced = (0, Mx - 1) if control == 'endpoints' else ()
    T = a.tables(xs, eps, P)
    SS = a.family(xs, N, eps, forced)
    t0 = time.perf_counter()
    _, ZD, ZP = a.endpoint_bank(xs, eps, P)
    UU, _ = a.exact_bounds(SS, T, ZD, ZP, N, s2)
    t_bank = time.perf_counter() - t0
    SN = a.nominal_argmax(SS, T, N, s2)
    g = a.gcs(T, SS, UU, N, s2, SN, forced=forced, seed=2026, cap=200000)
    t0 = time.perf_counter()
    LL = np.concatenate([a.cert(SS[i:i + 4096], T, N, s2) for i in range(0, len(SS), 4096)])
    t_full = time.perf_counter() - t0
    k = int(np.argmax(LL))
    ties = int(np.sum(LL >= LL[k] * (1 - 1e-12)))
    return dict(M=Mx, control=control, xP=P[0], yP=P[1], eps_over_lambda=ee, family_size=len(SS),
                L_exhaustive=float(LL[k]), L_gcs=g['L_hat'], rel_diff=g['L_hat'] / LL[k] - 1, ties=ties,
                same_layout=int(np.array_equal(SS[k], g['S_hat'])), exact=int(g['exact']), n_eval=g['n_eval'],
                survivors=g['survivors'], t_full_enum_batch4096=t_full, t_bank=t_bank, t_gcs_batch128=g['seconds'])


# ---------------------------------------------------------------- summaries

def q(x, p):
    x = np.asarray(x, dtype=float)
    return float(np.quantile(x, p)) if len(x) else None


def stats(x):
    x = np.asarray(x, dtype=float)
    return dict(n=int(len(x)), median=q(x, .5), p95=q(x, .95), max=float(x.max()) if len(x) else None,
                min=float(x.min()) if len(x) else None)


def summarize(df, st, sc):
    out = {}
    pos = df[df.eps_over_lambda > 0]
    pops = {'primary': (pos.xP != 0) | (pos.yP != 0)}
    pops['coaligned_xP0'] = pops['primary'] & (pos.xP == 0)
    pops['offaxis'] = pops['primary'] & (pos.xP != 0)
    pops['P_eq_D'] = (pos.xP == 0) & (pos.yP == 0)
    for fam in ('free', 'endpoints'):
        for pname, mask in pops.items():
            for role in ('hat', 'nom'):
                d = pos[mask & (pos.control == fam) & (pos.role == role)]
                if not len(d):
                    continue
                e = dict(rows=len(d))
                for c in ('g_pad_to_sec', 'g_sym_to_asym', 'g_v1_to_prod', 'ang_hi', 'sec_lo', 'sec_hi', 'secI_lo',
                          'secI_hi', 'des_hi', 'dep_lo', 'dep_hi', 'total_hi', 'interp_rel'):
                    e[c] = stats(d[c])
                if role == 'hat':
                    U = d['U_nom_stored']
                    e['certified_positive'] = {arm: int((d[arm] > U).sum()) for arm in
                                               ('L_sym_pad', 'L_sym_sec', 'L_asym_pad', 'L_asym_sec', 'L_v1')}
                out[f'{fam}/{pname}/{role}'] = e
    prim = pos[(pos.xP != 0) | (pos.yP != 0)]
    enc = (1 + prim.ang_hi) * (1 + prim.sec_hi) * (1 + prim.des_hi) - 1
    big = prim.total_hi > 1e-3
    out['enclosure_total_hi'] = stats(enc)  # angular x P-sector x desired, upper endpoints, rowwise
    out['enclosure_share_of_log_U8_over_L0'] = stats((np.log1p(enc) / np.log1p(prim.total_hi))[big])
    out['ladder'] = dict(UH_over_UC=stats(prim.U_H / prim.U_C - 1), UC_over_U8=stats(prim.U_C / prim.U_8 - 1))
    checks = [c for c in df.columns if c.startswith('check_')]
    out['checks_failed'] = {c: int((pos[c] == 0).sum()) for c in checks}
    out['production_reproduced_max_rel'] = float((pos['L_asym_sec'] / pos['L_stored'] - 1).abs().max())
    out['v1_literal_max_rel_diff'] = float(pos['v1_rel_diff'].max())
    out['resid_D_phase_max'] = float(pos['resid_D_phase'].max())
    out['D0_correction_max_rel'] = float((1 - pos['D0'] / pos['D0_raw']).max())
    z = df[df.eps_over_lambda == 0]
    if len(z):
        out['eps0_v1_penalty'] = stats(z['v1_zero_error_penalty'])
    if st is not None and len(st):
        out['stress'] = {k: stats(st[k]) for k in ('ladder_8_to_plus', 'dep_lo', 'dep_hi', 'bracket_before', 'bracket_after')}
        out['stress']['valid'] = int(st['valid'].sum())
        out['stress']['n'] = int(len(st))
        for sub, m in (('coaligned', st.xP == 0), ('offaxis', st.xP != 0)):
            out['stress'][sub] = {k: stats(st.loc[m, k]) for k in ('dep_lo', 'dep_hi', 'bracket_after')}
        # paired comparison after joint refinement: certified if W_lo(S_hat) > U_plus(S_nom)
        kk = ['control', 'xP', 'yP', 'eps_over_lambda', 'snr_db']
        pr = st[st.role == 'hat'].merge(st[st.role == 'nom'], on=kk, suffixes=('_hat', '_nom'))
        pr['Gamma_before'] = pr['L0_hat'] / pr['U_plus_nom'] - 1
        pr['Gamma_joint'] = pr['W_lo_hat'] / pr['U_plus_nom'] - 1
        pairs = [dict({k: r[k] for k in kk}, same_layout=int(r['S_hat'] == r['S_nom']), Gamma_before=r['Gamma_before'],
                      Gamma_joint=r['Gamma_joint']) for r in pr.to_dict('records')]
        out['stress']['pairs'] = pairs
        for sub, m in (('coaligned', pr.xP == 0), ('offaxis', pr.xP != 0)):
            d = pr[m]
            out['stress'][sub]['pairs'] = int(len(d))
            out['stress'][sub]['certified_before'] = int((d.Gamma_before > 0).sum())
            out['stress'][sub]['certified_after_joint'] = int((d.Gamma_joint > 0).sum())
    if sc is not None and len(sc):
        out['screen_m16'] = dict(n=int(len(sc)), max_abs_rel_diff=float(sc['rel_diff'].abs().max()),
                                 same_layout=int(sc['same_layout'].sum()), max_ties=int(sc['ties'].max()),
                                 note='timings use different batch sizes under concurrent workers; not a screening speedup')
    return out


def up(x, sig=3):
    """Round up to `sig` significant digits (outward for upper bounds)."""
    if x == 0:
        return 0.0
    e = np.floor(np.log10(abs(x))) - sig + 1
    return float(np.ceil(x / 10 ** e) * 10 ** e)


def down(x, sig=3):
    return -up(-x, sig) if x < 0 else (0.0 if x == 0 else float(np.floor(x / 10 ** (np.floor(np.log10(x)) - sig + 1))
                                                                * 10 ** (np.floor(np.log10(x)) - sig + 1)))


def fmt(x, sig=3):
    return '%.*g' % (sig, x)


def report_md(df, st, sc, mg, summary):
    """Paper-facing numbers (percent), bounds rounded outward; medians of bracketed quantities as [lo, hi]."""
    pos = df[df.eps_over_lambda > 0]
    prim = pos[(pos.xP != 0) | (pos.yP != 0)]
    hat = prim[prim.role == 'hat']
    enc = (1 + prim.ang_hi) * (1 + prim.sec_hi) * (1 + prim.des_hi) - 1
    pc = lambda v: 100 * v
    L = ['# Ablation R021: certificate-gap accounting (generated by ablation_gaps.py)', '',
         'All bounds are analytical statements evaluated numerically in float64; bound endpoints are rounded outward.',
         'Percent values. Populations: primary = eps > 0, P != D (528 rows per family); S_hat rows 1,056, both layouts 2,112.', '',
         '| Quantity | Value | Population |', '|---|---|---|']
    g = hat.g_pad_to_sec
    L.append('| Pad -> sec certificate gain: median / p95 / max | %.4g / %.4g / <= %s | 1,056 primary S_hat |'
             % (pc(g.median()), pc(g.quantile(.95)), fmt(up(pc(g.max()), 4), 4)))
    L.append('| Symmetric -> asymmetric gain: max | <= %s | 1,056 primary S_hat |' % fmt(up(pc(hat.g_sym_to_asym.max()))))
    L.append('| Angular / P-sector / desired-projection loss: max | <= %s / <= %s / <= %s | 2,112 primary layout-rows |'
             % (fmt(up(pc(prim.ang_hi.max()))), fmt(up(pc(prim.sec_hi.max()))), fmt(up(pc(prim.des_hi.max())))))
    L.append('| Combined enclosure loss (rowwise product): max | <= %s | 2,112 primary layout-rows |' % fmt(up(pc(enc.max()))))
    for fam in ('free', 'endpoints'):
        c = summary[f'{fam}/primary/hat']['certified_positive']
        L.append('| Certified-positive S_hat vs stored U_nom, %s: v1 / sym+sec / production | %d / %d / %d of 528 | primary |'
                 % (fam, c['L_v1'], c['L_sym_sec'], c['L_asym_sec']))
    if st is not None and len(st):
        for sub, m in (('off-axis', st.xP != 0), ('co-aligned (x_P = 0)', st.xP == 0)):
            d = st[m]
            L.append('| Median dependency factor, %s | [%s, %s] | %d stress layout-rows |'
                     % (sub, fmt(down(pc(d.dep_lo.median()), 4), 4), fmt(up(pc(d.dep_hi.median()), 4), 4), len(d)))
        d = st[st.xP == 0]
        L.append('| Certified dependency lower bound, co-aligned: min / median / max of lower endpoints | %s / %s / %s | %d stress layout-rows |'
                 % (fmt(down(pc(d.dep_lo.min()))), fmt(down(pc(d.dep_lo.median()))), fmt(down(pc(d.dep_lo.max()))), len(d)))
        pr = pd.DataFrame(summary['stress']['pairs'])
        fl = pr[(pr.xP == 0) & (pr.Gamma_joint > 0)]
        L.append('| Co-aligned pairs certified after joint refinement | %d of %d; gain [%s, %s] | stress pairs |'
                 % (len(fl), int((pr.xP == 0).sum()), fmt(down(pc(fl.Gamma_joint.min()))), fmt(up(pc(fl.Gamma_joint.max())))))
    for fam in ('free', 'endpoints'):
        s = summary['selection'][fam]
        L.append('| Swap -> completed GCS (certificate objective), %s: improved / median / max | %d/%d / %.4g / <= %s | exact cases |'
                 % (fam, s['strictly_improved_exact'], s['exact_cases'], pc(s['selection_gap_exact']['median']),
                    fmt(up(pc(s['selection_gap_exact']['max']), 4), 4)))
    if sc is not None and len(sc):
        L.append('| M = 16 no-screening audit: same maximum and layout | %d / %d | scaling slice |' % (int(sc.same_layout.sum()), len(sc)))
    z = df[df.eps_over_lambda == 0]
    L.append('| Literal-v1 artificial penalty at eps = 0: median / max | %.4g / <= %s | %d layout-rows |'
             % (pc(z.v1_zero_error_penalty.median()), fmt(up(pc(z.v1_zero_error_penalty.max()))), len(z)))
    L += ['', 'Witness ladder (primary layout-rows): max |U_H / U_C - 1| = %.3g; max 1 - U_8 / U_C = %s%%.'
          % (float((prim.U_H / prim.U_C - 1).abs().max()), fmt(up(pc(float((1 - prim.U_8 / prim.U_C).max()))))),
          'On the full grid, U_8 / (enclosure factors x Q) mixes D/P dependency with unresolved witness slack; the stress',
          'panel separates them. The M = 16 audit is a correctness check only (timing paths not matched).']
    return '\n'.join(L) + '\n'


def selection_accounting(mg):
    pos = mg[(mg.eps_over_lambda > 0) & ((mg.xP != 0) | (mg.yP != 0))]
    out = {}
    for fam in ('free', 'endpoints'):
        d = pos[pos.control == fam]
        ex, cp = d[d.exact == 1], d[d.exact == 0]
        out[fam] = dict(exact_cases=int(len(ex)), capped_cases=int(len(cp)),
                        selection_gap_exact=stats(ex['L_hat'] / ex['swap_L'] - 1),
                        strictly_improved_exact=int(((ex['L_hat'] / ex['swap_L'] - 1) > 1e-12).sum()),
                        capped_interval_lo=stats(cp['L_hat'] / cp['swap_L'] - 1) if len(cp) else None,
                        capped_interval_hi=stats(cp['U_star'] / cp['swap_L'] - 1) if len(cp) else None,
                        robust_regret_bound=stats(d['U_star'] / d['L_hat'] - 1),
                        unique=int(d['unique'].sum()))
    return out


def main():
    args = parse()
    res = HERE / 'results'
    mg = pd.read_csv(res / 'main_grid.csv')
    tag = args.tag
    t_all = time.perf_counter()
    meta = dict(args=vars(args), K_REF=K_REF, G=G, REL=REL, numpy=np.__version__, scipy=scipy.__version__,
                python=platform.python_version(), platform=platform.platform(), date=time.strftime('%Y-%m-%d %H:%M:%S'))
    gpath = res / f'ablation_gaps{tag}.csv'
    if args.stage in ('gaps', 'all'):
        groups = {}
        for r in mg.to_dict('records'):
            groups.setdefault((float(r['xP']), float(r['yP'])), {}).setdefault(float(r['eps_over_lambda']), []).append(r)
        jobs = [((P, e), rows) for P, byeps in groups.items() for e, rows in byeps.items()]
        jobs.sort(key=lambda j: -j[0][1])
        if args.limit:
            jobs = [j for j in jobs if j[0][1] > 0][:args.limit]
        rows, t0 = [], time.perf_counter()
        with Pool(args.workers) as pool:
            for k, (rr, dt) in enumerate(pool.imap_unordered(gap_group, jobs), 1):
                rows.extend(rr)
                if k % 10 == 0 or k == len(jobs):
                    print(f'gaps: {k}/{len(jobs)} groups, {len(rows)} layout-rows, {time.perf_counter() - t0:.0f}s', flush=True)
        pd.DataFrame(rows).sort_values(['control', 'snr_db', 'eps_over_lambda', 'yP', 'xP', 'role']).to_csv(gpath, index=False)
        meta['gaps_seconds'] = time.perf_counter() - t0
    df = pd.read_csv(gpath)
    st = sc = None
    spath, cpath = res / f'ablation_stress{tag}.csv', res / f'ablation_screen_m16{tag}.csv'
    if args.stage in ('stress', 'all'):
        pos = df[df.eps_over_lambda > 0]
        near = lambda v, vals: any(np.isclose(v, w, atol=1e-9) for w in vals)
        sel = pos[pos.apply(lambda r: any(np.isclose(r.xP, px, atol=1e-9) and np.isclose(r.yP, py, atol=1e-9)
                                          for px, py in STRESS_P)
                            and near(r.eps_over_lambda, STRESS_EPS) and near(r.snr_db, STRESS_SNR), axis=1)]
        jobs = [(r, args.refine_boxes, args.refine_seconds) for r in sel.to_dict('records')]
        t0, rows = time.perf_counter(), []
        with Pool(args.workers) as pool:
            for k, r in enumerate(pool.imap_unordered(stress_one, jobs), 1):
                rows.append(r)
                if k % 8 == 0 or k == len(jobs):
                    print(f'stress: {k}/{len(jobs)} layouts, {time.perf_counter() - t0:.0f}s', flush=True)
        pd.DataFrame(rows).sort_values(['control', 'xP', 'yP', 'eps_over_lambda', 'snr_db', 'role']).to_csv(spath, index=False)
        meta['stress_seconds'] = time.perf_counter() - t0
    if args.stage in ('screen', 'all'):
        jobs = [(16, c, P, e) for c in ('free', 'endpoints') for P in GEOMS6 for e in (0.03, 0.05)]
        t0 = time.perf_counter()
        with Pool(args.workers) as pool:
            rows = list(pool.imap_unordered(screen_one, jobs))
        pd.DataFrame(rows).sort_values(['control', 'xP', 'yP', 'eps_over_lambda']).to_csv(cpath, index=False)
        meta['screen_seconds'] = time.perf_counter() - t0
    if spath.exists():
        st = pd.read_csv(spath)
    if cpath.exists():
        sc = pd.read_csv(cpath)
    summary = summarize(df, st, sc)
    summary['selection'] = selection_accounting(mg)
    meta['seconds'] = time.perf_counter() - t_all
    summary['meta'] = meta
    (res / f'ablation_summary{tag}.json').write_text(json.dumps(summary, indent=1))
    (res / f'ablation_summary{tag}.md').write_text(report_md(df, st, sc, mg, summary))
    print(json.dumps({k: summary[k] for k in ('checks_failed', 'production_reproduced_max_rel', 'v1_literal_max_rel_diff',
                                              'resid_D_phase_max', 'D0_correction_max_rel')}, indent=1))
    print('saved', gpath.name, f'{meta["seconds"]:.0f}s')


if __name__ == '__main__':
    os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
    main()
