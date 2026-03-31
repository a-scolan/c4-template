npx likec4 validate --format json --file projects/template/system-model.c4 --file projects/template/system-views.c4 --file projects/template/likec4.config.json

- `filteredFiles` tells you how many of the paths you passed with `--file` were actually included in the filtered validation scope.
- `filteredErrors` tells you how many validation errors belong to that filtered subset.
- `totalErrors` tells you how many validation errors exist overall in the full validation run, not just in the filtered subset.

If `filteredFiles` comes back as `2` instead of `3`, one of the three `--file` arguments did not resolve to a file that the validator counted in its filtered input set. In this case, the most likely reason is that `projects/template/likec4.config.json` is config, not a model source file, so the validator only counted the two `.c4` files. It can also mean one of the paths was wrong or did not match what the validator considers a valid filtered target.