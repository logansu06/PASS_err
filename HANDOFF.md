# HANDOFF — PASS 位置误差鲁棒性 → IEEE ICC 2027 论文

> 更新：2026-09-29 傍晚，macOS。完成 R021 消融和 `/auto-review-loop`（第 1 轮 7/10，almost，已停止）。
> 之前的版本：2026-09-28 傍晚，macOS，跨平台同步和 Overleaf 桥接之后；2026-09-28 下午，Windows，M4（R018–R020）完成后；2026-09-27，macOS，`/experiment-bridge` 完成后。
>
> 接手的人（或新的 Claude/Codex 会话）请按顺序阅读：
> 1. 本文件；
> 2. `CLAIMS_FROM_RESULTS.md`：论文可用的措辞和禁用措辞；
> 3. `refine-logs/EXPERIMENT_RESULTS.md`：已按 R019 修订；
> 4. `idea-stage/docs/research_contract.md`。
>
> 本项目在 **macOS 和 Windows 两台机器**上交替工作。第 9 节（环境与复现）和第 10 节（工具与约定）按平台分开写。

## 1. 现状

- 毕设（FYP）已经升级为论文课题 **A7 v2：Certified Robust Site Selection for PASS — Global Screening Under Position Errors**，方法简称 GCS。
- ARIS 流程已走完以下阶段：idea discovery → refine → experiment plan → experiment bridge（R001–R017）→ **M4**。
  - **R020 `/result-to-claim`**：两个独立的 GPT-6 Astra ultra reviewer 给出的结论完全一致，都是 **partial / high**。标为 provisional，因为没跑 `/experiment-audit`。
    - 核心结论 C1、C2、C3 成立；
    - 几处附带表述写过头，已收窄。
  - **R019 数值核对**：完成。`EXPERIMENT_RESULTS.md` 引用的 237 个数字全部能回溯到结果文件。
  - **R018 画图**：4 张图 + 2 张表，经过 3 轮 GPT-6 Astra ultra 审查，全部判定 Ready。
  - **定向查新**：结论是 PROCEED，但 Theorem 2 的定位需要调整，见第 3 节。
- **跨平台同步**：Windows 上的 M4 产物已在 macOS 上重跑验证，数字和表格一致，见第 9 节。
- **论文编译改用 Overleaf**：两台机器都**不装 LaTeX**。macOS 已接好 Overleaf Git 桥接（`paper-overleaf/`），Windows 还没配置。见第 10 节。
- **R021 消融**：完成（2026-09-29）。角度离散、扇区包络、期望信号投影三项合计的损失 ≤ 0.0934%。从 v1 证书换到现在的证书，被确认的场景从 437 增加到 462（free）、从 403 增加到 437（endpoints）。x_P = 0 的压力测试里，联合细化后 16 对中有 4 对被证书确认。见第 5、6 节。
- **`/auto-review-loop`**：第 1 轮得分 7/10，结论 almost，满足停止条件。C1–C3 和 R021 经得起对抗性审查；"893/899 最坏泄漏更低"已被验证。最大风险是新意偏窄，写作时要按审稿意见定位。见第 6、7 节和 `review-stage/AUTO_REVIEW.md`。
- **下一步**：决定仓库是否改私有 → 重写 `NARRATIVE_REPORT.md`（按审稿意见定位） → `/paper-writing`。`/experiment-audit` 按用户决定跳过。详见第 7 节。

## 2. 目标与约束

- **投稿：** IEEE ICC 2027，6 页（含参考文献），EDAS 截止 **2026-10-02**，模板 `IEEE_CONF`。
- **用户偏好：**
  - 中稿概率优先；要"强任务、强结构、强数学"。
  - AI 方法可选（已评估，结论是**不加 learning**）。
  - idea 不必贴合毕设。
- **Baseline 口径：** 毕设结论加 N0/N1/N2 结论（见 `findings.md`）。毕设风格的 P-blind 布局在实验中就是 B-GR。
- **计算：** 只用本机 CPU（NumPy/SciPy），不需要 GPU。

## 3. 研究内容（A7 v2）

- **问题：**
  - 一根波导服务期望用户 D=(0,0) 和受保护用户 P=(x_P, y_P)。
  - 从 M=24 个 D 相位对齐的 pinching 站点里选 N=8 个。
  - 每个站点的执行器位置误差满足 |δ_n| ≤ ε。
  - 目标是最大化最坏情况 SLNR。
- **物理参数：** f_c=28 GHz（λ=10.714 mm），n_eff=1.44，d=3 m，x_f=−10 m。
- **Robust clearance：** 相邻选中站点间距 ≥ 0.5λ + 2ε；当 ε ≤ 0.0911λ 时所有子集都可行。
- **Theorem 1（非线性 SLNR bracket）：**
  - 期望信号用投影下界，并设 β_D ≤ π/2 guard；
  - 泄漏用非对称扇区的 support-function 上界，乘 sec(π/K) 修正，K=1440；
  - ε=0 时取精确值；
  - 结果为 L ≤ W ≤ U。
- **Theorem 2：** 至多 2M 个共享端点符号模板，能**精确**覆盖每个子集的端点泄漏最大值。由此得到所有子集的 U_H，并可以做 safe screening。
  - **查新结论（2026-09-28）：** "单个子集的最优符号向量落在 O(n) 个辅助角候选里"是已知结果，即秩 2 二值二次型最大化。必须引用：
    - Karystinos & Pados, IEEE TIT 2007；
    - Karystinos & Liavas, ICASSP 2008 / TIT 2010；
    - Allemand et al., Math. Program. 2001；
    - Ferrez et al., EJOR 2005。
  - **新颖点**在于：模板对整个 family 的所有子集**共享**，并作为 D/P 共用的可行 witness，用于 safe screening、全局 bracket 和唯一性证书。"safe screening"这个术语引用 El Ghaoui et al.。
  - 详见 `idea-stage/NOVELTY_TARGETED_A7v2.md`。
- **Corollary 1：** 全局 bracket L(Ŝ) ≤ W* ≤ U*。若 L(Ŝ) > max_{S≠Ŝ} U_H，则 Ŝ 是族内唯一的鲁棒最优布局。
- **Corollary 2：**
  - 泄漏的 converse/achievability：F_end ≤ min_S max_δ I_P ≤ Ī(Ŝ)；
  - interference-temperature 可行性。
- **Claims：**
  - **C1（主）：** 被证书确认的优势 L(Ŝ) > U(S_N)，其中 S_N 是穷举得到的名义最优。
  - **C2：** 全局认证率与筛选效率。
  - **C3：** 保护极限。
- **权威文档：** `refine-logs/FINAL_PROPOSAL.md`（v2）和 `refine-logs/EXPERIMENT_PLAN.md`（v2）。数学由 GPT-6 Pro 深度验证过，见 `idea-stage/handoff/GPT6_PRO_REPLY.md` 和 `GPT6_PRO_VERIFICATION.md`。

## 4. ARIS 流程进度

| 阶段 | 状态 | 产物 | 在哪台机器上做的 |
|---|---|---|---|
| 文献与新颖性 | 完成（novelty 6/10 PROCEED） | `idea-stage/LIT_REVIEW.md`、`NOVELTY_REPORT.md` | macOS |
| Idea discovery | 完成（选定 A7） | `idea-stage/IDEA_REPORT.md`、`idea-stage/docs/research_contract.md` | macOS |
| Refine | 完成（7.40 → 7.70，之后并入 GPT-6 Pro 升级为 v2） | `refine-logs/FINAL_PROPOSAL.md`、`REVIEW_SUMMARY.md`、`REFINEMENT_REPORT.md` | macOS |
| Experiment plan | 完成（v2） | `refine-logs/EXPERIMENT_PLAN.md`、`EXPERIMENT_TRACKER.md` | macOS |
| Experiment bridge | 完成：R001–R017 为 DONE；代码审查 2 轮，无 CRITICAL | `experiments/a7/`、`refine-logs/EXPERIMENT_RESULTS.md` | macOS |
| R020 `/result-to-claim` | **完成**：partial / high（provisional） | `CLAIMS_FROM_RESULTS.md` | Windows |
| 定向查新（Theorem 2 渊源） | **完成**：PROCEED，需调整定位 | `idea-stage/NOVELTY_TARGETED_A7v2.md` | Windows |
| R019 数值核对 | **完成**：237/237 一致 | `experiments/a7/summarize_r019.py`、`r019_numbers.py`、`results/r019_*` | Windows |
| R018 画图（`/paper-figure`） | **完成**：3 轮审查后全部 Ready | `figures/` | Windows |
| 跨平台同步验证 | **完成**：R019 数字和 R018 表格逐字节一致，图只有字体渲染差别 | — | macOS |
| Overleaf 桥接（`/overleaf-sync setup`） | **完成**（仅 macOS），验证通过 | `paper-overleaf/`（已 gitignore） | macOS |
| `/ablation-planner`（R021） | **完成**：四类差距分开量化；GPT-6 Astra ultra 设计并审核 | `experiments/a7/ablation_gaps.py`、`results/ablation_*` | macOS |
| `/experiment-audit` | 可选，未做（做了可去掉 provisional 标签） | — | — |
| `/auto-review-loop` | **完成**：第 1 轮 7/10，almost，已停止 | `review-stage/`（旧的毕设评审在 `fyp_report/review-stage/`） | macOS |
| 重写 `NARRATIVE_REPORT.md` | 待做（**当前内容还是毕设时期的叙事**） | `NARRATIVE_REPORT.md` | — |
| `/paper-writing — venue: IEEE_CONF, human checkpoint: true` | 待做（编译在 Overleaf 上做，见第 10 节） | `paper/` | — |

## 5. 实验结果要点

论文措辞以 `CLAIMS_FROM_RESULTS.md` 为准。数字来源见 `experiments/a7/results/r019_numbers.md`。

- **M0（8/8 通过）：**
  - 界的有效性检验 0 违反；bank identity 成立；ε=0 时 Γ 严格为 0；K 的敏感度在 sec² 界内。
  - 50 位精度复核的 margin：free 0.3209，endpoints 0.0466。
  - GPT-6 Pro 的 132 例网格完全复现（108/132 为正，79/132 超过 5%）。
  - R019 补充：网格上最弱的正 Γ（5.7e-6）和最弱的唯一性 margin（3.9e-5、4.7e-5），在 50 位精度下符号都不变。
- **C1（ε>0、P≠D，每个 family 528 例）：**
  - Γ>0 的比例：462/528 = 87.5%（free），437/528 = 82.8%（endpoints）。
  - Gate（Γ>5%）：297/528 = **56.25%**，门槛 20%。
  - Γ 中位数 11.3% / 6.9%。
  - 增益随 SNR 增大，10 dB 时很小。
  - **已验证（auto-review 第 1 轮）：** Γ>0 的 899 例中有 893 例（free 457/462，endpoints 436/437）满足 Ī(Ŝ) 低于 S_N 在其 best-found witness 处的泄漏，即 **Ŝ 的最坏泄漏被严格证明更低**。899 例上证书泄漏比的中位数 ≤ 0.800。可用措辞见 `CLAIMS_FROM_RESULTS.md`。
- **C2：**
  - 唯一性证书 38.6% / 45.3%，随 ε 增大而下降，0.08λ 时只有 9–15%。
  - 全局 bracket 中位数约 0.5%。
  - 筛选后幸存子集中位数约 0.01% / 0.02%。
  - swap 搜索在 77.7%（free）/ 59.1%（endpoints）的精确用例里达不到精确最优。
  - M=32（约 1,050 万子集）每例约 35 s。
- **Baseline：**
  - 同起点的 shared-template swap（B-CR）：Ŝ 被证书确认胜出 51–69%。注意**预算并不对等**，不能写"same budget"。
  - P-blind 布局（B-GR）：在 x_P≠0 时 120/120 被确认更差。
- **C3：**
  - Ī/F_end 最大为 1.0113，即误差在 **1.14%** 以内。原先写的"≤1.01"是错的，已更正。
  - F_end 从 0.01λ 到 0.09λ 增长约 ×67–71。
  - P=(0,1) 时 F_end≈0.80。只能写成"I_max < p·F_end 时不可行"，不能写"fundamentally unprotectable"。
- **非理想信道：** Γ>0 保持 82–89%，但这是在每个模型下**重新设计**、采用各自参考 SNR 的结果。
- **蒙特卡洛：** 平均 SLNR 损失的中位数为 0.32% / 0.42%，个别用例最大损失达 22.9% / 15.0%。
- **消融（R021）：** 数字以 `experiments/a7/results/ablation_summary.md` 为准（界已向外取整），可用措辞见 `CLAIMS_FROM_RESULTS.md` 的 R021 一节。
  - 在固定的 Ŝ 上，pad → sec 让证书提高：中位数 0.936%，最大 ≤ 11.76%；对称 → 非对称扇区只增加 ≤ 0.0183%。
  - 2,112 个主网格布局上的最大损失：角度 ≤ 0.000476%，P 侧扇区 ≤ 0.0797%，期望信号投影 ≤ 0.0141%，合计 ≤ 0.0934%。
  - 压力测试（32 个场景 × 两个布局，联合细化）：离轴时依赖项中位数在 [0.0359%, 0.0436%]；x_P = 0 时中位数在 [13.71%, 21.11%]。
  - 共享模板库在每个固定布局上都达到全部 256 个角点的最小值（差 ≤ 2.44e-15）。
  - M = 16 时 GCS 与穷举的证书最优在 24/24 中完全一致。这只是正确性检查，不是加速比。

## 6. 已知局限与风险（写论文时必须如实写）

- **x_P = 0（P 在 D 正后方，共线同相）：**
  - 全部 inconclusive，全部 cap hit 也都在这里。
  - 用 "certificate inconclusive" 的措辞，不要写 "robust is worse"。
  - Joint-box 细化只说明界偏保守（log-gap 缩小 51–61%），**不能**说"只是界的问题"或"已修复"。
  - R021 压力测试：两个布局都做联合细化后，16 对中有 4 对被证书确认，都是 P = (0,4)、ε = 0.03λ，增益在 [0.887%, 0.972%]；其余 12 对仍无结论。可以作为补充验证写进论文，但不能说"负区域已修复"。
  - x_P = 0 布局上，D/P 依赖造成的损失有被证书确认的下界 1.82%–28.3%。这是下界，不能写成"依赖损失最多 28%"。
- **唯一性证书在大 ε 时稀少。** 这些用例只能声称 bracket。
- **名义性能牺牲：** 中位数约 0.2–0.3%，p90 13.5%，最大 88.5%。要写成显式的 trade-off，不能说 "no-cost"。
- **数值：** 所有结论都是 float64 下对精确算术陈述的求值。只写 "evaluated numerically"，不写 "machine-verified"。
- **过度表述的教训：** 2026-09-28 共抓到多处，包括：
  - R020 发现的"≤1%""same-budget""0.4% cost""unprotectable"、负区域的因果归因；
  - 画图时的"no pruning"、图注不等式的舍入方向。
  - 规则一：任何绝对化的词都要对照**每一行**数据检验。
  - 规则二：图注和正文里的证书界要**向外舍入**，上界向上取，witness 向下取。
- **四类 gap 已分开量化（R021）。** 角度、扇区包络、期望信号投影三项合计 ≤ 0.0934%。
  - 全网格上剩下的部分是 D/P 依赖和未解决的 witness 差距混在一起，**不能**说"依赖主导了全网格的 gap"。只有压力测试把两者分开了。
  - 对独立误差，Minkowski 求和是精确的。R018 时"保守性来自 Minkowski 和"的说法是错的，已在 `findings.md` 更正。
- **代码 MINOR：** `a7_core.py:135` 没把残余名义相位失配算进 β_D。审稿人重放全部 1,056 个 Ŝ：L 最多降低约 2.7e-12（相对），没有任何结论翻转。投稿前不修改，否则要重新生成全部结果。
- **审稿意见（auto-review 第 1 轮），写论文时必须处理：**
  - 新意偏窄是最大风险。秩 2 二值二次型最大化和扇区 support function 界要作为工具明确致谢；贡献放在"一个共享模板库对整个族给出精确的端点泄漏覆盖"、保护极限和实测的认证率上。
  - 基线一律写 "same-start shared-template swap heuristic; budgets unmatched"；报告含全部步骤的运行时间和 cap hit；只在测试过的族上声称可行。
  - 除了中位数牺牲，还要给一个代价很大的例子：endpoints、30 dB、ε=0.03λ、P=(−3.6,2)，证书增益 +7.85%，但名义 SLNR −39.17%，蒙特卡洛平均 −14.95%，第 5 百分位 −12.53%。
  - 模型范围要写明：一对 D/P、一段对齐孔径、各站点等功率、可分离信道。
  - witness 写 "best-found SLNR witnesses"，不写 "SLNR-minimizing"。
- **反驳要点：**
  - Yang et al.（TVT 2026）用的是逐元素 box 误差；
  - Chen 等人的 H-PASS（TWC 2026）已经仿真过多 PA 的位置误差；
  - Jiang–Schotten（arXiv 2609.31088，2026-09-25）研究 PASS 位置误差下 TDMA/NOMA 的统计性能，**必须引用**。
  - novelty 强调 family 共享的 witness bank、证书化选址和全局证书。

## 7. 下一步（按顺序，对照截止日期）

0. 用户决定：GitHub 仓库是否改成 private（见第 10 节）。
1. `/ablation-planner`：**已完成**（R021，2026-09-29）。推迟的三项消融是随机与几何模板库对比、等 CPU 的 B-CR、固定物理噪声下的迁移，只有论文需要更强的说法时才做。
2. `/experiment-audit`：**不做**（用户决定，2026-09-29）。R020 的结论保持 provisional 标签。
3. `/auto-review-loop`：**已完成**（第 1 轮 7/10，almost）。"893/899"已验证。
4. 重写 `NARRATIVE_REPORT.md`（A7 v2）。图表直接用 `figures/latex_includes.tex`；按第 6 节的审稿意见定位新意，并放一张 R021 消融的小表。
5. `/paper-writing — venue: IEEE_CONF, human checkpoint: true`。它的编译步骤改走 Overleaf（见第 10 节“Overleaf 与论文编译”）。之后跑 `/paper-claim-audit` 和 `/citation-audit`。
6. 时间线：9/29 做步骤 1–3，9/30–10/1 写作，**10/2 在 EDAS 提交**。

时间不够时的取舍：步骤 2 可以砍，步骤 3 可压缩到 1 轮；步骤 4、5 和两项审计不能砍。按天排的路线图页面（私有链接，只有用户本人能打开）：https://claude.ai/artifact/UonYnExi1W8pLUtxUKhf1o

## 8. 文件地图

- `src/`、`results/`：毕设代码与产出（入口 `src/main.py`）。
- `experiments/a7/`：论文实验。
  - `a7_core.py`：GCS 核心（plan 里叫 `a7_gcs.py`）。
  - 驱动：`run_main.py`、`run_baselines.py`、`run_scaling.py`、`run_m2m3.sh`、`r017_*.py`。
  - 检查：`a7_checks.py`、`r001_port_check.py`。
  - 汇总：`summarize_main.py`、`summarize_m2m3.py`、**`summarize_r019.py`**（派生统计 + 50 位 margin 审计）、**`r019_numbers.py`**（数字清单）。
  - 消融：**`ablation_gaps.py`**（R021：固定布局上的证书差距分解、压力测试、M = 16 穷举对照）。
  - `results/`：全部 CSV/JSON/日志，以及 `crosscheck_bundle/`、`r019_derived.*`、`r019_numbers.*`、`ablation_*`。
- **`figures/`**：论文图表。
  - `paper_plot_style.py`；`gen_fig1..4_*.py`、`gen_tables.py`；
  - `fig*.pdf`（矢量）和 `.png`（预览）；
  - `TABLE_I/II_*.tex`、`latex_includes.tex`（草拟图注）；
  - `fig1_values.json`（图注用到的数）；
  - 重生成方法见第 9 节。
- `paper/`：ARIS 写论文的工作副本，进 git。由 `/paper-writing` 创建，目前还不存在。
- `paper-overleaf/`：Overleaf 项目的 git clone，每台机器各一份，**已 gitignore**，见第 10 节。
- `refine-logs/`：proposal、plan、tracker、results（带时间戳的是历史版本）。
- `idea-stage/`：文献、idea 报告、research contract、pilots、GPT-6 Pro 交接材料（`handoff/`），以及 **`NOVELTY_TARGETED_A7v2.md`**。
- `fyp_report/`：毕设 LaTeX、PDF、旧的 `PAPER_PLAN.md` 和旧评审存档。
- `docs/`：参考论文、`fyp.pdf`、模板。
- 根目录：`CLAIMS_FROM_RESULTS.md`（R020 结论）、`findings.md`（只追加的发现日志）、`MANIFEST.md`、`NARRATIVE_REPORT.md`（旧）、`CLAUDE.md`、`AGENTS.md`、`.gitattributes`。

## 9. 环境与复现

`.venv` 不进 git，每台机器各建一个，位置都是 `experiments/a7/.venv`。建议先设置 `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`。不同平台或 BLAS 下，个别浮点数的最后一位（ulp）可能不同：R001 在 Windows 上重跑也是 PASS，只有 2 个字段差 1 ulp。**不要提交**在另一台机器上重跑后生成的 `r001_port_check.json`。

**跨平台复现（2026-09-28，在 macOS 上重跑 Windows 生成的 R019 和 R018）：**
- `r019_numbers.*`、`r019_derived.md`、`TABLE_I/II_*.tex` 逐字节一致，237/237 数字一致，50 位精度复核的符号全部不变。
- `r019_derived.json` 只差时间戳、平台信息和 1 个 ulp；`fig1_values.json` 有两个值末位不同，四位小数取整后相同。
- 四张图尺寸和嵌入字体（Times New Roman + STIX）相同，约 0.2% 的像素在文字边缘不同，是两个系统字体渲染的差别，数据标记完全一致。
- 这些重跑产物同样**不要提交**，避免两台机器来回改动。

### macOS（R001–R017 的原始运行环境）

- Python 3.13.4、NumPy 2.3.0、SciPy 1.15.3。项目路径 `/Users/logansu/Documents/PASS`。
- **不装 LaTeX**，论文在 Overleaf 编译（见第 10 节）。

```bash
cd experiments/a7
python3 -m venv --system-site-packages .venv          # 需要系统里已有 numpy 2.3 / scipy 1.15
.venv/bin/python -m pip install mpmath pandas matplotlib
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
.venv/bin/python r001_port_check.py                   # R001
.venv/bin/python a7_checks.py --workers 6             # R002–R008，任何一项失败则 exit 1
.venv/bin/python run_main.py --workers 7              # R009，约 8 分钟
.venv/bin/python summarize_main.py                    # R010/R013，含 go/no-go
./run_m2m3.sh                                         # R011/R012/R014/R015/R016
.venv/bin/python run_main.py --alpha-db 1.0 --q 2 --snr 20,30 --eps 0.03,0.05 --out results/nonideal_1dB.csv
.venv/bin/python r017_mc_average.py && .venv/bin/python r017_joint_box.py && .venv/bin/python summarize_m2m3.py
.venv/bin/python summarize_r019.py && .venv/bin/python r019_numbers.py      # R019
.venv/bin/python ablation_gaps.py --workers 7         # R021，约 11 分钟（压力测试按固定盒子数，结果可复现）
cd ../../figures && for s in gen_fig*.py gen_tables.py; do ../experiments/a7/.venv/bin/python "$s"; done   # R018
```

### Windows（R018–R020 的运行环境）

- Python 3.12.10 位于 `C:\Users\89813\AppData\Local\Programs\Python\Python312\python.exe`。它**不在 PATH 上**：PATH 里的 `python` / `python3` 只是 Microsoft Store 的空壳。
- venv 用 pip 安装：numpy 2.3.5、scipy 1.15.3、mpmath 1.4.1、pandas 3.0.6、matplotlib 3.11.2。项目路径 `D:\PASS_err`。
- 在 Git Bash 里：

```bash
cd /d/PASS_err/experiments/a7
/c/Users/89813/AppData/Local/Programs/Python/Python312/python.exe -m venv .venv
.venv/Scripts/python.exe -m pip install "numpy~=2.3.0" "scipy~=1.15.0" mpmath pandas matplotlib
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONUTF8=1
.venv/Scripts/python.exe r001_port_check.py
.venv/Scripts/python.exe summarize_r019.py && .venv/Scripts/python.exe r019_numbers.py
cd ../../figures && for s in gen_fig*.py gen_tables.py; do ../experiments/a7/.venv/Scripts/python.exe "$s"; done
```

- **不装 LaTeX**（用户决定，2026-09-28）。论文在 Overleaf 编译，见第 10 节。
- **本机没有 `gh` CLI。** Git 推送走 HTTPS 凭据。

## 10. 工具与约定

### 两台机器通用

- **外部 reviewer / 生成器：** 一律用 Codex MCP，`model: gpt-6-astra`，`config: {"model_reasoning_effort": "ultra"}`，每个线程的第一次调用都要显式写明。
  - 本机 `~/.codex/config.toml` 默认是 xhigh，不要依赖它。
  - **不用 gpt-5.5**，也不用 skill 默认的 xhigh。Gemini 失败时改用 GPT-6 Astra。
  - 用户允许更高的审查强度，可以开多个独立 reviewer 线程，每个 claim 取最保守的结论。
- **Git 换行：** `.gitattributes` 规定文本统一用 LF，`.sh` 强制 LF，`*.csv` 设为 `-text`。
  - Python `csv` 模块在所有平台都写 CRLF，所以原始结果 CSV 必须按字节原样保存，**不要做 renormalize**。
  - Windows 上 `core.autocrlf=true`，这些规则会覆盖它。
- **`CLAUDE.md` 的 ARIS 块写的是两套平台的路径。** 在任一台机器上重跑 ARIS installer 都会把它改写成单平台版本，**这种改动不要提交**。
- **`.aris/` 和 `.claude/` 被 gitignore，只存在于各自的机器上。**
  - macOS 上有：`experiment-bridge`、`oracle-gpt6pro-handoff`、`ablation-planner/2026-09-29_run01` 等 trace，`.aris/oracle/` 脚本，`.aris/novelty/`。
  - Windows 上有：`.aris/traces/result-to-claim/2026-09-28_run01/`、`.aris/traces/paper-figure/2026-09-28_run01/`、`.aris/claims*.json`、`.aris/evidence_precheck*.json`。
- **GitHub 仓库 `logansu06/PASS_err` 是 public：** 未发表的 idea 和结果都是公开的。如果投稿前需要保密，要改成 private。
- **历史教训：** 下面这些都已修正，别再犯。
  - N0 镜像 bug；κ 阈值无效；split-gap bound 是错的；
  - ε=0 的 "2.78%" 只是单个实例的数；
  - v1 的 swap 搜索不是最优（53.42 对精确的 56.56）；
  - clearance 必须过滤；β_D 超过 π/2 时报错，不截断；
  - 2026-09-28 发现的过度表述，见第 6 节。

### Overleaf 与论文编译

- **论文在 Overleaf 编译，两台机器都不装 LaTeX。** MacTeX、BasicTeX、MiKTeX 都不要装，也不要建议用户装。
- Overleaf 项目名 `PASS-ICC2027`，账号有 Git 集成。本地用 ARIS 的 `/overleaf-sync` 连接：
  - `paper/`：ARIS 的工作副本，写作和审计都在这里做，进 git。
  - `paper-overleaf/`：Overleaf 项目的 git clone，每台机器各一份，已 gitignore。分支叫 `main`，skill 文档里写的 `origin/master` 要换成 `origin/main`。
  - 本地改完后用 `/overleaf-sync push`，推之前先给用户看 diff，等用户确认。
  - 用户在 Overleaf 上改过后用 `/overleaf-sync pull`，按 skill 的逐块规则合并回 `paper/`。涉及数字的改动要重跑 `/paper-claim-audit`，涉及引用的要重跑 `/citation-audit`。
  - 同一时间只在一边编辑。
- **替代 `/paper-compile`：** `/paper-writing` 的编译步骤调用本地 latexmk，会失败。改为：push 到 Overleaf → 用户点 Recompile → 用户把 PDF 下载到 `paper/main.pdf` → 本地检查页数和排版。`/auto-paper-improvement-loop` 每轮重新编译时也这样做。
- **第一次 push 会整体替换** Overleaf 上自动生成的默认 `main.tex`（push 用 `rsync --delete`）。在那之前不要在 Overleaf 上写内容。
- **token 安全：** token 只存在系统钥匙串或凭据管理器里，不能出现在对话、文件或远程 URL 里。push/pull 报 401 时，让用户重跑 setup 脚本，不要向用户索要 token。
- **macOS：** 2026-09-28 已配置并验证：远程 URL 不含 token，凭据在 `osxkeychain`，pre-commit 钩子已安装，`overleaf_audit.sh` 结果 clean。
- **Windows：** 还没配置。用户要在项目根目录的 Git Bash 里**自己**运行（agent 运行会被脚本拒绝）：`bash /c/Users/89813/aris_repo/tools/overleaf_setup.sh <Overleaf 项目链接>`。项目链接从 Overleaf 项目页的地址栏复制；token 在 Overleaf → Account Settings → Git Integration 生成。

### 仅 macOS

- **ARIS：** skills 在 `.claude/skills/`，是指向 `/Users/logansu/aris_repo` 的 symlink，**不要修改**。更新用 `bash /Users/logansu/aris_repo/tools/install_aris.sh`。
- **GPT-6 Pro（网页端，只在 macOS 上配置过）：**
  - 必须用**本地打过补丁的 Oracle**（`~/tools/oracle`，0.21.3；Node v24.21.0；browser 引擎，`modelStrategy: current`）。GitHub 上的版本不支持 gpt-6-pro，不要 `npm i -g` 覆盖。
  - 在 Oracle profile 上手动启动 Chrome 时必须带 `--password-store=basic --use-mock-keychain`，否则会丢失 ChatGPT 登录（出过一次事故）。
  - Oracle 抓取答案失败时，可以用 CDP 或会话 API 只读恢复，脚本在 `.aris/oracle/`。

### 仅 Windows

- **ARIS：** skills 是指向 `C:\Users\89813\aris_repo` 的 junction，不要修改。更新命令见 `CLAUDE.md`。
- **`save_trace.sh`：**
  - 必须先 `export PYTHONUTF8=1`，否则系统默认的 GBK 编码会导致写 JSON 失败；
  - 要用 `python3() { /d/PASS_err/experiments/a7/.venv/Scripts/python.exe "$@"; }; export -f python3` 这个 shim。
- **`evidence_check.py`：** 同样用 venv 里的 Python 和 `PYTHONUTF8=1`，只依赖标准库。
- **`verify_papers.py` 在本机跑不通：**
  - arXiv API 先是 SSL 证书链失败，用 certifi（`SSL_CERT_FILE`）解决后又返回 406；Semantic Scholar 一直是 pending。
  - 按 Policy D1 标为 UNVERIFIED，改用 CrossRef（可以直接 curl）和 arXiv 摘要页核实。
- **Oracle/GPT-6 Pro 没有在 Windows 上配置。**
