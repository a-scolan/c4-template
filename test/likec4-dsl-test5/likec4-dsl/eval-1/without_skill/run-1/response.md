Minimal `projects/template/likec4.config.json` example:

```json
{
  "$schema": "https://likec4.dev/schemas/likec4.config.schema.json",
  "specification": ["../shared/spec-*.c4"],
  "include": ["./**/*.c4"]
}
```

How file-to-project resolution works with multiple configs:
- LikeC4 assigns a `.c4` file to the nearest `likec4.config.json` in its directory ancestry.
- So files under `projects/template/` resolve to `projects/template/likec4.config.json`.
- Files under another folder with its own config resolve to that other project.
- Shared spec files are reused by reference (via config paths), but ownership still follows the file’s nearest config.