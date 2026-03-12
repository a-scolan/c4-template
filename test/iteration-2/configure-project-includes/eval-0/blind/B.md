Keep the config minimal and project-relative.

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

Rules to follow:

- Keep the core fields: `$schema`, `name`, `title`, `include`, and `imageAliases`.
- Resolve paths from `projects/payments/`, so `../shared` and `../shared/images/` are the correct references.
- Keep the shared image alias `@` pointed at `../shared/images/`.
- Avoid workspace-root or absolute paths; they are fragile and can break imports on another machine.