Use:

`npx likec4 validate --json --no-layout-drift projects/template/system-model.c4 projects/template/system-views.c4`

To confirm the filter was applied, inspect the JSON and verify that every reported file/path entry belongs to exactly those two paths and that no other source files appear anywhere in the diagnostics payload; if the JSON includes an explicit files/documents list, it should contain only `projects/template/system-model.c4` and `projects/template/system-views.c4`.