`npx likec4 validate --json --no-layout --file projects/template/system-model.c4 projects/template`

Use these JSON fields:

- `filteredFiles`: should be `1` here, confirming the `--file` filter matched only `projects/template/system-model.c4`.
- `filteredErrors`: errors in the filtered file only. If this is `> 0`, your edited file failed.
- `totalErrors`: errors across the whole project. If `filteredErrors` is `0` but `totalErrors` is high, your file is clean and something else in the project is broken.

`valid` is the overall project result, but `filteredErrors` vs `totalErrors` is what tells you whether the problem is only your file or the wider project.