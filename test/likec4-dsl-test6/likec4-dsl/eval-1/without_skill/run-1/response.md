Minimal `projects/template/likec4.config.json` example:

```json
{
  "$schema": "https://likec4.dev/schemas/likec4.config.schema.json",
  "include": [
    "./**/*.c4",
    "../shared/**/*.c4"
  ]
}
```

How LikeC4 assigns files to a project when multiple configs exist:

1. Each `likec4.config.json` defines a project root (its directory).
2. A `.c4` file belongs to the project whose config includes it via `include` patterns.
3. If multiple config files exist in the workspace, they represent separate projects; in practice, the nearest/selected project context controls which include set is used for CLI operations.
4. So for deterministic behavior, run CLI from the intended project root or pass the project path explicitly.