Keep the template config shape intact and only replace the project-specific values.

Preserve these fields:
- `$schema`
- `name`
- `title`
- `include.paths`
- `imageAliases`

Because `likec4.config.json` lives in `projects/payments/`, the shared references must stay relative to that folder:
- shared specs: `../shared`
- shared images: `@`: `../shared/images/`

A safe starting point is:

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

Do not switch to workspace-root references or absolute paths. If you add more shared sources later, append them to `include.paths` instead of replacing the existing entry.