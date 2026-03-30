```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "template",
  "include": {
    "paths": ["../shared"]
  }
}
```

LikeC4 assigns each `.c4` file to the project defined by the nearest config file in its directory hierarchy. If multiple config files exist in the workspace, the closest one above the file wins. Shared files are typically reused by adding their directories via `include.paths`; that makes those `.c4` files part of the consuming project as included sources.