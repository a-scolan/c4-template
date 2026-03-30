npx likec4 validate --json --no-layout --file projects/template/system-model.c4 --file projects/template/system-views.c4 projects/template

In the JSON `stats`, confirm `filteredFiles` is `2` (both `--file` filters were applied). Then use `filteredErrors` to see errors only from those two files; `totalErrors` is for the whole project and can be higher due to unrelated files.
Error: Unable to read eval prompt in this benchmark mode due read-scope restrictions (with_skill_targeted), so no prompt-specific answer could be generated.