npx likec4 validate --file projects/template/system-model.c4 --file projects/template/system-views.c4 --file projects/template/likec4.config.json

This is a validation-only command, so it checks syntax and semantics without rewriting layouts.

- `filteredFiles`: how many of the `--file` paths were actually included in the filtered validation set.
- `filteredErrors`: how many validation errors belong to that filtered set of files.
- `totalErrors`: how many validation errors exist in the whole validation run overall, including errors outside the files you filtered to.

If `filteredFiles` comes back as `2` instead of `3`, one of the three paths did not make it into the filtered set. That usually means one path did not resolve as expected, was not considered a valid input for the validator, or was collapsed/ignored during filtering. In practice, check the repo-root-relative path spelling first, and then confirm whether `projects/template/likec4.config.json` is counted by the validator the same way as the two `.c4` files.