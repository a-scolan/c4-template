You can split these changes into two groups.

## Can be pushed to the template

- `.github/skills/create-relationship/SKILL.md` — generic skill content belongs in the template.
- `projects/shared/spec-context.c4` — shared reusable spec content can go back to the template **if** the change is still generic.

## Must stay local

- `projects/payments/system-model.c4` — this is a project-specific model.
- `README.md` — this is project introduction/documentation and should stay local.

## Before pushing anything

1. **Generalize the content**: remove project names, internal identifiers, and any local assumptions.
2. **Run a confidentiality review**: make sure the diff does not expose internal architecture, security details, employee/team names, or other confidential context.
3. **Push only the generic files** from a dedicated `sync/*` branch.

If a change only makes sense for the `payments` project, or another project would need to adapt it heavily, keep it local instead of pushing it to the template.
