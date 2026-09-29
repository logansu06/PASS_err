# Provenance

## Upstream skill

`paper-writing-craft` includes and extends **paper-writing-skill** by Arpit Gupta / SNL-UCSB
(<https://github.com/SNL-UCSB/paper-writing-skill>, MIT licence, copied 2026-09-29, default branch).
Kept unchanged: `profiles/snl-default/` (their `author_profile/`), `brainstorming_guide.md`,
`figure_synthesis_guide.md`, `writing_checklists/`, `section_rhetorical_moves/`, `figure_templates/`, `examples/`,
`UPSTREAM_DESIGN.md` (their `DESIGN.md`), `LICENSE`. Adapted: `red_team_protocol.md`, `loop_mode.md`.
Rewritten: `SKILL.md` (ARIS orchestration, profile switch, modes). The upstream `setup` script is **not** used: it
installs to `~/.claude/skills/paper-writing/`, which collides with ARIS's own `paper-writing` (Workflow 3).

If you use the methodology in research, cite the upstream project:

```
@misc{paper-writing-skill,
  author = {Gupta, Arpit},
  title  = {paper-writing-skill: A Claude Code skill for research paper writing},
  year   = {2026},
  publisher = {GitHub},
  url    = {https://github.com/SNL-UCSB/paper-writing-skill}
}
```

## Added here

- `profiles/weidong-mei/` and the scripts/assets that support it: distilled 2026-09-29/30 from the 102 arXiv
  papers listing Weidong Mei as an author (see `profiles/weidong-mei/README.md` and `corpus_manifest.md`).
  Only aggregate statistics and short generic collocations are stored; no paper text or LaTeX source is redistributed.
- `scripts/style_gate.py`, `fact_guard.py`, `mei_plot.py`, `calibrate.py`, `render_gate_doc.py` and the corpus
  statistics scripts; `assets/mei_ieee.mplstyle`.

## Relation to ARIS

Composes with the ARIS skills `paper-plan`, `paper-write`, `paper-figure`, `figure-spec`, `paper-compile`,
`paper-claim-audit`, `citation-audit`, `auto-paper-improvement-loop`, and the shared references on reviewer
independence and citation discipline. It is **not** registered in the ARIS repository's skill catalog
(`tools/skill-groups.tsv`), so the ARIS installer, `-Reconcile` and `smart_update` leave it alone.
