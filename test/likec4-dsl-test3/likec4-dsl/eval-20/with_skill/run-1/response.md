```bash
npx likec4 validate --json --no-layout --file projects/template/system-model.c4 --file projects/template/system-views.c4 projects/template 2>/dev/null
```

In the JSON output, check `stats`:

- `filteredFiles` should be `2` (confirms both `--file` filters were applied).
- `filteredErrors` are errors from only those two files.
- `totalFiles` / `totalErrors` describe the whole project, so `totalErrors` can be higher even when filtering works.
