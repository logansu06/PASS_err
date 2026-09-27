"""M0 sanity and numerical audit (refine-logs/EXPERIMENT_PLAN.md v2, block B0; tracker R002-R008).

R002  bound validity: 20 pre-listed cases x 5 eps (+ 4 non-ideal cases x 5 eps). Per layout (S_hat, S_nom, 2 random):
      1e5 uniform draws in the box + all 2^N corners; require SLNR >= L, G_D >= (sum c)^2/N, I_P <= Ibar, L <= U_H.
R003  endpoint-bank identity: 40 random layouts per (P, eps, channel); bank max leakage == 256-corner max; H <= 2M.
R004  eps = 0 (R004_eps0): L = U_H = U = nominal SLNR exactly (one arithmetic path), Gamma = global gap = 0, and
      S_hat = S_nom or an exact tie; 34 geometries x 2 controls x 4 SNR.
      Angular correction (R004_K): K in {720, 1440, 5760}; pairwise L ratio within sec^2(pi/720); K = 720 valid on corners.
R005  clearance and guards: eps just above the clearance threshold shrinks the family; beta_D > pi/2 and a
      non-aligned family raise.
R006  reproducibility: two CLI runs of run_main.py agree bit-for-bit on all non-timing fields.
R007  featured margin audit, P = (3, 2), eps = 0.05 lam, 30 dB, both controls: an independent scalar implementation
      (mpmath, 50 digits, when available) of L(S_hat), the top-5 rival U_H and U(S_nom) at the stored witness.
R008  cross-check: rerun the GPT-6 Pro bundle's a7_grid.py and a7_unit_checks.py in a scratch copy and compare
      with the stored results (matched family: 108/132 positive, 79/132 above 5%).
"""
import argparse, csv, itertools, json, math, os, shutil, subprocess, sys, time, zlib
from math import comb
from multiprocessing import Pool
from pathlib import Path

import numpy as np

import a7_core as a
from run_main import GEOMS

HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parents[1] / 'idea-stage/handoff/gpt6pro_bundle/bundle/a7_verification_bundle'
M, N = 24, 8
EPS = (0.0, 0.01, 0.03, 0.05, 0.08)
TOL = 1e-10
CORNERS = np.array(list(itertools.product((-1., 1.), repeat=N)))
NONIDEAL = (0.08, 2.0)  # B5: 0.08 dB/m, cos^2 field directivity
LISTED = [(3., 2.), (-3., 1.), (6., 1.), (0., 4.), (0., 0.)]
CASES = [(P, c, snr) for P in LISTED for c in ('free', 'endpoints') for snr in (10., 30.)]  # 20 pre-listed cases
CASES_NONIDEAL = [(P, c, 30.) for P in [(3., 2.), (6., 1.)] for c in ('free', 'endpoints')]


def instance(P, control, snr, ee, nonideal=False, K=1440):
    ch = a.Channel(*NONIDEAL) if nonideal else None
    xs = a.aligned_sites(M)
    mid = (M - N) // 2
    s2 = abs(a.z(xs[mid:mid + N], 0, 0, ch).sum()) ** 2 / N / 10 ** (snr / 10)
    eps = ee * a.LAM
    forced = (0, M - 1) if control == 'endpoints' else ()
    T = a.tables(xs, eps, P, K=K, ch=ch)
    SS = a.family(xs, N, eps, forced)
    _, ZD, ZP = a.endpoint_bank(xs, eps, P, ch)
    UU, EE = a.exact_bounds(SS, T, ZD, ZP, N, s2)
    SN = a.nominal_argmax(SS, T, N, s2)
    g = a.gcs(T, SS, UU, N, s2, SN, forced=forced, seed=2026)
    return dict(xs=xs, s2=s2, eps=eps, T=T, SS=SS, UU=UU, EE=EE, SN=SN, g=g, P=P, ch=ch)


def index_of(SS, S):
    return int(np.flatnonzero(np.all(SS == np.asarray(S), axis=1))[0])


# ---------------------------------------------------------------- R002
def r002_job(job):
    P, control, snr, ee, nonideal, ndraw = job
    I = instance(P, control, snr, ee, nonideal)
    xs, eps, T, SS, s2, ch = I['xs'], I['eps'], I['T'], I['SS'], I['s2'], I['ch']
    rng = np.random.default_rng(zlib.crc32(repr((P, control, snr, ee, nonideal)).encode()))
    layouts = {'S_hat': I['g']['S_hat'], 'S_nom': I['SN']}
    for k, idx in enumerate(rng.choice(len(SS), 2, replace=False)):
        layouts['rand%d' % k] = SS[idx]
    D = np.vstack([rng.uniform(-eps, eps, (ndraw, N)), eps * CORNERS])
    rows = []
    for name, S in layouts.items():
        slnr, GD, IP = a.exact_at(xs, S, D, P, N, s2, ch)
        L = float(a.cert(S, T, N, s2)[0])
        gd = float(T['cD'][S].sum()) ** 2 / N
        Ib = a.leakage_upper(S, T, N)
        UH = float(I['UU'][index_of(SS, S)])
        rows.append(dict(layout=name, L=L, min_slnr=float(slnr.min()), U_H=UH,
                         rel_L=(L - float(slnr.min())) / L, rel_GD=(gd - float(GD.min())) / gd,
                         rel_IP=(float(IP.max()) - Ib) / Ib, L_over_UH=L / UH))
    ok = all(r['rel_L'] <= TOL and r['rel_GD'] <= TOL and r['rel_IP'] <= TOL and r['L_over_UH'] <= 1 + TOL for r in rows)
    return dict(P=P, control=control, snr=snr, eps=ee, nonideal=nonideal, ok=ok, rows=rows)


# ---------------------------------------------------------------- R003
def r003():
    rng = np.random.default_rng(7)
    xs = a.aligned_sites(M)
    worst, H, n = 0.0, 0, 0
    for nonideal in (False, True):
        ch = a.Channel(*NONIDEAL) if nonideal else None
        for P in LISTED:
            for ee in EPS[1:]:
                eps = ee * a.LAM
                signs, ZD, ZP = a.endpoint_bank(xs, eps, P, ch)
                H = max(H, signs.shape[1])
                SS = a.family(xs, N, eps)
                pick = SS[rng.choice(len(SS), 40, replace=False)]
                _, EE = a.bank_bounds(pick, ZD, ZP, N, 1.0)
                for S, e in zip(pick, EE):
                    ex = float((abs(a.z(xs[S][None] + eps * CORNERS, *P, ch).sum(1)) ** 2).max() / N)
                    worst = max(worst, abs(e - ex) / ex)
                    n += 1
    return dict(n_layouts=n, max_rel_diff=worst, max_templates=H, ok=bool(worst <= 1e-12 and H <= 2 * M))


# ---------------------------------------------------------------- R004
def r004_job(job):
    P, control, snr = job
    I = instance(P, control, snr, 0.0)
    xs, T, SS, s2, SN, g = I['xs'], I['T'], I['SS'], I['s2'], I['SN'], I['g']
    nomN = float(a.nominal(SN, T, N, s2)[0])
    nomH = float(a.nominal(g['S_hat'], T, N, s2)[0])
    rel = lambda v: abs(v - nomN) / nomN
    U_nom = a.witnesses(xs, SN, 0.0, P, N, s2)[0]
    same = bool(np.array_equal(g['S_hat'], SN))
    r = dict(P=P, control=control, snr=snr, same_layout=same, tie=bool(not same and nomH == nomN),
             rel_Lhat=rel(g['L_hat']), rel_nom_hat=rel(nomH), rel_L_nom=rel(float(a.cert(SN, T, N, s2)[0])),
             rel_UH_nom=rel(float(I['UU'][index_of(SS, SN)])), rel_U_nom=rel(U_nom),
             Gamma=g['L_hat'] / U_nom - 1, global_gap=g['U_star'] / g['L_hat'] - 1, unique=g['unique'])
    # exact identities on one arithmetic path: L = U_H = U = nominal, Gamma = global gap = 0
    r['ok'] = bool((same or r['tie']) and max(r['rel_Lhat'], r['rel_nom_hat'], r['rel_L_nom'], r['rel_UH_nom'], r['rel_U_nom']) == 0
                   and r['Gamma'] == 0 and r['global_gap'] == 0)
    return r


# ---------------------------------------------------------------- R005
def r005_job(job):
    P, control, snr, ee = job
    I = instance(P, control, snr, ee)
    xs, eps, s2 = I['xs'], I['eps'], I['s2']
    TK = {K: a.tables(xs, eps, P, K=K) for K in (720, 1440, 5760)}
    bound = 1 / math.cos(math.pi / 720) ** 2
    out = dict(P=P, control=control, snr=snr, eps=ee, ok=True)
    for name, S in (('S_hat', I['g']['S_hat']), ('S_nom', I['SN'])):
        LK = {K: float(a.cert(S, T, N, s2)[0]) for K, T in TK.items()}
        ratio = max(LK.values()) / min(LK.values())
        cmin = float(a.exact_at(xs, S, eps * CORNERS, P, N, s2)[0].min())
        out[name] = dict(L=LK, ratio=ratio, corner_min=cmin)
        out['ok'] &= bool(ratio <= bound * (1 + 1e-12) and LK[720] <= cmin * (1 + TOL))
    out['sec2_bound'] = bound
    return out


def guards():
    xs = a.aligned_sites(M)
    thr = (np.diff(xs).min() - a.D_MIN) / 2 / a.LAM
    sizes = {ee: int(len(a.family(xs, N, ee * a.LAM))) for ee in (0.0911, 0.0912, 0.095, 0.1)}
    p0 = a.psi(xs, 0, 0)
    bd = lambda e: max((a.psi(xs + e, 0, 0) - p0).max(), (p0 - a.psi(xs - e, 0, 0)).max())
    lo, hi = 0.0, 0.5 * a.LAM
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if bd(mid) < np.pi / 2 else (lo, mid)
    eps_beta = 0.5 * (lo + hi)

    def raises(fn):
        try:
            fn()
            return False
        except ValueError:
            return True
    bad = xs.copy()
    bad[5] += 1e-4
    r = dict(clearance_threshold_over_lambda=thr, family_sizes=sizes, full=comb(M, N), eps_beta_over_lambda=eps_beta / a.LAM,
             beta_raises_above=raises(lambda: a.tables(xs, 1.01 * eps_beta, (3., 2.))),
             beta_ok_below=not raises(lambda: a.tables(xs, 0.99 * eps_beta, (3., 2.))),
             misaligned_raises=raises(lambda: a.tables(bad, 0.01 * a.LAM, (3., 2.))))
    r['ok'] = bool(sizes[0.0911] == comb(M, N) and sizes[0.0912] < comb(M, N) and sizes[0.1] <= sizes[0.095] < sizes[0.0911]
                   and r['beta_raises_above'] and r['beta_ok_below'] and r['misaligned_raises'])
    return r


# ---------------------------------------------------------------- R006
def r006():
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
    cmd = [sys.executable, 'run_main.py', '--geoms', '3,2;6,1;0,0', '--eps', '0,0.03,0.08', '--snr', '10,30', '--workers', '3']
    rows = {}
    for tag in 'ab':
        out = 'results/repro_%s.csv' % tag
        subprocess.run(cmd + ['--out', out], cwd=HERE, env=env, check=True, capture_output=True)
        with open(HERE / out) as f:
            rows[tag] = [{k: v for k, v in r.items() if 'seconds' not in k} for r in csv.DictReader(f)]  # drop timing
    return dict(n_rows=len(rows['a']), ok=bool(len(rows['a']) > 0 and rows['a'] == rows['b']))


# ---------------------------------------------------------------- R007 (independent implementation)
class Ext:
    """Scalar backend: mpmath at `dps` digits if available, else float64 (math)."""

    def __init__(self, dps=50):
        try:
            import mpmath
            mpmath.mp.dps = dps
            self.f, self.sqrt, self.cos, self.sin, self.pi = mpmath.mpf, mpmath.sqrt, mpmath.cos, mpmath.sin, mpmath.pi
            self.atan2, self.floor = mpmath.atan2, mpmath.floor
            self.name = 'mpmath %s, dps=%d' % (mpmath.__version__, dps)
        except ImportError:
            self.f, self.sqrt, self.cos, self.sin, self.pi = float, math.sqrt, math.cos, math.sin, math.pi
            self.atan2, self.floor = math.atan2, math.floor
            self.name = 'float64 (mpmath unavailable)'
        f = self.f
        self.lam = f(3) * 10 ** 8 / (f(28) * 10 ** 9)
        self.k0 = 2 * self.pi / self.lam
        self.d, self.neff, self.xf = f(3), f(144) / 100, f(-10)

    def R(self, x, P):
        return self.sqrt((x - P[0]) ** 2 + P[1] ** 2 + self.d ** 2)

    def psi(self, x, P):
        return self.k0 * (self.R(x, P) + self.neff * (x - self.xf))

    def wrap(self, t):
        return t - 2 * self.pi * self.floor(t / (2 * self.pi) + self.f(1) / 2)

    def zsum(self, xx, P):  # sum_n exp(-j psi) / R as (re, im)
        re = im = self.f(0)
        for x in xx:
            p, r = self.psi(x, P), self.R(x, P)
            re += self.cos(p) / r
            im -= self.sin(p) / r
        return re, im

    def slnr(self, xx, P, N, s2):
        dr, di = self.zsum(xx, (0, 0))
        pr, pi_ = self.zsum(xx, P)
        return (dr * dr + di * di) / (N * s2 + pr * pr + pi_ * pi_)

    def lower(self, xs, eps, P, N, s2, K):
        """Theorem 1 certificate from the paper formulas, with the float64 sites' residual D-misalignment included."""
        ref = self.psi(xs[0], (0, 0))
        c = self.f(0)
        for x in xs:
            o = self.wrap(self.psi(x, (0, 0)) - ref)
            lo = self.psi(x - eps, (0, 0)) - self.psi(x, (0, 0)) + o
            hi = self.psi(x + eps, (0, 0)) - self.psi(x, (0, 0)) + o
            beta = max(abs(lo), abs(hi))
            assert beta <= self.pi / 2
            c += self.cos(beta) / max(self.R(x - eps, (0, 0)), self.R(x + eps, (0, 0)))
        sec = []
        for x in xs:
            pp, pm = self.psi(x + eps, P), self.psi(x - eps, P)
            rmin = self.sqrt(P[1] ** 2 + self.d ** 2) if x - eps <= P[0] <= x + eps else min(self.R(x - eps, P), self.R(x + eps, P))
            sec.append((-(pp + pm) / 2, (pp - pm) / 2, 1 / rmin, 1 / max(self.R(x - eps, P), self.R(x + eps, P))))
        best = None
        for k in range(K):
            th = -self.pi + 2 * self.pi * k / K
            tot = self.f(0)
            for phi, half, amax, amin in sec:
                mc = self.cos(max(abs(self.wrap(th - phi)) - half, self.f(0)))
                tot += (amax if mc >= 0 else amin) * mc
            best = tot if best is None or tot > best else best
        B = max(best / self.cos(self.pi / K), self.f(0))
        return c * c / (N * s2 + B * B)

    def bank_upper(self, xs_all, S, eps, P, N, s2):
        """U_H(S): minimum exact SLNR over the <= 2M shared endpoint sign templates, rebuilt from scratch."""
        d = []
        for x in xs_all:
            p1, r1, p2, r2 = self.psi(x + eps, P), self.R(x + eps, P), self.psi(x - eps, P), self.R(x - eps, P)
            d.append(((self.cos(p1) / r1 - self.cos(p2) / r2) / 2, (-self.sin(p1) / r1 + self.sin(p2) / r2) / 2))
        tw = 2 * self.pi
        br = sorted({(self.atan2(di, dr) + s * self.pi / 2) % tw for dr, di in d for s in (1, -1)})
        mids = [(br[i] + (br[i + 1] if i + 1 < len(br) else br[0] + tw)) / 2 for i in range(len(br))]
        best = None
        for th in mids:
            ct, st = self.cos(th), self.sin(th)
            xx = [xs_all[n] + (eps if d[n][0] * ct + d[n][1] * st >= 0 else -eps) for n in S]
            v = self.slnr(xx, P, N, s2)
            best = v if best is None or v < best else best
        return best


def r007(dps=50):
    X = Ext(dps)
    P, snr, ee = (3., 2.), 30., 0.05
    out = dict(backend=X.name, cases={})
    ok = True
    for control in ('free', 'endpoints'):
        I = instance(P, control, snr, ee)
        xs, eps, s2, SS, UU, g = I['xs'], I['eps'], I['s2'], I['SS'], I['UU'], I['g']
        Sh, SN = g['S_hat'], I['SN']
        order = np.argsort(-UU)
        rivals = [SS[k] for k in order[:7] if not np.array_equal(SS[k], Sh)][:6]
        UN, dN, _, _ = a.witnesses(xs, SN, eps, P, N, s2, refine=4)
        xe = [X.f(float(v)) for v in xs]
        epse = X.f(float(eps))
        mid = (M - N) // 2
        dr, di = X.zsum(xe[mid:mid + N], (0, 0))
        s2e = (dr * dr + di * di) / N / 10 ** (X.f(snr) / 10)
        Le = X.lower([xe[n] for n in Sh], epse, P, N, s2e, 1440)
        UHe = [X.bank_upper(xe, [int(n) for n in S], epse, P, N, s2e) for S in rivals]
        assert all(abs(X.f(float(v))) <= epse for v in dN)
        UNe = X.slnr([xe[n] + X.f(float(v)) for n, v in zip(SN, dN)], (P[0], P[1]), N, s2e)
        rivalUH = [float(UU[index_of(SS, S)]) for S in rivals]
        c = dict(S_hat=Sh.tolist(), S_nom=SN.tolist(),
                 L_hat=(g['L_hat'], float(Le)), rel_L=float(abs(Le - g['L_hat']) / Le),
                 rival_UH=[(u, float(v)) for u, v in zip(rivalUH, UHe)],
                 max_rel_UH=max(float(abs(v - u) / v) for u, v in zip(rivalUH, UHe)),
                 U_nom=(UN, float(UNe)), rel_U_nom=float(abs(UNe - UN) / UNe),
                 margin=(g['margin'], float(Le - max(UHe[:5]))), margin_6th=float(Le - UHe[5]),
                 Gamma=(g['L_hat'] / UN - 1, float(Le / UNe - 1)))
        c['ok'] = bool(c['rel_L'] <= 1e-9 and c['max_rel_UH'] <= 1e-9 and c['rel_U_nom'] <= 1e-9
                       and (c['margin'][0] > 0) == (c['margin'][1] > 0) and (c['Gamma'][0] > 0) == (c['Gamma'][1] > 0))
        ok &= c['ok']
        out['cases'][control] = c
    out['ok'] = bool(ok and X.name.startswith('mpmath'))  # B0 requires extended precision
    return out


# ---------------------------------------------------------------- R008
def r008():
    dst = HERE / 'results' / 'crosscheck_bundle'
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)
    for f in BUNDLE.glob('a7_*.py'):
        shutil.copy(f, dst / f.name)
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
    for iy in range(3):
        subprocess.run([sys.executable, 'a7_grid.py', str(iy)], cwd=dst, env=env, check=True, capture_output=True)
    subprocess.run([sys.executable, 'a7_unit_checks.py'], cwd=dst, env=env, check=True, capture_output=True)
    new, old = [], []
    for iy in range(3):
        new += json.loads((dst / ('a7_grid_part%d.json' % iy)).read_text())
        old += json.loads((BUNDLE / ('a7_grid_part%d.json' % iy)).read_text())
    same_layouts = all(r['SN'] == q['SN'] and r['SR'] == q['SR'] for r, q in zip(new, old))
    max_rel = max(abs(r[k] - q[k]) / abs(q[k]) for r, q in zip(new, old) for k in ('LR', 'UN', 'UR'))
    counts = {fam: dict(n=sum(r['family'] == fam for r in new),
                        positive=sum(r['family'] == fam and r['gain'] > 1e-10 for r in new),
                        above5=sum(r['family'] == fam and r['gain'] > 0.05 for r in new)) for fam in ('free', 'matched')}
    unit_new = json.loads((dst / 'a7_unit_checks_results.json').read_text())
    unit_old = json.loads((BUNDLE / 'a7_unit_checks_results.json').read_text())
    unit_ok = all(unit_new[k] == unit_old[k] if isinstance(unit_old[k], int) else abs(unit_new[k] - unit_old[k]) <= 1e-12
                  for k in unit_old)
    return dict(rows=len(new), same_layouts=same_layouts, max_rel_diff=max_rel, counts=counts, unit_checks=unit_new,
                unit_checks_match=unit_ok,
                ok=bool(len(new) == len(old) == 264 and same_layouts and max_rel <= 1e-9 and unit_ok
                        and counts['matched'] == dict(n=132, positive=108, above5=79)))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--only', default='R002,R003,R004,R005,R006,R007,R008')
    p.add_argument('--ndraw', type=int, default=100000)
    p.add_argument('--workers', type=int, default=6)
    p.add_argument('--dps', type=int, default=50)
    p.add_argument('--out', default='results/m0_checks.json')
    args = p.parse_args()
    only = set(args.only.split(','))
    res = dict(date=time.strftime('%Y-%m-%d %H:%M:%S'), numpy=np.__version__)
    t0 = time.perf_counter()
    with Pool(args.workers) as pool:
        if 'R002' in only:
            jobs = [(P, c, snr, ee, False, args.ndraw) for P, c, snr in CASES for ee in EPS]
            jobs += [(P, c, snr, ee, True, args.ndraw) for P, c, snr in CASES_NONIDEAL for ee in EPS]
            rr = pool.map(r002_job, jobs)
            worst = {k: max(r[k] for x in rr for r in x['rows']) for k in ('rel_L', 'rel_GD', 'rel_IP', 'L_over_UH')}
            res['R002'] = dict(n_instances=len(rr), n_layout_checks=sum(len(x['rows']) for x in rr), draws=args.ndraw + 2 ** N,
                               worst=worst, failures=[x for x in rr if not x['ok']], ok=all(x['ok'] for x in rr))
        if 'R004' in only:
            rr = pool.map(r004_job, [(P, c, snr) for P in GEOMS for c in ('free', 'endpoints') for snr in (10., 20., 30., 40.)])
            res['R004_eps0'] = dict(n=len(rr), same_layout=sum(r['same_layout'] for r in rr), unique=sum(r['unique'] for r in rr),
                               worst=max(max(r['rel_Lhat'], r['rel_nom_hat'], r['rel_L_nom'], r['rel_UH_nom'], r['rel_U_nom']) for r in rr),
                               failures=[r for r in rr if not r['ok']], ok=all(r['ok'] for r in rr))
        if 'R005' in only:
            rr = pool.map(r005_job, [(P, c, snr, ee) for P, c, snr in CASES for ee in (0.03, 0.05, 0.08)])
            res['R004_K'] = dict(n=len(rr), max_ratio=max(max(r['S_hat']['ratio'], r['S_nom']['ratio']) for r in rr),
                               sec2_bound=rr[0]['sec2_bound'], failures=[r for r in rr if not r['ok']],
                               ok=all(r['ok'] for r in rr))
    if 'R003' in only:
        res['R003'] = r003()
    if 'R005' in only:
        res['R005'] = guards()
    if 'R006' in only:
        res['R006'] = r006()
    if 'R007' in only:
        res['R007'] = r007(args.dps)
    if 'R008' in only:
        res['R008'] = r008()
    res['seconds'] = time.perf_counter() - t0
    res['all_ok'] = all(v['ok'] for v in res.values() if isinstance(v, dict) and 'ok' in v)
    out = HERE / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=2, default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o)))
    for k, v in res.items():
        if isinstance(v, dict) and 'ok' in v:
            print(k, 'PASS' if v['ok'] else 'FAIL', {kk: vv for kk, vv in v.items() if kk not in ('failures', 'cases', 'unit_checks')})
    print('ALL PASS' if res['all_ok'] else 'SOME CHECKS FAILED', '%.0fs' % res['seconds'])
    sys.exit(0 if res['all_ok'] else 1)


if __name__ == '__main__':
    main()
