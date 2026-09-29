# Independent adversarial red-team (adapted for ARIS and profiles)

> Adapted from the upstream `paper-writing-skill` (MIT). Why it exists: the agent that wrote the prose also ran
> the style audit and reported "passed"; self-audit rationalizes its own phrasing, and the mechanical check was
> skipped or its output never shown. This protocol makes review **independent** and **evidence-gated**.

## Three gates; text must survive all three

1. **WRITE**: the author agent produces the draft.
2. **MECHANICAL**: run the profile's gate and paste the raw output.
   - `weidong-mei`: `python scripts/style_gate.py <main.tex>` (rule table + metrics table). Zero FAIL rules; every WARN fixed or justified in the ledger.
   - `snl-default`: the grep block of `profiles/snl-default/gate_mechanical.md` Part C, per-category counts.
   "Audited" without pasted output is invalid.
3. **INDEPENDENT RED-TEAM**: a reviewer that did **not** write the text:
   - re-runs the mechanical gate itself (does not trust the author's report);
   - applies the profile's `gate_semantic.md` (plus the inherited default items it names) with a fresh-reader lens:
     "a reader in this venue who has never seen the paper: flag every undefined symbol, every claim not tied to the
     paper's thesis, every unfollowable step, every result paragraph that does not explain its figure";
   - returns a **findings list**, not a yes/no. Each finding cites the exact rule id (`MM#`, `S#`, `W#`), the
     `file:line`, the quoted text, a concrete fix, and a severity.

## How to run the reviewer in ARIS

A fresh `mcp__codex__codex` thread per round (model `gpt-6-astra`, `config: {"model_reasoning_effort": "ultra"}`
stated explicitly on the first call of every thread, as required by the project's HANDOFF). Never
`mcp__codex__codex-reply` for a review round. The prompt points at files and the rubric; it never carries the
author's summary of the text, of what changed, or of what the author thinks is wrong
(`../shared-references/reviewer-independence.md`). The exact prompt is in `SKILL.md` ("Independent red-team").

Two reviewer roles must not be mixed:

- **Style red-team** (this protocol): rubric = the profile. It judges conformance to the voice and the semantic checks.
- **Scientific reviewers / auditors** (`/auto-paper-improvement-loop`, `/paper-claim-audit`, `/citation-audit`,
  `/kill-argument`, `/research-review`): they read the artifact alone and never see the profile.

## Evidence rule

The pasted gate output plus the red-team findings are the audit record. A section is CLEAN only when the reviewer
returns zero surviving CRITICAL / MAJOR findings **and** the pasted gate output shows no FAIL rule. Never report
clean on a mental pass. After any substantive change, re-run the relevant lens; the last step is a **closure
reviewer** (fresh thread, whole paper, all lenses) that returns zero CRITICAL / MAJOR.

## Failure classes the reviewer hunts

AI-sounding prose (as defined by the profile's gate, not by taste), inaccessible text (undefined symbols and
acronyms), incoherent structure (claims that do not map to results), illogical steps (a benchmark that is not the one
described, an assumption that changes between model and simulation).
