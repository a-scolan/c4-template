npx likec4 check --file projects/template/system-model.c4 --file projects/template/system-views.c4 --file projects/template/likec4.config.json
`filteredFiles` tells you how many of the explicitly requested `--file` paths were actually included in this check run.
`filteredErrors` tells you how many errors are attached to that filtered file set only.
`totalErrors` tells you the total errors in the whole analyzed workspace/project context, including files outside the filter.
If `filteredFiles` is `2` instead of `3`, one requested path did not participate in the filtered run (for example due to a typo, a non-matching path, or a file excluded/not recognized by the analyzer for this check).