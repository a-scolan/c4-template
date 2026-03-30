```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "template",
  "include": {
    "paths": ["../shared"]
  }
}
```

LikeC4 assigns each `.c4` file to the project defined by the nearest config file in that file's directory hierarchy. In a multi-project workspace, the closest `likec4.config.*` (or `.likec4rc`) wins; shared files outside that tree are brought into the project through `include.paths`.