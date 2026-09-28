"""R019 (M4): numbers table — every number quoted in refine-logs/EXPERIMENT_RESULTS.md, traced to a result file.

For each entry: (1) the quoted string must occur in EXPERIMENT_RESULTS.md, (2) the value is read from its source file by
key (never re-derived here), (3) the quote must be consistent with it:
  round  — the quote equals the value rounded to the quote's own precision (a trailing % means value x 100);
  kn     — the quote "k/n" equals the stored count;
  le/ge  — the value is <= / >= the quoted bound (e.g. "within 1.14%").
Writes results/r019_numbers.md (human table) and results/r019_numbers.json (id/value/source/cited records, the input
schema of the ARIS evidence pre-check). Exit 1 if any entry fails.
"""
import json, sys
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES = HERE / 'results'
DOC = HERE.parents[1] / 'refine-logs' / 'EXPERIMENT_RESULTS.md'
_J = {}


def js(fn):
    if fn not in _J:
        _J[fn] = json.loads((RES / fn).read_text(encoding='utf-8'))
    return _J[fn]


def kp(fn, *path):
    def f():
        o = js(fn)
        for p in path:
            o = o[p]
        return o
    f.src = fn
    f.key = '.'.join(map(str, path))
    return f


def lim(control, xp, yp, eps, field):
    def f():
        for r in js(MM)['limits']:
            if (r['control'], r['xP'], r['yP'], r['eps_over_lambda']) == (control, xp, yp, eps):
                return r[field]
        raise KeyError((control, xp, yp, eps))
    f.src = MM
    f.key = 'limits[%s,(%g,%g),%g].%s' % (control, xp, yp, eps, field)
    return f


def jb(i, field):
    f = lambda: js(MM)['joint_box'][i][field]
    f.src, f.key = MM, 'joint_box[%d].%s' % (i, field)
    return f


def mo(fn, fnc, key, *path):
    """Value derived by a one-line expression on a stored value (documented in the key)."""
    base = kp(fn, *path)
    f = lambda: fnc(base())
    f.src, f.key = fn, key
    return f


MS, MM, M0, R9 = 'main_summary.json', 'm2m3_summary.json', 'm0_checks.json', 'r019_derived.json'
BL, NI, SC, MC = 'baselines', 'nonideal', 'scaling', 'mc_average'
F, E = 'free', 'endpoints'
ITEMS = [
    # ------------------------------------------------ M0
    ('M0', 'm0_R002_worst', '3.7e-16', 'round', kp(M0, 'R002', 'worst', 'rel_GD')),
    ('M0', 'm0_R003_maxdiff', '1.0e-15', 'round', kp(M0, 'R003', 'max_rel_diff')),
    ('M0', 'm0_R003_templates', '48', 'round', kp(M0, 'R003', 'max_templates')),
    ('M0', 'm0_R004_n', '272', 'round', kp(M0, 'R004_eps0', 'same_layout')),
    ('M0', 'm0_R004_Kratio', '1.0000187', 'round', kp(M0, 'R004_K', 'max_ratio')),
    ('M0', 'm0_R004_sec2', '1.0000190', 'round', kp(M0, 'R004_K', 'sec2_bound')),
    ('M0', 'm0_R005_thresh', '0.091110', 'round', kp(M0, 'R005', 'clearance_threshold_over_lambda')),
    ('M0', 'm0_R005_family', '660,858', 'round', kp(M0, 'R005', 'family_sizes', '0.0912')),
    ('M0', 'm0_R005_beta', '0.1704', 'round', kp(M0, 'R005', 'eps_beta_over_lambda')),
    ('M0', 'm0_R007_free_L', '56.559334', 'round', kp(M0, 'R007', 'cases', F, 'L_hat', 0)),
    ('M0', 'm0_R007_free_margin', '0.320874', 'round', kp(M0, 'R007', 'cases', F, 'margin', 0)),
    ('M0', 'm0_R007_free_margin6', '0.813', 'round', kp(M0, 'R007', 'cases', F, 'margin_6th')),
    ('M0', 'm0_R007_free_Gamma', '34.17%', 'round', kp(M0, 'R007', 'cases', F, 'Gamma', 0)),
    ('M0', 'm0_R007_end_L', '55.574007', 'round', kp(M0, 'R007', 'cases', E, 'L_hat', 0)),
    ('M0', 'm0_R007_end_margin', '0.046616', 'round', kp(M0, 'R007', 'cases', E, 'margin', 0)),
    ('M0', 'm0_R007_end_Gamma', '2.79%', 'round', kp(M0, 'R007', 'cases', E, 'Gamma', 0)),
    ('M0', 'm0_R007_maxrel', '2.7e-12', 'round', kp(M0, 'R007', 'cases', E, 'max_rel_UH')),
    ('M0', 'm0_R008_pos', '108/132', 'kn', mo(M0, lambda c: '%d/%d' % (c['positive'], c['n']), 'R008.counts.matched', 'R008', 'counts', 'matched')),
    ('M0', 'm0_R008_above5', '79/132', 'kn', mo(M0, lambda c: '%d/%d' % (c['above5'], c['n']), 'R008.counts.matched', 'R008', 'counts', 'matched')),
    ('M0', 'm0_R008_maxrel', '1.5e-15', 'round', kp(M0, 'R008', 'max_rel_diff')),
    ('M0', 'r019_audit_G_f64', '5.696860e-06', 'round', kp(R9, 'margin_audit', 'cases', 'min_positive_Gamma', 'Gamma', 'float64')),
    ('M0', 'r019_audit_G_ext', '5.696865e-06', 'round', kp(R9, 'margin_audit', 'cases', 'min_positive_Gamma', 'Gamma', 'extended')),
    ('M0', 'r019_audit_mrel', '4.738776e-05', 'round', kp(R9, 'margin_audit', 'cases', 'min_relative_uniqueness_margin', 'margin', 'extended')),
    ('M0', 'r019_audit_mabs', '3.943808e-05', 'round', kp(R9, 'margin_audit', 'cases', 'min_absolute_uniqueness_margin', 'margin', 'extended')),
    # ------------------------------------------------ C1 main grid
    ('C1', 'gate_kn', '297/528', 'kn', mo(R9, lambda c: '%d/%d' % (c['k'], c['n']), 'counts.endpoints.gamma_above5', 'counts', E, 'gamma_above5')),
    ('C1', 'gate_frac', '56.25%', 'round', kp(MS, 'gate', 'fraction')),
    ('C1', 'free_pos', '87.5%', 'round', kp(MS, 'overall', F, 'pos')),
    ('C1', 'free_pos_k', '(462)', 'kn', mo(R9, lambda c: '(%d)' % c['k'], 'counts.free.gamma_pos.k', 'counts', F, 'gamma_pos')),
    ('C1', 'free_above5', '61.9%', 'round', kp(MS, 'overall', F, 'above5')),
    ('C1', 'free_above5_k', '(327)', 'kn', mo(R9, lambda c: '(%d)' % c['k'], 'counts.free.gamma_above5.k', 'counts', F, 'gamma_above5')),
    ('C1', 'free_median', '11.3%', 'round', kp(MS, 'overall', F, 'median')),
    ('C1', 'free_q25', '1.6', 'round', mo(MS, lambda v: 100 * v, 'overall.free.q25 x100', 'overall', F, 'q25')),
    ('C1', 'free_q75', '27.6', 'round', mo(MS, lambda v: 100 * v, 'overall.free.q75 x100', 'overall', F, 'q75')),
    ('C1', 'free_inconcl', '12.5%', 'round', kp(MS, 'overall', F, 'inconclusive')),
    ('C1', 'free_inconcl_k', '(66)', 'kn', mo(R9, lambda c: '(%d)' % c['k'], 'counts.free.inconclusive.k', 'counts', F, 'inconclusive')),
    ('C1', 'free_sacr', '0.16%', 'round', kp(MS, 'overall', F, 'sacrifice_median')),
    ('C1', 'end_pos', '82.8%', 'round', kp(MS, 'overall', E, 'pos')),
    ('C1', 'end_pos_k', '(437)', 'kn', mo(R9, lambda c: '(%d)' % c['k'], 'counts.endpoints.gamma_pos.k', 'counts', E, 'gamma_pos')),
    ('C1', 'end_median', '6.9%', 'round', kp(MS, 'overall', E, 'median')),
    ('C1', 'end_q25', '0.5', 'round', mo(MS, lambda v: 100 * v, 'overall.endpoints.q25 x100', 'overall', E, 'q25')),
    ('C1', 'end_q75', '19.4', 'round', mo(MS, lambda v: 100 * v, 'overall.endpoints.q75 x100', 'overall', E, 'q75')),
    ('C1', 'end_inconcl', '17.2%', 'round', kp(MS, 'overall', E, 'inconclusive')),
    ('C1', 'end_inconcl_k', '(91)', 'kn', mo(R9, lambda c: '(%d)' % c['k'], 'counts.endpoints.inconclusive.k', 'counts', E, 'inconclusive')),
    ('C1', 'end_sacr', '0.32%', 'round', kp(MS, 'overall', E, 'sacrifice_median')),
    ('C1', 'xP_free_pos', '96.25%', 'round', kp(R9, 'xP_nonzero', F, 'gamma_pos')),
    ('C1', 'xP_free_above5', '68.1%', 'round', kp(R9, 'xP_nonzero', F, 'gamma_above5')),
    ('C1', 'xP_free_med', '14.2%', 'round', kp(R9, 'xP_nonzero', F, 'gamma_median')),
    ('C1', 'xP_free_inc', '3.75%', 'round', mo(R9, lambda v: 1 - v, '1 - xP_nonzero.free.gamma_pos', 'xP_nonzero', F, 'gamma_pos')),
    ('C1', 'xP_end_pos', '91.0%', 'round', kp(R9, 'xP_nonzero', E, 'gamma_pos')),
    ('C1', 'xP_end_above5', '61.9%', 'round', kp(R9, 'xP_nonzero', E, 'gamma_above5')),
    ('C1', 'xP_end_med', '8.9%', 'round', kp(R9, 'xP_nonzero', E, 'gamma_median')),
    ('C1', 'xP_end_inc', '9.0%', 'round', mo(R9, lambda v: 1 - v, '1 - xP_nonzero.endpoints.gamma_pos', 'xP_nonzero', E, 'gamma_pos')),
    ('C1', 'eps001_free_pos', '86%', 'round', kp(MS, 'by_eps', F, '0.01', 'pos')),
    ('C1', 'eps001_end_pos', '77%', 'round', kp(MS, 'by_eps', E, '0.01', 'pos')),
    ('C1', 'eps001_free_a5', '42%', 'round', kp(MS, 'by_eps', F, '0.01', 'above5')),
    ('C1', 'eps001_end_a5', '30%', 'round', kp(MS, 'by_eps', E, '0.01', 'above5')),
    ('C1', 'eps005_free_a5', '70%', 'round', kp(MS, 'by_eps', F, '0.05', 'above5')),
    ('C1', 'eps005_end_a5', '70%', 'round', kp(MS, 'by_eps', E, '0.05', 'above5')),
    ('C1', 'eps005_free_med', '15.9%', 'round', kp(MS, 'by_eps', F, '0.05', 'median')),
    ('C1', 'eps005_end_med', '11.6%', 'round', kp(MS, 'by_eps', E, '0.05', 'median')),
    ('C1', 'eps008_free_pos', '85%', 'round', kp(MS, 'by_eps', F, '0.08', 'pos')),
    ('C1', 'eps008_end_a5', '66%', 'round', kp(MS, 'by_eps', E, '0.08', 'above5')),
    ('C1', 'snr10_free_a5', '25%', 'round', kp(MS, 'by_snr', F, '10.0', 'above5')),
    ('C1', 'snr10_end_a5', '27%', 'round', kp(MS, 'by_snr', E, '10.0', 'above5')),
    ('C1', 'snr10_free_med', '1.6%', 'round', kp(MS, 'by_snr', F, '10.0', 'median')),
    ('C1', 'snr10_end_med', '1.1%', 'round', kp(MS, 'by_snr', E, '10.0', 'median')),
    ('C1', 'snr40_free_a5', '83%', 'round', kp(MS, 'by_snr', F, '40.0', 'above5')),
    ('C1', 'snr40_end_a5', '75%', 'round', kp(MS, 'by_snr', E, '40.0', 'above5')),
    ('C1', 'snr40_free_med', '27.6%', 'round', kp(MS, 'by_snr', F, '40.0', 'median')),
    ('C1', 'snr40_end_med', '17.2%', 'round', kp(MS, 'by_snr', E, '40.0', 'median')),
    ('C1', 'snr40_free_sacr', '3.7%', 'round', kp(MS, 'by_snr', F, '40.0', 'sacrifice_median')),
    ('C1', 'snr40_end_sacr', '9.2%', 'round', kp(MS, 'by_snr', E, '40.0', 'sacrifice_median')),
    ('C1', 'PeqD_med', '−12%', 'round', kp(MS, 'control_P_eq_D', F, 'median')),
    ('C1', 'mech_n', 'n = 899', 'kn', mo(R9, lambda v: 'n = %d' % v, 'mechanism_gamma_pos.pooled.n', 'mechanism_gamma_pos', 'pooled', 'n')),
    ('C1', 'mech_desired', '1.000', 'round', kp(R9, 'mechanism_gamma_pos', 'pooled', 'desired_ratio_at_witness_median')),
    ('C1', 'mech_leak', '0.79', 'round', kp(R9, 'mechanism_gamma_pos', 'pooled', 'leakage_ratio_at_witness_median')),
    ('C1', 'mech_cert_kn', '893/899', 'kn', mo(R9, lambda c: '%d/%d' % (c['k'], c['n']), 'mechanism_gamma_pos.pooled.certified_leakage_lower',
                                            'mechanism_gamma_pos', 'pooled', 'certified_leakage_lower')),
    ('C1', 'mech_cert_frac', '99.3%', 'round', kp(R9, 'mechanism_gamma_pos', 'pooled', 'certified_leakage_lower', 'frac')),
    ('C1', 'mech_cert_ratio', '0.80', 'round', kp(R9, 'mechanism_gamma_pos', 'pooled', 'certified_leakage_ratio_median')),
    ('C1', 'mech_cert_free', '0.77', 'round', kp(R9, 'mechanism_gamma_pos', F, 'certified_leakage_ratio_median')),
    ('C1', 'mech_cert_end', '0.83', 'round', kp(R9, 'mechanism_gamma_pos', E, 'certified_leakage_ratio_median')),
    ('C1', 'mech_cert_desired', '0.9999', 'round', kp(R9, 'mechanism_gamma_pos', 'pooled', 'certified_desired_ratio_median')),
    ('C1', 'sacr_pooled_med', '0.22%', 'round', kp(R9, 'nominal_sacrifice', 'pooled', 'median')),
    ('C1', 'sacr_p90', '13.5%', 'round', kp(R9, 'nominal_sacrifice', 'pooled', 'p90')),
    ('C1', 'sacr_p90_free', '8.7%', 'round', kp(R9, 'nominal_sacrifice', F, 'p90')),
    ('C1', 'sacr_p90_end', '21.9%', 'round', kp(R9, 'nominal_sacrifice', E, 'p90')),
    ('C1', 'sacr_max', '88.5%', 'round', kp(R9, 'nominal_sacrifice', 'pooled', 'max')),
    ('C1', 'maxcase_nomN', '9,997', 'round', kp(R9, 'nominal_sacrifice', 'max_case', 'nom_slnr_nom')),
    ('C1', 'maxcase_UN', '2.09', 'round', kp(R9, 'nominal_sacrifice', 'max_case', 'U_nom')),
    ('C1', 'maxcase_nomR', '1,147', 'round', kp(R9, 'nominal_sacrifice', 'max_case', 'nom_slnr_hat')),
    ('C1', 'maxcase_L', '3.02', 'round', kp(R9, 'nominal_sacrifice', 'max_case', 'L_hat')),
    ('C1', 'maxcase_G', '+44.5%', 'round', kp(R9, 'nominal_sacrifice', 'max_case', 'Gamma')),
    ('C1', 'inc_total', '157', 'round', kp(R9, 'inconclusive', 'total')),
    ('C1', 'inc_xP0', '96/96', 'kn', mo(R9, lambda d: '%d/%d' % (d['at_xP0'], d['n_xP0']), 'inconclusive.at_xP0/n_xP0', 'inconclusive')),
    ('C1', 'inc_other', '61', 'round', kp(R9, 'inconclusive', 'other')),
    ('C1', 'inc_other_end', '43', 'round', kp(R9, 'inconclusive', 'other_by_control', E)),
    ('C1', 'inc_other_free', '18', 'round', kp(R9, 'inconclusive', 'other_by_control', F)),
    ('C1', 'inc_other_med', '−0.19%', 'round', kp(R9, 'inconclusive', 'other_gamma_median')),
    ('C1', 'inc_other_min', '−11%', 'round', kp(R9, 'inconclusive', 'other_gamma_min')),
    ('C1', 'inc_same', '46%', 'round', kp(R9, 'inconclusive', 'other_same_layout')),
    ('C1', 'inc_eps001', '24', 'round', kp(R9, 'inconclusive', 'other_by_eps', '0.01')),
    ('C1', 'inc_eps008', '20', 'round', kp(R9, 'inconclusive', 'other_by_eps', '0.08')),
    ('C1', 'xP0_UL_med', '1.09', 'round', kp(R9, 'inconclusive', 'xP0_bracket_hat_median')),
    ('C1', 'xP0_UL_max', '1.73', 'round', kp(R9, 'inconclusive', 'xP0_bracket_hat_max')),
    ('C1', 'cap_full', '64', 'round', kp(R9, 'counts', 'capped_full_grid', 'total')),
    ('C1', 'cap_full_PD', '16', 'round', kp(R9, 'counts', 'capped_full_grid', 'P_eq_D')),
    # ------------------------------------------------ C2
    ('C2', 'unique_free', '38.6%', 'round', kp(MS, 'overall', F, 'unique')),
    ('C2', 'unique_free_kn', '204/528', 'kn', mo(R9, lambda c: '%d/%d' % (c['k'], c['n']), 'counts.free.unique', 'counts', F, 'unique')),
    ('C2', 'unique_end', '45.3%', 'round', kp(MS, 'overall', E, 'unique')),
    ('C2', 'unique_end_kn', '239/528', 'kn', mo(R9, lambda c: '%d/%d' % (c['k'], c['n']), 'counts.endpoints.unique', 'counts', E, 'unique')),
    ('C2', 'unique_e001_f', '76%', 'round', kp(MS, 'by_eps', F, '0.01', 'unique')),
    ('C2', 'unique_e001_e', '80%', 'round', kp(MS, 'by_eps', E, '0.01', 'unique')),
    ('C2', 'unique_e008_f', '9%', 'round', kp(MS, 'by_eps', F, '0.08', 'unique')),
    ('C2', 'unique_e008_e', '15%', 'round', kp(MS, 'by_eps', E, '0.08', 'unique')),
    ('C2', 'gap_free', '0.51%', 'round', kp(MS, 'overall', F, 'global_gap_median')),
    ('C2', 'gap_end', '0.49%', 'round', kp(MS, 'overall', E, 'global_gap_median')),
    ('C2', 'LU_free', '99.49%', 'round', kp(R9, 'counts', F, 'median_L_over_Ustar')),
    ('C2', 'LU_end', '99.51%', 'round', kp(R9, 'counts', E, 'median_L_over_Ustar')),
    ('C2', 'gapmax_free', '74.5%', 'round', kp(MS, 'overall', F, 'global_gap_max')),
    ('C2', 'gapmax_end', '73.9%', 'round', kp(MS, 'overall', E, 'global_gap_max')),
    ('C2', 'surv_free', '70', 'round', kp(MS, 'overall', F, 'survivors_median')),
    ('C2', 'surv_end', '15', 'round', kp(MS, 'overall', E, 'survivors_median')),
    ('C2', 'survfrac_free', '0.0095%', 'round', kp(MS, 'overall', F, 'survivor_frac_median')),
    ('C2', 'survfrac_end', '0.020%', 'round', kp(MS, 'overall', E, 'survivor_frac_median')),
    ('C2', 'gcs_free', '0.20 s', 'round', kp(MS, 'overall', F, 'gcs_seconds_median')),
    ('C2', 'gcs_end', '0.12 s', 'round', kp(MS, 'overall', E, 'gcs_seconds_median')),
    ('C2', 'gcs_max', '7.3 s', 'round', kp(MS, 'overall', F, 'gcs_seconds_max')),
    ('C2', 'incl_free', '3.9 s', 'round', kp(R9, 'runtime', F, 'inclusive_median')),
    ('C2', 'incl_end', '0.55 s', 'round', kp(R9, 'runtime', E, 'inclusive_median')),
    ('C2', 'incl_max', '11.5 s', 'round', kp(R9, 'runtime', F, 'inclusive_max')),
    ('C2', 'swap_free', '77.7%', 'round', kp(MS, 'overall', F, 'selection_gap_pos')),
    ('C2', 'swap_free_kn', '373/480', 'kn', mo(R9, lambda c: '%d/%d' % (c['k'], c['n']), 'counts.swap_below_exact.free', 'counts', 'swap_below_exact', F)),
    ('C2', 'swap_end', '59.1%', 'round', kp(MS, 'overall', E, 'selection_gap_pos')),
    ('C2', 'swap_end_kn', '312/528', 'kn', mo(R9, lambda c: '%d/%d' % (c['k'], c['n']), 'counts.swap_below_exact.endpoints', 'counts', 'swap_below_exact', E)),
    ('C2', 'swap_med_free', '0.92%', 'round', kp(MS, 'overall', F, 'selection_gap_median')),
    ('C2', 'swap_med_end', '0.29%', 'round', kp(MS, 'overall', E, 'selection_gap_median')),
    ('C2', 'swap_max_free', '24.3%', 'round', kp(MS, 'overall', F, 'selection_gap_max')),
    ('C2', 'swap_max_end', '25.9%', 'round', kp(MS, 'overall', E, 'selection_gap_max')),
    ('C2', 'swap_pooled_n', '1,008', 'round', kp(R9, 'selection_gap_pooled', 'n_exact')),
    ('C2', 'swap_pooled_pos', '68%', 'round', kp(R9, 'selection_gap_pooled', 'positive')),
    ('C2', 'swap_pooled_med', '0.6%', 'round', kp(R9, 'selection_gap_pooled', 'median')),
    ('C2', 'swap_pooled_p90', '7.6%', 'round', kp(R9, 'selection_gap_pooled', 'p90')),
    ('C2', 'capped_free', '48', 'round', kp(MS, 'overall', F, 'capped')),
    ('C2', 'sc16_free_fam', '12,870', 'round', kp(MM, SC, '16|free', 'family')),
    ('C2', 'sc32_free_fam', '10,518,300', 'round', kp(MM, SC, '32|free', 'family')),
    ('C2', 'sc32_end_fam', '593,775', 'round', kp(MM, SC, '32|endpoints', 'family')),
    ('C2', 'sc24_free_surv', '276', 'round', kp(MM, SC, '24|free', 'survivors')),
    ('C2', 'sc32_free_surv', '608', 'round', kp(MM, SC, '32|free', 'survivors')),
    ('C2', 'sc16_free_frac', '7.8e-4', 'round', kp(MM, SC, '16|free', 'survivor_frac')),
    ('C2', 'sc32_free_frac', '5.8e-5', 'round', kp(MM, SC, '32|free', 'survivor_frac')),
    ('C2', 'sc32_free_tmed', '35.3', 'round', kp(MM, SC, '32|free', 't_med')),
    ('C2', 'sc32_free_tmax', '36.9', 'round', kp(MM, SC, '32|free', 't_max')),
    ('C2', 'sc32_gmax', '2.8', 'round', kp(MM, SC, '32|free', 'g_max')),
    # ------------------------------------------------ baselines
    ('A1', 'nom_free_pos', '89%', 'round', kp(MM, BL, 'free|all', 'nom_pos')),
    ('A1', 'nom_free_med', '17.6%', 'round', kp(MM, BL, 'free|all', 'nom_med')),
    ('A1', 'nom_end_med', '13.1%', 'round', kp(MM, BL, 'endpoints|all', 'nom_med')),
    ('A1', 'nom_xP_free_med', '20.2%', 'round', kp(MM, BL, 'free|x_P != 0', 'nom_med')),
    ('A1', 'nom_xP_end_med', '14.7%', 'round', kp(MM, BL, 'endpoints|x_P != 0', 'nom_med')),
    ('A1', 'cr_same_free', '8%', 'round', kp(MM, BL, 'free|all', 'cr_same')),
    ('A1', 'cr_same_end', '22%', 'round', kp(MM, BL, 'endpoints|all', 'cr_same')),
    ('A1', 'cr_same_xP_end', '24%', 'round', kp(MM, BL, 'endpoints|x_P != 0', 'cr_same')),
    ('A1', 'cr_L_free', '92%', 'round', kp(MM, BL, 'free|all', 'cr_L_strict')),
    ('A1', 'cr_L_end', '78%', 'round', kp(MM, BL, 'endpoints|all', 'cr_L_strict')),
    ('A1', 'cr_pos_free', '69%', 'round', kp(MM, BL, 'free|all', 'cr_pos')),
    ('A1', 'cr_pos_end', '51%', 'round', kp(MM, BL, 'endpoints|all', 'cr_pos')),
    ('A1', 'cr_pos_xP_free', '76%', 'round', kp(MM, BL, 'free|x_P != 0', 'cr_pos')),
    ('A1', 'cr_pos_xP_end', '56%', 'round', kp(MM, BL, 'endpoints|x_P != 0', 'cr_pos')),
    ('A1', 'cr_ref_free', '33%', 'round', kp(MM, BL, 'free|all', 'cr_refuted')),
    ('A1', 'cr_ref_end', '36%', 'round', kp(MM, BL, 'endpoints|all', 'cr_refuted')),
    ('A1', 'cr_ref_xP_end', '39%', 'round', kp(MM, BL, 'endpoints|x_P != 0', 'cr_refuted')),
    ('A1', 't_cr', '0.03 s', 'round', kp(MM, BL, 'free|all', 't_cr')),
    ('A1', 'gr_pos', '91%', 'round', kp(MM, BL, 'free|all', 'gr_pos')),
    ('A1', 'gr_xP_kn', '120/120', 'kn', mo(MM, lambda r: '%d/%d' % (round(r['gr_pos'] * r['n']), r['n']), 'baselines.free|x_P != 0.gr_pos x n',
                                            BL, 'free|x_P != 0')),
    ('A1', 'gr_med_free', '60%', 'round', kp(MM, BL, 'free|all', 'gr_med')),
    ('A1', 'gr_med_end', '146%', 'round', kp(MM, BL, 'endpoints|all', 'gr_med')),
    ('A1', 'gr_xP_med_free', '68%', 'round', kp(MM, BL, 'free|x_P != 0', 'gr_med')),
    ('A1', 'gr_xP_med_end', '159%', 'round', kp(MM, BL, 'endpoints|x_P != 0', 'gr_med')),
    # ------------------------------------------------ C3
    ('C3', 'ratio_max', '1.0113', 'round', kp(R9, 'limits', 'ratio_max')),
    ('C3', 'ratio_within', '1.14%', 'le', mo(R9, lambda v: v - 1, 'limits.ratio_max - 1', 'limits', 'ratio_max')),
    ('C3', 'ratio_above', '2/54', 'kn', mo(R9, lambda d: '%d/%d' % (d['n_ratio_above_1_01'], d['n']), 'limits.n_ratio_above_1_01/n', 'limits')),
    ('C3', 'Fend_32f_001', '5.08e-4', 'round', lim(F, 3.0, 2.0, 0.01, 'F_end')),
    ('C3', 'Fend_32f_005', '1.19e-2', 'round', lim(F, 3.0, 2.0, 0.05, 'F_end')),
    ('C3', 'Fend_32f_009', '3.57e-2', 'round', lim(F, 3.0, 2.0, 0.09, 'F_end')),
    ('C3', 'Fend_32e_005', '1.21e-2', 'round', lim(E, 3.0, 2.0, 0.05, 'F_end')),
    ('C3', 'Fend_32e_009', '3.59e-2', 'round', lim(E, 3.0, 2.0, 0.09, 'F_end')),
    ('C3', 'Fend_61f_001', '1.06e-4', 'round', lim(F, 6.0, 1.0, 0.01, 'F_end')),
    ('C3', 'Fend_61f_005', '2.39e-3', 'round', lim(F, 6.0, 1.0, 0.05, 'F_end')),
    ('C3', 'Fend_61f_009', '7.50e-3', 'round', lim(F, 6.0, 1.0, 0.09, 'F_end')),
    ('C3', 'Fend_61e_001', '1.17e-4', 'round', lim(E, 6.0, 1.0, 0.01, 'F_end')),
    ('C3', 'Fend_61e_009', '7.84e-3', 'round', lim(E, 6.0, 1.0, 0.09, 'F_end')),
    ('C3', 'Fend_01', '0.80', 'round', lim(F, 0.0, 1.0, 0.05, 'F_end')),
    ('C3', 'L_32f', '56.56', 'round', lim(F, 3.0, 2.0, 0.05, 'L_hat')),
    ('C3', 'U_32f', '56.58', 'round', lim(F, 3.0, 2.0, 0.05, 'U_star')),
    ('C3', 'U_32e', '55.60', 'round', lim(E, 3.0, 2.0, 0.05, 'U_star')),
    ('C3', 'L_61f', '219.0', 'round', lim(F, 6.0, 1.0, 0.05, 'L_hat')),
    ('C3', 'U_61f', '220.5', 'round', lim(F, 6.0, 1.0, 0.05, 'U_star')),
    ('C3', 'L_61e', '208.5', 'round', lim(E, 6.0, 1.0, 0.05, 'L_hat')),
    ('C3', 'U_01f', '1.11', 'round', lim(F, 0.0, 1.0, 0.05, 'U_star')),
    ('C3', 'U_01e', '1.10', 'round', lim(E, 0.0, 1.0, 0.05, 'U_star')),
    ('C3', 'G_32f', '+34.2%', 'round', lim(F, 3.0, 2.0, 0.05, 'Gamma')),
    ('C3', 'G_32e', '+2.8%', 'round', lim(E, 3.0, 2.0, 0.05, 'Gamma')),
    ('C3', 'G_61f', '+22.1%', 'round', lim(F, 6.0, 1.0, 0.05, 'Gamma')),
    ('C3', 'G_61e', '+40.7%', 'round', lim(E, 6.0, 1.0, 0.05, 'Gamma')),
    ('C3', 'G_01', '−17%', 'round', lim(F, 0.0, 1.0, 0.05, 'Gamma')),
    ('C3', 'growth_lo', '×67', 'ge', mo(R9, lambda g: min(v for k, v in g.items() if '(0,1)' not in k) + 0.5, 'min growth excl. (0,1), rounded',
                                        'limits', 'F_end_growth_001_to_009')),
    ('C3', 'growth_hi', '71', 'le', mo(R9, lambda g: max(v for k, v in g.items() if '(0,1)' not in k) - 0.5, 'max growth excl. (0,1), rounded',
                                       'limits', 'F_end_growth_001_to_009')),
    # ------------------------------------------------ non-ideal, MC, joint box
    ('A2', 'ni008_free_pos', '89%', 'round', kp(MM, NI, 'free|0.08 dB/m', 'pos')),
    ('A2', 'ni008_end_pos', '83%', 'round', kp(MM, NI, 'endpoints|0.08 dB/m', 'pos')),
    ('A2', 'ni008_free_a5', '60%', 'round', kp(MM, NI, 'free|0.08 dB/m', 'above5')),
    ('A2', 'ni008_free_med', '7.7%', 'round', kp(MM, NI, 'free|0.08 dB/m', 'median')),
    ('A2', 'ni008_end_med', '6.5%', 'round', kp(MM, NI, 'endpoints|0.08 dB/m', 'median')),
    ('A2', 'ni1_free_pos', '82%', 'round', kp(MM, NI, 'free|1 dB/m', 'pos')),
    ('A2', 'ni1_end_pos', '85%', 'round', kp(MM, NI, 'endpoints|1 dB/m', 'pos')),
    ('A2', 'ni1_free_med', '9.4%', 'round', kp(MM, NI, 'free|1 dB/m', 'median')),
    ('A2', 'ni1_end_med', '8.0%', 'round', kp(MM, NI, 'endpoints|1 dB/m', 'median')),
    ('A2', 'ni_ideal_end_gap', '1.00%', 'round', kp(MM, NI, 'endpoints|ideal', 'gap')),
    ('A2', 'ni008_xP', '94.2%', 'round', kp(R9, 'nonideal_xP_nonzero', '0.08 dB/m', 'pooled')),
    ('A2', 'ni008_xP_free', '97.5%', 'round', kp(R9, 'nonideal_xP_nonzero', '0.08 dB/m', F)),
    ('A2', 'ni008_xP_end', '90.8%', 'round', kp(R9, 'nonideal_xP_nonzero', '0.08 dB/m', E)),
    ('A4', 'mc_free', '0.9968', 'round', kp(MM, MC, 'free|all', 'mean_ratio_median')),
    ('A4', 'mc_end', '0.9958', 'round', kp(MM, MC, 'endpoints|all', 'mean_ratio_median')),
    ('A4', 'mc_loss_free', '0.32%', 'round', kp(R9, 'mc_mean_ratio', F, 'median_mean_loss')),
    ('A4', 'mc_loss_end', '0.42%', 'round', kp(R9, 'mc_mean_ratio', E, 'median_mean_loss')),
    ('A4', 'mc_max_free', '22.9%', 'round', kp(R9, 'mc_mean_ratio', F, 'max_mean_loss')),
    ('A4', 'mc_max_end', '15.0%', 'round', kp(R9, 'mc_mean_ratio', E, 'max_mean_loss')),
    ('A4', 'mc_p05_free', '77%', 'round', kp(MM, MC, 'free|all', 'p05_better')),
    ('A4', 'mc_p05_end', '55%', 'round', kp(MM, MC, 'endpoints|all', 'p05_better')),
    ('A4', 'mc_p05_ratio_end', '1.0006', 'round', kp(MM, MC, 'endpoints|all', 'p05_ratio_median')),
    ('A4', 'mc_min_free', '85%', 'round', kp(MM, MC, 'free|all', 'min_better')),
    ('A4', 'mc_min_end', '79%', 'round', kp(MM, MC, 'endpoints|all', 'min_better')),
    ('A3', 'jb_evals', '300,031', 'round', jb(0, 'n_eval')),
    ('A3', 'jb0_L', '0.839', 'round', jb(0, 'L_refined')),
    ('A3', 'jb0_gap_before', '0.730', 'round', jb(0, 'gap_before')),
    ('A3', 'jb0_gap_after', '0.305', 'round', jb(0, 'gap_after')),
    ('A3', 'jb0_closed', '51%', 'round', jb(0, 'gap_closed')),
    ('A3', 'jb2_closed', '61%', 'round', jb(2, 'gap_closed')),
    ('A3', 'jb2_G_after', '−0.089', 'round', jb(2, 'Gamma_after')),
]


def to_dec(s):
    t = s.replace(',', '').replace('−', '-').replace('+', '').replace('×', '').replace(' s', '').strip()
    pct = t.endswith('%')
    d = Decimal(t[:-1] if pct else t)
    tol = Decimal(5) * Decimal(10) ** (d.as_tuple().exponent - 1)
    return (d / 100, tol / 100) if pct else (d, tol)


def main():
    doc = DOC.read_text(encoding='utf-8')
    rows, bad = [], 0
    for group, cid, cited, mode, get in ITEMS:
        v = get()
        in_doc = cited in doc
        if mode == 'kn':
            ok = str(v) == cited
            shown = str(v)
        else:
            c, tol = to_dec(cited)
            x = Decimal(repr(float(v)))
            ok = {'round': abs(x - c) <= tol + Decimal('1e-15'), 'le': x <= c, 'ge': x >= c}[mode]
            shown = repr(float(v))
        ok = bool(ok and in_doc)
        bad += not ok
        rows.append(dict(group=group, id=cid, cited=cited, check=mode, in_doc=in_doc, value=shown, source='experiments/a7/results/' + get.src,
                         key=get.key, ok=ok))
    (RES / 'r019_numbers.json').write_text(json.dumps(rows, indent=1, ensure_ascii=False), encoding='utf-8')
    L = ['# R019 numbers table — EXPERIMENT_RESULTS.md vs result files', '',
         '%d quoted numbers; %d consistent; %d failing. Generated by `r019_numbers.py`.' % (len(rows), len(rows) - bad, bad), '',
         '| group | id | quoted | check | value in file | source : key | ok |', '|---|---|---|---|---|---|---|']
    for r in rows:
        L.append('| %s | %s | %s | %s | %s | `%s` : `%s` | %s |' % (r['group'], r['id'], r['cited'], r['check'], r['value'],
                                                             r['source'].split('/')[-1], r['key'], 'OK' if r['ok'] else '**FAIL**'))
    (RES / 'r019_numbers.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
    print('%d quoted numbers; %d consistent; %d failing' % (len(rows), len(rows) - bad, bad))
    for r in rows:
        if not r['ok']:
            print('FAIL', r)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
