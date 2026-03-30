```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "template",
  "include": {
    "paths": ["../shared"]
  }
}
```

LikeC4 assigns each `.c4` file to the project defined by the **nearest** config file in its directory ancestry (`likec4.config.*`, `.likec4rc`, etc.). In a multi-config workspace, nearest-config wins; `include.paths` just pulls extra source files into that project.