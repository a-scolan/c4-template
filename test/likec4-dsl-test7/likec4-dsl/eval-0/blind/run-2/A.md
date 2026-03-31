Run this from the repo root:

`npx likec4 check --json --no-layout --files projects/template/system-model.c4`

Use these JSON parts to tell scope of failure:

- Top-level overall status (`ok` / `success` depending on CLI version): whether the check as a whole failed.
- Per-file diagnostics (`files` entries and/or `diagnostics[*].file`): which file(s) failed.
- Error counters (`summary.errors` or equivalent): total project error count.

Interpretation:
- **Only your file failed**: overall failed, and the only failing file path is `projects/template/system-model.c4`.
- **Whole project broken**: failing file list includes additional paths beyond `projects/template/system-model.c4` (or global errors not tied only to that file).