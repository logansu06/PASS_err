import os
from dataclasses import replace

import numpy as np

import config
import design_delta_star
import pass_model as pm
import placement_baselines as pb
import plotters
import robustness
import theory_extensions as tx
import utils


def run_main_experiment(cfg, design_out, rng, logger, results_dir):
    eps_norm_list = cfg.epsilon_norm_list
    lam = design_out["lambda_m"]
    k0 = design_out["k0"]
    delta_star = design_out["delta_star"]
    xi = design_out["xi"]
    a_ideal = design_out["a_ideal"]
    phi_ref = design_out["phi_ref"]

    weights = tx.normalized_weights(delta_star, cfg.d)
    xi_mean = tx.weighted_mean(xi, weights)
    xi_max = np.max(np.abs(xi))
    epsilon_valid = (np.pi / 2) / (k0 * xi_max)
    epsilon_valid_norm = epsilon_valid / lam
    logger.info(
        "xi_max=%.6e, xi_mean=%.6e, epsilon_valid=%.6e m, epsilon_valid_norm=%.6e",
        xi_max,
        xi_mean,
        epsilon_valid,
        epsilon_valid_norm,
    )

    ideal_norm = np.ones_like(eps_norm_list)
    wc_norm_arr = np.zeros_like(eps_norm_list)
    split_norm_arr = np.zeros_like(eps_norm_list)
    common_bias_norm_arr = np.zeros_like(eps_norm_list)
    lb_full_norm_arr = np.zeros_like(eps_norm_list)
    lb_simpl_norm_arr = np.zeros_like(eps_norm_list)
    mc_mean_arr = np.zeros_like(eps_norm_list)
    mc_p05_arr = np.zeros_like(eps_norm_list)
    mc_p50_arr = np.zeros_like(eps_norm_list)
    mc_p95_arr = np.zeros_like(eps_norm_list)
    method_used_list = []
    reorder_flags = []
    delta_wc_all = []
    delta_split_all = []
    delta_common_all = []
    previous_wc_delta = np.zeros_like(delta_star)

    rows = []
    for idx, eps_norm in enumerate(eps_norm_list):
        eps = float(eps_norm * lam)
        split_delta = tx.split_error_vector(eps, xi, weights, delta_star=delta_star)
        common_delta = tx.common_bias_vector(eps, delta_star.size)

        mc_stats, reorder_mc = robustness.monte_carlo_stats(
            eps,
            delta_star,
            a_ideal,
            k0,
            cfg.d,
            cfg.n_eff,
            cfg.eta,
            cfg.mc.samples,
            rng,
            phi_ref,
        )
        mc_mean_arr[idx] = mc_stats["mean"]
        mc_p05_arr[idx] = mc_stats["p05"]
        mc_p50_arr[idx] = mc_stats["p50"]
        mc_p95_arr[idx] = mc_stats["p95"]

        wc_norm, delta_wc, method_used, reorder_wc = robustness.worst_case_gain(
            eps,
            delta_star,
            a_ideal,
            k0,
            cfg.d,
            cfg.n_eff,
            cfg.eta,
            cfg,
            rng,
            logger,
            phi_ref,
            extra_starts=[previous_wc_delta, split_delta, common_delta],
        )
        previous_wc_delta = delta_wc.copy()
        wc_norm_arr[idx] = wc_norm
        method_used_list.append(method_used)
        delta_wc_all.append(delta_wc)

        split_norm = (
            pm.array_gain(delta_star + split_delta, k0, cfg.d, cfg.n_eff, cfg.eta, phi_ref=phi_ref) / a_ideal
        )
        split_norm_arr[idx] = split_norm
        delta_split_all.append(split_delta)

        common_bias_norm = (
            pm.array_gain(delta_star + common_delta, k0, cfg.d, cfg.n_eff, cfg.eta, phi_ref=phi_ref) / a_ideal
        )
        common_bias_norm_arr[idx] = common_bias_norm
        delta_common_all.append(common_delta)

        lb = robustness.lower_bounds(
            eps,
            delta_star,
            xi,
            a_ideal,
            k0,
            cfg.d,
            cfg.n_eff,
            cfg.eta,
        )
        lb_full_norm_arr[idx] = lb["lb_full_norm"]
        lb_simpl_norm_arr[idx] = lb["lb_simpl_norm"]

        reorder_split = utils.detect_reorder(delta_star + split_delta)
        reorder_common = utils.detect_reorder(delta_star + common_delta)
        warn_reorder = reorder_mc or reorder_wc or reorder_split or reorder_common
        reorder_flags.append(int(warn_reorder))

        rows.append(
            {
                "eps_norm": float(eps_norm),
                "eps_m": eps,
                "a_ideal": a_ideal,
                "ideal_norm": 1.0,
                "wc_norm": wc_norm,
                "split_norm": split_norm,
                "common_bias_norm": common_bias_norm,
                "lb_full_norm": lb["lb_full_norm"],
                "lb_simpl_norm": lb["lb_simpl_norm"],
                "mc_mean": mc_stats["mean"],
                "mc_p05": mc_stats["p05"],
                "mc_p50": mc_stats["p50"],
                "mc_p95": mc_stats["p95"],
                "method_used": method_used,
                "warning_reorder": int(warn_reorder),
                "xi_max": lb["xi_max"],
                "xi_mean": xi_mean,
            }
        )

    delta_wc_all = np.array(delta_wc_all)
    delta_split_all = np.array(delta_split_all)
    delta_common_all = np.array(delta_common_all)
    utils.save_npz(
        os.path.join(results_dir, "delta_wc.npz"),
        delta_wc=delta_wc_all,
        delta_split=delta_split_all,
        delta_common=delta_common_all,
        epsilon_norm=eps_norm_list,
        indices=design_out["indices"],
        delta_star=delta_star,
    )
    utils.save_csv(
        os.path.join(results_dir, "data_main.csv"),
        fieldnames=[
            "eps_norm",
            "eps_m",
            "a_ideal",
            "ideal_norm",
            "wc_norm",
            "split_norm",
            "common_bias_norm",
            "lb_full_norm",
            "lb_simpl_norm",
            "mc_mean",
            "mc_p05",
            "mc_p50",
            "mc_p95",
            "method_used",
            "warning_reorder",
            "xi_max",
            "xi_mean",
        ],
        rows=rows,
    )

    curve_data = {
        "eps_norm": eps_norm_list,
        "ideal_norm": ideal_norm,
        "wc_norm": wc_norm_arr,
        "split_norm": split_norm_arr,
        "common_bias_norm": common_bias_norm_arr,
        "lb_full_norm": lb_full_norm_arr,
        "lb_simpl_norm": lb_simpl_norm_arr,
        "mc_mean": mc_mean_arr,
        "mc_p05": mc_p05_arr,
        "mc_p50": mc_p50_arr,
        "mc_p95": mc_p95_arr,
    }

    meta_text = (
        f"N={cfg.N}, d={cfg.d} m, f_c={cfg.f_c/1e9:.1f} GHz, "
        f"n_eff={cfg.n_eff:.2f}, delta_p={cfg.delta_p}"
    )
    plotters.plot_main(curve_data, epsilon_valid_norm, xi_max, meta_text, os.path.join(results_dir, "fig_main"))

    plotters.plot_xi_distribution(
        design_out["indices"], xi, xi_max, os.path.join(results_dir, "fig_xi_distribution")
    )

    return {
        "curve_data": curve_data,
        "epsilon_valid": epsilon_valid,
        "epsilon_valid_norm": epsilon_valid_norm,
        "xi_max": xi_max,
        "xi_mean": xi_mean,
        "rows": rows,
    }


def run_box_validation(cfg, design_out, rng, logger, results_dir):
    eps_norm_list = np.array(cfg.box_search.validation_eps_norm_list, dtype=float)
    lam = design_out["lambda_m"]
    k0 = design_out["k0"]
    delta_star = design_out["delta_star"]
    xi = design_out["xi"]
    a_ideal = design_out["a_ideal"]
    phi_ref = design_out["phi_ref"]
    weights = tx.normalized_weights(delta_star, cfg.d)

    previous_box_delta = np.zeros_like(delta_star)
    rows = []
    corner_curve = []
    split_curve = []
    box_curve = []

    for eps_norm in eps_norm_list:
        eps = float(eps_norm * lam)
        split_delta = tx.split_error_vector(eps, xi, weights, delta_star=delta_star)
        corner_norm, corner_delta, corner_reorder = robustness.corner_worst_case_gain(
            eps,
            delta_star,
            a_ideal,
            k0,
            cfg.d,
            cfg.n_eff,
            cfg.eta,
            logger,
            phi_ref,
        )
        box_norm, delta_box, method_used, box_reorder = robustness.worst_case_gain(
            eps,
            delta_star,
            a_ideal,
            k0,
            cfg.d,
            cfg.n_eff,
            cfg.eta,
            cfg,
            rng,
            logger,
            phi_ref,
            extra_starts=[previous_box_delta, split_delta, corner_delta],
        )
        previous_box_delta = delta_box.copy()
        split_norm = (
            pm.array_gain(delta_star + split_delta, k0, cfg.d, cfg.n_eff, cfg.eta, phi_ref=phi_ref) / a_ideal
        )

        rows.append(
            {
                "eps_norm": float(eps_norm),
                "eps_m": eps,
                "corner_norm": corner_norm,
                "split_norm": split_norm,
                "box_norm": box_norm,
                "corner_minus_box": corner_norm - box_norm,
                "split_minus_box": split_norm - box_norm,
                "method_used": method_used,
                "corner_reorder": int(corner_reorder),
                "box_reorder": int(box_reorder),
            }
        )
        corner_curve.append(corner_norm)
        split_curve.append(split_norm)
        box_curve.append(box_norm)

    utils.save_csv(
        os.path.join(results_dir, "data_box_validation.csv"),
        fieldnames=[
            "eps_norm",
            "eps_m",
            "corner_norm",
            "split_norm",
            "box_norm",
            "corner_minus_box",
            "split_minus_box",
            "method_used",
            "corner_reorder",
            "box_reorder",
        ],
        rows=rows,
    )
    plotters.plot_box_validation(
        {
            "eps_norm": eps_norm_list,
            "corner_norm": np.array(corner_curve),
            "split_norm": np.array(split_curve),
            "box_norm": np.array(box_curve),
        },
        os.path.join(results_dir, "fig_box_validation"),
    )
    return rows


def run_error_scenarios(cfg, design_out, rng, logger, results_dir):
    eps_norm_list = cfg.scenarios.epsilon_norm_list
    lam = design_out["lambda_m"]
    k0 = design_out["k0"]
    delta_star = design_out["delta_star"]
    xi = design_out["xi"]
    a_ideal = design_out["a_ideal"]
    phi_ref = design_out["phi_ref"]
    weights = tx.normalized_weights(delta_star, cfg.d)
    size = delta_star.size
    corr_len = cfg.scenarios.corr_length

    iid_mean = np.zeros_like(eps_norm_list)
    iid_approx = np.zeros_like(eps_norm_list)
    common_mean = np.zeros_like(eps_norm_list)
    common_approx = np.zeros_like(eps_norm_list)
    corr_mean = np.zeros_like(eps_norm_list)
    corr_approx = np.zeros_like(eps_norm_list)
    rows = []

    for idx, eps_norm in enumerate(eps_norm_list):
        eps = float(eps_norm * lam)
        sigma2 = eps**2 / 3.0

        iid_batch = tx.sample_iid_uniform(eps, size, cfg.scenarios.samples, rng)
        iid_stats = tx.scenario_stats(
            iid_batch,
            delta_star,
            a_ideal,
            k0,
            cfg.d,
            cfg.n_eff,
            cfg.eta,
            phi_ref,
        )
        iid_mean[idx] = iid_stats["mean"]
        iid_approx[idx] = tx.quadratic_expected_gain(k0, xi, weights, sigma2 * np.eye(size))

        common_batch = tx.sample_common_bias(eps, size, cfg.scenarios.samples, rng)
        common_stats = tx.scenario_stats(
            common_batch,
            delta_star,
            a_ideal,
            k0,
            cfg.d,
            cfg.n_eff,
            cfg.eta,
            phi_ref,
        )
        common_mean[idx] = common_stats["mean"]
        common_approx[idx] = tx.quadratic_expected_gain(k0, xi, weights, sigma2 * np.ones((size, size)))

        corr_batch = tx.sample_correlated_gaussian(sigma2, corr_len, size, cfg.scenarios.samples, rng)
        corr_stats = tx.scenario_stats(
            corr_batch,
            delta_star,
            a_ideal,
            k0,
            cfg.d,
            cfg.n_eff,
            cfg.eta,
            phi_ref,
        )
        corr_mean[idx] = corr_stats["mean"]
        corr_cov = tx.exponential_covariance(size, sigma2, corr_len)
        corr_approx[idx] = tx.quadratic_expected_gain(k0, xi, weights, corr_cov)

        for scenario_name, stats, approx in [
            ("iid_uniform", iid_stats, iid_approx[idx]),
            ("common_bias", common_stats, common_approx[idx]),
            ("correlated_gaussian", corr_stats, corr_approx[idx]),
        ]:
            rows.append(
                {
                    "scenario": scenario_name,
                    "eps_norm": float(eps_norm),
                    "eps_m": eps,
                    "mean": stats["mean"],
                    "p05": stats["p05"],
                    "p50": stats["p50"],
                    "p95": stats["p95"],
                    "quadratic_approx": approx,
                }
            )

    utils.save_csv(
        os.path.join(results_dir, "data_error_scenarios.csv"),
        fieldnames=["scenario", "eps_norm", "eps_m", "mean", "p05", "p50", "p95", "quadratic_approx"],
        rows=rows,
    )
    plotters.plot_error_scenarios(
        {
            "eps_norm": eps_norm_list,
            "iid_mean": iid_mean,
            "iid_approx": iid_approx,
            "common_mean": common_mean,
            "common_approx": common_approx,
            "corr_mean": corr_mean,
            "corr_approx": corr_approx,
        },
        os.path.join(results_dir, "fig_error_scenarios"),
    )
    logger.info("Completed stochastic scenario sweep with corr_length=%.2f", corr_len)
    return rows


def run_baseline_section(cfg, design_out, logger, results_dir):
    lam = design_out["lambda_m"]
    k0 = design_out["k0"]
    delta_star = design_out["delta_star"]
    eps_norm_list = cfg.baselines.epsilon_norm_list
    summary_eps_norm = cfg.baselines.summary_eps_norm

    uniform_delta = pb.uniform_aperture_from(delta_star)
    nominal_opt = pb.optimize_nominal_same_aperture(cfg, delta_star, k0, logger)

    placements = [
        {"placement": "aligned_constructive", "label": "Constructive aligned", "delta": delta_star},
        {"placement": "uniform_aperture", "label": "Uniform aperture", "delta": uniform_delta},
        {
            "placement": "nominal_opt_same_aperture",
            "label": "Direct nominal optimizer",
            "delta": nominal_opt["delta"],
        },
    ]

    curve_rows = []
    summary_rows = []
    box_curves = []
    iid_curves = []
    aligned_nominal_abs = None
    aligned_box_abs_ref = None
    aligned_iid_abs_ref = None

    for idx, entry in enumerate(placements):
        placement = entry["placement"]
        label = entry["label"]
        delta = entry["delta"]
        nominal_abs = pm.array_gain(delta, k0, cfg.d, cfg.n_eff, cfg.eta, None)
        xi = pm.xi_from_delta(delta, cfg.d, cfg.n_eff)
        weights = tx.normalized_weights(delta, cfg.d)
        rng = np.random.default_rng(cfg.random_seed + idx)
        previous_wc_delta = np.zeros_like(delta)

        box_abs_curve = []
        iid_abs_curve = []
        box_abs_ref = None
        iid_mean_abs_ref = None
        common_bias_abs_ref = None
        corr_mean_abs_ref = None

        for eps_norm in eps_norm_list:
            eps = float(eps_norm * lam)
            split_delta = tx.split_error_vector(eps, xi, weights, delta_star=delta)
            wc_norm, delta_wc, method_used, reorder_wc = robustness.worst_case_gain(
                eps,
                delta,
                nominal_abs,
                k0,
                cfg.d,
                cfg.n_eff,
                cfg.eta,
                cfg,
                rng,
                logger,
                None,
                extra_starts=[previous_wc_delta, split_delta],
            )
            previous_wc_delta = delta_wc.copy()
            iid_stats, reorder_mc = robustness.monte_carlo_stats(
                eps,
                delta,
                nominal_abs,
                k0,
                cfg.d,
                cfg.n_eff,
                cfg.eta,
                cfg.mc.samples,
                rng,
                None,
            )
            box_abs = nominal_abs * wc_norm
            iid_mean_abs = nominal_abs * iid_stats["mean"]
            box_abs_curve.append(box_abs)
            iid_abs_curve.append(iid_mean_abs)
            curve_rows.append(
                {
                    "placement": placement,
                    "eps_norm": float(eps_norm),
                    "eps_m": eps,
                    "nominal_abs": nominal_abs,
                    "box_norm": wc_norm,
                    "box_abs": box_abs,
                    "iid_mean_norm": iid_stats["mean"],
                    "iid_mean_abs": iid_mean_abs,
                    "method_used": method_used,
                    "warning_reorder": int(reorder_wc or reorder_mc),
                }
            )

            if abs(float(eps_norm) - summary_eps_norm) < 1e-12:
                box_abs_ref = box_abs
                iid_mean_abs_ref = iid_mean_abs

        summary_eps = float(summary_eps_norm * lam)
        common_batch = tx.sample_common_bias(summary_eps, delta.size, cfg.scenarios.samples, rng)
        common_stats = tx.scenario_stats(
            common_batch,
            delta,
            nominal_abs,
            k0,
            cfg.d,
            cfg.n_eff,
            cfg.eta,
            None,
        )
        common_bias_abs_ref = nominal_abs * common_stats["mean"]

        sigma2 = summary_eps**2 / 3.0
        corr_batch = tx.sample_correlated_gaussian(
            sigma2,
            cfg.scenarios.corr_length,
            delta.size,
            cfg.scenarios.samples,
            rng,
        )
        corr_stats = tx.scenario_stats(
            corr_batch,
            delta,
            nominal_abs,
            k0,
            cfg.d,
            cfg.n_eff,
            cfg.eta,
            None,
        )
        corr_mean_abs_ref = nominal_abs * corr_stats["mean"]

        if placement == "aligned_constructive":
            aligned_nominal_abs = nominal_abs
            aligned_box_abs_ref = box_abs_ref
            aligned_iid_abs_ref = iid_mean_abs_ref

        summary_rows.append(
            {
                "placement": placement,
                "label": label,
                "nominal_abs": nominal_abs,
                "box_abs_ref": box_abs_ref,
                "iid_mean_abs_ref": iid_mean_abs_ref,
                "common_bias_abs_ref": common_bias_abs_ref,
                "corr_mean_abs_ref": corr_mean_abs_ref,
                "xi_std": float(np.std(xi)),
                "aperture_span_m": float(delta[-1] - delta[0]),
            }
        )
        box_curves.append({"label": label, "eps_norm": eps_norm_list, "box_abs": np.array(box_abs_curve)})
        iid_curves.append({"label": label, "eps_norm": eps_norm_list, "iid_abs": np.array(iid_abs_curve)})

    for row in summary_rows:
        row["nominal_rel_aligned"] = float(row["nominal_abs"] / aligned_nominal_abs)
        row["box_abs_ref_rel_aligned"] = float(row["box_abs_ref"] / aligned_box_abs_ref)
        row["iid_mean_abs_ref_rel_aligned"] = float(row["iid_mean_abs_ref"] / aligned_iid_abs_ref)

    utils.save_csv(
        os.path.join(results_dir, "data_baseline_curves.csv"),
        fieldnames=[
            "placement",
            "eps_norm",
            "eps_m",
            "nominal_abs",
            "box_norm",
            "box_abs",
            "iid_mean_norm",
            "iid_mean_abs",
            "method_used",
            "warning_reorder",
        ],
        rows=curve_rows,
    )
    utils.save_csv(
        os.path.join(results_dir, "data_baseline_summary.csv"),
        fieldnames=[
            "placement",
            "label",
            "nominal_abs",
            "box_abs_ref",
            "iid_mean_abs_ref",
            "common_bias_abs_ref",
            "corr_mean_abs_ref",
            "xi_std",
            "aperture_span_m",
            "nominal_rel_aligned",
            "box_abs_ref_rel_aligned",
            "iid_mean_abs_ref_rel_aligned",
        ],
        rows=summary_rows,
    )
    plotters.plot_baseline_box_curves(box_curves, os.path.join(results_dir, "fig_baseline_box"))
    plotters.plot_baseline_iid_curves(iid_curves, os.path.join(results_dir, "fig_baseline_iid"))
    plotters.plot_baseline_tradeoff(
        summary_rows,
        summary_eps_norm,
        os.path.join(results_dir, "fig_baseline_tradeoff"),
    )
    logger.info("Completed baseline section with %d placement families", len(placements))
    return summary_rows


def run_sweep_fc(cfg, logger, results_dir):
    eps_m_list = cfg.eps_m_list
    rows = []
    curves = []
    for fc in cfg.sweep.f_c_list:
        cfg_fc = replace(cfg, f_c=fc)
        design_out = design_delta_star.design_delta_star(cfg_fc, logger)
        lam = design_out["lambda_m"]
        a_ideal = design_out["a_ideal"]
        k0 = design_out["k0"]
        delta_star = design_out["delta_star"]
        phi_ref = design_out["phi_ref"]
        xi = design_out["xi"]
        weights = tx.normalized_weights(delta_star, cfg_fc.d)
        rng = np.random.default_rng(cfg_fc.random_seed)
        wc_norm_arr = []
        previous_wc_delta = np.zeros_like(delta_star)
        reorder_any = False
        for eps_m in eps_m_list:
            eps_norm = float(eps_m / lam)
            eps = float(eps_m)
            split_delta = tx.split_error_vector(eps, xi, weights, delta_star=delta_star)
            wc_norm, delta_wc, method_used, reorder_wc = robustness.worst_case_gain(
                eps,
                delta_star,
                a_ideal,
                k0,
                cfg_fc.d,
                cfg_fc.n_eff,
                cfg_fc.eta,
                cfg_fc,
                rng,
                logger,
                phi_ref,
                extra_starts=[previous_wc_delta, split_delta],
            )
            previous_wc_delta = delta_wc.copy()
            wc_norm_arr.append(wc_norm)
            reorder_any = reorder_any or reorder_wc
            rows.append(
                {
                    "f_c": fc,
                    "eps_norm": float(eps_norm),
                    "eps_m": eps_m,
                    "wc_norm": wc_norm,
                    "method_used": method_used,
                    "warning_reorder": int(reorder_wc),
                }
            )
        if reorder_any:
            logger.warning("Reorder detected in freq sweep at f_c=%.3e", fc)
        curves.append({"f_c": fc, "eps_m": np.array(eps_m_list), "wc_norm": np.array(wc_norm_arr)})
    utils.save_csv(
        os.path.join(results_dir, "data_freq_sweep.csv"),
        fieldnames=["f_c", "eps_norm", "eps_m", "wc_norm", "method_used", "warning_reorder"],
        rows=rows,
    )
    plotters.plot_freq_sweep(curves, os.path.join(results_dir, "fig_freq_sweep"))
    return curves


def run_sweep_neff(cfg, logger, results_dir):
    rows = []
    curves = []
    for neff in cfg.sweep.n_eff_list:
        cfg_neff = replace(cfg, n_eff=neff)
        design_out = design_delta_star.design_delta_star(cfg_neff, logger)
        lam = design_out["lambda_m"]
        a_ideal = design_out["a_ideal"]
        k0 = design_out["k0"]
        delta_star = design_out["delta_star"]
        phi_ref = design_out["phi_ref"]
        xi = design_out["xi"]
        weights = tx.normalized_weights(delta_star, cfg_neff.d)
        rng = np.random.default_rng(cfg_neff.random_seed)
        wc_norm_arr = []
        previous_wc_delta = np.zeros_like(delta_star)
        reorder_any = False
        for eps_norm in cfg_neff.epsilon_norm_list:
            eps = float(eps_norm * lam)
            split_delta = tx.split_error_vector(eps, xi, weights, delta_star=delta_star)
            wc_norm, delta_wc, method_used, reorder_wc = robustness.worst_case_gain(
                eps,
                delta_star,
                a_ideal,
                k0,
                cfg_neff.d,
                cfg_neff.n_eff,
                cfg_neff.eta,
                cfg_neff,
                rng,
                logger,
                phi_ref,
                extra_starts=[previous_wc_delta, split_delta],
            )
            previous_wc_delta = delta_wc.copy()
            wc_norm_arr.append(wc_norm)
            reorder_any = reorder_any or reorder_wc
            rows.append(
                {
                    "n_eff": neff,
                    "eps_norm": float(eps_norm),
                    "eps_m": eps,
                    "wc_norm": wc_norm,
                    "method_used": method_used,
                    "warning_reorder": int(reorder_wc),
                }
            )
        if reorder_any:
            logger.warning("Reorder detected in n_eff sweep at n_eff=%.3f", neff)
        curves.append({"n_eff": neff, "eps_norm": cfg_neff.epsilon_norm_list, "wc_norm": np.array(wc_norm_arr)})
    utils.save_csv(
        os.path.join(results_dir, "data_neff_sweep.csv"),
        fieldnames=["n_eff", "eps_norm", "eps_m", "wc_norm", "method_used", "warning_reorder"],
        rows=rows,
    )
    plotters.plot_neff_sweep(curves, os.path.join(results_dir, "fig_neff_sweep"))
    return curves


def main():
    cfg = config.get_config()
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results_dir = os.path.join(repo_root, "results")
    utils.ensure_dir(results_dir)
    logger = utils.setup_logger(os.path.join(results_dir, "run_log.txt"))
    logger.info("Loaded config / Ready")

    rng = np.random.default_rng(cfg.random_seed)
    design_out = design_delta_star.design_delta_star(cfg, logger)
    exp_out = run_main_experiment(cfg, design_out, rng, logger, results_dir)

    run_box_validation(cfg, design_out, rng, logger, results_dir)
    run_error_scenarios(cfg, design_out, rng, logger, results_dir)
    run_baseline_section(cfg, design_out, logger, results_dir)
    run_sweep_fc(cfg, logger, results_dir)
    run_sweep_neff(cfg, logger, results_dir)

    cfg_dict = cfg.to_serializable()
    cfg_dict.update(
        {
            "lambda_m": design_out["lambda_m"],
            "k0": design_out["k0"],
            "xi_max": exp_out["xi_max"],
            "xi_mean": exp_out["xi_mean"],
            "epsilon_valid_m": exp_out["epsilon_valid"],
            "epsilon_valid_norm": exp_out["epsilon_valid_norm"],
            "a_ideal": design_out["a_ideal"],
            "random_seed": cfg.random_seed,
            "version_info": utils.version_info(),
        }
    )
    utils.save_json(os.path.join(results_dir, "config.json"), cfg_dict)

    logger.info("All experiments completed. Results in %s", results_dir)


if __name__ == "__main__":
    main()
