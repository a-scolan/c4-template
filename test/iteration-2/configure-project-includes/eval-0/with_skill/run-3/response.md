# Eval 0 — Creating `projects/payments/likec4.config.json`

## Which fields to keep

When bootstrapping from the workspace baseline, preserve all five required fields:

| Field | Purpose |
|---|---|
| `$schema` | Enables IDE validation against the official JSON schema |
| `name` | Stable machine identifier for the project |
| `title` | Human-readable display name |
| `include.paths` | Relative paths to shared spec folders |
| `imageAliases` | Maps the `@` shorthand to the shared images folder |

## How to reference shared specs and images

- Paths are **relative to the project folder** (e.g., `projects/payments/`), not the workspace root.
- Always use `"../shared"` — never an absolute path.
- Keep `"@": "../shared/images/"` intact so every `@`-prefixed icon reference in views continues to resolve.

## Correct minimal config

```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "payments",
  "title": "Payments Architecture",
  "include": {
    "paths": ["../shared"]
  },
  "imageAliases": {
    "@": "../shared/images/"
  }
}
```

## Rules not to break

- ❌ Do not use absolute paths (`/home/user/shared` breaks portability).
- ❌ Do not drop `imageAliases` — omitting it breaks all `@`-prefixed icon refs across every view in the project.
- ❌ Do not rename the file — LikeC4 expects `likec4.config.json` exactly.
