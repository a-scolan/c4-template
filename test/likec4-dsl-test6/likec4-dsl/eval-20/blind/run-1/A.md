`npx likec4 validate --json --no-layout --file projects/template/system-model.c4 --file projects/template/system-views.c4 projects/template`

To confirm both files were actually filtered, check the JSON `stats.filteredFiles` value is `2`; `filteredErrors` then counts only errors from those two files, while `totalErrors` is for the whole project.