```bash
npx likec4 validate --file projects/template/system-model.c4 --file projects/template/system-views.c4 --file projects/template/likec4.config.json
```

`filteredFiles` is how many of the files you explicitly filtered were actually processed by validation, `filteredErrors` is how many errors were found within that filtered set, and `totalErrors` is how many errors exist across the full validation scope regardless of filtering. If `filteredFiles` is `2` instead of `3`, one of the three `--file` targets did not enter the validated set (for example wrong path, unsupported target type for that command, or a file excluded by config).```
npx likec4 check --file projects/template/system-model.c4 --file projects/template/system-views.c4 --file projects/template/likec4.config.json
```

**What each metric means**

- **`filteredFiles`** — the number of files from your `--file` list that the checker recognised as model source documents and actually loaded. It tells you how many of your edited files are in scope for the filtered error report.

- **`filteredErrors`** — the count of syntax or semantic errors found exclusively inside those `filteredFiles`. Use this to judge whether *your* edits introduced any problems, independently of the rest of the project.

- **`totalErrors`** — the count of all errors across the entire project (every `.c4` file reachable from the config), not just the files you specified. If `totalErrors` is zero, the whole model is clean; if it is greater than `filteredErrors`, errors exist elsewhere in the project that are unrelated to your changes.

**What `filteredFiles = 2` instead of `3` means**

`likec4.config.json` is a JSON configuration file, not a LikeC4 DSL source document. The `check` command counts only recognised model files (`.c4` files) in its `filteredFiles` tally; the config file is processed internally as project metadata but is not itself a source unit that can carry DSL errors. So the checker finds both `.c4` files you listed but does not count the JSON file, yielding `filteredFiles: 2`. This is expected behaviour — it does not indicate a missing file or a path error. If you see `filteredFiles: 1`, that is the signal that one of the two `.c4` paths was not resolved.
