Keep the current shared source first and add the new one after it if you want current behavior to keep winning on conflicts.

```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "payments",
  "title": "Payments",
  "include": {
    "paths": ["../shared", "../platform-shared"]
  },
  "imageAliases": {
    "@": "../shared/images/",
    "@platform": "../platform-shared/images/"
  }
}
```

Rules:
- Add `../platform-shared`; do not replace `../shared`.
- Keep paths relative to the project folder.
- Treat `include.paths` as an explicit resolution order. If `../shared` stays first, its current behavior remains the baseline. Moving `../platform-shared` earlier would change which overlapping definitions win.
- Do not reuse the same image alias key for both sources. Keep `@` mapped to the current shared images and give the new source a distinct prefix such as `@platform`, or rename the colliding aliases in the new source.
- Only choose an intentional override if you really want the new source to replace the old one; otherwise avoid blind alias merging.
