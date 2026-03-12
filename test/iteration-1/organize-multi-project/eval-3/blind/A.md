Do not put everything in `projects/shared/`.

Use two layers, not one:
1. `projects/shared/` for truly reusable specs, conventions, relationship/tag definitions, and shared images/assets.
2. Separate reusable domain projects for business models that are shared by more than one project.

A simple structure is:
- `projects/shared/`
- `projects/payments/`
- `projects/customers/`
- `projects/business-common/` only if some business models are genuinely reused

Rules to keep it simple:
- Do not place project-specific business models in `projects/shared/`.
- Keep each business capability owned by one project or one reusable domain library.
- Let product projects depend on `../shared` and, when needed, a small number of reusable domain projects.
- Reusable domain projects may depend on `../shared`, but not on product projects.
- Keep dependencies one-way and acyclic.

A good default is:
- start with `projects/shared/` for conventions only
- keep business models in their owning project
- extract a reusable domain project only when at least two projects need the same model

If you need to wire include paths or image aliases for those projects, handle that in the separate project-configuration step.
