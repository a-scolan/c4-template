Start from a **minimal fresh project**, not by treating `spec-showcase` as the canonical source.

Create a new folder such as `projects/payments/` with only these baseline files:

- `likec4.config.json`
- `system-model.c4`
- `system-views.c4`

A clean minimum setup is:

```text
projects/
  shared/
  payments/
    likec4.config.json
    system-model.c4
    system-views.c4
```

Use one config file **per project**. The minimum config should point back to the reusable shared area:

```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "payments",
  "title": "Payments",
  "include": {
    "paths": ["../shared"]
  },
  "imageAliases": {
    "@": "../shared/images/"
  }
}
```

Keep the project self-contained:

- put the `paymentsCore` system, actors, containers, and relationships in `system-model.c4`
- put the views in `system-views.c4`

Keep `projects/shared/` only for **reusable specs and assets**:

- shared element/relationship definitions
- tag and color conventions
- shared icons/images

That gives you a clean bootstrap without over-structuring the repo too early. Add more files only when the payments project becomes large enough to justify it.
