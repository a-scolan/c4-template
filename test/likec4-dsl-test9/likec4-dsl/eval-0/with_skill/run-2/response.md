Run this from the repo root:

```bash
npx likec4 validate --json --no-layout --file projects/template/system-model.c4 projects/template
```

Check these JSON fields:

- `stats.filteredFiles` — should be `1`, confirming only `projects/template/system-model.c4` matched your `--file` filter.
- `stats.filteredErrors` — errors in that filtered file only.
- `stats.totalErrors` — errors across the whole LikeC4 project.
- `valid` — overall project validation result.

How to tell what broke:

- **Only your file failed:** `stats.filteredFiles == 1` and `stats.filteredErrors > 0`.
- **Your file is clean, but the project is broken elsewhere:** `stats.filteredFiles == 1`, `stats.filteredErrors == 0`, and `stats.totalErrors > 0`.
- **Everything is clean:** `valid == true` (so both filtered and total errors are effectively `0`).
- **Your file failed and other files also failed:** `stats.filteredErrors > 0` and `stats.totalErrors > stats.filteredErrors`.
