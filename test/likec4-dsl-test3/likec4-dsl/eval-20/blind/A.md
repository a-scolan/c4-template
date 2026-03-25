Use this single command:

`npx likec4 validate --format json --no-layout-drift --files projects/template/system-model.c4 projects/template/system-views.c4`

To confirm filtering in JSON output, verify that the file-list field (for example `files`, `filteredFiles`, or similarly named array in the result) contains **exactly** these two paths and no others:

- `projects/template/system-model.c4`
- `projects/template/system-views.c4`

A valid confirmation is:

1. Array length is `2`
2. Both exact paths are present
3. No additional file paths appear