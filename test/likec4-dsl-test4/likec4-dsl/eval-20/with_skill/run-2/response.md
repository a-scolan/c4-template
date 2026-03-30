## Exact command

```bash
npx likec4 validate --json --no-layout --file projects/template/system-model.c4 --file projects/template/system-views.c4 projects/template
```

- `--json` — structured JSON output on stdout
- `--no-layout` — skips layout drift checks (syntax + semantics only)
- `--file` (repeated) — filters error reporting to the two specified files
- `projects/template` — the project directory (location of `likec4.config.json`)

## Confirming both files were filtered

In the JSON output, check the `stats` object:

```json
{
  "valid": true,
  "errors": [],
  "stats": {
    "totalFiles": 10,
    "totalErrors": 0,
    "filteredFiles": 2,
    "filteredErrors": 0
  }
}
```

- **`filteredFiles: 2`** confirms both `--file` arguments were matched and included in the filtered report. If it returns `1`, one path was not resolved or did not match any project file.
- **`filteredErrors`** shows errors only from your two files — this is zero even if `totalErrors` is high (meaning other files in the project have pre-existing issues, which are not your problem).
- If `filteredFiles` is `0`, the paths are wrong or relative to the wrong working directory — run the command from the repo root.
