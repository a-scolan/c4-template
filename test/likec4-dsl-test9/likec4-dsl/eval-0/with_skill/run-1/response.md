```bash
npx likec4 validate --json --no-layout --file projects/template/system-model.c4 projects/template
```

Use these JSON fields:

- `stats.filteredFiles`: should be `1` here, which confirms your `--file` filter matched only `projects/template/system-model.c4`.
- `stats.filteredErrors`: errors in the filtered file set only.
- `stats.totalErrors`: errors across the whole LikeC4 project.
- `valid`: overall project validity after the merged model is parsed.

How to read it:

- If `stats.filteredErrors > 0`, your file failed validation.
- If `stats.filteredErrors == 0` and `stats.totalErrors > 0`, your file is clean but the project is broken somewhere else.
- If `stats.filteredFiles == 1` and `stats.filteredErrors == stats.totalErrors`, then all reported errors are coming from your file.
- `valid` can still be `false` even when `stats.filteredErrors == 0`, because `valid` reflects the whole project, not just the filtered file.