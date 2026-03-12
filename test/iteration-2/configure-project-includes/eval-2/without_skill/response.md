Treat this as a targeted config edit, not a full model reorganization.

Edit rules:

- Keep the existing `include.paths` entries exactly as they are.
- Add the new shared source without replacing `../shared` or `../platform-shared`.
- Keep the existing image alias that current diagrams already use.
- Use project-relative paths only; avoid absolute paths.

Example pattern:

```json
{
  "include": {
    "paths": [
      "../shared",
      "../platform-shared",
      "../new-shared"
    ]
  },
  "imageAliases": {
    "@": "../shared/images/"
  }
}
```

If the new shared source also provides icons, add a new alias for it instead of removing or repointing the current shared alias.