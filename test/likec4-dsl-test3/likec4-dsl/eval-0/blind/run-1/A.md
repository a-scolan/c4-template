From the repo root, run:

`npx likec4 validate projects/template/system-model.c4 --format json`

In the JSON output, use these fields:

- Top-level success/summary field (typically `ok` or equivalent) → overall pass/fail status.
- Diagnostics/issues array (typically `issues`/`errors`) with each item’s file path (`path`/`source.path`/`location.path`) → which file failed.

How to decide:

- **Only your file failed**: overall failed, and every reported issue path is `projects/template/system-model.c4`.
- **Whole project is broken**: issues include paths from other files (or multiple distinct file paths), not just `projects/template/system-model.c4`.