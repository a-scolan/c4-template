# iteration-2 notes

Launched on 2026-03-12 after the skill cleanup pass.

Scope of this iteration:
- validate updated skill quality after decoupling from example projects
- measure impact of revised eval wording
- verify restrained guidance on `rank` and optional `autoLayout LeftRight`

Preflight status:
- skills with evals: 19
- total eval prompts: 78
- direct template/showcase coupling in `.github/skills/**`: cleaned, except intentional explanatory references in `sync-with-template`
- support/reference docs genericized away from `vault.*`

Execution note:
This repository currently exposes the evaluation protocol (`test/skill-suite-eval-prompt.md`) and helper utilities (`test/scripts/skill_suite_tools.py`), but no single end-to-end runner script is present in the checkout. The actual run must therefore be orchestrated phase by phase.
