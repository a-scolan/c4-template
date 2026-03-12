Do **not** put everything into `projects/shared/`.

Use `projects/shared/` only for things that are truly reusable across the workspace:
- shared specs
- common tags, kinds, and styles
- shared images/assets
- global conventions

Keep reusable business models separate from that. A simple structure is:
- `projects/shared/` for specs and assets
- domain projects such as `projects/payments/`, `projects/orders/`, `projects/customer/`
- if a business model is genuinely reused by multiple projects, give it a small dedicated project such as `projects/common-domain/` or `projects/externals/`

That keeps the repository simple without turning `shared/` into a dumping ground. The rule of thumb is:
- conventions/specs/assets -> `shared/`
- domain models -> owning project
- truly reusable business surface -> small dedicated project with clear ownership

Keep cross-project references explicit and preferably one-way, and avoid circular dependencies between projects. If you also need to wire `include.paths` or image aliases for that structure, pair this with `configure-project-includes` rather than expanding the shared area beyond reusable specs and assets.