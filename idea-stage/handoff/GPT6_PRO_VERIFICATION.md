# Claude's Verification of the GPT-6 Pro Reply (2026-09-26)

## Provenance

- **Prompt:** `idea-stage/handoff/GPT6_PRO_PROMPT.md`, sent through Oracle MCP (local patched 0.21.3, browser engine, `modelStrategy: current`).
- **Oracle session:** `pass-a7-gpt6pro-deep-verificati`. It completed after 34 minutes of reasoning, but Oracle's answer capture failed and returned only an 8-token code fragment.
- **Recovery:** the full answer was fetched read-only from the ChatGPT conversation API; conversation `6ab77e85-d634-83ec-b591-ba71b968896f`.
- **Model verified:** the conversation `default_model_slug` is `gpt-6-pro`, and all 82 assistant messages carry `model_slug = gpt-6-pro`. Oracle itself could not verify this (`verified=no`).
- **Work visible in the thread:** 27 code executions, 13 web searches, and a final answer of 57,134 characters.
- **Files:**
  - reply: `GPT6_PRO_REPLY.md`
  - sandbox bundle: `gpt6pro_bundle/` (code, results, logs)
  - raw thread: `.aris/oracle/conversation_raw.json`
  - trace: `.aris/traces/oracle-gpt6pro-handoff/2026-09-26_run01/`
- **Incident:** while recovering the answer, Claude launched Chrome on the Oracle profile without Oracle's `--use-mock-keychain --password-store=basic` flags. Chrome discarded the encrypted cookies and the profile was logged out. The user re-logged in, and the session cookie is confirmed persisted after a graceful close.

## Mathematics Checked by Claude

| Item | Check | Result |
|---|---|---|
| $z''$ exact formula | Re-derived: $A'' = (3t^2 - 1)/R^3$, $\psi'' = k_0(1 - t^2)/R$, imaginary coefficient $1 - 3t^2 - 2n_{\mathrm{eff}}t$ | Correct |
| Proposition 1 proof; the $\beta > \pi/2$ clipping issue | The projection argument holds; clipping is invalid only when $\beta > \pi/2$ | Correct. `a7_main.py` skips invalid cases (`T["valid"]`), so the paper runs are safe |
| Proposition 2: sector support including the $A^-$ branch; Minkowski sum; Lipschitz pad | Standard support-function argument | Correct |
| $\sec(\pi/K)$ multiplicative correction | Some grid angle lies within $\pi/K$ of $\arg w^\star$ | Correct, and tighter than the additive pad |
| Asymmetric sectors | Center $-(\psi^+ + \psi^-)/2$, half-width $(\psi^+ - \psi^-)/2$ | Correct |
| **Theorem 2 (shared endpoint bank):** at most $2M$ templates cover every subset's endpoint-leakage maximum | Zonotope vertices, convexity of $\lvert w\rvert^2$, the max-modulus point is a support point in direction $\arg w^\star$, and the breakpoints of all $M$ sites refine every subset's cells | Correct |
| Safe pruning ⇒ exact $\max_S L$ | Discarding $U_H \le$ incumbent $L$ is safe because $L \le W \le U_H$ | Correct |
| Unique global robust optimum test: $L(\hat S) > \max_{S \ne \hat S} U_H(S)$ | Direct from the bracket | Correct (exact arithmetic; float64 evaluation) |
| Endpoint converse and the sine floor | $\lvert v\rvert^2 = (A_+ - A_-)^2/4 + A_+A_-\sin^2(\Delta\psi/2)$; $\Delta\psi \ge 2k_0(n_{\mathrm{eff}} - 1)\eta$ | Correct |
| Dinkelbach / per-angle sorting | The min–max interchange counterexample is valid | Correct. The $(C_{\min}/C_{\max})^2$ approximation is also correct |
| Fixed-pair noise region | Union over witnesses of linear inequalities in $\sigma^2$ | Correct |

## Numerical Reproduction by Claude (this machine)

`a7_global.py` from the bundle, rerun locally (1.28 s). All eight key quantities match GPT-6 Pro to machine precision:

| | Free family | Identical endpoints |
|---|---|---|
| Family size | 735,471 | 74,613 |
| Certificate-optimal subset | [0,1,4,5,6,11,14,19] | [0,1,4,8,9,12,13,23] |
| $L(\hat S)$ | 56.5593 | 55.5740 |
| Global upper bound $U^\star$ | 56.5828 (+0.042%) | 55.6040 (+0.054%) |
| Largest rival $U_H$ | 56.2385 | 55.5274 |
| Unique-optimality margin | 0.3209 | 0.0466 |
| Certified gain over exhaustive nominal | +34.17% | +2.79% |
| Min endpoint worst leakage $F_{\rm end}$ | 0.011858 | 0.012070 |

Implication: our swap search (L = 53.42) was **not** certificate-optimal on this instance. The exact optimum is 56.56.

## Corrections Accepted into the Plan

- **Clearance filtering must be part of the feasible family.** It only binds for $\epsilon > 0.0911\lambda$. The declared grid goes to $0.08\lambda$, and `a7_main.py` asserts clearance.
- **$\epsilon = 0$ must use the exact nominal SLNR.** `a7_main.py` already does this. The "2.78%" figure is instance-specific and should not be quoted.
- **Clip-free β guard:** raise or skip when $\beta_D > \pi/2$.
- **Keep the free and matched gains separate.** At the reference geometry they are +34% vs +2.8%.
- **Report the nominal sacrifice.** The robust layouts give up 20.5% (free) or 5.4% (matched) of nominal SLNR.
- **Terminology:** use "actuator position errors", not "activation errors".
- **Report four separate gaps:** angular discretization, sector enclosure, D/P dependency, and selection.

## Not Yet Independently Verified by Claude

- GPT-6 Pro's independent matched grid: 108/132 certified positive and 79/132 above 5% (`a7_grid.py`, results in the bundle). Rerunning it is part of experiment milestone M0/M1.
- Literature items it cites. They are consistent with our own verified list (`idea-stage/LIT_REVIEW.md`, `NOVELTY_REPORT.md`) and add no new collision.
