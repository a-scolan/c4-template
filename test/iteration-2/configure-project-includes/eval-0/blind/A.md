Keep the same minimal config shape as the workspace baseline and only change the project-specific values.

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

Key rules:
- Keep `$schema`, `name`, `title`, `include.paths`, and `imageAliases`.
- Resolve paths relative to `projects/payments/`, so `../shared` and `../shared/images/` are correct.
- Keep the `@` alias pointing at the shared images folder so existing icon references keep working.
- Do not use absolute paths or workspace-root paths.
- If you add more shared sources later, append them to `include.paths` instead of replacing the existing entry.
