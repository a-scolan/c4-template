```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "template",
  "title": "Template",
  "extends": "../shared"
}
```

LikeC4 assigns each `.c4` / `.likec4` file to the project defined by the **nearest config file** in its directory hierarchy (`likec4.config.json`, `.likec4rc`, or `likec4.config.{ts,js}`).

So in a workspace with multiple configs, file ownership is resolved by closest-parent config: files under `projects/template/` belong to the `template` project unless a deeper subfolder has its own config.