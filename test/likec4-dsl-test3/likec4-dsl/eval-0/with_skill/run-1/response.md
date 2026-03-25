Run this from the repo root:

```bash
npx likec4 validate --json --no-layout --file projects/template/system-model.c4 projects/template 2>/dev/null
```

Use these JSON fields:

- `stats.filteredFiles` — should be `1` (confirms your `--file` filter matched exactly that file).
- `stats.filteredErrors` — errors in your edited file only.
- `stats.totalErrors` — errors across the whole project.
- `valid` — global project validity.

How to interpret:

- **Your file failed:** `stats.filteredErrors > 0`.
- **Your file is clean but project is broken elsewhere:** `stats.filteredErrors == 0` and `stats.totalErrors > 0`.
- **Likely only your file is failing:** `stats.filteredErrors > 0` and `stats.totalErrors == stats.filteredErrors` (with `filteredFiles == 1`).