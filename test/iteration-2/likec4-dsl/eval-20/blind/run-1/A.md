Use:

```bash
npx likec4@latest validate --json --no-layout \
  --file projects/template/system-model.c4 \
  --file projects/template/system-views.c4 \
  projects/template
```

Confirm filtering in JSON with:
- `stats.filteredFiles` should be `2`.
- `stats.filteredErrors` is the error count limited to those two files.