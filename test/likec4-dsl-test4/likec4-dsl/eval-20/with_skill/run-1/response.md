## Exact command

```bash
npx likec4 validate --json --no-layout --file projects/template/system-model.c4 --file projects/template/system-views.c4 projects/template
```

- `--no-layout` skips layout drift checks (syntax + semantic only).
- `--file` is repeated once per file; both paths are relative to the repo root.
- `projects/template` is the project directory argument.

## Confirming both files were filtered

Check the `stats` object in the JSON output:

```json
{
  "valid": true,
  "errors": [],
  "stats": {
    "totalFiles": 5,
    "totalErrors": 0,
    "filteredFiles": 2,
    "filteredErrors": 0
  }
}
```

- **`filteredFiles: 2`** — confirms that exactly your two `--file` paths were matched and reported on. If this is `1` or `0`, the path(s) you passed don't match what LikeC4 resolved (check relative vs. absolute paths).
- **`filteredErrors`** — number of errors originating in those two files specifically. This is the value to check for your edit being clean.
- **`totalErrors`** — errors across the whole project. If `filteredErrors` is `0` but `totalErrors` is high, your files are clean and something else in the project is broken (not caused by your edits).
