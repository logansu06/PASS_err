<!-- GPT-6 Pro reply, retrieved 2026-09-26 via the ChatGPT backend API from the signed-in Oracle profile.
     conversation: https://chatgpt.com/c/6ab77e85-d634-83ec-b591-ba71b968896f (title: 'Read Prompt Tasks')
     model_slug: gpt-6-pro | conversation default_model_slug: gpt-6-pro | Oracle session: pass-a7-gpt6pro-deep-verificati
     prompt: idea-stage/handoff/GPT6_PRO_PROMPT.md | tool use in thread: 27 code executions, 13 web.run calls
     raw conversation JSON: .aris/oracle/conversation_raw.json -->

## 1. Executive summary

1. **[NUMERICALLY OBSERVED]** 原 reference code 已复现：\(L(S_R)=53.422097\)、\(U(S_N)=42.154125\)，certified gain 为 **+26.7%**。
2. **[PROVEN]** Lemma 0、Proposition 1、Proposition 2、Corollary 和 Lemma 3 的主要数学结论成立，但必须明确 phase、amplitude、normalization、feasibility 和 denominator assumptions。
3. **[CORRECTED]** 原代码没有执行 robust clearance filtering；当 \(\epsilon=0.1\lambda\) 时，735,471 个 subsets 中只有 **112,251 个**满足你规定的 clearance。
4. **[CORRECTED]** \(\epsilon=0\) 时应直接计算 exact nominal leakage；仅删除 grid pad 并不安全，“人工损失 2.78%”也不是普遍结论。
5. **[PROVEN]** 可以用 asymmetric phase sectors 和 \(1/\cos(\pi/K)\) angular correction，替换较松的 symmetric sectors 与 additive grid pad。
6. **[PROVEN]** 最有价值的升级是 **shared endpoint-witness bank + global screening**：至多 \(2M\) 个共同 templates 可为整个 finite family 提供 feasible-witness upper bounds，并支持 global-optimality certificates。
7. **[NUMERICALLY OBSERVED]** 对参考 geometry，升级后的 free-family certified gain 为 **+34.17%**；其 lower bound 超过所有其他 layouts 的 witness upper bounds，数值上满足 unique global robust optimum 的充分条件。
8. **[NUMERICALLY OBSERVED]** 同一 geometry 的 matched-endpoint certified gain 是 **+2.79%**，不是 +26.7%；独立 matched grid 的 132 cases 中，108 cases 满足 certified dominance，79 cases 超过 5%。
9. 已核验文献排除了“首次研究 PASS position errors”“首次 nonlinear all-error certificate”等宽泛 novelty claims；尤其要正面区分 **Hybrid PASS、FullPASS、Zhang et al. 和 Arnestad et al.**。citeturn360996view6turn174295view2turn174295view3turn903389view6
10. 我的最终建议是：保留 PASS、SLNR 和 matched aligned family，但把论文中心从“一个更稳健的 heuristic”升级为 **“具有可核查 global bounds、layout dominance 和 leakage converse 的 finite-family robust selection”**；不加入 AI。

---

# 2. Task A — Deep verification

## A.1 Verification table

下表中的证明编号对应后文。数学结论按 exact arithmetic 陈述；本次程序运行采用 `float64`，其 numerical certification 层面的限制单独说明。

| Statement | Status | 正确表述或必要修正 | Proof |
|---|---|---|---|
| Lemma 0：phase monotonicity | **[PROVEN]** | 对给定 one-way guided-path model，\(n_{\mathrm{eff}}>1\) 保证 strict monotonicity；endpoint interval 对 **unwrapped phase** exact | A.2 |
| Lemma 0：complex sensitivity floor | **[PROVEN]** | 在 \(A>0\)、\(A\) 为 real differentiable amplitude 时成立；不能据此断言 received power 一阶敏感 | A.2 |
| Lemma 0：upstream/downstream limits | **[PROVEN]** | 是 \(t\to\pm1\) 的 asymptotic statements，不是有限 upstream/downstream sites 的精确取值 | A.2 |
| Common nominal phase | **[PROVEN]** | alignment equation 必须保留统一常数；feed offset 改变共同 phase，但不破坏 alignment | A.2 |
| Isotropic amplitude extrema | **[PROVEN]** | \(A^-\) 来自最大 endpoint distance；\(A^+\) 还须检查 interval 内是否包含 \(x_r\) | A.3 |
| Attenuation/directivity amplitude extrema | **[PROVEN]** | 必须检查 endpoints **及所有 interior stationary points**；不能直接沿用 isotropic endpoint rule | A.3 |
| Proposition 1 | **[PROVEN]** | 需要 common nominal phase、每个 selected site 的 \(\beta_{D,n}\le\pi/2\)，以及 nonnegative amplitude | A.4 |
| 原代码的 `cos(min(beta,pi/2))` | **[CORRECTED]** | 它不是超出 \(\pi/2\) 后的有效 extension；必须拒绝 invalid case 或使用允许 negative projection 的 bound | A.4 |
| Proposition 2：sector support | **[PROVEN]** | 使用 circular distance；negative-cosine branch 必须取 \(A^-\) | A.5 |
| Proposition 2：support maximization/grid pad | **[PROVEN]** | 原 Lipschitz correction 有效，但不是这里最紧的便宜 correction | A.5、D.2 |
| Corollary：\(L\le W\le U\) | **[PROVEN]** | \(L_D,\bar I\) 都须包括 \(1/N\)；witness 必须使用同一个 physical error vector 计算 D 和 P | A.6 |
| Corollary：dominance/noise inequality | **[PROVEN]** | 在 denominators strictly positive 时成立；最简单的充分 assumption 是 \(\sigma^2>0\) | A.6 |
| \(\epsilon=0\) treatment | **[CORRECTED]** | 应使用 exact nominal modulus，而不是只关闭 pad；2.78% 不是 universal loss | A.6 |
| Lemma 3：Taylor model 与 \(b_n\) | **[PROVEN]** | 原 \(b_n\) 正确；下文给出 fully computable \(H_n\ge\sup|z_n''|\) | A.7 |
| Lemma 3：random-sign lower bound | **[PROVEN]** | 是 artificial Rademacher averaging 的 existence argument，不要求 physical errors 为随机变量 | A.7 |
| Independent-box clearance | **[CORRECTED]** | 必须将 \(d_{\min}+2\epsilon\) 写入 feasible family，并对 nominal/robust methods 同时执行 | A.8 |

---

## A.2 Lemma 0、feed offset 和 alignment

### 全部推导共享的 model assumptions

这里采用你给定的

\[
R_r(x)=\sqrt{(x-x_r)^2+y_r^2+d^2},
\qquad
\psi_r(x)=k_0\left[R_r(x)+n_{\mathrm{eff}}(x-x_f)\right].
\]

需要明确：

- 所有 uncertainty intervals 均位于所采用的 one-way guided-path branch；在本例中，它们都位于 feed 的 downstream。
- \(d>0\)，因此 \(R_r(x)>0\)。
- \(A_r(x)\) 是 real、nonnegative、per-site separable amplitude；没有尚未建模的 selection-dependent coupling。
- 原模型中的 equal-power weights 不会在发生 actuator errors 后重新优化。
- D 和 P 受到的是**同一组** actuator errors，而不是可以独立选择的两组 errors。
- “independent boxes”描述 Cartesian-product uncertainty set，不必赋予 errors 一个 probability distribution。

### [PROVEN] Monotone guided phase

令

\[
t_r(x)=\frac{x-x_r}{R_r(x)}.
\]

则

\[
R_r'(x)=t_r(x),\qquad
R_r''(x)=\frac{1-t_r(x)^2}{R_r(x)}.
\]

由于 \(d>0\)，有 \(-1<t_r(x)<1\)，所以

\[
\psi_r'(x)
=k_0\big(n_{\mathrm{eff}}+t_r(x)\big)
>k_0(n_{\mathrm{eff}}-1)>0.
\]

因此 \(\psi_r\) continuous 且 strictly increasing。由 continuous monotone function 的 interval image，

\[
\left\{\psi_r(x_n+\delta):
|\delta|\le\epsilon\right\}
=
[\psi_r(x_n-\epsilon),\psi_r(x_n+\epsilon)].
\]

这证明了 endpoint interval 对 **unwrapped phase** exact。映射到 complex plane 后，需要处理 modulo \(2\pi\)；不能直接用普通 real-line distance 代替 circular distance。证毕。

### [PROVEN] Complex sensitivity floor

对 real differentiable \(A\)，

\[
z'(x)
=e^{-j\psi(x)}
\left[A'(x)-jA(x)\psi'(x)\right].
\]

括号内的 real 和 imaginary parts 正交，因此

\[
|z'(x)|^2
=A'(x)^2+A(x)^2\psi'(x)^2
\ge
k_0^2(n_{\mathrm{eff}}-1)^2A(x)^2.
\]

当 \(A(x)>0\) 时，右侧 strictly positive。证毕。

**需要限制原句的含义：**这证明的是单个 site 的 **complex contribution** 不可能 first-order insensitive，并不证明 \(|h_D|^2\)、\(|h_P|^2\) 或 SLNR 必然 first-order sensitive。对 complex field 的一阶变化，仍可能在 power derivative 中抵消。

如果引入具有 zero 的 directivity pattern，则 \(A=0\) 处不能再由该式推出 strict positivity。

### [PROVEN] Upstream/downstream limits

固定 receiver 后，

\[
\lim_{x\to+\infty}t_r(x)=1,\qquad
\lim_{x\to-\infty}t_r(x)=-1,
\]

所以

\[
\xi_r=n_{\mathrm{eff}}+t_r
\longrightarrow n_{\mathrm{eff}}\pm1.
\]

这是 algebraic model 的 asymptotic result。对于有限 waveguide，特别是必须保持 \(x\ge x_f\) 的 physical segment，应表述为“趋近于”，而不是把任意 upstream site 的 \(\xi_r\) 直接设为 \(n_{\mathrm{eff}}-1\)。证毕。

### [PROVEN] Feed offset 不破坏正确构造的 alignment

假设

\[
R_D(x_n)+n_{\mathrm{eff}}x_n=m_n\lambda+C,
\qquad m_n\in\mathbb Z.
\]

那么

\[
\psi_D(x_n)
=2\pi m_n+k_0(C-n_{\mathrm{eff}}x_f).
\]

所有 sites 的 nominal phase modulo \(2\pi\) 相同，共同 phase 是

\[
\psi_0=k_0(C-n_{\mathrm{eff}}x_f).
\]

因此，feed offset 不能被不一致地丢弃，但作为所有 sites 共享的常数，它不会破坏 alignment。证毕。

Strict monotonicity 保证每个 alignment level 在整个 real line 上至多一个 root；若限定 finite physical segment，还必须检查该 level 落在 segment 的 phase range 内。

---

## A.3 Amplitude extrema：isotropic、attenuation 和 directivity

### [PROVEN] \(A=1/R\) 的 exact extrema

对 interval \(I=[l,u]\)，令

\[
b_r=\sqrt{y_r^2+d^2}>0.
\]

最小和最大 distance 分别为

\[
R_{\min}
=
\sqrt{b_r^2+\operatorname{dist}(x_r,I)^2},
\]

\[
R_{\max}=\max\{R_r(l),R_r(u)\}.
\]

理由是 \(R_r(x)\) 随 \(|x-x_r|\) 单调增加；到 \(x_r\) 的最近点是 interval projection，最远点必为 endpoint。因此

\[
A^-=\frac1{R_{\max}},\qquad
A^+=\frac1{R_{\min}}.
\]

这与原 `amp_range` 一致。证毕。

### [PROVEN] 带 attenuation 和 directivity 时的 exact extrema

先把 angle convention 写清楚。假设

\[
\cos\theta=\frac{b_r}{R_r(x)},\qquad q\ge0,
\]

且 \(\cos^q\theta\) 是 **field-amplitude pattern**，则

\[
A(x)
=
\frac{e^{-\alpha(x-x_f)}\cos^q\theta}{R_r(x)}
=
b_r^q e^{-\alpha(x-x_f)}R_r(x)^{-p},
\quad p=q+1.
\]

若 \(\cos^q\theta\) 表示的是 **power pattern**，则 field amplitude 应取平方根，此时 \(p=1+q/2\)。

令 \(v=x-x_r\)。因为 \(A>0\)，

\[
\frac{A'(x)}{A(x)}
=
-\alpha-\frac{pv}{v^2+b_r^2}.
\]

所以 interior stationary points 满足

\[
\alpha v^2+pv+\alpha b_r^2=0.
\]

当 \(\alpha=0\) 时，只需检查 \(v=0\)。当 \(\alpha>0\) 时，若 discriminant 非负，候选 roots 是

\[
v_\pm
=
\frac{-p\pm\sqrt{p^2-4\alpha^2b_r^2}}{2\alpha}.
\]

在 compact interval 上，continuous differentiable function 的 extrema 必在 endpoints 或 interior stationary points。因此，计算 endpoints 以及所有落入 interval 的上述 roots，即得到 exact extrema。证毕。

两个不能忽略的 modeling details：

**[PROVEN]** 若 waveguide power loss 为 \(\ell\) dB/m，则 field attenuation coefficient 是

\[
\alpha=\frac{\ln 10}{20}\ell,
\]

因为 \(e^{-\alpha L}=10^{-\ell L/20}\)。这里不是 \(\ln 10/10\)。

此外，加入 attenuation 后必须说明“固定的是 feed-input power，还是总 radiated power”。不能对每个 layout 重新归一化其 attenuated amplitudes，却继续声称所有 layouts 使用相同 physical power model。

如果 amplitude 还依赖其他 activated sites 引起的 guided-power depletion，就不再是简单的 \(A_n(x_n+\delta_n)\) separable model。FullPASS 的模型明确包括 activation-dependent upstream loss；这部分不能被当前 precomputed tables 自动覆盖。citeturn174295view2

---

## A.4 Proposition 1：desired-gain lower bound

### [PROVEN] 原 proposition 在给定条件下成立

设所有 nominal phases modulo \(2\pi\) 等于 \(\psi_0\)，并令

\[
e_n(\delta_n)
=
\psi_D(x_n+\delta_n)-\psi_D(x_n).
\]

由 monotonicity 和 \(\beta_{D,n}\) 的定义，

\[
|e_n(\delta_n)|\le\beta_{D,n}\le\pi/2.
\]

旋转总 field：

\[
e^{j\psi_0}h_D
=
\sum_{n\in S}A_D(x_n+\delta_n)e^{-je_n}.
\]

逐项取 real part，

\[
A_D(x_n+\delta_n)\cos e_n
\ge
A^-_{D,n}\cos\beta_{D,n}
\ge0.
\]

因此

\[
|h_D|
\ge
\Re(e^{j\psi_0}h_D)
\ge
\sum_{n\in S}A^-_{D,n}\cos\beta_{D,n}.
\]

右侧 nonnegative，平方即得

\[
|h_D|^2
\ge
\left(
\sum_{n\in S}A^-_{D,n}\cos\beta_{D,n}
\right)^2.
\]

证毕。

### [CORRECTED] Clipping \(\beta\) 到 \(\pi/2\) 不是有效 extension

原代码中的

```python
np.cos(np.minimum(bD, np.pi / 2))
```

只有在已经确认所有 relevant \(\beta_{D,n}\le\pi/2\) 时才无害。

一旦某个 contribution 允许 negative projection，就不能把它的 lower bound 人为改成零：在 sector-information 层面，\(1+(-1)=0\) 已说明，把第二项的 negative contribution 忽略会产生假的 positive lower bound。

一个有效的 general extension 是令

\[
m_n=\cos(\min\{\beta_{D,n},\pi\}),
\]

\[
q_n=
\begin{cases}
A^-_{D,n}m_n,&m_n\ge0,\\
A^+_{D,n}m_n,&m_n<0.
\end{cases}
\]

则

\[
\boxed{
|h_D|^2\ge
\left[\sum_{n\in S}q_n\right]_+^2.
}
\]

证明：\(\cos e_n\ge m_n\)；当 \(m_n<0\) 时，最小 projection 使用最大 amplitude。因此每项 projection 至少为 \(q_n\)。再用 \(|h_D|\ge[\Re(e^{j\psi_0}h_D)]_+\) 即得。证毕。

**这篇 six-page paper 的更便宜选择是保留 \(\beta_D\le\pi/2\) 的工作区间，并让代码显式拒绝 invalid cases。**

---

## A.5 Proposition 2：sector support 和 angular grid

### [PROVEN] Sector support，包括 \(A^-\) branch

考虑

\[
\mathcal C_n
=
\left\{
Ae^{j\phi}:
A\in[A_n^-,A_n^+],\
\phi\in[\phi_n-\beta_n,\phi_n+\beta_n]
\right\}.
\]

令 \(d_{\mathbb S^1}(\theta,\phi_n)\in[0,\pi]\) 为 circular distance，并定义

\[
g_n(\theta)
=
\left[d_{\mathbb S^1}(\theta,\phi_n)-\beta_n\right]_+.
\]

沿该 arc，最大 directional cosine 为 \(\cos g_n(\theta)\)。当 \(\beta_n\ge\pi\) 时，arc 覆盖整个 circle，该式也给出 \(g_n=0\)。

Support function 为

\[
s_n(\theta)
=
\max_{w\in\mathcal C_n}
\Re(e^{-j\theta}w).
\]

固定最大 cosine 后，对 amplitude 优化：

\[
s_n(\theta)=
\begin{cases}
A_n^+\cos g_n(\theta),&\cos g_n(\theta)\ge0,\\
A_n^-\cos g_n(\theta),&\cos g_n(\theta)<0.
\end{cases}
\]

当 cosine 为 negative，较小 amplitude 才给出较大的 projection，因此 \(A^-\) branch 是必需的。证毕。

这里的 sector 是 true curve

\[
\left\{
z_P(x_n+\delta):|\delta|\le\epsilon
\right\}
\]

的 enclosing set。即使 amplitude extrema 和 phase interval 分别 exact，二者的 Cartesian product 通常仍不是 exact uncertainty set，因为 amplitude 和 phase 由同一个 \(\delta\) 决定。

### [PROVEN] Minkowski-sum support 给出 leakage bound

令

\[
\mathcal C_S=\sum_{n\in S}\mathcal C_n.
\]

Support functions 在 Minkowski sum 下相加：

\[
h_{\mathcal C_S}(\theta)=\sum_{n\in S}s_n(\theta).
\]

又因为

\[
|w|=\max_\theta \Re(e^{-j\theta}w),
\]

且两个 maxima 均存在，

\[
\max_{w\in\mathcal C_S}|w|
=
\max_\theta \sum_{n\in S}s_n(\theta).
\]

True field \(h_P\in\mathcal C_S\)，故

\[
|h_P|
\le
\max_\theta\sum_{n\in S}s_n(\theta).
\]

证毕。

### [PROVEN] 原 Lipschitz grid correction 有效

对任意 \(\theta,\eta\)，

\[
|s_n(\theta)-s_n(\eta)|
\le
A_n^+|e^{-j\theta}-e^{-j\eta}|
\le
A_n^+d_{\mathbb S^1}(\theta,\eta).
\]

第一步来自 support function 的定义及

\[
|\Re((e^{-j\theta}-e^{-j\eta})w)|
\le |e^{-j\theta}-e^{-j\eta}|\,|w|.
\]

所以总 support 的 Lipschitz constant 可取

\[
C_S=\sum_{n\in S}A_n^+.
\]

Uniform grid 的任意 angle 距最近 grid point 至多 \(\Delta\theta/2=\pi/K\)，因此

\[
\max_\theta\sum_ns_n(\theta)
\le
\max_{\theta_k}\sum_ns_n(\theta_k)
+\frac{\pi}{K}\sum_nA_n^+.
\]

证毕。

这是正确的 bound，但 D.2 给出的 multiplicative correction 在这个问题上明显更合适。

---

## A.6 Corollary：bracket、dominance 和 zero-error case

### [PROVEN] 正确 normalization 下的 bracket

定义

\[
L_D(S)
=
\frac1N
\left(
\sum_{n\in S}A^-_{D,n}\cos\beta_{D,n}
\right)^2,
\]

并设 \(B_P(S)\) 是 valid field-amplitude upper bound，

\[
\bar I(S)=\frac{B_P(S)^2}{N}.
\]

对任意 feasible \(\delta\)，

\[
G_D(S,\delta)\ge L_D(S),\qquad
I_P(S,\delta)\le\bar I(S).
\]

若 \(\sigma^2>0\)，则

\[
\frac{G_D(S,\delta)}{\sigma^2+I_P(S,\delta)}
\ge
\frac{L_D(S)}{\sigma^2+\bar I(S)}.
\]

取 minimum 得

\[
L(S)\le W(S).
\]

另一方面，对任意非空 feasible witness set \(\mathcal V_S\)，

\[
U(S)=
\min_{\delta\in\mathcal V_S}
\frac{G_D(S,\delta)}{\sigma^2+I_P(S,\delta)}
\ge W(S).
\]

故

\[
\boxed{L(S)\le W(S)\le U(S).}
\]

证毕。

这里并未假定 numerator 和 denominator 的 extrema 出现在同一个 error vector；分别取 bound 是安全的，代价是 conservatism。

同样，**L-BFGS-B 不必找到 global minimum，甚至不必成功收敛，才能产生 upper bound**。只要最终使用的 witness 确实 feasible，且 objective 重新 exact-model evaluation，它就提供一个 valid upper bound。

### [PROVEN] Certified dominance 与 noise inequality

直接由 bracket，

\[
L(S_R)>U(S_N)
\Longrightarrow
W(S_R)>W(S_N).
\]

固定 \(S_R,S_N,\hat\delta\)，写成

\[
\frac{a}{\sigma^2+b}
>
\frac{c}{\sigma^2+d}.
\]

在两个 denominators positive 时，交叉相乘等价于

\[
a(\sigma^2+d)>c(\sigma^2+b),
\]

即

\[
\boxed{
(a-c)\sigma^2>cb-ad.
}
\]

证毕。

### [CORRECTED] \(\epsilon=0\) 不能只“关闭 pad”

当 \(\epsilon=0\) 时，uncertainty set 是 singleton，因此应直接使用

\[
B_P(S)=\left|\sum_{n\in S}z_P(x_n)\right|,
\]

从而

\[
L(S)=W(S)=\operatorname{SLNR}_{\mathrm{nom}}(S).
\]

如果只删除 additive pad，却仍使用

\[
m_K=\max_{\theta_k}\Re(e^{-j\theta_k}h_P),
\]

通常有 \(m_K<|h_P|\)，从而低估 leakage。

一个 exact counterexample 是：singleton field 的 angle 位于两个 adjacent grid angles 的正中间。此时

\[
m_K=|h_P|\cos(\pi/K)<|h_P|.
\]

所以“不加 correction 的 sampled support”不是 valid upper bound。证毕。

**[NUMERICALLY OBSERVED]** 对本次 reference 的 \(S_N\)，原代码在 \(\epsilon=0\) 下得到

\[
L_{\mathrm{old}}=997.437583,
\]

而 exact nominal value 为

\[
999.737470.
\]

这里的 artificial relative loss 是 **0.23005%**，不是 2.78%。原文的 2.78% 最多只能是某个特定 instance 的观察。

---

## A.7 Lemma 3：完整证明与 explicit curvature bound

### [PROVEN] First derivative

对 \(A=1/R\)、\(t=(x-x_P)/R\)，

\[
A'=-\frac{t}{R^2},\qquad
\psi'=k_0(n_{\mathrm{eff}}+t).
\]

所以

\[
\boxed{
b_n=z_P'(x_n)
=
e^{-j\psi_n}
\left[
-\frac{t_n}{R_n^2}
-jk_0\frac{n_{\mathrm{eff}}+t_n}{R_n}
\right].
}
\]

原式正确。证毕。

### [PROVEN] Exact second derivative

由

\[
A''=\frac{3t^2-1}{R^3},\qquad
\psi''=k_0\frac{1-t^2}{R},
\]

以及

\[
z''
=
e^{-j\psi}
\left[
A''-A(\psi')^2
-j(2A'\psi'+A\psi'')
\right],
\]

得到

\[
\boxed{
z_P''(x)
=
e^{-j\psi}
\left[
\frac{3t^2-1}{R^3}
-\frac{k_0^2(n_{\mathrm{eff}}+t)^2}{R}
-jk_0\frac{1-3t^2-2n_{\mathrm{eff}}t}{R^2}
\right].
}
\]

这由直接 substitution 得到，因而是 exact identity。证毕。

### [PROVEN] Fully computable \(H_n\ge\sup|z_P''|\)

在第 \(n\) 个 interval 上，计算：

\[
r_n^-=\min_{|u|\le\epsilon}R_P(x_n+u),
\]

\[
t_n^-=
\frac{x_n-\epsilon-x_P}{R_P(x_n-\epsilon)},
\qquad
t_n^+=
\frac{x_n+\epsilon-x_P}{R_P(x_n+\epsilon)}.
\]

\(t(x)\) strictly increasing，因此这个 \(t\)-interval exact。

定义

\[
V_n=k_0(n_{\mathrm{eff}}+t_n^+),
\]

\[
C_n=
\max_{t\in[t_n^-,t_n^+]}|3t^2-1|,
\]

\[
E_n=
\max_{t\in[t_n^-,t_n^+]}
|1-3t^2-2n_{\mathrm{eff}}t|.
\]

计算 \(C_n\) 只需 endpoints 和 interval 内的 \(t=0\)；计算 \(E_n\) 只需 endpoints 和 interval 内的 \(t=-n_{\mathrm{eff}}/3\)。这是因为 absolute value 的 positive interior maxima 只能出现在原 polynomial 的 stationary points，而 zeros 不会产生更大的 absolute value。

于是可取

\[
\boxed{
H_n=
\sqrt{
\left(
\frac{C_n}{(r_n^-)^3}
+\frac{V_n^2}{r_n^-}
\right)^2
+
\left(
\frac{k_0E_n}{(r_n^-)^2}
\right)^2
}.
}
\]

证明：对 exact \(z''\) 的 real 和 imaginary parts 分别应用 triangle inequality、\(R\ge r_n^-\)、\(\psi'\le V_n\)，再合并平方即可。证毕。

注意 \(H_n\) 是一个 explicit upper bound，**不是声称等于 exact supremum**。

### [PROVEN] Taylor remainder

Integral remainder 给出

\[
z_P(x_n+\delta_n)
=
z_P(x_n)+b_n\delta_n
+
\delta_n^2
\int_0^1(1-v)z_P''(x_n+v\delta_n)\,dv.
\]

因此

\[
|r_n|
\le
\frac{\delta_n^2H_n}{2}
\le
\frac{\epsilon^2H_n}{2}.
\]

求和后

\[
h_P(\delta)=h_0+\sum_nb_n\delta_n+r,
\]

\[
\boxed{
|r|\le\rho
=
\frac{\epsilon^2}{2}\sum_{n\in S}H_n.
}
\]

证毕。

### [PROVEN] Random-sign averaging

令 \(s_n\) 为 auxiliary independent Rademacher signs。因为

\[
\mathbb E[s_n]=0,\qquad
\mathbb E[s_ns_m]=0\quad(n\ne m),
\]

有

\[
\mathbb E
\left|
h_0+\epsilon\sum_nb_ns_n
\right|^2
=
|h_0|^2+\epsilon^2\sum_n|b_n|^2.
\]

因此至少存在一个 sign vector \(s^\star\)，使 affine field magnitude 不小于该 mean-square 的平方根。对应的 physical corner \(\delta_n=\epsilon s_n^\star\) feasible，所以

\[
\max_\delta |h_P(\delta)|
\ge
\left[
\sqrt{|h_0|^2+\epsilon^2\sum_n|b_n|^2}
-\rho
\right]_+.
\]

平方并除以 \(N\sigma^2\)，得到原 Lemma 3。证毕。

这个证明只说明“某个 feasible error 会导致至少这么大的 leakage”，不说明另一个 subset 必然更好。因此它不能支持 universal \(\kappa\)-threshold。

### [PROVEN] Attenuation/directivity model 也可给出 explicit remainder

对 A.3 的 amplitude，设

\[
g(x)=\frac{A'}A
=-\alpha-\frac{p(x-x_P)}{R^2}.
\]

可取

\[
|g|\le G=\alpha+\frac{p}{2b_P},
\qquad
|g'|\le G'=\frac{p}{(r^-)^2},
\]

以及

\[
\psi'\le V,\qquad
|\psi''|\le V'=\frac{k_0b_P^2}{(r^-)^3}.
\]

因为 \(A''=A(g^2+g')\)，可取

\[
H
=
A^+
\sqrt{
(G^2+G'+V^2)^2
+
(2GV+V')^2
}.
\]

将这些 bounds 代入 exact general formula for \(z''\) 即得。证毕。

**[NUMERICALLY OBSERVED]** 我另外运行了 384,384 个 curvature sample checks；sampled \(|z''|/H\) 的最大值约为 \(0.999999999984\)。这支持实现正确性，但不替代上述 proof。

---

## A.8 Clearance、C1 和实际运行审计

### [PROVEN] Robust clearance 的必要且充分条件

考虑 nominally ordered adjacent selected sites \(x_i<x_j\)。其最小 actual separation 为

\[
\min_{\delta_i,\delta_j\in[-\epsilon,\epsilon]}
\big[(x_j+\delta_j)-(x_i+\delta_i)\big]
=
x_j-x_i-2\epsilon.
\]

Minimum 由 \(\delta_i=\epsilon,\delta_j=-\epsilon\) 达到。因此，所有 independent errors 下都保持 separation 至少 \(d_{\min}\)，当且仅当

\[
\boxed{x_j-x_i\ge d_{\min}+2\epsilon.}
\]

对所有 adjacent selected pairs 检查即可；非相邻 pairs 的 separation 是相邻 separations 的和。证毕。

**[NUMERICALLY OBSERVED]** 本次 candidates 的 minimum spacing 为

\[
0.6822207184\lambda.
\]

所以全部 subsets 自动 feasible 的 tolerance 上限是

\[
\epsilon/\lambda\le0.0911103592.
\]

当 \(\epsilon=0.1\lambda\) 时：

| 项目 | 结果 |
|---|---:|
| 未筛选 subsets | 735,471 |
| 满足 robust clearance 的 subsets | 112,251 |
| reference \(S_N\) 是否仍 feasible | 否 |
| reference \(S_R\) 是否仍 feasible | 否 |

这不会推翻 \(\epsilon=0.05\lambda\) 的 reference result，但会影响任何未经 filtering 的较高-tolerance aggregate result。

### [CORRECTED] C1 的正确适用范围

在 **frozen amplitudes** 下，令 \(\alpha_n\ge0\)、\(\sum_n\alpha_n=1\)，并令 phase errors 为 \(e_n\)。则

\[
\left|\sum_n\alpha_ne^{-je_n}\right|^2
=
\sum_{n,m}\alpha_n\alpha_m\cos(e_n-e_m).
\]

用 cosine expansion，

\[
\left|\sum_n\alpha_ne^{-je_n}\right|^2
=
1-\operatorname{Var}_\alpha(e)+O(\|e\|^4).
\]

因为

\[
\frac12\sum_{n,m}\alpha_n\alpha_m(e_n-e_m)^2
=
\sum_n\alpha_ne_n^2-
\left(\sum_n\alpha_ne_n\right)^2.
\]

证毕。

若 \(e\approx k_0D_\xi\delta\)，且 \(\delta\) zero-mean、covariance 为 \(\Sigma\)，才有你给出的 trace predictor。若 mean 为 \(\mu\ne0\)，还要加入

\[
k_0^2
\mu^\mathsf TD_\xi M_\alpha D_\xi\mu.
\]

此外，common position error 不等于 common phase error。若 \(\delta_n=\delta\)，其 phase-variance term 是

\[
k_0^2\delta^2\operatorname{Var}_\alpha(\xi),
\]

只有 \(\xi_n\) 相同才严格消失。Amplitude perturbations 还会产生其他 terms。

### [NUMERICALLY OBSERVED] Reference reproduction

实际运行输出为：

```text
S_nom [1 6 7 8 16 18 19 20]
S_rob [3 4 7 8 9 13 14 17]
L(S_rob)=53.422
U(S_nom)=42.154
certified gain=+26.7%
```

本次环境为 Python 3.13.5、NumPy 2.3.5、SciPy 1.17.0，CPU execution，BLAS threads 设为 1。

另外运行了：

- 100,000 个 feasible random checks，其中 80,000 个使用 nonzero tolerance；
- 40 个 endpoint-witness-bank 与全部 256 corners 的 identity checks；
- 100 个 sector-support checks，其中 28 个涉及 negative support branch。

Random checks 中最小 \( \mathrm{SLNR}-L\) 为约 \(-3.4\times10^{-13}\)，属于本次 observed floating-point scale；没有发现大于 \(10^{-10}\) 的 violation。

**没有完成的部分：**本次没有执行 outward-rounded validated interval arithmetic。因此应区分：

> 数学上的 exact-arithmetic certificate；  
> `float64` 对 certificate inequalities 的 numerical verification。

### 哪些内容 standard，哪些与 PASS 真正相关？

Projection lower bounds、support functions、Minkowski sums、interval enclosures、Taylor remainders 和 random-sign averaging 都不宜单独列为新的 fundamental tools。Arnestad et al. 已系统使用 interval/Minkowski geometry 处理 array uncertainty。citeturn903389view6turn203911view7

真正与当前 PASS task 紧密相关的是：guided-path derivative floor、无 phase shifter 的 D-aligned site construction、independent actuator errors 与 robust clearance 的结合，以及如何把这些结构变成可核查的 finite-family selection guarantees。PASS alignment 和 propagation model 本身仍应引用其基础工作。citeturn883219view1

---

# 3. Task B — Hostile ICC review

## Mock review

**评审对象：原 A7 方案，而不是后文新增的 global-screening 版本。**

### Summary

论文研究 finite D-aligned candidate family 内的 PASS site selection，在 independent bounded actuator position errors 下优化 worst-case SLNR。作者使用 desired-field projection lower bound 和 leakage sector-support upper bound，构造可计算的 robust objective，并通过 swap local search 选择 sites。Feasible adversarial witnesses 用于证明某些 robust designs 优于 exhaustive nominal optimum。

### Strengths

问题定义比泛化的“robust PASS optimization”更具体：errors 作用于实际 radiating positions，且同时影响 desired 和 protected channels。

比较基准中的 exhaustive nominal optimum 是实质性优点，避免把收益建立在弱 nominal heuristic 上。

论文有清楚的 mathematical guarantee 路径，不依赖 Monte Carlo success rate 来声称 robustness。

### Weaknesses

主要 mathematical ingredients 已有明确先例。当前版本容易被看作 existing interval tools、PASS propagation model 和 local search 的组合，而不是新的 optimization insight。尤其不能忽略近期的 nonlinear position-error robust MA work，以及已经讨论 multi-PA position errors 的 Hybrid PASS。citeturn174295view3turn360996view6

D-aligned restriction 虽然合理，但也是一个有利于证明、未必有利于 globally optimal SLNR 的限制。论文必须解释为何这是一个有意义的 architecture/design constraint，而不是只为产生结果而选择的 family。

现有 empirical story 还存在混淆：free-family gain、matched-endpoint gain、certificate tightness 和真实 robust improvement 不能互相替代。

代码层面的 clearance omission，以及对 \(\epsilon=0\) 和 invalid \(\beta_D\) 的处理，要求完整 audit。

### Score、confidence、decision

**[CONJECTURE]**

- **Score：5/10**
- **Confidence：4/5**，但这不是对完整 six-page manuscript 的正式评审。
- **Decision：Weak Reject / Borderline**

如果加入后文的 global witness screening、finite-family converse/achievability，并完成 matched-family 和 numerical audit，我会把它重新评为约 **7/10、Weak Accept**，而不只是“修复后仍然相同的论文”。

---

## Top 5 rejection risks 与 cheapest fixes

| Rejection risk | Reviewer 最可能的质疑 | 最便宜的修复 |
|---|---|---|
| **1. Novelty collision** | “Sector bounds、nonlinear phase enclosure、position-error robustness 都不是新的。” | 不以这些工具为主贡献；改为 shared-witness global screening、a posteriori global certificates、finite-family leakage converse |
| **2. Restricted family / baseline fairness** | “你只打败了自己限制后的 nominal design。” | 主图使用 matched endpoints、same power/noise/clearance；加一个 corner-robust selection baseline；所有结论明确限定于 \(\mathcal F_\epsilon\) |
| **3. Certificate implementation correctness** | “理论成立，但程序没有执行理论 assumptions。” | 加 phase/clearance guards、exact zero-error branch、feasible-witness re-evaluation；对关键 comparisons 做独立 numerical audit |
| **4. Idealized PASS hardware model** | “Equal per-site power 忽略 upstream depletion；attenuation 加法不一致。” | 明确 ideal equal-power architecture；做 separable attenuation/directivity controls；不声称覆盖 selection-dependent coupling |
| **5. Evidence 与 claimed generality 不匹配** | “只展示 favorable geometry；gain 是否来自 aperture；gap 是否普遍 tight？” | 公布完整 geometry grid、negative cases、nominal sacrifice、runtime/gap distributions；把未证实情况标为 inconclusive |

## “Certified dominance over exhaustive nominal optimum within a matched aligned family”公平吗？

**公平，而且有意义，但意义必须准确限定。**

**[PROVEN]** 在相同 \(\mathcal F_\epsilon\)、\(N\)、noise、power 和 uncertainty set 下，如果

\[
S_N\in\arg\max_{S\in\mathcal F_\epsilon}
\operatorname{SLNR}_{\mathrm{nom}}(S),
\]

并且

\[
L(S_R)>U(S_N),
\]

那么你证明了：

> 在该 matched hardware/design family 内，nominal-optimal selection 并不是 robust-optimal selection，而且改进不是 nominal solver 没有求好造成的。

这是一个严格且有解释力的结论。

但它**没有**证明：

- D-aligned restriction 对 SLNR globally optimal；
- 方法优于所有 continuous-position PASS designs；
- 方法优于所有其他 robust optimization approaches；
- nominal performance 没有代价。

Matched endpoints 只固定 **nominal aperture span**。它不固定 internal spacing、aperture second moment、amplitude distribution 或受 errors 影响后的 actual aperture。内部结构正是 selection 的设计自由度，但论文不应把“相同 endpoints”描述成“除算法之外一切 electromagnetic properties 均相同”。

我的建议是把 D-aligned family 解释为：

> 一个通过 nominal coherent delivery、无需 per-site phase shifters 的 phase-aligned codebook，研究在保留这一 architecture constraint 后，如何分配剩余的 site-selection freedom 来保护 P。

这比把它包装成 unrestricted PASS optimum 更可信。

---

# 4. Task C — Verified collision search

我核验了下列 arXiv records、相关正文，以及 Hybrid PASS 的 author-hosted paper/DOI。IEEE Xplore 和 Google Scholar 的部分站内查询未能完整读取，因此这不是一次可声称“穷尽全部数据库”的 search。

## 已核验的主要相关论文

| Paper / verified identifier | 与 A7 的真实重叠 | 对 novelty claim 的影响 |
|---|---|---|
| **FullPASS: Geometry Optimization for Full-Duplex Pinching-Antenna Systems** — **arXiv:2607.19546** | Binary activation、desired links、self-interference leakage constraint、guided attenuation 和 activation-dependent upstream loss；正文将 position uncertainty 留作 future work | 是最接近的 PASS selection/task collision，但不是 A7 的 independent actuator-box robust certificate。citeturn174295view2turn203911view5 |
| **Robust Beamforming and Antenna Position Optimization for MA-Assisted ISAC with Imperfectly Positioned MAs** — **arXiv:2609.23323** | 明确处理 position errors，使用 nonlinear phase enclosure 和 all-error robust constraints | 直接排除“首次 nonlinear all-error position-error certificate”。其 enclosure 不是你这里的 annular-sector formulation，不能混称。citeturn174295view3turn360996view4 |
| **Movable Antenna-Enhanced Near-Field Flexible Beamforming: Performance Analysis and Optimization** — **arXiv:2601.17825** | Near-field desired/nulling design；讨论 bounded per-element position errors，采用 Taylor-based worst-case analysis/optimization | 排除“首次 near-field position-error robust nulling”；需强调 PASS guided phase、finite selection 和 nonlinear certification 的区别。citeturn931337view2turn903389view5 |
| **Hybrid Pinching Antenna Systems: Architecture and Beamforming Design** — **DOI:10.1109/TWC.2026.3664320** | Multi-PA position errors 及性能影响；用 reconfigurable leaky-wave antenna/electronic beamforming 提高 robustness | 不能声称“首次研究 multiple coherent PASS antennas 的 position errors”；你的区别是 bounded all-error site selection，而非仅 error simulation 或硬件补偿。citeturn360996view6turn170539view5 |
| **Impact of Position Uncertainty on the Secrecy Performance of Pinching Antenna Systems** — **arXiv:2604.12156** | Pinching-position activation uncertainty、Bob/Eve channel dependence、secrecy outage；system model 明确为一个 reconfigurable radiator，并将 multi-PA extension 留待未来 | 与 position-error/secrecy framing 重叠，但不是 multi-element coherent robust selection。citeturn785204view3 |
| **Pinching Antenna-Assisted Full-Duplex Communication Systems** — **arXiv:2609.29200** | PASS positions、beamforming、power allocation 和 WMMSE-based nominal full-duplex optimization | 是近期 nominal design 背景；已核验内容没有给出 A7 的 actuator-box certificate。citeturn903389view1turn206025view2 |
| **Robust and Secure Blockage-Aware Pinching Antenna-assisted Wireless Communication** — **arXiv:2601.06430** | Robust/secure PASS、geometry/CSI-related uncertainty 和 secrecy design | 说明转向“robust secrecy PASS”不会自动增加 novelty；其 uncertainty 不是当前 independent per-actuator boxes。citeturn417071view0 |
| **Worst-case analysis of array beampatterns using interval arithmetic** — **arXiv:2306.13106**, **DOI:10.1121/10.0019715** | Annular sectors、Minkowski sums、worst-case beampatterns、backtracking，以及多类 array uncertainties | 是 sector/interval geometry 的关键 prior art。不能把这些 generic tools 本身写成主要新定理。citeturn903389view6turn203911view7 |
| **Sparse Fluid Antenna Arrays: Continuous Position Design Beyond Classical DOF Limits** — **arXiv:2605.19455** | Sparse FAS、continuous positions、DOA estimation；明确分析 finite position accuracy | 是 related position-accuracy work，但其主要 task 是 DOA estimation，不是 A7 的 robust SLNR selection。citeturn785204view2 |

### 两处应纠正的 literature interpretation

**Xiu et al., arXiv:2508.13839** 的 *Distributed Distortion-Aware Robust Optimization for Movable Antenna-aided Cell-Free ISAC Systems*，其主要 hardware uncertainty 是 power-amplifier distortion coefficients，而不是可直接等同于 actuator position errors。不能仅凭“hardware impairment”就把它列为同一 uncertainty model 的直接 baseline。citeturn417071view1

**Xu–Ding–Schober–Chang, arXiv:2506.23966** 确实研究 in-waveguide attenuation 及 position optimization。因此 generic attenuation-driven upstream placement 不能在这篇文章里重新包装为核心 novelty。citeturn417071view2

Poli et al. 的 phase-tolerance 条目和 **DOI:10.1109/TAP.2015.2421952** 可在已核验的 Arnestad bibliography 中核对；本次没有独立逐式审阅 Poli 原文，因此不对其具体 theorem coverage 作进一步断言。citeturn203911view6

## 是否已有论文包含完整 A7 result？

**在本次已核验的正文中，没有找到同时包含以下组合的工作：**

> PASS guided-phase model + multiple coherent selected sites + independent bounded actuator errors + nonlinear all-error SLNR bracket + dominance over exhaustive nominal selection in a matched D-aligned family。

但这不等于证明“全世界没有做过”。

更重要的是，即使完整组合尚未出现，**原 A7 仍然可能被认为是 incremental combination**。因此，我建议把贡献进一步推进到下一节的 global witness screening 和 converse/achievability，而不是依赖“组合尚未见过”来支撑整篇论文。

---

# 5. Task D — Innovation upgrades

下表的 acceptance lift 是 **[CONJECTURE]**：是对稿件说服力的主观判断，不是统计预测，也不能相加。

| Rank | Upgrade | 工作量判断 | 主观 acceptance lift | 是否进入主稿 |
|---|---|---|---|---|
| 1 | Shared endpoint-witness bank + global screening | 核心实现已运行；主要剩余工作是扩展 audit | 约 +10–15 percentage points | **必须** |
| 2 | Asymmetric sectors + multiplicative angular certificate | 已实现；proof 很短 | 约 +2–4 points | **必须** |
| 3 | Remainder-free leakage converse + achievability bracket | 可复用 witness bank；已得到实例结果 | 约 +3–6 points | **建议** |
| 4 | Interference-temperature feasibility corollary | 少量推导和 threshold plots | 约 +1–3 points | 简短 corollary/解释 |
| 5 | 正确的 noise-region dominance theorem | 推导便宜，实验简单 | 约 +0–2 points | Remark，非主贡献 |
| 6 | Dependency-aware error-box refinement | 实现风险较高，可能消耗剩余时间 | 约 +0–3 points | Optional |

---

## D.1 最佳升级：shared endpoint witnesses 与 global screening

### Idea

不要只对最终两个 layouts 计算 upper bounds。

应当利用 endpoint structure，为 **整个 candidate family** 快速生成 feasible-witness upper bounds，用来：

1. 安全排除不可能击败 incumbent 的 layouts；
2. 精确优化当前 certificate；
3. 给出 global robust optimum 的 upper bound；
4. 在条件满足时，直接证明某个 layout 是 unique global robust optimum。

### [PROVEN] Theorem：至多 \(2M\) 个 shared templates 覆盖所有 subset 的 endpoint leakage maxima

定义每个 candidate site 的 exact endpoint contributions：

\[
z_n^\pm=z_P(x_n\pm\epsilon),
\]

\[
m_n=\frac{z_n^++z_n^-}{2},
\qquad
v_n=\frac{z_n^+-z_n^-}{2}.
\]

对 subset \(S\)，所有 endpoint sums 的 convex hull 是

\[
\mathcal Z_S
=
\sum_{n\in S}m_n+
\sum_{n\in S}[-v_n,v_n].
\]

这是 translated two-dimensional zonotope。

对任意 direction \(\theta\)，其 support-maximizing signs 为

\[
s_n(\theta)
=
\operatorname{sign}
\Re(e^{-j\theta}v_n).
\]

每个 nonzero \(v_n\) 的 sign 只会在

\[
\theta=\arg v_n\pm\pi/2
\]

处变化。收集全部 \(M\) 个 sites 的 breakpoints，circle 被分成至多 \(2M\) 个 cells。在每个 cell 内取一个 angle，即得到共同 sign templates

\[
s^{(1)},\ldots,s^{(H)}\in\{-1,1\}^M,
\qquad H\le2M.
\]

那么，对任意 subset \(S\)，

\[
\boxed{
\max_{s\in\{-1,1\}^{|S|}}
\left|
\sum_{n\in S}z_n^{s_n}
\right|^2
=
\max_{1\le q\le H}
\left|
\sum_{n\in S}z_n^{s_n^{(q)}}
\right|^2.
}
\]

#### Proof

Endpoint sums 是 hypercube vertices 在线性映射下的 images，其 convex hull 正是 \(\mathcal Z_S\)。

Convex function \(|w|^2\) 在 polygon 上的最大值可在某个 vertex 达到：任意 point 是 vertices 的 convex combination，convexity 保证其 function value 不超过 vertices 中的最大值。

每个 zonotope vertex 都可由某个非 breakpoint direction 的 support maximization 得到。该 direction 下各 segment 的 maximizing sign 是 \(\operatorname{sign}\Re(e^{-j\theta}v_n)\)。

使用全部 \(M\) 个 sites 的 breakpoints 只会进一步细分 subset 自身的 angular cells，不会漏掉任何 subset vertex。因此每个 subset 的 maximizing endpoint sum 都由至少一个 shared template 的 restriction 表示。反向不等式显然成立，因为每个 template restriction 本身就是 endpoint corner。证毕。

**边界：**这个 theorem 对 **endpoint leakage maximum** exact；它没有声称 nonlinear box maximum 必在 endpoints，更没有声称 SLNR minimum 必在这些 templates 中。

### [PROVEN] Corollary：全 family 的 feasible-witness upper bounds

对每个 template，用同一个 error vector 同时计算 D 和 P：

\[
\delta_{n,q}=\epsilon s_n^{(q)}.
\]

定义

\[
U_H(S)
=
\min_q
\frac{G_D(S,\delta_q)}
{\sigma^2+I_P(S,\delta_q)}.
\]

因为每个 \(\delta_q\) feasible，

\[
W(S)\le U_H(S).
\]

设 incumbent 为 \(\widehat S\)，且 \(\ell=L(\widehat S)\)。那么

\[
U_H(S)\le\ell
\]

的任何 layout 都不可能具有比 incumbent 更好的 true worst-case SLNR，因为

\[
W(S)\le U_H(S)\le\ell\le W(\widehat S).
\]

同样，其 certificate 也不可能超过 \(\ell\)。因此，对剩余 layouts 计算 \(L\)，并随着 incumbent 提升继续 pruning，最后能精确求出

\[
\max_{S\in\mathcal F_\epsilon}L(S).
\]

证毕。

### [PROVEN] Global robust bound 与 unique-optimality test

令

\[
U^\star=\max_{S\in\mathcal F_\epsilon}U_H(S).
\]

则

\[
\boxed{
L(\widehat S)\le
W^\star:=\max_{S\in\mathcal F_\epsilon}W(S)
\le U^\star.
}
\]

从而，只要 \(U^\star>0\)，

\[
\frac{W(\widehat S)}{W^\star}
\ge
\frac{L(\widehat S)}{U^\star}.
\]

更强地，如果

\[
\boxed{
L(\widehat S)>
\max_{S\in\mathcal F_\epsilon,\ S\ne\widehat S}U_H(S),
}
\]

那么对每个 rival，

\[
W(\widehat S)\ge L(\widehat S)>U_H(S)\ge W(S),
\]

所以 \(\widehat S\) 是该 family 内的 **unique global robust-optimal layout**。证毕。

### [NUMERICALLY OBSERVED] 本次已经得到的结果

同样使用

\[
P=(3,2),\quad
\epsilon=0.05\lambda,\quad
\mathrm{SNR}_{\rm ref}=30\text{ dB}.
\]

| 项目 | Free family | Matched endpoints \(0,23\) |
|---|---:|---:|
| Family size | 735,471 | 74,613 |
| Shared templates | 48 | 48 |
| Initial screening 后 survivors | 1 | 12 |
| Final \(L(\widehat S)\) | 56.559334 | 55.574007 |
| \(U^\star\) | 56.582829 | 55.603996 |
| 最大 rival \(U_H\) | 56.238460 | 55.527391 |
| Strict layout-dominance margin | 0.320874 | 0.046616 |
| Global value-bracket relative width \(U^\star/L-1\) | 0.04154% | 0.05396% |
| 对 exhaustive nominal 的 certified gain | **34.17%** | **2.79%** |

对应 layouts 为

```text
Free:
S_R = [0, 1, 4, 5, 6, 11, 14, 19]

Matched endpoints:
S_R = [0, 1, 4, 8, 9, 12, 13, 23]
```

这两个 numerical instances 都满足上面的 strict unique-optimality inequality。

需要区分：表中的 \(U^\star/L-1\) 是 **value bracket width**。一旦 unique-layout condition 被可靠验证，layout selection 本身已被证明 global optimal；只是其 exact worst-case objective value 仍位于一个小 interval 内。

本次全 family witness enumeration 约为 1.59 s，整个 featured-instance audit 约为 1.78 s。这是本容器的 observed runtime，不是普遍性能保证。

### Complexity 与风险

**[PROVEN]** 若实际计算 certificate 的 survivor 数为 \(J\)，主要成本为

\[
O\!\left(
MK+MH+
|\mathcal F_\epsilon|NH+
JNK
\right),
\qquad H\le2M.
\]

各项分别来自 sector tables、endpoint tables、全 family witness evaluations 和 survivor certificate evaluations。可以 batching，避免保存全部高维 temporary arrays。

**最坏情况仍然随 \(|\mathcal F_\epsilon|\) 增长。**不能把它宣传为 polynomial-time solution。若 D 与 P responses 很相似，witness upper bounds 可能较松，\(J\) 可以很大。

Generic zonotope geometry 也不应宣称首次提出。贡献应放在：**exact nonlinear endpoint evaluations 被组织成全 family 共享的 adversarial witness bank，并用于 robust selection 的 safe screening 和 optimality certification。**

### 对 Dinkelbach、sorting、DP 的判断

**[CORRECTED]** “固定 \(\theta\) 时 support additive，因此 Dinkelbach + per-angle sorting 可以解完整问题”不成立。

原因有两个：不能随意交换 selection 与 worst-direction optimization；\((\sum c_n)^2\) 和 \((\sum s_n)^2\) 也没有因 Dinkelbach 而变成 per-site additive objective。

一个 elementary noncommutation example 是两个 singleton complex fields \(+1,-1\)。它们的 supports 为 \(\cos\theta,-\cos\theta\)，于是

\[
\min_S\max_\theta h_S(\theta)=1,
\]

但

\[
\max_\theta\min_S h_S(\theta)
=
\max_\theta[-|\cos\theta|]
=0.
\]

因此这种 min–max interchange 没有一般依据。

不过存在一个正确的 approximation result。

**[PROVEN]** 写

\[
L(S)=\frac{C(S)^2}{N\sigma^2+B(S)^2},
\qquad
C_{\min}\le C(S)\le C_{\max}.
\]

若 \(\widetilde S\) exact minimizes \(B(S)\)，则

\[
\boxed{
\frac{L(\widetilde S)}
{\max_{S\in\mathcal F_\epsilon}L(S)}
\ge
\left(\frac{C_{\min}}{C_{\max}}\right)^2.
}
\]

证明：令 \(S^\star_L\) maximize \(L\)。由 \(B(\widetilde S)\le B(S^\star_L)\)，并分别使用 numerator 的 lower/upper bounds，即得该 ratio。证毕。

\(B\)-minimization 可写成 binary MILP：

\[
\min_{u,b} b,
\]

\[
b\ge
\frac{\sum_n s_n(\theta_k)u_n}{\cos(\pi/K)}
\quad\forall k,
\]

加上 cardinality、clearance conflicts 和 forced endpoints。SciPy 提供 `milp`，并返回 MIP gap/dual-bound information，但它不意味着 unrestricted polynomial complexity。citeturn174295view0

**[NUMERICALLY OBSERVED]** 本 reference 的简单 coefficient ratio 为约 \(0.98807\)。但我没有实际运行该 MILP；它是一个可选 backup，不应写成已完成的 exact optimization result。

---

## D.2 Asymmetric sectors + multiplicative angular correction

### Idea

True endpoint phase interval 通常不以 nominal phase 为中心。使用

\[
\phi_{c,n}
=
-\frac{\psi_P(x_n+\epsilon)+\psi_P(x_n-\epsilon)}2,
\]

\[
\beta_{c,n}
=
\frac{\psi_P(x_n+\epsilon)-\psi_P(x_n-\epsilon)}2
\]

构造 sector，可避免不必要的 symmetric expansion。

其次，使用 support geometry 的 multiplicative correction，而不是 additive Lipschitz pad。

### [PROVEN] Theorem：uniform angular sampling 的 multiplicative radius bound

对任意 nonempty compact set \(\mathcal C\subset\mathbb C\)，设

\[
R_{\mathcal C}=\max_{w\in\mathcal C}|w|,
\]

\[
m_K=
\max_{\theta_k}
\max_{w\in\mathcal C}
\Re(e^{-j\theta_k}w),
\]

其中 grid uniform，\(K\ge3\)。则

\[
\boxed{
m_K\le R_{\mathcal C}
\le \frac{m_K}{\cos(\pi/K)}.
}
\]

#### Proof

第一项由 projection 不超过 modulus 立即成立。

取 \(w^\star\) 满足 \(|w^\star|=R_{\mathcal C}\)。存在 grid angle \(\theta_k\)，使

\[
|\theta_k-\arg w^\star|_{\mathbb S^1}\le\pi/K.
\]

因此

\[
m_K
\ge
\Re(e^{-j\theta_k}w^\star)
\ge
R_{\mathcal C}\cos(\pi/K).
\]

因 \(K\ge3\)，cosine positive，除以它即得。证毕。

应用于 enclosing Minkowski sum，得到

\[
B_P(S)=
\frac{\max_k\sum_{n\in S}s_n(\theta_k)}
{\cos(\pi/K)}.
\]

**[NUMERICALLY OBSERVED]** 在 \(K=1440\) 时，对 enclosure radius 的 angular discretization，power inflation factor 不超过

\[
\sec^2(\pi/1440)-1
\approx4.76\times10^{-6}.
\]

这只控制 **angular discretization**，不控制 sector enclosure、D/P dependency 或 subset search 的 conservatism。

**最小实验：**固定同一 subset，比较 old pad、symmetric-sector sec correction、asymmetric-sector sec correction，避免把不同 local-search outputs 的变化全部归因于一个 bound。

**风险：**数学本身 generic，不能作为唯一 novelty。它的价值是让主结论更紧、更可信。

---

## D.3 Remainder-free converse / achievability pair

### Idea

与其使用可能被 \(\rho\) 吃掉的 Taylor converse，不如直接使用 exact endpoint contributions。

### [PROVEN] Exact endpoint averaging converse

沿用 D.1 的 \(m_n,v_n\)。Auxiliary random-sign averaging 给出

\[
\mathbb E
\left|
\sum_{n\in S}(m_n+s_nv_n)
\right|^2
=
\left|\sum_{n\in S}m_n\right|^2
+
\sum_{n\in S}|v_n|^2.
\]

所以

\[
\max_\delta |h_P(S,\delta)|^2
\ge
\left|\sum_{n\in S}m_n\right|^2+
\sum_{n\in S}|v_n|^2.
\]

证明与 A.7 的 zero-cross-term argument 相同，但这里使用 exact nonlinear endpoint values，没有 Taylor remainder。证毕。

### [PROVEN] 使用 guided sensitivity floor 的 strictly positive family converse

令

\[
\eta=
\min\left\{
\epsilon,\,
\frac{\pi}{2k_0(n_{\mathrm{eff}}+1)}
\right\}.
\]

使用 feasible sub-box endpoints \(x_n\pm\eta\)。设其 phase difference 为 \(\Delta\psi_n\)，则由 Lemma 0，

\[
k_0(n_{\mathrm{eff}}-1)\eta
\le
\frac{\Delta\psi_n}{2}
\le
k_0(n_{\mathrm{eff}}+1)\eta
\le\pi/2.
\]

Exact identity 为

\[
|v_n|^2
=
\frac{(A_n^+-A_n^-)^2}{4}
+
A_n^+A_n^-
\sin^2\left(\frac{\Delta\psi_n}{2}\right),
\]

这里 \(A_n^\pm\) 表示两个 endpoint amplitudes，而不是 extrema notation。

若 \(\underline A_n\) 是该 sub-box 上的 amplitude minimum，则

\[
|v_n|^2
\ge
\underline A_n^2
\sin^2\left(k_0(n_{\mathrm{eff}}-1)\eta\right).
\]

因此

\[
\boxed{
\min_{S\in\mathcal F_\epsilon}
\max_\delta |h_P(S,\delta)|^2
\ge
\sin^2\left(k_0(n_{\mathrm{eff}}-1)\eta\right)
\min_{S\in\mathcal F_\epsilon}
\sum_{n\in S}\underline A_n^2.
}
\]

证明：endpoint-difference identity 来自展开
\(\frac14|A_+e^{-j\psi_+}-A_-e^{-j\psi_-}|^2\)；随后使用 sine 在 \([0,\pi/2]\) 上单调、amplitudes 的 lower bound，以及上面的 averaging converse。证毕。

只要 \(\epsilon>0\)、finite family 非空、selected amplitudes positive，右侧严格为正。

它不是 geometry-independent universal floor：当 P 远离所有 sites 时，amplitudes 可以很小。它也不是 robust selection 必然获益的 theorem。

### [PROVEN] Additive floor 可用 DP exact 计算

将 sites 按 \(x\) 排序，令 \(p(i)\) 为与 site \(i\) 满足 clearance 的最大前驱 index。对 additive weights \(w_i\)，定义

\[
D[i,k]
=
\min\left\{
D[i-1,k],\,
w_i+D[p(i),k-1]
\right\}.
\]

第一种情况不选 \(i\)；第二种情况选 \(i\)，其余 selected sites 必位于 \(p(i)\) 之前。两类穷尽所有 feasible selections，因此 recurrence exact。初始化 \(D[i,0]=0\)，不可行状态为 \(+\infty\)。计算成本为 \(O(MN)\)。Forced endpoints 可先固定并删除与其冲突的 interior sites。证毕。

### [PROVEN] 更强、可直接计算的 endpoint converse / achievability bracket

定义

\[
F_{\rm end}
=
\min_{S\in\mathcal F_\epsilon}
\max_{q\le H}
\frac1N
\left|
\sum_{n\in S}z_P(x_n+\epsilon s_n^{(q)})
\right|^2.
\]

由 D.1，内部 maximum 是 exact endpoint maximum；endpoint set 是 full box 的 subset。所以

\[
F_{\rm end}
\le
\min_{S\in\mathcal F_\epsilon}\max_\delta I_P(S,\delta).
\]

另一方面，对任意 selected layout \(\widehat S\)，

\[
\min_S\max_\delta I_P(S,\delta)
\le
\max_\delta I_P(\widehat S,\delta)
\le\bar I(\widehat S).
\]

因此

\[
\boxed{
F_{\rm end}
\le
\min_S\max_\delta I_P(S,\delta)
\le
\bar I(\widehat S).
}
\]

证毕。

### [NUMERICALLY OBSERVED] 本例的 converse / achievability 已很接近

| Family | \(F_{\rm end}\) | Selected-layout \(\bar I\) | Relative bracket width |
|---|---:|---:|---:|
| Free | 0.0118577594 | 0.0118626192 | 0.04098% |
| Matched endpoints | 0.0120698441 | 0.0120764004 | 0.05432% |

本例中，SLNR-certificate-optimal subset 恰好也达到 minimum endpoint worst leakage。这是 **instance observation**，不是一般 equivalence theorem。

**最小实验：**在主 grid 中报告这个 leakage bracket 的 distribution，至少包括 tight、loose 和 P≈D cases。

**风险：**不要把一个 instance 的 near-matching converse 描述成 universal tightness。

---

## D.4 Task reframing：优先 interference temperature，不转 secrecy 主线

### [PROVEN] Certified power-feasibility corollary

给定 layout 的 bounds

\[
G_D\ge L_D>0,\qquad I_P\le\bar I,
\]

设 total transmit power 为 \(p\in[0,p_{\max}]\)，desired SNR target 为 \(\gamma\)，protected interference ceiling 为 \(I_{\max}\)。

Certificate constraints 是

\[
pL_D\ge\gamma\sigma_D^2,
\qquad
p\bar I\le I_{\max}.
\]

它们存在 feasible \(p\)，当且仅当

\[
\boxed{
\frac{\gamma\sigma_D^2}{L_D}
\le
\min\left\{
p_{\max},
\frac{I_{\max}}{\bar I}
\right\}.
}
\]

若 \(\bar I=0\)，第二个 upper bound 解释为 \(+\infty\)。

证明：第一项给出 \(p\) 的 lower bound，后两项给出 upper bounds；interval 非空恰好等价于该 inequality。证毕。

这里的“当且仅当”只对 **certificate constraints** 成立，不是对原 physical robust feasibility 的必要充分条件。

结合 D.3，还得到必要条件：

\[
pF_{\rm end}>I_{\max}
\]

时，没有任何 family member 能在所有 errors 下满足 leakage ceiling。理由是每个 layout 的 true worst leakage 至少为 \(F_{\rm end}\)。

这形成了清楚的 engineering task：

> 哪些 protection requirements 是该 actuator tolerance 下根本不可能满足的，哪些可以由某个 layout certified 满足？

### Secrecy 是否值得转？

**[PROVEN]** 对明确定义的 instantaneous Gaussian secrecy-rate metric，可由 monotonicity 得到

\[
R_s^{\rm wc}
\ge
\left[
\log_2\left(1+\frac{pL_D}{\sigma_D^2}\right)
-
\log_2\left(1+\frac{p\bar I}{\sigma_P^2}\right)
\right]_+.
\]

证明：第一项随 desired power 增加，第二项随 leakage power 增加；分别代入 lower/upper bounds，再使用 positive-part function 的 monotonicity。证毕。

但 **SLNR 不等于 secrecy rate，更不等于 secrecy capacity**。转向 secrecy 会引入 Eve noise、CSI assumptions 和更多直接文献碰撞，而相关 PASS position-uncertainty/secrecy 工作已经存在。citeturn785204view3turn417071view0

**建议：主目标仍用 robust SLNR；用 interference-temperature corollary 增强 task meaning，不在最后几天更换 secrecy 主线。**

---

## D.5 正确的“何时 robust selection 有帮助”定理

### [PROVEN] Fixed-pair certified-dominance region

固定 layouts \(S_R,S_N\) 和一组 witnesses。令 \(s=\sigma^2>0\)，并定义

\[
L_R(s)=\frac{a}{s+b},
\]

\[
U_N(s)=\min_q\frac{c_q}{s+d_q}.
\]

那么

\[
L_R(s)>U_N(s)
\]

当且仅当存在某个 \(q\)，使

\[
(a-c_q)s>c_qb-ad_q.
\]

证明：一个数大于有限集合的 minimum，当且仅当它大于其中至少一个元素；再使用 A.6 的 cross multiplication。证毕。

令

\[
A_q=a-c_q,\qquad B_q=c_qb-ad_q.
\]

则每个 witness 的 certified region 是

\[
\begin{cases}
s>B_q/A_q,&A_q>0,\\
s<B_q/A_q,&A_q<0,\\
\text{全部 }s>0,&A_q=0,\ B_q<0,\\
\varnothing,&A_q=0,\ B_q\ge0.
\end{cases}
\]

再与 \(s>0\) 相交，对所有 \(q\) 取 union。

这是一个 exact certificate-region characterization，而不是 universal sensitivity threshold。

**关键限制：**当 noise 改变时，exhaustive nominal optimum \(S_N\) 也可能改变。因此这个 theorem 对 **fixed pair** 有效；不能固定一个 \(S_N\)，再把整个 noise axis 上的结果都称为“击败当前 exhaustive nominal optimum”。

**最小实验：**对一个 fixed pair 画 predicted region 与 direct certificate evaluation；另外展示 nominal optimum 随 noise 改变后的重新比较。

**风险：**容易写成比实际更强的“necessary and sufficient condition for true robust improvement”。它只对该 pair 的 certificate test 必要充分；测试失败仍然可能存在真实 improvement。

---

## D.6 Dependency-aware error-box refinement

### Idea

当 D 与 P 对同一个 error 的响应高度相似时，分别取 desired lower bound 和 leakage upper bound 会松。最直接的修复不是再造一个 \(\kappa\)，而是在 **同一个 physical error box** 上做 limited refinement。

### [PROVEN] Joint-box refinement theorem

令 \(Q\) 是 error space 的一个 sub-box，center 为 \(c\)，half-widths 为 \(w_n\)。取

\[
D_{r,n}\ge
\sup_{\delta_n\in Q_n}
|z_r'(x_n+\delta_n)|,
\]

并定义

\[
r_r(Q)=\sum_nD_{r,n}w_n.
\]

由 integral mean-value bound，

\[
|h_r(\delta)-h_r(c)|\le r_r(Q)
\qquad(\delta\in Q).
\]

因此

\[
\ell_Q
=
\frac{
[|h_D(c)|-r_D(Q)]_+^2
}{
N\sigma^2+
(|h_P(c)|+r_P(Q))^2
}
\]

是 \(Q\) 内 SLNR 的 lower bound。

若 \(\{Q_j\}\) partition 原 uncertainty box，则

\[
\boxed{
\min_j\ell_{Q_j}\le W(S).
}
\]

Proof：每个 feasible error 属于至少一个 \(Q_j\)，并受对应 \(\ell_{Q_j}\) 约束；因此受到所有 local lower bounds 的 minimum 约束。

若 child lower bound 使用

\[
\max\{\ell_{\rm parent},\ell_{\rm child}\},
\]

则 refinement 不会降低 global lower bound。随着最大 box diameter 趋于零，\(r_D,r_P\to0\)。由于 channel functions continuous、domain compact、\(\sigma^2>0\)，上述 bounds uniformly approach exact SLNR，故 lower bounds 收敛到 \(W(S)\)。证毕。

这条 construction 不需要 sub-box centers 保持 D-aligned，避免了错误地在 shifted centers 重用 Proposition 1 的问题。

**最小实验：**只对最大的几个 bracket-gap cases 设置固定 CPU budget，报告 gap reduction。

**风险：**dimension 是 \(N=8\)，最坏复杂度依然高。它应当是 targeted repair，不是主算法的必要组件。

---

## AI/learning，以及 C1/N2 是否保留

**AI：不建议加入。** 当前 task 的 bottleneck 不是缺少一个 geometry-to-subset predictor；你已经有 milliseconds-level local search 和 seconds-level featured-instance global audit。Learning-augmented screening 当然可以设计，但“可以使用”不等于“必要”。在现有时间约束下，它会增加 training protocol、generalization 和 fair-compute 的审稿负担。

**C1：压缩到一两句 mechanism explanation。** 可说明 nominal nulls 对 differential phase errors 敏感，但不单独列 contribution。

**N0：放 system construction。** 正确 root construction 是必要基础，不应把修复自身 mirroring bug 写成新的 research contribution。

**N2：不进入主线。** 至多用一个 attenuation control 说明当前效果不是简单 upstream shifting；不要再加入一套 aperture-shift optimization story。Attenuation-driven placement 已有直接背景文献。citeturn417071view2

---

# 6. Task E — Final recommendation

## E.1 我会押注的单一 paper plan

### Title

**Certified Robust Site Selection for Pinching-Antenna Systems: Global Screening Under Position Errors**

### One-sentence thesis

在满足 robust clearance 的 finite D-aligned PASS family 内，利用 nonlinear field enclosures 与 shared exact endpoint witnesses，为 actuator-error-aware site selection 提供可计算的 robust performance brackets、global screening 和可核查的 layout-optimality certificates。

### 三项 contributions

- **[PROVEN] Nonlinear robust certification：**构造与 PASS guided phase、independent actuator boxes 和 equal-power model 一致的 SLNR lower bound，采用 asymmetric sectors 和 tightly controlled angular discretization。
- **[PROVEN] Global witness screening：**用至多 \(2M\) 个 shared endpoint templates 为整个 finite family 提供 feasible upper bounds，支持 safe pruning、certificate optimization、global robust brackets 和 unique-layout dominance tests。
- **Experimental contribution：**在 matched endpoints、fixed physical noise 和相同 clearance 下，与 exhaustive nominal selection 及 robust baselines 比较，同时报告 leakage converse/achievability、nominal sacrifice、certification gaps 和 CPU cost。

第三项中尚未完成的 model-stress/global-grid experiments，应在真正运行后再写成完成时态。

---

## E.2 最终稿的 theorem/lemma list

不建议把本回答的所有数学都塞进六页。

| 编号 | 建议保留的 exact statement |
|---|---|
| **Lemma 1 — PASS phase and interval geometry** | **[PROVEN]** \(\psi_r'>0\)，unwrapped phase interval 由 endpoints exact 给出；给出 amplitude extrema 和 D-aligned construction |
| **Theorem 1 — Nonlinear SLNR bracket** | **[PROVEN]** 在 stated assumptions 下，\(L(S)\le W(S)\le U(S)\)，其中 leakage 使用 asymmetric sectors 与 sec correction |
| **Theorem 2 — Shared endpoint bank and safe screening** | **[PROVEN]** 至多 \(2M\) 个 shared templates exact cover endpoint leakage maxima；相应 feasible-witness upper bounds 支持 safe pruning 和 \(\max L\) 的 exact finite-family search |
| **Corollary 1 — Global robust certification** | **[PROVEN]** \(L(\widehat S)\le W^\star\le\max_SU_H(S)\)；若 \(L(\widehat S)>\max_{S\ne\widehat S}U_H(S)\)，则 \(\widehat S\) unique global robust optimal |
| **Corollary 2 — Leakage converse/achievability** | **[PROVEN]** \(F_{\rm end}\le\min_S\max_\delta I_P(S,\delta)\le\bar I(\widehat S)\) |

**从主稿删除 Lemma 3 的完整 Taylor derivation。**它在本次 verification 中是正确的，但作为论文主线，它不如 exact endpoint converse 有力，还占 proof space。

---

## E.3 Figure/table plan：最多四幅 figures

| Figure | 内容 | 要回答的问题 |
|---|---|---|
| **Fig. 1 — Geometry and certificate construction** | PASS geometry、D/P、matched endpoints；true contribution curve、outer sector、endpoint zonotope 的示意 | “实际 uncertainty 是什么，内外 bounds 分别来自哪里？” |
| **Fig. 2 — Matched-family certified gains** | 四个 settings 的 certified-gain distributions；保留 negative/inconclusive cases | “改进是否超出一个 favorable geometry？” |
| **Fig. 3 — Tolerance and converse/achievability** | 少量预先指定 geometries 的 SLNR brackets 与 leakage lower/upper bounds | “什么 tolerance 下 protection 变困难，bounds 有多紧？” |
| **Fig. 4 — Global screening efficiency** | survivors、runtime、global gap/unique-certification outcomes 随 candidate size 或 geometry 的变化 | “为什么不是只在一个 subset 上贴 certificate？” |

建议另用一个小 table 列 experiment protocol，一个小 table 列 featured global-certification results。不要给 background、MLP failure 或 N2 再分配 figures。

---

## E.4 本次已有的 matched-endpoint evidence

### [NUMERICALLY OBSERVED] Independent grid

本次 grid 明确为：

\[
x_P\in\{-5,-4,\ldots,5\},
\qquad
y_P\in\{0,2,4\}.
\]

四个 settings：

\[
(\mathrm{SNR}_{\rm ref}\text{ dB},\epsilon/\lambda)
\in
\{(20,0.03),(20,0.05),(30,0.03),(30,0.05)\}.
\]

每个 setting 有 33 geometries。Nominal selection exhaustive；robust selection 使用 corrected certificate、swap search 加 8 starts；witness 使用全部 256 corners。这个 grid 没有对每个 case 运行 global screening，也没有使用 L-BFGS refinement。

定义

\[
\Gamma=
\frac{L(S_R)}{U(S_N)}-1.
\]

| Matched setting | \(\Gamma>0\) | \(\Gamma>5\%\) | Median \(\Gamma\) |
|---|---:|---:|---:|
| 20 dB，\(0.03\lambda\) | 26/33 | 18/33 | 5.13% |
| 20 dB，\(0.05\lambda\) | 27/33 | 20/33 | 8.89% |
| 30 dB，\(0.03\lambda\) | 27/33 | 20/33 | 9.35% |
| 30 dB，\(0.05\lambda\) | 28/33 | 21/33 | 11.76% |
| **合计** | **108/132** | **79/132** | — |

这些是 deterministic grid 上的 counts，不是 population-level success probabilities。

这个结果足以支持继续写作，但**不能把它替换成你原报告中的 359/528 或 247/528**。两次实验的 protocol 不同。

### [NUMERICALLY OBSERVED] Robustness 不是免费的 nominal improvement

本次 featured instance 的 nominal SLNR：

| Family | Nominal-optimal layout | Robust-selected layout | Nominal sacrifice |
|---|---:|---:|---:|
| Free | 999.7375 | 794.5929 | 20.52% |
| Matched endpoints | 999.6244 | 945.2299 | 5.44% |

这张表很重要。论文的真实故事不是“所有指标一起提高”，而是：

> 牺牲一部分 extremely deep nominal null，换取 actuator errors 下更好的 guaranteed protection 和 SLNR。

---

## E.5 Experiment list

| Priority | Experiment | 当前状态/要求 |
|---|---|---|
| **Must-run** | 完整 correctness audit：phase alignment、\(\beta_D\) guard、clearance、\(\epsilon=0\)、same-error witnesses | 主要实现已修正；publication 前独立复核关键 comparisons |
| **Must-run** | Matched-family main grid，fixed \(N\)、fixed physical noise、fixed endpoints | 已有 132-case local-search evidence；主稿应明确哪些 cases 做了 global screening |
| **Must-run** | Exhaustive nominal baseline | 已完成当前 grid；任何新 tolerance 都须重新建立 feasible family |
| **Must-run** | 至少一个 robust baseline，例如优化 corner-witness objective 的 same-budget swap search | 尚需加入，防止只比较“robust 对 nominal” |
| **Must-run** | Global screening 的 runtime、survivors、upper/lower gaps | Featured case 已完成；扩展到有代表性的 tight/loose cases |
| **Must-run** | Nominal SLNR、desired power、leakage power 的分解 | Featured case 已完成；主图/表至少报告这些 trade-offs |
| **Must-run** | Separable attenuation/directivity controls，明确 power convention | 尚未运行；不要声称已有 hardware-model robustness |
| **Must-run** | Negative controls：\(\epsilon=0\)、P=D 或 P≈D、noise-dominated regime | 当前 grid 包含 P=D；需单独解释 inconclusive certificates |
| **Optional** | First-order/Taylor robust baseline | 在 page/time 允许时加入 |
| **Optional** | Adaptive error-box refinement | 仅修复最大-gap cases |
| **Optional** | 更大的 \(M\) 或多个 protected receivers | 不作为这次投稿的必要条件 |
| **Cut** | MLP、GNN、learned warm starts | 当前没有必要性证据 |

关于 numerical rigor：至少应独立复算关键 inequalities，并记录 margins。若写 **machine-verified global optimality**，则必须进一步提供 validated arithmetic 或覆盖全 family 的可靠 rounding-error bounds；只把 winner 用更高精度重算，不足以验证全部 rival upper bounds。

---

## E.6 Six-page budget

| Section | Pages |
|---|---:|
| Introduction + closest-work distinction | 0.70 |
| System model + feasible aligned family | 0.65 |
| Certificates + main theorems | 1.45 |
| Shared-witness screening algorithm | 0.80 |
| Experiments | 1.65 |
| Conclusion | 0.15 |
| References | 0.60 |
| **Total** | **6.00** |

### 必须 cut 的内容

C1 的完整 tolerance-theory discussion；原 mirroring bug 的详细历史；N2 的 upstream optimization；MLP experiments；universal \(\kappa\) threshold；“PASS nulls universally more fragile”的叙述；secrecy 主线；完整 Taylor remainder theorem；与核心 task 无关的 multiuser/learning extensions。

---

## E.7 Acceptance estimate

**[CONJECTURE]** 对“原 A7 + 当前 pilot narrative”，我仍会给大约 **40–50%** 的主观接受机会。

对本回答建议的版本——尤其是加入 global screening、明确 matched-family scope、补 robust baseline、完成 model/numerical audits——我会给大约 **60–70%**。

这不是基于 ICC acceptance statistics 的 calibrated prediction。提高判断的理由是：现在可以形成一条更强的论证链：

> 不是只得到一个较好的 layout；  
> 而是给出全 family 的 adversarial upper bounds；  
> 在部分 instances 中排除所有 rivals；  
> 同时给出 protection limit 的 converse 和接近的 achievability。

如果剩余审计发现 global margins 不可靠、matched effect 主要消失，或结果仅在不一致的 power model 下成立，这个判断必须下调。

---

## E.8 Results → allowed-claims table

| 实际 outcome | 可以写的 claim | 不能写的 claim |
|---|---|---|
| **[PROVEN]** Matched family 内 \(L_R>U_N\) | “Certified worst-case SLNR improvement over exhaustive nominal selection within the matched aligned family” | “优于所有 PASS designs” |
| **[PROVEN]** \(L(\widehat S)>\max_{S\ne\widehat S}U_H(S)\) | 在 stated model/family 和可靠数值验证下，unique global robust-optimal layout | Unrestricted continuous-position global optimum |
| **[PROVEN]** 只有 \(L(\widehat S)\le W^\star\le U^\star\) | Global robust bracket；performance ratio 至少为 \(L/U^\star\) | 未满足 rival-dominance condition 时声称 exact optimizer |
| **[NUMERICALLY OBSERVED]** 多个 matched settings 中出现 positive certified gains | 在公开列出的 tested grid 上，收益不依赖改变 nominal aperture endpoints | Universal gain 或 population success probability |
| **[PROVEN]** \(L_R\le U_N\) | Certificate inconclusive | “Robust design 比 nominal 更差” |
| **[PROVEN]** \(pF_{\rm end}>I_{\max}\) | 该 finite family 内没有 layout 能满足所定义的 all-error leakage ceiling | 所有 architectures、所有 candidate families 都不可能保护 P |
| **[NUMERICALLY OBSERVED]** 只在 isotropic model 下有效 | Ideal equal-power isotropic-model result | 已验证 practical coupling/depletion robustness |
| **[NUMERICALLY OBSERVED]** Free gain 很大，matched gain 小 | 分别报告 free 和 matched results | 把 free gain 写成 fixed-aperture gain |
| Clearance 未执行或 family 不一致 | 修复并重新运行后再使用结果 | 将 infeasible layouts 纳入 main result |
| 只做了 floating-point evaluation | “Analytical certificates evaluated numerically”，并报告 audit/margins | “Machine-verified interval certificate” |
| Per-layout \(U/L\) 很小，但没有全 family upper bound | 该 layout 的 worst-case value 被 tight bracketed | Global layout optimality |
| Nominal SLNR 降低而 robust bound 提高 | 明确的 nominal–robust trade-off | “No-cost robustness improvement” |

---

# 7. Anything you did not ask about but should have

## 7.1 “Position errors”和“activation errors”不能混用

当前模型处理的是 selected radiators 的 **continuous position displacement**。

它没有处理 missed activation、stuck-on/stuck-off、错误 site index 或 selected cardinality 变化。后者会改变 summation set，甚至改变 equal-power normalization。因此，title 和 abstract 应使用 **actuator position errors**，不要未经定义扩展为所有 activation errors。

## 7.2 需要分开报告不同来源的 gap

这里至少有四个不同问题：

**Angular discretization gap** 来自有限 angle grid；D.2 可以把它控制得很小。

**Sector-enclosure gap** 来自把 amplitude/phase 的 true coupled curve 扩大成 sector。

**D/P dependency gap** 来自分别 bounding numerator 和 denominator。

**Selection gap** 来自没有找到 certificate-optimal 或 robust-optimal subset。

改善一个 gap 不意味着其他 gap 自动消失。特别是 \(K=1440\) 的小 angular factor 不能用来解释整个 \(U/L\) 都应接近 1。

## 7.3 Deadline 与 submission scope

ICC 2027 官方作者页面的 indexed information 列出 symposium paper deadline 为 **2 October 2026**；submission-guidelines 的 indexed text 也强调 initial submissions 超过 six pages 会不经审稿退回。具体关闭时刻和 timezone 本次未能核验，不应自行假定 AoE。citeturn976201search4turn206025search4

## 7.4 本次没有把未提供的历史日志当成已验证证据

你的原始 528-case protocol、216,576-check logs，以及 graduation-project 中 N1/N2 的完整 reproduction inputs，没有包含在本次给出的 reference code 中。

因此，本回答没有把那些 historical counts 重新认证为事实；我另外运行并明确标注了自己的 reference reproduction、264 comparisons、global featured-instance audit 和 unit checks。

## 7.5 可复现文件

[下载完整 verification bundle：代码、README、environment、全部结果和日志](sandbox:/mnt/data/a7_verification_bundle.zip)

[查看 global screening 的完整 numerical results](sandbox:/mnt/data/a7_global_results.json)

[查看 independent grid 的 protocol、summary 和全部 264 comparisons](sandbox:/mnt/data/a7_independent_grid_results.json)

**最终判断：这篇论文值得继续，但最值得写的已经不是原来的“sector certificate + swap search”。真正应当成为标题、abstract 和主 theorem 中心的是：在一个清楚限定且公平匹配的 PASS family 内，把 nonlinear robustness 从局部 heuristic performance，推进到全 family 可核查的 bounds、dominance 和 protection limits。**