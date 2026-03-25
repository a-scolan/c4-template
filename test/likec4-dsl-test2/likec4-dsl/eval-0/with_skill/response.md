**CLI command** (run from repo root):

```bash
npx likec4 validate --json --no-layout --file projects/template/system-model.c4 projects/template
```

- `--no-layout` skips layout drift checks → syntax + semantic only
- `--file projects/template/system-model.c4` scopes reported errors to that file
- `projects/template` is the project directory (contains `likec4.config.json`)

**JSON fields for triage** (from the `stats` object):

| Field | Meaning |
|---|---|
| `stats.filteredErrors` | Errors in your file only. `0` → your file is clean. |
| `stats.totalErrors` | Errors across the whole project. |
| `stats.filteredFiles` | Should be `1`; confirms the `--file` filter matched exactly your file. |
| `valid` | `false` if the project has any error at all (yours or others'). |

**Decision rule:**
- `filteredErrors > 0` → your file has a problem, fix it.
- `filteredErrors == 0` and `totalErrors > 0` → your file is clean; something else in the project is broken (not caused by your edit).
- `filteredErrors == 0` and `totalErrors == 0` → everything is fine.
