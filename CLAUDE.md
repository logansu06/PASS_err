<!-- ARIS:BEGIN -->
## ARIS Skill Scope
ARIS skills installed in this project: 84 entries.
Manifest: `.aris/installed-skills.txt` (lists every skill ARIS installed and its upstream target).
Project skill path: `.claude/skills/<skill-name>`. For ARIS workflows, prefer these project-local skills over global skills.

The skills link into the ARIS repo on whichever machine you are using. Do not edit or delete them in place. Update upstream, or rerun that machine's installer:
- **macOS** (symlinks into `/Users/logansu/aris_repo`; project at `/Users/logansu/Documents/PASS`): `bash /Users/logansu/aris_repo/tools/install_aris.sh`
- **Windows** (junctions into `C:\Users\89813\aris_repo`; project at `D:\PASS_err`): `powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\89813\aris_repo\tools\install_aris.ps1" "D:\PASS_err" -Platform claude -Reconcile`

Each installer rewrites this block for its own machine only. Do not commit that rewrite; keep this two-platform version.
Machine-specific setup (Python, venv, helper quirks) is in `HANDOFF.md` §9–§10.
<!-- ARIS:END -->

## Project-local skills (not ARIS-managed)
- `paper-writing-craft` — `.claude/skills/paper-writing-craft/`, a real directory tracked in this repo (`.gitignore` has an exception for it), so it arrives on macOS with `git pull`. The ARIS installers and `-Reconcile` never touch it, and it is deliberately not registered in the ARIS repo (`tools/skill-groups.tsv`). It layers an author voice on ARIS Workflow 3: default profile `weidong-mei` (distilled from the 102 arXiv papers carrying his name; sentence habits, section moves, figure / table / caption style, LaTeX idioms, a script-run style gate), plus the original `snl-default`. Invoke `/paper-writing-craft`. Precedence: ARIS wins on evidence, citations, audits, reviewer independence; the profile wins on voice and structure. Never pass the profile to scientific reviewers or auditors. Details: its `SKILL.md`, `profiles/weidong-mei/README.md`, `PROVENANCE.md`.
