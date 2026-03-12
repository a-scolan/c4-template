Treat these as two separate root-cause checks, not one vague rename problem.

1. `Unknown kind Container_WebUi`
   - In this workspace, element kinds are spec-defined. Check the shared specs — or `read-project-summary` if that is part of your workflow — before editing.
   - `Container_WebUi` is not a valid container kind in the shared taxonomy. Valid nearby kinds include `Container_Webapp`, `Container_Spa`, and `Container_Browser`.
   - So the root cause is an invalid kind, not a typo the compiler can infer.

2. `Element not found: api`
   - That usually means the reference is too short or points at the wrong scope.
   - Verify where the element is declared, then use its full FQN, for example `system.api` rather than just `api`.

Targeted fix:
- First confirm the valid kind from the shared specs / project summary.
- Then find the actual declaration of the API element and update references to its exact FQN.
- Do not start by randomly renaming things; fix the invalid kind and the broken reference separately.

If the intent was a web UI container talking to an API, the corrected shape is usually:
- declare the UI as `Container_Webapp` or `Container_Spa`
- reference the API by its full path such as `system.api`
