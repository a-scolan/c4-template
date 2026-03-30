```
npx likec4 validate --json --no-layout --file projects/template/system-model.c4 --file projects/template/system-views.c4 --file projects/template/likec4.config.json projects/template
```

- **`filteredFiles`**: the number of `--file` paths that the validator matched against actually-parsed LikeC4 source files. Expected value here is `3` (or `2` — see below).
- **`filteredErrors`**: the count of syntax/semantic errors found specifically in those filtered files. A value of `0` means all three edited files are clean.
- **`totalErrors`**: the total error count across the entire project. If `filteredErrors` is `0` but `totalErrors` is non-zero, your files are fine — the errors live elsewhere in the project and are pre-existing (not your problem).

**If `filteredFiles` comes back as `2` instead of `3`:** `likec4.config.json` is a JSON config file, not a `.c4` source file. The validator parses only LikeC4 DSL files (`.c4`/`.likec4`); it does not track config files as filterable source units. Passing it via `--file` is silently ignored for counting purposes. Only `system-model.c4` and `system-views.c4` matched as parseable files, hence `filteredFiles: 2`. To validate all three files you edited, pass only the two `.c4` files via `--file` and verify the project directory points to the right config location — the config is loaded automatically from `projects/template/`.
