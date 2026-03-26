Minimal `projects/template/likec4.config.json`:

```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "template",
  "include": {
    "paths": ["../shared"]
  }
}
```

Project ownership rule: a `.c4` file belongs to the project defined by the **nearest** LikeC4 config file in its directory ancestry (`likec4.config.*`, `.likec4rc`, etc.).