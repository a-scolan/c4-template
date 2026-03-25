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

LikeC4 determines project ownership by **nearest config file** in the directory tree (`likec4.config.json`, `.likec4rc`, etc.).

- A `.c4` file is assigned to the project whose config is closest in its parent folders.
- With multiple configs in a workspace, this nearest-config rule disambiguates which project a file belongs to.
- The `include` setting in `projects/template/likec4.config.json` lets that project also load shared files from `projects/shared/` for reuse.