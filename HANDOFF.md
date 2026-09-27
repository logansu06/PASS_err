# HANDOFF — PASS 位置误差鲁棒性 → IEEE ICC 2027 论文

> 更新：2026-09-27（`/experiment-bridge` 完成后）。接手的人（或新的 Claude/Codex 会话）请先读本文件，再读 `refine-logs/EXPERIMENT_RESULTS.md` 和 `idea-stage/docs/research_contract.md`。

## 1. 现状

- 毕设（FYP）已经升级成论文课题 **A7 v2：Certified Robust Site Selection for PASS — Global Screening Under Position Errors**（下文简称 GCS）。
- ARIS 流程已经走完 idea discovery → refine → experiment plan → **experiment bridge**。R001–R017 全部实验跑完：
  - 预先声明的 go/no-go 门槛**通过**（56.2%，门槛 20%）。
  - 下一步是 `/result-to-claim`，然后画图 → 评审 → 重写叙事 → 写论文。

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
- **Theorem 2：** 至多 2M 个共享端点符号模板（zonotope），能**精确**覆盖每个子集的端点泄漏最大值。由此得到所有子集的 U_H，并可以做 safe screening。
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

| 阶段 | 状态 | 产物 |
|---|---|---|
| 文献与新颖性 | 完成（novelty 6/10 PROCEED） | `idea-stage/LIT_REVIEW.md`、`NOVELTY_REPORT.md` |
| Idea discovery | 完成（选定 A7） | `idea-stage/IDEA_REPORT.md`、`idea-stage/docs/research_contract.md` |
| Refine | 完成（7.40 → 7.70，之后并入 GPT-6 Pro 升级为 v2） | `refine-logs/FINAL_PROPOSAL.md`、`REVIEW_SUMMARY.md`、`REFINEMENT_REPORT.md` |
| Experiment plan | 完成（v2） | `refine-logs/EXPERIMENT_PLAN.md`、`EXPERIMENT_TRACKER.md` |
| **Experiment bridge** | **完成**：R001–R017 为 DONE；代码审查 2 轮，无 CRITICAL | `experiments/a7/`、`refine-logs/EXPERIMENT_RESULTS.md` |
| M4：R018 图 / R019 数值核对 / R020 `/result-to-claim` | **待做** | — |
| `/auto-review-loop` | 待做（有限轮次；旧评审已归档到 `fyp_report/review-stage/`） | `review-stage/`（运行时创建） |
| 重写 `NARRATIVE_REPORT.md` | 待做（**当前内容还是毕设时期的叙事**） | `NARRATIVE_REPORT.md` |
| `/paper-writing — venue: IEEE_CONF, human checkpoint: true` | 待做 | `paper/` |

## 5. 实验结果要点（详见 `refine-logs/EXPERIMENT_RESULTS.md`）

- **M0（8/8 通过）：**
  - 界的有效性检验 0 违反；
  - bank identity 成立；
  - ε=0 时 Γ 严格等于 0；
  - K 的敏感度在 sec² 界内；
  - 50 位精度复核的 margin：free 0.3209，endpoints 0.0466；
  - GPT-6 Pro 的 132 例网格完全复现（108/132 为正，79/132 超过 5%）。
- **C1（1,360 例；ε>0，P≠D）：** Γ>0 为 87.5% / 82.8%（free / endpoints），中位数 11.3% / 6.9%。
  - 增益随 SNR 增大；10 dB 时很小。
  - 机理：期望信号功率不变，最坏情况泄漏降低 21%。
- **C2：**
  - 唯一性证书 39% / 45%，随 ε 下降；
  - 全局 bracket 中位数 0.5%；
  - 筛选后幸存子集 ≤ 0.02%；
  - swap 搜索有 68% 的用例达不到精确最优（最大差 25.9%）；
  - M=32（1,050 万子集）每例约 35 s。
- **Baseline：**
  - 同预算的角点鲁棒 swap（B-CR）只在 8–22% 的用例里选中 Ŝ，Ŝ 被证书确认胜出 51–69%；
  - P-blind 布局（B-GR）在 x_P≠0 时 100% 被确认更差。
- **C3：** Ī/F_end ≤ 1.01，即 converse 与 achievability 几乎重合。F_end 约按 ε² 增长。P=(0,1) 时 F_end≈0.80，无法保护。
- **非理想信道（0.08 / 1 dB/m 损耗，cos² 方向性）：** Γ>0 保持 82–89%，增益中位数约减半。
- **R017 额外项：**
  - 蒙特卡洛平均 SLNR 只低约 0.4%，低尾更好；
  - D.6 joint-box 细化在 x_P=0 的用例上把 log-gap 收窄 51–61%，但没有翻正。

## 6. 已知局限与风险（写论文时必须如实写）

- **x_P = 0（P 在 D 正后方，共线同相）：**
  - 全部 inconclusive，全部 cap hit 也都在这里。
  - 原因是 Theorem 1 把期望信号和泄漏解耦取界。
  - 措辞用"certificate inconclusive"，不要写"robust is worse"。
- **其余 61 个 inconclusive 用例是边缘情况：** Γ 中位数 −0.19%，其中 46% 的 Ŝ = S_N。
- **唯一性证书在大 ε 时稀少**（ε=0.08λ 时只有 9–15%）。这些用例只能声称 bracket（性能比 ≥ L/U*）。
- **名义性能牺牲：** 中位数约 0.3%，p90 13.5%，最大 88.5%（高 SNR 下名义最优的深零点很脆弱）。要写成显式 trade-off，不能说"no-cost"。
- **数值：** 所有结论都是 float64 下对精确算术陈述的求值。只写"evaluated numerically"，不写"machine-verified"。
- **过期文件：**
  - `CLAIMS_FROM_RESULTS.md` 仍是旧的（verdict: REVIEW_UNAVAILABLE），要由 R020 替换；
  - `NARRATIVE_REPORT.md` 仍是毕设叙事。
- **反驳要点：** 相关工作里 Yang et al.（TVT 2026）用的是逐元素 box 误差；Chen 等人的 H-PASS（TWC 2026）已经仿真过多 PA 的位置误差。novelty 应强调 Theorem 2 / Corollary 1。

## 7. 下一步（按顺序，对照截止日期）

1. **R020 `/result-to-claim`**：reviewer 用 GPT-6 Astra ultra，输入 `refine-logs/EXPERIMENT_RESULTS.md` 和 `idea-stage/docs/research_contract.md`。
2. **R018 画图**（`/paper-figure`）：
   - Fig. 1：几何示意与证书构造；
   - Fig. 2：Γ 分布，数据来自 `main_grid.csv`；
   - Fig. 3：容差 bracket，数据来自 `limits.csv`；
   - Fig. 4：筛选效率，数据来自 `main_grid.csv` 和 `scaling.csv`。
3. **R019 数值核对**：论文里的每个数都要能回溯到 CSV/JSON。
4. 可选：`/ablation-planner`（非对称与对称扇区、sec 与加性 pad）。
5. 有限轮次的 `/auto-review-loop`。
6. 重写 `NARRATIVE_REPORT.md`（A7 v2），然后 `/paper-writing — venue: IEEE_CONF, human checkpoint: true`。
7. 计划时间线：M4 在 9/28–9/29，写作 9/30–10/1，**10/2 在 EDAS 提交**。

## 8. 文件地图

- `src/`、`results/`：毕设代码与产出（入口 `src/main.py`）。
- `experiments/a7/`：论文实验。
  - `a7_core.py`：GCS 核心（plan 里叫 `a7_gcs.py`）。
  - 驱动：`run_main.py`、`run_baselines.py`、`run_scaling.py`、`run_m2m3.sh`、`r017_*.py`。
  - 检查：`a7_checks.py`、`r001_port_check.py`。
  - 汇总：`summarize_main.py`、`summarize_m2m3.py`。
  - `results/`：全部 CSV/JSON/日志，以及 `crosscheck_bundle/`。
- `refine-logs/`：proposal、plan、tracker、results（带时间戳的是历史版本）。
- `idea-stage/`：文献、idea 报告、research contract、pilots，以及 GPT-6 Pro 交接材料（`handoff/`，含 prompt、回复和验证代码包）。
- `fyp_report/`：毕设 LaTeX、PDF、旧的 `PAPER_PLAN.md` 和旧评审存档。
- `docs/`：参考论文、`fyp.pdf`、模板。
- 根目录：`findings.md`（append-only 发现日志）、`MANIFEST.md`、`NARRATIVE_REPORT.md`、`CLAIMS_FROM_RESULTS.md`、`CLAUDE.md`、`AGENTS.md`。

## 9. 环境与复现

`.venv` 不在 git 里，新机器上需要重建：

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
```

## 10. 工具与约定

- **ARIS：** skills 在 `.claude/skills/`，是指向 `/Users/logansu/aris_repo` 的 symlink，**不要修改**。更新用 `bash /Users/logansu/aris_repo/tools/install_aris.sh`。
- **外部 reviewer / 生成器：** 一律用 Codex MCP，`model: gpt-6-astra`，`config: {"model_reasoning_effort": "ultra"}`。**不用 gpt-5.5**，也不用 skill 默认的 xhigh。Gemini 失败时改用 GPT-6 Astra 代替。
- **GPT-6 Pro（网页端）：**
  - 必须用**本地打过补丁的 Oracle**（`~/tools/oracle`，0.21.3；Node v24.21.0；browser 引擎，`modelStrategy: current`）。GitHub 上的版本不支持 gpt-6-pro，不要 `npm i -g` 覆盖。
  - 在 Oracle profile 上手动启动 Chrome 时必须带 `--password-store=basic --use-mock-keychain`，否则会丢失 ChatGPT 登录（出过一次事故）。
  - Oracle 抓取答案失败时，可以用 CDP 或会话 API 只读恢复，脚本在 `.aris/oracle/`。
- **Git：**
  - `.aris/`（含 traces 和 oracle 脚本）与 `.claude/` 被 gitignore，**只存在本机**。审查 trace 在 `.aris/traces/experiment-bridge/2026-09-27_run01/`。
  - GitHub 仓库 `logansu06/PASS_err` 是 **public**：未发表的 idea 和结果已经公开。如果要在投稿前保密，需要把仓库改成 private。
- **历史教训：** 这些都已修正，别再犯。
  - N0 镜像 bug；
  - κ 阈值无效；
  - split-gap bound 是错的；
  - ε=0 的 "2.78%" 只是单个实例的数；
  - v1 的 swap 搜索不是最优（53.42 对精确的 56.56）；
  - clearance 必须过滤；
  - β_D 超过 π/2 时报错，不截断。
