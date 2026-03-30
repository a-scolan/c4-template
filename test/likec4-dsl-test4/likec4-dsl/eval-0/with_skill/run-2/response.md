# Exact CLI command

Run from the repo root:

```bash
npx likec4 validate --json --no-layout --file projects/template/system-model.c4 projects/template 2>/dev/null
```

- `--no-layout` skips layout-drift checks → only syntax and semantic validation.
- `--file projects/template/system-model.c4` scopes error reporting to that single file.
- `projects/template` is the project directory (where `likec4.config.json` lives).
- `2>/dev/null` discards the progress log so stdout is clean JSON.

# JSON fields that distinguish "my file failed" vs "whole project broken"

The output contains a `stats` object:

```json
{
  "valid": false,
  "errors": [ ... ],
  "stats": {
    "totalFiles": 100,
    "totalErrors": 500,
    "filteredFiles": 1,
    "filteredErrors": 1
  }
}
```

| Field | What it tells you |
|---|---|
| `filteredErrors` | Errors **inside the file(s) you passed to `--file`**. If this is **0**, your file is clean. |
| `totalErrors` | Errors across the **entire project**. If this is high while `filteredErrors` is 0, something else in the project is broken — not your file. |
| `filteredFiles` | Should equal the number of `--file` arguments you passed (here: **1**). Verify this matches so you know the filter actually hit your file. |
| `valid` | `false` if **any** error exists in the project — not reliable for scoping to a single file. Use `filteredErrors` instead. |

**Decision rule:**
- `filteredErrors == 0` → your file is fine, any remaining `totalErrors` are pre-existing issues elsewhere in the project.
- `filteredErrors > 0` → your file has errors; fix those first.
