npx likec4 validate --file projects/template/system-model.c4 --file projects/template/system-views.c4 --file projects/template/likec4.config.json --output json

- `filteredFiles`: how many files matched your `--file` filters and were included in the filtered validation scope.
- `filteredErrors`: how many errors belong to that filtered file set.
- `totalErrors`: how many errors exist overall in the full validation run (filtered + non-filtered files).

If `filteredFiles` is `2` instead of `3`, one of the three file filters did not resolve into the filtered validation scope (commonly a wrong path/filename, or that file is outside what the validator loaded for this run).
# LikeC4 Syntax/Semantic Validation — Three Edited Files

## Validation Command

```
npx likec4 check --file projects/template/system-model.c4 --file projects/template/system-views.c4 --file projects/template/likec4.config.json
```

---

## What Each Output Field Means

| Field | Meaning |
|---|---|
| `filteredFiles` | The number of files, among those passed with `--file`, that the checker actually found and processed as part of the model graph. It confirms how many of your specified files were loaded and indexed. |
| `filteredErrors` | The count of diagnostics (syntax or semantic errors) found **exclusively within** the files matched by `--file`. This is the actionable number for your change set — the errors you are directly responsible for. |
| `totalErrors` | The count of all diagnostics across the **entire project**, including every file not in your filter. A non-zero `totalErrors` with a zero `filteredErrors` means pre-existing errors exist elsewhere that your edits did not introduce. |

---

## What `filteredFiles = 2` Instead of `3` Means

If `filteredFiles` comes back as `2` instead of `3`, one of the three paths passed via `--file` was **not recognized as a model source file** by the checker. The most likely cause is `projects/template/likec4.config.json`: it is a JSON project-configuration file, not a LikeC4 model (`.c4`) file, so the parser does not register it in the model file index and does not count it toward `filteredFiles`. The two `.c4` files are counted; the config file is silently excluded from the file filter result. This is expected behaviour — it does not indicate an error with the config file itself.
