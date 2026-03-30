```
npx likec4 validate --json --no-layout --file projects/template/system-model.c4 --file projects/template/system-views.c4 --file projects/template/likec4.config.json projects/template
```

**What each JSON field means:**

- **`filteredFiles`** — how many of the paths you passed with `--file` were actually matched and processed by the validator. With three `--file` flags you expect `3`.
- **`filteredErrors`** — total error count across only the filtered files. This is the number you care about: if it is `0`, your three edited files are clean.
- **`totalErrors`** — total error count across the entire project (all files). If `filteredErrors` is `0` but `totalErrors` is large, your files are fine and the broken code is elsewhere in the project (not caused by your edits).

**If `filteredFiles` comes back as `2` instead of `3`:**

One of the three `--file` paths did not match any file that the validator tracks as a source file. The most likely cause is that `likec4.config.json` is a project configuration file, not a LikeC4 DSL source file, so the validator may not count it in the filtered set. Verify the path spelling for all three flags; if the config is the culprit, drop it from the `--file` list (it has no DSL syntax to validate).
