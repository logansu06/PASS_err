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
