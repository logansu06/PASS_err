---
name: paper-writing-craft
description: "Author-voice paper writing layered on ARIS: five-stage pipeline (brainstorm, architecture, section drafts, integration, compression), a script-run style gate, an independent red-team, figure / table / caption style, and swappable author profiles. Ships profile `weidong-mei` (distilled from 102 arXiv papers; IEEE wireless-communication optimization papers) and the original `snl-default` (systems/networking). Use when user says \"按 Mei 的风格写\", \"Weidong Mei 写作风格\", \"润色论文\", \"论文风格审查\", \"style audit\", \"paper style gate\", \"写 introduction / system model / simulation 部分\", \"图表和 caption 的风格\", \"蒸馏写作风格\", or wants to write, polish, compress or audit a paper in a specific author's voice."
argument-hint: "[file-or-section] [— profile: weidong-mei|snl-default] [— register: letter|conference|full|tutorial] [— mode: draft|audit|polish|compress|figures|distill]"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Skill, mcp__codex__codex
---

# Paper Writing Craft: author voice on top of the ARIS paper pipeline

Task: **$ARGUMENTS**

This skill merges two things. (1) The writing methodology of the open-source
[`paper-writing-skill`](https://github.com/SNL-UCSB/paper-writing-skill) (MIT; five-stage pipeline,
introduction-twice, topic-sentence-first drafting, style gates, independent red-team, figure workflow), kept
as profile `snl-default`. (2) A **measured author profile**, `weidong-mei`, distilled from the 102 arXiv
papers that carry his name: sentence-level habits, section skeleton, figure / table / caption conventions,
LaTeX idioms, and a calibrated gate. ARIS supplies everything that concerns evidence: outlines, figures from
results, compilation, claim and citation audits, cross-model review.

The skill is **user-owned** (a real directory in `.claude/skills/`, tracked in the project's git). The ARIS
installer and `-Reconcile` never touch it.

## Constants

- **PROFILE = `weidong-mei`** — directory `profiles/<PROFILE>/`. Other value: `snl-default`.
- **REGISTER = `auto`** — `letter` (5-page IEEE letter), `conference` (5-6 page IEEE conference paper: ICC, GLOBECOM), `full` (regular journal paper), `tutorial` (magazine / overview). `auto` = detect from the draft (`this letter` in the text, `\documentclass[conference]`, no simulation section); for a new paper choose from the target venue. Conference and letter are written the same way (4-paragraph introduction, contributions inside the paragraph, no roadmap sentence).
- **VENUE = `IEEE_JOURNAL`** — value passed to `/paper-plan` and `/paper-write`; use `IEEE_CONF` with `REGISTER = conference` (this project's ICC 2027 paper: `— venue: IEEE_CONF, register: conference`).
- **REVIEWER_MODEL = `gpt-6-astra`**, **REVIEWER_EFFORT = `ultra`** — Codex MCP reviewer (this project's HANDOFF section 10 requires `ultra` and an explicit `config` on the first call of every thread).
- **RED_TEAM_MAX_ROUNDS = 4**, **LEDGER = `notes/STYLE_AUDIT_LEDGER.md`** (in the paper directory).

Override inline: `/paper-writing-craft "paper/sec/intro.tex" — mode: audit, register: letter`.

## Resolve paths and Python (run once per session)

```bash
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
SKILL_DIR="$ROOT/.claude/skills/paper-writing-craft"; [ -d "$SKILL_DIR" ] || SKILL_DIR="$HOME/.claude/skills/paper-writing-craft"
export PYTHONUTF8=1                       # Windows consoles default to GBK
for c in python3 python "py -3" "$ROOT/experiments/a7/.venv/Scripts/python.exe" "$ROOT/experiments/a7/.venv/bin/python"; do
  $c -c "import sys; assert sys.version_info >= (3,9)" 2>/dev/null && PY="$c" && break
done
echo "$SKILL_DIR  $PY"                     # the scripts use the standard library only; mei_plot.py needs matplotlib
```
On the Windows machine `python` on PATH can be a Microsoft Store stub; the project venv Python works.

## Precedence contract with ARIS (read before mixing the two)

| concern | who wins | files |
|---|---|---|
| numbers, claims, evidence, `DATA_NEEDED` markers, citations (DBLP / CrossRef), anonymity, reviewer independence, output manifests | **ARIS** | `../shared-references/*` (citation-discipline, reviewer-independence, acceptance-gate, evidence-precheck), `/paper-claim-audit`, `/citation-audit`, `/result-to-claim` |
| venue template, page limit, submission checklist | **ARIS** | `../shared-references/venue-checklists.md`, `/paper-write` `VENUE`, `MAX_PAGES` |
| voice, sentence habits, section skeleton and moves, headings, captions, figures and plots, LaTeX idioms, phrase choices | **the profile** | `profiles/$PROFILE/*` — it overrides `../shared-references/writing-principles.md` and the drafting defaults of `/paper-write` |
| process: Draft 0 introduction, topic sentences before prose, red-team before shipping | **this skill** | below |

Reviewer separation. The **style red-team** (this skill) is a conformance auditor: its rubric is the profile.
Every **scientific** reviewer or auditor (`/auto-review-loop`, `/auto-paper-improvement-loop` reviewer,
`/paper-claim-audit`, `/citation-audit`, `/kill-argument`, `/research-review`) must run on the artifact alone and
**never receives the profile, its files, or any style instruction** (`reviewer-independence.md`; the same rule
ARIS applies to `— style-ref`). Do not pass `— style-ref` to writer skills together with a profile: the profile
replaces it.

## Three layers

1. **Pipeline** (fixed): Stage 1 brainstorming -> 2 architecture -> 3 section drafts -> 4 integration -> 5 compression, with gates.
2. **Profile** (swappable): `profiles/<PROFILE>/`. Voice, moves, figures, gates.
3. **Project context** (per paper): `project_context.md` in the paper directory: identity sentence, venue, register, contribution claims (as results), locked decisions, term map. Add it to `.gitignore` (the repository may be public). Pre-fill it from `NARRATIVE_REPORT.md`, `CLAIMS_FROM_RESULTS.md`, `findings.md`, `refine-logs/`, and `idea-stage/` when they exist, then ask only the questions of `brainstorming_guide.md` that remain open.

## When invoked, MUST

1. Read this file. Resolve `PROFILE`, `REGISTER`, `mode`.
2. Read the profile's voice files: for `weidong-mei` all of `README.md`, `craft_reference.md`, `rhetorical_moves.md`, `figures_tables.md`, `latex_idioms.md`, `lexicon.md`, `editorial_principles.md`, `gate_semantic.md` (+ `gate_mechanical.md` for rule ids); for `snl-default` all seven files of `profiles/snl-default/`.
3. Locate the inputs (`NARRATIVE_REPORT.md`, `CLAIMS_FROM_RESULTS.md`, `PAPER_PLAN.md`, `results/`, `figures/`, `paper/**/*.tex`, `project_context.md`) and say which exist.
4. Dispatch on `mode` (default: `draft` if no `.tex` exists, else `audit`).
5. Never present text as clean without the pasted script output (mechanical gate) and the red-team findings (see below).

## Modes

### `draft` — write sections in the profile's voice

Enforced order (introduction twice): **Draft 0 introduction -> Results -> System model / Solution -> (Related
prior art lives in the introduction) -> Final introduction -> Abstract -> Conclusion**. Draft 0 is a disposable
framing scaffold; the final introduction is rewritten from scratch after the results exist and promises only what
they show. Before any full prose, write the topic sentence of every paragraph as a `%` comment, read them in order,
and proceed only when they form an argument (`SKILL` stage 3 of the default pipeline).

Mapping onto ARIS (Workflow 3 with the profile injected):

| stage | do | ARIS skill called (Skill tool) |
|---|---|---|
| 0 context | build `project_context.md` from the narrative + claims files | — |
| 1 plan | outline = the profile skeleton (`rhetorical_moves.md`): Introduction, System Model (and Problem Formulation), Solution(s), Numerical Results, Conclusion; three contribution items mapped to sections and figures; figure plan (Fig. 1 system model + one figure per result paragraph) | `/paper-plan "<narrative> — venue: IEEE_JOURNAL"` then reconcile `PAPER_PLAN.md` with the skeleton |
| 2 figures | data plots from real results with `assets/mei_ieee.mplstyle` / `scripts/mei_plot.py`; schematics via a FigureSpec (`figures_tables.md` section 4) | `/paper-figure`, `/figure-spec` |
| 3 drafts | write section by section with the profile files open; after each section run the mechanical gate and fix | `/paper-write "PAPER_PLAN.md — venue: IEEE_JOURNAL"` for LaTeX scaffolding, DBLP-verified BibTeX, `DATA_NEEDED` markers; the profile decides wording and structure |
| 4 integration | term-map, contribution-to-evidence map (W7), notation (W2), figure/legend/benchmark names (W8, W13), first sentence of every section | — |
| 5 compression | only for a page limit; `profiles/<PROFILE>/compression_overrides.md` | — |
| build | compile; this machine has no LaTeX: use Overleaf | `/paper-compile` or `/overleaf-sync` |
| audits | numbers vs raw results; bibliography | `/paper-claim-audit`, `/citation-audit` (no profile) |
| improvement | scientific review loop | `/auto-paper-improvement-loop` (no profile); afterwards **re-run the style gate**, because fixes drift the voice |

Never fabricate a result, number, citation, or figure to fill a slot the profile expects; write
`<!-- DATA_NEEDED: <slot> -->` (ARIS convention) and continue.

### `audit` — grade existing text (default when `.tex` exists)

1. Run the mechanical gate on every in-scope file (below); paste the raw output.
2. Read `gate_semantic.md` (and the inherited `snl-default` items it lists) and apply it yourself section by section.
3. Run the independent red-team (below). Merge findings; every finding carries a rule id (`MM#`, `S#`, `W#`), `file:line`, quote, concrete fix, severity.
4. Report. Fix only if the user asked (`— fix: true`); then run `scripts/fact_guard.py before after` and iterate to closure.

### `polish` — rewrite form, keep facts

Rewrite selected paragraphs toward the profile (front-loaded `we` frames, connector inventory, terms, results
paragraph anatomy). **Facts are frozen**: copy the file first, edit, then run
`"$PY" "$SKILL_DIR/scripts/fact_guard.py" before.tex after.tex`; any difference in numbers, `\cite` keys,
`\ref` labels, or inline math is reverted or explained. Do not add claims, hedges that change a claim's scope,
or citations. Then run the gate and the red-team.

### `compress` — page-limit fit

`profiles/<PROFILE>/compression_overrides.md` (for `snl-default`: `compression_patterns.md`, 30-50%). Report words,
pages, sentence mean before and after and which operation supplied each cut. Facts frozen (`fact_guard.py`).

### `figures` — figures, captions, tables, algorithm boxes

Read `figures_tables.md`. For a plot: produce the plotting code with `scripts/mei_plot.py`
(`use()`, `fig_single()`, `curve(..., proposed=True)`, `finish(...)`, `save(...)`), the LaTeX environment from
`latex_idioms.md`, and a caption of the form `<Metric> versus <variable>[ with <fixed parameters>].` Then
**render and look at the figure** (W14: a checklist pass without rendering does not count) and run the
gate rules MM05, MM21-MM27. For schematics: state the icon vocabulary and layout (`figures_tables.md` section 4)
and hand a FigureSpec to `/figure-spec`, or describe the PowerPoint drawing.

### `distill` — build a profile for another author or venue

Same pipeline that produced `weidong-mei` (documented in `profiles/weidong-mei/README.md`, "Regenerate or extend"):
`scripts/fetch_corpus.py` (arXiv API + e-print) -> `style_stats.py` -> `aggregate.py` -> `fig_stats.py` ->
`aggregate_floats.py` -> `phrases.py` -> `extras.py` -> read about a dozen papers and inspect a dozen figure files ->
write the prose files by copying `profiles/weidong-mei/` and replacing every number -> `rules.json` from the tables ->
`calibrate.py --write-norms` (back-test: a FAIL rule that flags more than ~5% of the author's own papers is a
calibration bug) -> `render_gate_doc.py`. Selection rule: the papers the user names (e.g. everything carrying the
author's name). Guardrails: public, open-access arXiv content only; store aggregates and short generic collocations,
never paper text or LaTeX source; state the limits (regex statistics, co-authored text, one subfield); the profile
describes forms, not content to reuse.

## Mechanical gate (script, not eyeballing)

```bash
"$PY" "$SKILL_DIR/scripts/style_gate.py" paper/main.tex --profile weidong-mei --register auto
```
Exit 1 on any FAIL rule. Paste the rule table (hits per rule) and the metrics table into the report. WARN rules are
fixed or justified in the ledger. Run it after **every** edit to `.tex` prose (a paragraph edit included), and again
after the improvement loop. `snl-default` has no script: run the grep block of
`profiles/snl-default/gate_mechanical.md` Part C and paste the counts.

## Independent red-team (fresh reviewer; the author never grades its own text)

Use a **fresh** `mcp__codex__codex` thread for every round. Never `mcp__codex__codex-reply` (a reviewer that
sees "I fixed X" inflates scores; `auto-paper-improvement-loop` documents this). Point at files; do not summarize,
interpret, or list what changed.

```
mcp__codex__codex:
  model: gpt-6-astra
  config: {"model_reasoning_effort": "ultra"}
  prompt: |
    You are an independent style-conformance auditor for an IEEE wireless-communications paper.
    You did not write it. Read these files yourself.
    Draft: <absolute paths of the .tex files in scope>
    Rubric: <SKILL_DIR>/profiles/<PROFILE>/gate_semantic.md, gate_mechanical.md, craft_reference.md,
            rhetorical_moves.md, figures_tables.md; for the inherited items it names,
            <SKILL_DIR>/profiles/snl-default/gate_semantic.md.
    Run <PY> <SKILL_DIR>/scripts/style_gate.py <main.tex> yourself and include its raw output.
    Apply the semantic gate with the eyes of a reader who has never seen the paper.
    Return findings only: rule id, file:line, quoted text, concrete fix, severity (CRITICAL / MAJOR / MINOR).
    Do not return a yes/no verdict and do not rewrite the paper.
```
The author fixes every finding; repeat with a fresh thread until a **closure reviewer** (fresh thread, whole paper)
returns zero CRITICAL and MAJOR findings (default gate S31). At most `RED_TEAM_MAX_ROUNDS`; if two consecutive rounds
return the same findings, stop and surface the blocker. If Codex MCP is unavailable, write the prompt to
`notes/RED_TEAM_PROMPT.md` and ask the user to run it manually; do not substitute the author as reviewer.

## Loop mode

The style audit can run under `/loop` following `loop_mode.md` (durable ledger, one section per iteration, stops
when every section is `CLEAN`). **Do not** wrap `/auto-paper-improvement-loop` in `/loop` (ARIS forbids it).

## Guardrails

- Form, not content: never import sentences, claims, numbers, figures, or citations from the profile's corpus into the
  user's paper; never claim the text was written by the author of the profile.
- Facts frozen in `polish` / `compress` (`fact_guard.py`); results only from files under `results/`; a number the text
  cannot trace is cut or marked `DATA_NEEDED`.
- Honest scope: hedge claims about others' work and approximations, assert measured results, never hedge a number you measured.
- Scripts are read-only on the paper (they report); edits are made by the agent and re-checked.

## Files

| path | role |
|---|---|
| `profiles/weidong-mei/` | the measured profile: `README`, `craft_reference`, `rhetorical_moves`, `figures_tables`, `latex_idioms`, `lexicon`, `editorial_principles`, `gate_mechanical` (+ `rules.json`, `norms.json`), `gate_semantic`, `compression_overrides`, `stats_*.md`, `corpus_manifest.md` |
| `profiles/snl-default/` | the upstream author profile, unchanged (7 files) |
| `brainstorming_guide.md`, `figure_synthesis_guide.md`, `red_team_protocol.md`, `loop_mode.md`, `writing_checklists/`, `section_rhetorical_moves/`, `figure_templates/`, `examples/` | upstream method files (systems / networking flavoured; the profile files take precedence for wireless papers). `red_team_protocol.md` and `loop_mode.md` are adapted to ARIS |
| `scripts/style_gate.py`, `fact_guard.py`, `mei_plot.py`, `calibrate.py`, `render_gate_doc.py`, corpus scripts | executable checks and the regeneration pipeline (standard library; `mei_plot.py` needs matplotlib) |
| `scripts/selftest.py` | assertions for the gate, `fact_guard.py`, `rules.json` <-> `gate_mechanical.md`; run it after any change to a rule or script (`"$PY" scripts/selftest.py`) |
| `assets/mei_ieee.mplstyle` | matplotlib style reproducing the curve plots |
| `PROVENANCE.md`, `LICENSE`, `UPSTREAM_DESIGN.md` | origin, MIT licence of the upstream skill, upstream rationale |
| `MACOS_ADOPTION.md` | steps for the Claude Code on the macOS machine: import, adapt the ARIS mapping to the local ARIS, dry-run the red-team, what is verified and what is not |
