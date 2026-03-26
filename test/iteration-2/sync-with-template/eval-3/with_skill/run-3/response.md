Verification checklist before upstream push via `c4-template`:

1. Generic across repos: works outside your current project/domain.
2. No local assumptions: strip domain-specific naming/rules.
3. Confidentiality clean: no sensitive internals, secrets, personal/team identifiers.
4. Correct sync surface: file is in `projects/shared/` and remains reusable.
5. Clean sync diff: `sync/*` branch from `c4-template/main`, include only the shared file.

If any check fails, keep local or split the change into generic vs local parts.