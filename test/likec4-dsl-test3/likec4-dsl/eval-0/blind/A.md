Run this from the repo root:

`npx likec4 validate projects/template/system-model.c4 --format json`

In the JSON output, use:

- The top-level summary validity/error count (project-wide health)
- The per-diagnostic/per-file `path` (or `file`) field

Interpretation:

- **Only your file failed**: all reported errors point to `projects/template/system-model.c4`.
- **Whole project is broken**: any error points to a different file (or a project-level error not tied to that file).