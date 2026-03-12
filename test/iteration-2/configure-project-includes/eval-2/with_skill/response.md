Treat this as a targeted config edit, not a full model reorganization.

Edit rules:
- Preserve the existing `include.paths` entries.
- Add the new shared source without replacing `../shared` or `../platform-shared`.
- Keep paths relative to the project folder; do not switch to absolute paths.
- Keep the existing `imageAliases`, especially the shared `@` alias, so icons keep resolving.
- If the current resolution already works, keep the current order and append the new source at the end.

Example:

```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "payments",
  "title": "Payments",
  "include": {
    "paths": [
      "../shared",
      "../platform-shared",
      "../new-common-source"
    ]
  },
  "imageAliases": {
    "@": "../shared/images/"
  }
}
```

In short: append, preserve, stay relative, and do not drop the shared image alias.
