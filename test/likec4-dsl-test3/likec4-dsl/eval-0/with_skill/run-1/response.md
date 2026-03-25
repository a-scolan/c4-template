Run this from the repo root:

```bash
npx likec4 validate --json --no-layout --file projects/template/system-model.c4 projects/template 2>/dev/null
```

Use these JSON fields to interpret scope of failure:

- `stats.filteredFiles` should be `1` (confirms your `--file` filter matched exactly one file).
- `stats.filteredErrors` tells whether your edited file failed validation.
- `stats.totalErrors` tells total project errors.

How to read it:

- `filteredErrors > 0` → your target file has syntax/semantic errors.
- `filteredErrors == 0` and `totalErrors > 0` → your file is clean; other files/project parts are broken.
- `totalErrors == 0` → project is fully valid.