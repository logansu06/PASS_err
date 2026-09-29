# Adopting `paper-writing-craft` on macOS (instructions for the Claude Code running there)

The skill was built and verified on the Windows machine (session of 2026-09-29/30) and pushed as tracked
files under `.claude/skills/paper-writing-craft/`. The macOS working tree had **uncommitted changes** at that
time, so the push touched **only this directory**: `CLAUDE.md`, `HANDOFF.md`, `.gitignore`, `.aris/` and every
ARIS link in `.claude/skills/` are exactly as they were. **Do not edit any file outside this directory as part
of the adoption unless the user asks** (suggested optional text is at the end).

## What the user wants done here

Import the skill (it teaches an author's voice, `weidong-mei`, distilled from the 102 arXiv papers carrying
Weidong Mei's name) and **adapt it to the ARIS skills installed on this machine**, so `/paper-writing-craft`
works with the local ARIS for the ICC 2027 paper (`— venue: IEEE_CONF, register: conference`).

## Steps

1. **Pull without touching the user's uncommitted work.** `git status` first. `git pull --ff-only origin main`
   adds only new files under `.claude/skills/paper-writing-craft/`; if git refuses because of local changes
   in other files, tell the user and let them choose (stash or commit); do not discard anything.
   `.claude/` is in `.gitignore`, but tracked files are still checked out and tracked; **new** files you create
   in this directory need `git add -f`.
2. **Load check.** `ls .claude/skills/paper-writing-craft` and confirm the skill appears in the skill list.
3. **Self-test** (standard library only): `python3 .claude/skills/paper-writing-craft/scripts/selftest.py`
   must print `ALL CHECKS PASSED`. `mei_plot.py` needs matplotlib: use `experiments/a7/.venv/bin/python`.
4. **Adapt the ARIS mapping to the local ARIS.** `SKILL.md` ("Precedence contract", "Mapping onto ARIS") was
   written against the Windows `aris_repo` at commit `341f914` (ARIS-Code v0.4.27 banner). The macOS
   `/Users/logansu/aris_repo` may be a different revision. Verify that these exist and take the arguments the
   table uses; edit **only this skill's** `SKILL.md` if they changed (never the ARIS skills):
   - skills: `paper-plan`, `paper-write` (`— venue: IEEE_CONF`, `IEEE_JOURNAL`, `DATA_NEEDED` markers, DBLP
     BibTeX), `paper-figure`, `figure-spec`, `paper-compile`, `overleaf-sync`, `paper-claim-audit`,
     `citation-audit`, `auto-paper-improvement-loop`, `result-to-claim`, `kill-argument`;
   - shared references: `reviewer-independence.md`, `venue-checklists.md`, `writing-principles.md`,
     `citation-discipline.md`, `acceptance-gate.md`.
   The phases of Workflow 3 (`skills/paper-writing/SKILL.md`: plan, contract, figures, writing, compile, claim
   audit, improvement loop, citation audit, forensics) are the anchors of the mapping table.
5. **Compilation and files.** macOS builds through the Overleaf bridge (`paper-overleaf/`, gitignored). Point
   `scripts/style_gate.py` at the clone's `main.tex` (it follows `\input`); run the gate before syncing to Overleaf.
6. **Red-team dry run (not executed yet).** The reviewer prompt in `SKILL.md` ("Independent red-team") was
   written from the ARIS conventions but never run. Run one round on a short section: `mcp__codex__codex`,
   `model: gpt-6-astra`, `config: {"model_reasoning_effort": "ultra"}` (HANDOFF section 10), fresh thread, files by
   absolute path, no summary of what changed. Check that the reviewer can read the profile files; if its sandbox
   cannot run `python`, run the gate yourself and hand the reviewer the raw output **file** (a deterministic report
   is evidence, not executor interpretation). Confirm compliance with `reviewer-independence.md`.
7. **Smoke tests on the real project:** `python3 scripts/style_gate.py <paper main.tex> --register conference`;
   `python3 scripts/fact_guard.py before.tex after.tex` on a copy; render a plot with
   `python scripts/mei_plot.py demo /tmp/demo.pdf` and look at it (Arial may be missing on macOS; the style falls
   back to Helvetica / DejaVu Sans, which is acceptable).
8. **First real use.** Draft or polish the ICC paper with `/paper-writing-craft` as the writer stage and keep the
   ARIS audits (`/paper-claim-audit`, `/citation-audit`, improvement loop) unchanged and profile-blind.

## Verified on Windows (2026-09-30)

`selftest.py` passes; `style_gate.py` back-tested on the 85 technical papers of the corpus (FAIL rules flag at
most 8% of the author's own papers, each of those a real typo) and run on the project's own LaTeX report;
`fetch_corpus.py` -> `style_stats.py` -> `aggregate.py` reproduces the shipped numbers from a fresh download
(102 papers in 21 s); `fact_guard.py`; `mei_plot.py` demo compared with an original figure; a fresh clone of the
GitHub repository passes the self-test.

## Not verified yet (do on macOS)

The Codex red-team round; the end-to-end composition with ARIS `/paper-plan` + `/paper-write` through the Skill
tool; `--register conference` on the real ICC draft; `mei_plot.py` in the macOS venv; Python 3.13 (scripts are
standard library, expected fine).

## Boundaries that must stay

- Keep the skill user-owned: do not register it in the ARIS repo (`tools/skill-groups.tsv`, catalog, README
  counts) and do not let reconcile remove it.
- Precedence: ARIS owns numbers, claims, citations, audits, reviewer independence; the profile owns voice,
  structure, figures, captions, LaTeX idioms. Never pass the profile to scientific reviewers or auditors.
- Form, not content: never import sentences, claims, numbers or figures from the corpus; do not present text as
  written by the profile's author.
- The profile is statistics from arXiv LaTeX (regex-based; 77 of 102 papers have him as a middle author). Limits are
  in `profiles/weidong-mei/README.md`; re-run the pipeline there to update.

## Optional, only if the user agrees: text for the project files

`CLAUDE.md`, after the `<!-- ARIS:END -->` marker (the installer only rewrites inside the markers):

```markdown
## Project-local skills (not ARIS-managed)
- `paper-writing-craft` — `.claude/skills/paper-writing-craft/`, a real directory tracked in this repo; the ARIS
  installers and `-Reconcile` never touch it and it is not registered in the ARIS repo. It layers an author voice
  (default profile `weidong-mei`) on ARIS Workflow 3. Precedence: ARIS wins on evidence, citations, audits and
  reviewer independence; the profile wins on voice and structure. Never pass the profile to scientific reviewers.
```

`HANDOFF.md`, section 10 ("两台机器通用"): one bullet stating where the skill is, that the style check is
`python scripts/style_gate.py <main.tex>`, and that the plotting style is `assets/mei_ieee.mplstyle` +
`scripts/mei_plot.py`. To have future new files under the skill tracked, add to `.gitignore` after `.claude/`:
`.claude/*`, `!.claude/skills/`, `.claude/skills/*`, `!.claude/skills/paper-writing-craft/` (replacing the plain
`.claude/` line).
