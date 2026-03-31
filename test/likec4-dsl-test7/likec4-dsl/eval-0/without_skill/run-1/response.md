Run from repo root:

`npx likec4 check projects/template/system-model.c4 --format json`

In the JSON output, use:

- `diagnostics` (or `issues`) entries’ file path field (commonly `file`, `path`, or `source.path`) to see **which files** failed.
- Top-level summary counters (commonly `errorCount` / `errors`, and `filesWithErrors`) to see **scope**.

Interpretation:

- **Only your file failed**: every error points to `projects/template/system-model.c4` and `filesWithErrors` contains only that file.
- **Project-wide breakage**: errors also point to other files (or summary shows multiple files/config/project-level failures).