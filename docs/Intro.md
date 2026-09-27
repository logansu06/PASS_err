# PASS 位置误差仿真简介

本仿真用于评估阵列单元位置误差对阵列增益的影响，重点比较
理想情况、最坏情况、Monte Carlo 统计以及解析下界，并在不同
载频和有效折射率扫描下分析鲁棒性趋势。

## 仿真流程（概览）
1. 由配置参数生成名义最优相位与几何量（`design_delta_star.py`）。
2. 主实验：对给定误差幅度扫描列表，计算
   - 最坏情况（`worst_case_gain`）
   - Monte Carlo 统计（`monte_carlo_stats`）
   - 构造性“坏模式”测试向量（`delta_test_vector`）
   - 解析下界（`lower_bounds`）
3. 扫参：改变载频 `f_c` 与有效折射率 `n_eff`，重复最坏情况评估。
4. 保存 CSV/NPZ 与图表输出，并记录运行日志。

## 如何运行
在仓库根目录下执行：

```bash
python src/main.py
```

主要参数在 `src/config.py` 中配置；固定随机种子确保复现实验。

## 结果文件说明（`results/`）
- `data_main.csv`：主实验结果（`eps_norm`、`wc_norm`、MC 统计、下界等）
- `data_freq_sweep.csv`：载频扫描（`f_c`、`eps_norm/eps_m`、`wc_norm`）
- `data_neff_sweep.csv`：`n_eff` 扫描（`n_eff`、`eps_norm/eps_m`、`wc_norm`）
- `delta_wc.npz`：保存每个误差幅度下的最坏情况向量与相关量
- `fig_*.pdf/png`：主图与扫描图
- `config.json`：运行时配置快照
- `run_log.txt`：详细日志（求解过程与约束检查）

## 图像生成
如需论文级绘图，可使用 MATLAB 脚本 `plot_publication.m`
（放在包含 CSV 的目录下运行即可）。

## 备注
本仿真将误差归一化为 `eps_norm = eps / lambda`，
并输出相应的物理尺度 `eps_m` 以便在不同频率下对比。
