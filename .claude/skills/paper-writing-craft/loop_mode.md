# Loop mode: resumable style audit-and-fix (for `/loop`)

> Adapted from the upstream `paper-writing-skill` (MIT). Purpose: let the user run
> `/loop apply paper-writing-craft iteratively` and have the skill run an audit -> red-team -> fix cycle
> with no further instructions. Each iteration reads its state from disk, does one unit of work, and updates the
> state, so progress survives context loss. The loop ends itself when the paper is clean.
>
> **Do not** put `/auto-paper-improvement-loop` (the ARIS scientific review loop) under `/loop`; it loops
> internally and forbids external timers. This loop only governs the **style** audit of this skill.

## Invocation

- `/loop apply paper-writing-craft iteratively`  (self-paced; recommended)
- `/loop audit §2 and §3 with paper-writing-craft until clean`  (scoped)
Optional inline overrides: `— profile: <name>`, `— register: letter|full|tutorial`.

## Durable ledger: `notes/STYLE_AUDIT_LEDGER.md` (paper directory)

| Section | Mechanical (script output) | Semantic (`S#` / `W#`) | Independent red-team | Status |
|---|---|---|---|---|

Statuses: `PENDING` / `FINDINGS(n)` / `CLEAN`. Per section record the pasted gate counts (rule id: hits), the last
red-team findings, and the rule id of **every** fix (`MM11: split 2 sentences; W8: renamed benchmark 2 in legend`).
The ledger is the loop's memory: read it at the start of every iteration.

## One iteration

1. Read the ledger (create it from the section list if absent) and `project_context.md`.
2. Pick the highest-priority section not `CLEAN` (paper order unless the user scoped it).
3. Run the three gates on it (`red_team_protocol.md`):
   a. mechanical: `scripts/style_gate.py` (paste counts);
   b. semantic: the profile's `gate_semantic.md`;
   c. craft: compare with `craft_reference.md` / `rhetorical_moves.md`;
   d. independent red-team: fresh `mcp__codex__codex` thread (never `codex-reply`).
4. Fix every finding. Facts frozen: `scripts/fact_guard.py before after` must report identical fact tokens.
5. Re-run the gates. Zero FAIL rules and zero CRITICAL / MAJOR findings -> `CLEAN`, else `FINDINGS(n)`.
6. Update the ledger; rebuild the PDF if a section changed (`/paper-compile` or Overleaf).
7. Emit one line: section, rule ids fixed, findings left, status.

## Stop condition

Every in-scope section is `CLEAN` through all three gates and a closure reviewer has signed off on the whole
paper: report the final ledger and stop. If two consecutive iterations leave the same findings, stop and surface
the blocker instead of spinning.

## Rules

- The reviewer is always a separate fresh thread; the author never grades its own text.
- Keep each iteration small (one section, or one gate on a large section).
- For figures, "clean" means rendered and inspected (`figures_tables.md`, W14), not a checklist pass.
