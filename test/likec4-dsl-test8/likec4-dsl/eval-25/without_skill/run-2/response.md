npx likec4 validate --format json --file projects/template/system-model.c4 --file projects/template/system-views.c4 --file projects/template/likec4.config.json

- `filteredFiles`: how many of the files you explicitly passed with `--file` were actually included in validation.
- `filteredErrors`: how many validation errors belong to that filtered file set.
- `totalErrors`: how many validation errors exist overall in the full validation scope, including errors outside the files you filtered to.

If `filteredFiles` is `2` instead of `3`, one of the three `--file` paths did not end up in the validator's filtered source-file set. In this specific case, the most likely reason is that `projects/template/likec4.config.json` influenced the run but was not counted as a validated model source file, so only the two `.c4` files were counted. More generally, it means one path was not recognized as an in-scope validated input for that filtered result.