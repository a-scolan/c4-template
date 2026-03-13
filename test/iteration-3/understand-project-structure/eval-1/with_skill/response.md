When you switch projects before editing a C3 view, revalidate context before touching the model.
Verification sequence:
1. Reconfirm the active project immediately after the switch.
2. Re-run MCP checks in this order: `list-projects` -> `read-project-summary` for the explicit project -> `search-element` or `read-element` for the target system/container boundary you plan to edit.
3. Re-read shared semantics before the C3 change: `projects/shared/SPEC_CHEATSHEET.md`, then confirm the actual taxonomy in `projects/shared/spec-components.c4`, `spec-containers.c4`, `spec-global.c4`, and any other relevant shared spec.
4. Re-open the target project's `likec4.config.json` to confirm it still includes `../shared`.
5. Inspect the exact model/view files for that C3 area, then edit.
Risks avoided: stale context from the previous project, invalid kind or relationship names copied from the wrong context, wrong C3 parent container/system, and broken FQNs or references. Keep semantic validation ahead of browsing example files; examples can illustrate patterns, but shared specs plus the project summary remain the truth.
