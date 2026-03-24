1. Probable error category: dynamic-view containment + invalid layout hint.
2. Root cause: `system -> system.api` models a parent calling its own child, which is usually just containment expressed as an interaction. Then `rank same user, system.api` is invalid because `rank same` should only be used for siblings in the same parent context; `user` and `system.api` do not share one.
3. Verification step: confirm that `system.api` is nested under `system` from its FQN, and confirm that `user` and `system.api` are not siblings.
4. Minimal fix: remove the parent-to-child interaction and show the real caller targeting the child directly. Only keep `rank same` for true siblings.
Example:
`user -> system.api 'Starts request'`
If you need a rank hint, use siblings such as `rank same system.web, system.api`.
