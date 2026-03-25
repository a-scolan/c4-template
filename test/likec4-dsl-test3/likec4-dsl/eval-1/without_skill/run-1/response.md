A minimal `projects/template/likec4.config.json` can look like this:

```json
{
  "name": "template",
  "include": {
    "paths": [
      "./*.c4",
      "../shared/*.c4"
    ]
  }
}
```

How LikeC4 decides project ownership when multiple configs exist:

- Each `likec4.config.json` defines a separate project scope.
- A `.c4` file belongs to the project(s) whose `include` rules match it (after any `exclude` filtering).
- Paths in `include.paths` are resolved relative to that config file’s folder.
- So with multiple configs in one workspace, project membership is rule-based (include/exclude matching), not just “nearest folder” by itself.
- If two project configs both include the same `.c4` file, that file is effectively shared across those two projects.