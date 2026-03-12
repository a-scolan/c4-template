Do not put everything in `projects/shared/`.

A simple structure that stays readable is:

- `projects/shared/` → truly reusable technical conventions and assets (`spec-*.c4`, tags, styles, relationship kinds, images)
- domain projects such as `projects/payments/`, `projects/orders/`, `projects/customer/` → domain-owned systems, actors, containers, and views
- optionally one small dedicated project for reusable cross-domain business abstractions if they are genuinely shared by multiple domains

The key boundary is:

- technical conventions belong in `projects/shared/`
- business models do **not** go in `projects/shared/` just because several teams can see them

If a business concept is reused across projects, either:

- model it as a small shared external abstraction, or
- give it its own dedicated project with clear ownership

Keep cross-project references explicit and minimal, and avoid circular dependencies between projects.

If you also need to adjust `include.paths` or image aliases while setting this up, use `configure-project-includes` for the config details.
