Command:

npx likec4 validate --json --no-layout --file projects/template/system-model.c4 --file projects/template/system-views.c4 projects/template 2>/dev/null

Explanation of each flag:
- `--json` emits structured JSON to stdout.
- `--no-layout` skips layout drift checks (syntax + semantic only).
- `--file projects/template/system-model.c4` restricts error reporting to that file.
- `--file projects/template/system-views.c4` adds the second file to the filter (the flag can repeat).
- `projects/template` is the project directory (the folder containing `likec4.config.json`).

How to confirm both files were actually filtered in the JSON output:

Inspect the `stats.filteredFiles` field in the JSON output. Because two `--file` arguments were passed, its value must equal 2. If it shows 1 or 0, one of the paths was not matched (wrong relative path, typo, or the file is outside the project directory). Also cross-check `stats.filteredErrors` against `stats.totalErrors`: if `filteredErrors` is 0 while `totalErrors` is high, your two files are clean but other project files have errors — that is expected and not your problem. The selfcheck rule from the skill is: `filteredFiles` must equal the number of `--file` arguments supplied (2 in this case).
