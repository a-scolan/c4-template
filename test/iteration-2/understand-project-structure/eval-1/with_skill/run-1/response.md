After a project switch, treat previous context as stale.

Re-run these checks before editing a C3 view:

1. `list-projects` to verify the intended project ID.
2. `read-project-summary` with explicit project.
3. `search-element` (or `read-element`) for the target system/container boundary.
4. Re-open shared taxonomy sources:
   - `projects/shared/SPEC_CHEATSHEET.md`
   - `projects/shared/spec-*.c4`
5. Confirm project include wiring (`likec4.config.json`) still points to shared specs.

Why this matters for C3 views:

- C3 needs the exact parent container/system.
- Wrong active project causes false “element not found” or invalid kind usage.
- Relationship labels can differ between model vs deployment context.

Safe anti-error routine:

- Validate project
- Validate taxonomy
- Validate parent chain/FQN
- Then edit view
- Re-check references once done

This prevents the most common context errors: wrong project, wrong kind, wrong parent, wrong relationship namespace.