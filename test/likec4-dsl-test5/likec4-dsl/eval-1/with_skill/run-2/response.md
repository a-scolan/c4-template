```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "template",
  "include": {
    "paths": ["../shared"]
  }
}
```

LikeC4 assigns each `.c4` file to the project defined by the **nearest** config file in its directory hierarchy. In a multi-config workspace, the closest config wins; shared files can be pulled in via `include.paths`.