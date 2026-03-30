npx likec4 validate --json --no-layout --file projects/template/system-model.c4 --file projects/template/system-views.c4 --file projects/template/likec4.config.json projects/template

`filteredFiles` tells you how many LikeC4 source files were actually covered by the repeated `--file` filters. `filteredErrors` tells you how many validation errors were found only within that filtered subset. `totalErrors` tells you how many validation errors exist across the entire project model, including files outside the filtered subset.

If `filteredFiles` comes back as `2` instead of `3`, it means only two of the paths you passed were counted as LikeC4 source files for DSL validation, so the config file was not included in that source-file count.