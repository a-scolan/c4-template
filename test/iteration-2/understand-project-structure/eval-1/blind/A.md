After a project switch, assume the previous project context is stale.

## Revalidation sequence before editing a C3 view

1. Re-run `list-projects` to confirm which projects are available in the workspace.
2. Re-run `read-project-summary` for the project you just switched to.
3. Read that project's `likec4.config.json` to confirm include paths and image aliases.
4. Re-read the shared specs that govern C3 work:
   - `projects/shared/spec-context.c4`
   - `projects/shared/spec-containers.c4`
   - `projects/shared/spec-components.c4`
   - `projects/shared/spec-global.c4`
5. Use `read-element` on the container that will own the C3 view so you confirm the parent container exists in the new project.
6. If the target container or view name is unclear, use `search-element` before editing.
7. Re-open the current project's model/view files and verify the C3 view belongs in the correct folder and naming pattern.

## Why this avoids context errors

- **Stale context** — you avoid carrying kinds, tags, elements, or assumptions from the previous project into the new one.
- **Invalid kind/relationship usage** — you re-anchor on the real shared taxonomy instead of guessing from memory.
- **Wrong C3 parent** — you confirm that the target component view belongs to the correct container in the active project.
- **Wrong file/project edits** — you avoid updating a view in `projects/template` while actually intending to work in `projects/spec-showcase`, or the reverse.

## Practical rule

Do not edit a C3 view immediately after switching projects. Re-establish the active project, re-read shared specs, confirm the container parent, then edit. That small pause prevents the expensive kind of LikeC4 mistake: the one that looks valid until rendering time.