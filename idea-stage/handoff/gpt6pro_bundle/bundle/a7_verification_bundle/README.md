# A7 verification bundle — 2026-09-26

本目录包含实际执行的 NumPy/SciPy reference reproduction、corrected certificates、independent grid、shared endpoint-witness global screening，以及原始数值日志。

## 运行

建议在独立 Python environment 中安装 requirements.txt，然后从本目录执行：

```bash
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
python a7_reference.py
python a7_audit.py
python a7_global.py
python a7_unit_checks.py
python a7_grid.py 0
python a7_grid.py 1
python a7_grid.py 2
```

a7_reference.py 保留原 reference algorithm；不能把它用于未经 clearance 检查的高 tolerance family。
a7_audit.py 加入 beta guard、clearance filtering、asymmetric sectors、sec(pi/K) angular correction、epsilon=0 exact evaluation 和 feasible L-BFGS-B witnesses。
a7_global.py 用至多 2M 个 shared endpoint templates，为全部 feasible subsets 计算 upper bounds，再安全筛除无竞争力 layouts。它不宣称所有连续 uncertainty-box maxima 均发生在 corners，也不宣称 polynomial-time global optimization。
a7_grid.py 只执行预先列出的 epsilon/lambda=0.03,0.05；这些参数下全部 subsets 自动满足 clearance。修改为更大 epsilon 时，必须在每个 tolerance 下重新筛选 allS、matched 和 nominal optimum。

## 结果入口

- a7_nominal_tradeoff_results.json：nominal SLNR sacrifice、desired/leakage powers 和 aperture 对照。
- a7_global_results.json：P=(3,2), epsilon/lambda=0.05, SNRref=30 dB；free 与 matched-endpoint finite families 的 global screening。
- a7_independent_grid_results.json：33 P-geometries × 4 settings × 2 families，共 264 comparisons；每个 family 132 cases。这不是原报告的未给出完整 protocol 的 528-case grid。
- a7_audit_results.json：原 code reproduction、correctness checks、initial swap solutions；matched global improvement 应读取 a7_global_results.json，而非 initial swap。
- a7_unit_checks_results.json：384384 curvature samples、40 endpoint-bank identities、100 sector support tests。
- a7_environment.json：实际运行 environment。Runtime 仅代表本次容器，不是普遍性能承诺。

## 重要限制

所有数值均使用 float64；本次没有执行 outward-rounded validated interval arithmetic。因此应区分 exact-arithmetic theorems 与 numerical verification of certificate inequalities。
随机检查不能替代证明。严格 global-optimality 文字依赖文中条件的可靠数值验证；publication 前应对关键 comparison margins 作 arithmetic audit。
Global screening 的 worst-case complexity 仍随 family size 增长，少量 surviving layouts 只是本实例观察。
所有 comparison 使用固定 Aref、固定 physical noise、相同 N、相同 tolerance 与同一 family；D 和 P 使用同一个 physical error vector。

本打包版本仅把输出路径从 /mnt/data 改为脚本所在目录，计算流程和现有日志未改变。
