# PASS 位置误差仿真验证

## 目录结构
- `src/`：仿真与分析代码（入口 `src/main.py`）。
- `results/`：实验产出（CSV/NPZ/图表/日志），由 `src/main.py` 生成。
- `fyp_report/`：毕设报告存档（`latex/` 为 LaTeX 工程、编译好的 PDF、毕设版 `PAPER_PLAN.md`、毕设阶段的 `review-stage/` 评审记录）。
- `docs/`：参考论文 `2501.05657v2.pdf`、`fyp.pdf`、报告模板，以及 `Intro.md`、`THEORY_EXTENSIONS.md`。
- `review-stage/`：ARIS Workflow 2（`/auto-review-loop`）的输出目录，运行时自动创建（目前不存在）；毕设阶段的旧评审记录已存档到 `fyp_report/review-stage/`。
- 根目录：`NARRATIVE_REPORT.md`（ICC 2027 论文写作输入）、`findings.md`、`CLAIMS_FROM_RESULTS.md`（ARIS 各技能默认从根目录读取）。
- `paper/`：留给 `/paper-writing` 生成会议论文，目前不存在。

## 运行方式
- 安装依赖：`numpy`, `scipy`, `matplotlib`（Python 3.10+）。
- 一键运行全部实验并生成结果：在仓库根目录下执行 `python src/main.py`。
- 运行日志与全部产出保存在 `results/` 下；随机种子固定为 `20260111`（见 `src/config.py` 和 `results/config.json`）。

## 模块与核心接口（代码位于 `src/`，公式对应关系见 `docs/fyp.pdf` 指定章节）
- `pass_model.py`（见 fyp.pdf 2.2, 2.3）：
  - `distance(d, delta)` 计算 \(R_n(\Delta_n)=\sqrt{d^2+\Delta_n^2}\)。
  - `phase(k0, d, n_eff, delta)` 计算 \(\Phi_n(\Delta_n)=k_0(R_n+n_\text{eff}\Delta_n)\)。
  - `array_gain(delta, k0, d, n_eff, eta, phi_ref)` 计算 \(a(\Delta)=(\eta/N)|\sum w_n e^{-j(\Phi_n-\Phi_n^*)}|^2\)，其中 `phi_ref` 为名义相位对齐项。
  - `compute_a_ideal(...)` 计算 \(a_\text{ideal}=(\eta/N)(\sum 1/R_n)^2\)。
  - `xi_from_delta(...)` 输出一阶敏感度 \(\xi_n\)（见 fyp.pdf 3.3）。
- `design_delta_star.py`（见 fyp.pdf 3.2–3.3）：
  - `design_delta_star(config, logger)` 生成右半部初值、波长网格吸附、Brent 求根 + 间距约束，输出 `indices`、`delta_star`、`phi_ref`、`a_ideal`、`xi`。
- `robustness.py`（见 fyp.pdf 4.1, 4.2, 5.1）：
  - `monte_carlo_stats(eps, delta_star, ..., phi_ref)`：Uniform[-ε, ε] 采样，返回 mean/p05/p50/p95 与是否乱序。
  - `worst_case_gain(eps, ...)`：N≤20 角点枚举，否则坐标下降随机重启，输出 `wc_norm`、对应 `delta_wc`、`method_used`、乱序标记。
  - `delta_test_vector(eps, xi)`：构造性坏模式 \(\delta_\text{test,n}=\epsilon\cdot \text{sign}(\xi_n)\)。
  - `lower_bounds(...)`：计算解析下界 \(LB_\text{full}\) 与 \(LB_\text{simpl}\)（见 5.1）。
- `plotters.py`：统一生成主图、频率扫参、n_eff 扫参、\(\xi_n\) 分布图。
- `main.py`：加载配置→生成 Δ*→主实验（MC + worst-case + bound + δ_test）→扫参→保存所有 CSV/NPZ/图表→记录版本信息。
- `config.py`：默认参数、Monte Carlo、worst-case、扫参列表等。
- `utils.py`：日志、保存 csv/json/npz、版本记录、乱序检测。

## 输出文件说明（`results/`）
- `fig_main.(png|pdf)`：主图 \(a_\text{norm}\) vs \(\epsilon/\lambda\)，包含 Ideal baseline、Worst-case、\(LB_\text{full}\)、\(\delta_\text{test}\)、Monte Carlo 平均与 [p05,p95] 阴影，虚线标出小误差有效区 \(\epsilon_\text{valid}/\lambda\)（见 fyp.pdf 5.1）。
- `fig_freq_sweep.(png|pdf)`：不同载频 \(f_c\) 的 worst-case \(a_\text{norm}\) 曲线（扫参 1）。
- `fig_neff_sweep.(png|pdf)`：不同 \(n_\text{eff}\) 的 worst-case \(a_\text{norm}\) 曲线（扫参 2）。
- `fig_xi_distribution.(png|pdf)`：\(\xi_n\) 随索引分布，并标注 \(\xi_\text{max}\)（见 fyp.pdf 3.3）。
- `data_main.csv`：主实验逐 \(\epsilon_\text{norm}\) 记录：`eps_norm, eps_m, a_ideal, ideal_norm, wc_norm, test_norm, lb_full_norm, lb_simpl_norm, mc_mean, mc_p05, mc_p50, mc_p95, method_used, warning_reorder, xi_max`。
- `data_freq_sweep.csv`：频率扫参：`f_c, eps_norm, eps_m, wc_norm, method_used, warning_reorder`。
- `data_neff_sweep.csv`：n_eff 扫参：`n_eff, eps_norm, eps_m, wc_norm, method_used, warning_reorder`。
- `delta_wc.npz`：保存每个 \(\epsilon\) 的 worst-case \(\delta_\text{wc}\)、\(\delta_\text{test}\)、\(\Delta^*\)、`indices`。
- `config.json`：完整参数、随机种子、\(\lambda,k_0,\xi_\text{max},\epsilon_\text{valid}\) 与 numpy/scipy/matplotlib 版本，便于复现。
- `run_log.txt`：求根细节、间距检查、\(\xi_\text{max}\)、\(\epsilon_\text{valid}\)、worst-case 运行状态等。

## 图示与结论要点
- 主图展示：位置误差增大时 worst-case 增益整体下降；Monte Carlo 统计与 \(\delta_\text{test}\) 曲线提供可行上界；解析下界 \(LB_\text{full}\) 在小误差区（\(\epsilon<\epsilon_\text{valid}\)）紧贴数值 worst-case；竖线标注 \(\epsilon_\text{valid}/\lambda\)。
- 频率扫参：\(f_c\) 越高（波长越短），同样 \(\epsilon/\lambda\) 下退化更快。
- n_eff 扫参：\(n_\text{eff}\) 越大，敏感度 \(\xi_\text{max}\) 越大，worst-case 曲线更陡。

## 复现与自定义
- 修改参数：编辑 `src/config.py`（例如 `epsilon_norm_list`, `mc.samples`, worst-case 网格等），或直接修改 `results/config.json` 中的记录作为参考。
- 同一随机种子重复运行，CSV/图数值保持一致（图像元数据除外）。
- 若求根或枚举超出可接受时间，可调小 `epsilon_norm_list` 长度或提高 `enum_threshold_N` 切换到坐标下降。运行失败时查看 `run_log.txt` 中的清晰报错。 
