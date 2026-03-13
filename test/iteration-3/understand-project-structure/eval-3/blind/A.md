Once project context is established, hand off to `c4-modeling-process`.
Before that handoff, this first skill must lock in:
- the active project, or the exact method to confirm it;
- the semantic source of truth: project summary plus `projects/shared/spec-*.c4` and `projects/shared/SPEC_CHEATSHEET.md`;
- the valid local kinds, relationships, and tags for the target change;
- the target project's `likec4.config.json`;
- the nearby model/view files that will actually be edited.
Role split:
- `understand-project-structure` = workspace framing and semantic validation.
- `c4-modeling-process` = sequencing the actual modeling work from C1 -> C2 -> C3.
The handoff should stay explicit that shared specs and the project summary define semantic truth, while `.github/skills/` provides workflow guidance only.
