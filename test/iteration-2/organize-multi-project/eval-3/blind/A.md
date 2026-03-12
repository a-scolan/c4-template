Do **not** put everything into `projects/shared/`.

A clean split is:

- `projects/shared/` for truly reusable **specs, conventions, tags, relationships, and images**
- project folders for **project-owned business models**
- an extra shared domain folder/project only when a business model is genuinely reused by multiple projects

That keeps the repo simple without turning it into a maze.

A practical structure is:

```text
projects/
  shared/                  # specs, conventions, icons
  payments/                # owns payments-specific systems and views
  billing/                 # owns billing-specific systems and views
  domains/                 # optional: only for truly reusable business models
    shared-business/       # small, explicit, reusable domain model
```

Rules of thumb:

- keep technical conventions in `shared`
- do **not** place project-specific business models in `shared`
- move business concepts into a reusable domain project only if multiple projects genuinely share them
- keep dependencies **one-way** and avoid circular references between projects

In practice, most repos only need:

1. one shared specs area
2. one folder per owning project
3. optionally one small reusable domain project for cross-project business concepts

Keep the include/config wiring per project in that project's own `likec4.config.json`, with relative paths back to `../shared` where needed.
