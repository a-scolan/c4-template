A minimal `projects/template/likec4.config.json` can look like this:

```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "template",
  "title": "Template",
  "include": [
    "./**/*.c4",
    "../shared/**/*.c4"
  ]
}
```

How project ownership works when multiple config files exist:

- A LikeC4 project is defined by a config file (`likec4.config.json`, `.likec4rc`, etc.).
- By default, a `.c4` file belongs to the project of the **nearest config file in its parent directory chain**.
- So if multiple configs exist in the workspace, LikeC4 resolves membership by proximity (closest ancestor config wins).
- `include` lets a project intentionally pull in files (such as `../shared/**/*.c4`) so shared specs are reused in that project.