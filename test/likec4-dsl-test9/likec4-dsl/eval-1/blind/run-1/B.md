```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "template",
  "include": {
    "paths": ["../shared"]
  }
}
```

This makes the `projects/template/` project load `.c4` files from `projects/shared/` as shared sources.

When multiple LikeC4 config files exist in one workspace, each config file defines a separate project, and a `.c4` file belongs to the project of the **nearest config file in its directory hierarchy**. In practice, LikeC4 walks up from the `.c4` file’s folder and uses the first config it finds. So a file under `projects/template/` belongs to the project defined by `projects/template/likec4.config.json`, while shared files under `projects/shared/` are not automatically part of that project unless you bring them in through `include.paths`.