## CLI Command

Run this from the repo root:

```bash
npx likec4 validate --json --no-layout --file projects/template/system-model.c4 projects/template 2>/dev/null
```

- `--no-layout` skips layout-drift checks, keeping validation to syntax and semantics only.
- `--file projects/template/system-model.c4` scopes error reporting to that one file.
- `projects/template` is the project directory (the folder containing the nearest `likec4.config.json`).

## Which JSON Fields to Read

| Field | What it tells you |
|---|---|
| `filteredErrors` | Errors in **your file only**. If `0`, your file is clean. |
| `totalErrors` | Errors across the **entire project**. |
| `filteredFiles` | Sanity-check: should equal `1` (the number of `--file` arguments you passed). |
| `valid` | Overall project validity — `false` does **not** mean your file is broken. |

**Interpretation rule:**

- `filteredErrors == 0` → your file is valid regardless of `totalErrors`.
- `filteredErrors > 0` → your file has errors; fix those first.
- `filteredErrors == 0` but `totalErrors > 0` → another file in the project is broken; that is not your problem right now.
- `filteredFiles != 1` → the `--file` path did not match; double-check the path.
