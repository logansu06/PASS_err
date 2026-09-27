"""R001: the ported GCS core must reproduce the GPT-6 Pro bundle's featured global audit."""
import json, sys
from pathlib import Path
import numpy as np
import a7_core as a

BUNDLE = Path(__file__).resolve().parents[2] / 'idea-stage/handoff/gpt6pro_bundle/bundle/a7_verification_bundle/a7_global_results.json'
ref = json.loads(BUNDLE.read_text())
M, N = 24, 8
xs = a.aligned_sites(M)
ee, snr, P = 0.05, 30, (3.0, 2.0)
eps = ee * a.LAM
ar = abs(a.z(xs[8:16], 0, 0).sum()) ** 2 / N
s2 = ar / 10 ** (snr / 10)
T = a.tables(xs, eps, P)
_, ZD, ZP = a.endpoint_bank(xs, eps, P)
ok = True
out = {}
for name, forced in [('free', ()), ('matched', (0, 23))]:
    SS = a.family(xs, N, eps, forced)
    UU, EE = a.bank_bounds(SS, ZD, ZP, N, s2)
    SN = SS[np.argmax(a.nominal(SS, T, N, s2))]
    g = a.gcs(T, SS, UU, N, s2, SN, forced=forced)
    UN = a.witnesses(xs, SN, eps, P, N, s2, refine=4)[0]
    mine = {'family_size': len(SS), 'certificate_optimum_subset': g['S_hat'].tolist(), 'certificate_optimum_L': g['L_hat'],
            'global_robust_SLNR_upper': g['U_star'], 'largest_other_layout_U': g['rival_U'],
            'strict_global_layout_dominance_margin': g['margin'], 'certified_gain_over_nominal': g['L_hat'] / UN - 1,
            'minimum_endpoint_worst_leakage_power': float(EE.min()), 'selected_leakage_upper_power': a.leakage_upper(g['S_hat'], T, N)}
    out[name] = mine
    for k, v in mine.items():
        r = ref[name][k]
        same = (v == r) if not isinstance(r, float) else abs(v - r) <= 1e-12 * max(1.0, abs(r))
        ok &= same
        print(f"{name:8s} {k:42s} port={v}  bundle={r}  {'OK' if same else 'MISMATCH'}")
print('R001', 'PASS' if ok else 'FAIL')
json.dump({'pass': ok, 'port': out}, open(Path(__file__).parent / 'results/r001_port_check.json', 'w'), indent=2, default=float)
sys.exit(0 if ok else 1)
