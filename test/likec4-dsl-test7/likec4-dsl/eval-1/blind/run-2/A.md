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

LikeC4 decides project membership by the **nearest config file in the directory hierarchy**. A `.c4` file belongs to the project defined by the closest `likec4.config.json` (or other supported config filename) in its folder or any parent folder. In a multi-project workspace, shared `.c4` files are typically reused via `include.paths` rather than by belonging to multiple projects directly.
