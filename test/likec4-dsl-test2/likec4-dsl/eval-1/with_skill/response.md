**Minimal `projects/template/likec4.config.json`:**

```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "template",
  "title": "Template Project",
  "include": [
    { "paths": ["../shared"] }
  ]
}
```

This config lives at `projects/template/`, so all `.c4` files under `projects/template/` belong to this project. The `include.paths` entry points up one level to `projects/shared/` so those shared spec files are also parsed as part of this project.

**How LikeC4 determines project ownership:**

LikeC4 uses **nearest-config-file wins**: a `.c4` file belongs to the project whose config file (`likec4.config.json`, `.likec4rc`, or `likec4.config.{ts,js}`) is closest in the directory hierarchy (i.e., the config file in the same directory or the nearest ancestor directory). Files in `projects/template/` resolve to `projects/template/likec4.config.json`; files in `projects/shared/` have no config of their own, so they are not autonomously owned — they are pulled in only because the template project explicitly includes them via `include.paths`.
