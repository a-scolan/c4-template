```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "template",
  "title": "Template",
  "include": {
    "paths": ["../shared"]
  }
}
```

LikeC4 decides project ownership by the **nearest config file in the directory hierarchy**. That means a `.c4` file belongs to the project defined by the closest `likec4.config.json` (or other supported config filename) in its folder or any parent folder.

So with `projects/template/likec4.config.json`, files under `projects/template/` belong to the `template` project. Shared files in `projects/shared/` are **not** automatically part of that project just because they are nearby; they are brought in because `include.paths` explicitly points to `../shared`.