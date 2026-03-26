# Eval 5 — Smallest safe JSON edit to add `../platform-shared`

## Two targeted changes only

1. Append `"../platform-shared"` to `include.paths` — after `"../shared"`, not replacing it.
2. Add `"@platform": "../platform-shared/images/"` to `imageAliases` — new key, no collision with existing `"@"`.

Do not touch any other field.

## Before

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

## After (minimal edit)

```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "payments",
  "title": "Payments Architecture",
  "include": {
    "paths": [
      "../shared",
      "../platform-shared"
    ]
  },
  "imageAliases": {
    "@": "../shared/images/",
    "@platform": "../platform-shared/images/"
  }
}
```

## What changed

| Field | Change |
|---|---|
| `include.paths` | `"../platform-shared"` appended |
| `imageAliases` | `"@platform"` key added |
| Everything else | Unchanged |

## What did NOT change and why

- `"@": "../shared/images/"` — kept intact; removing or changing it would break all existing `@`-prefixed icon references in every view.
- `"../shared"` in paths — kept; it provides shared element specs and the base image set.
- `$schema`, `name`, `title` — no reason to touch them.
