Run from repo root:

```bash
npx likec4@latest validate --json --no-layout --file projects/template/system-model.c4 projects/template
```

Use these JSON fields:
- `stats.filteredFiles`: confirms the `--file` filter matched your file.
- `stats.filteredErrors`: errors in the filtered file(s) only.
- `stats.totalErrors`: total project errors.

Interpretation:
- Your file failed: `filteredErrors > 0`.
- Your file is clean but project is broken elsewhere: `filteredErrors = 0` and `totalErrors > 0`.