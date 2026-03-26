`npx likec4 validate --project projects/template --files projects/template/system-model.c4 --files projects/template/system-views.c4 --json --no-layout`

Confirm filtering in JSON by checking:
1. `files[].path` contains exactly those two file paths.
2. The filtered/selected files count field (if present) equals `2`.
3. No diagnostics appear for paths outside those two files.