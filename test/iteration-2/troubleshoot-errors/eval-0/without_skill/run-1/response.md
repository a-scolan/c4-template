Root cause is likely two separate issues:

1) `Unknown kind Container_WebUi`
- LikeC4 kind names are case-sensitive and must be declared in the spec/config before use.
- Diagnose by checking where `Container_WebUi` is declared versus where it is used.
- If your project defines `container`/`webui` differently (or not at all), this identifier is invalid.

2) `Element not found: api`
- This is usually scope/FQN mismatch.
- In nested scopes, short names resolve relative to current scope. `api` may need full FQN (for example `system.api`) or the element may not exist in the current model file/include set.

Proper diagnosis sequence:
- First fix model parsing/type issues (`Unknown kind ...`) so symbol tables are valid.
- Then resolve element lookup with exact declared id/FQN and scope.
- Verify declarations exist in included files and ids match exactly (case-sensitive).

Clean fix:
- Replace `Container_WebUi` with a valid declared kind.
- Replace `api` with the correct declared element id/FQN in the current scope.