Run the validation command from the repo root as:

npx likec4 check --config projects/template/likec4.config.json --files projects/template/system-model.c4 --format json

Why this one: `check` gives syntax + semantic validation only; it does not do diagram/layout drift checks.

In the JSON output, use these fields to tell whether only your file failed or the whole project is broken:
- `ok`: overall pass/fail for the check run.
- `files["projects/template/system-model.c4"]`: the per-file result for the file you edited.
- `files`: inspect whether any other file keys besides `projects/template/system-model.c4` also contain errors.
- `errors`: project-level/global errors; if this is non-empty, the project is broken beyond just your file.

Interpretation:
- Only your file failed: `ok` is `false`, `files["projects/template/system-model.c4"]` has errors, no other `files[...]` entries have errors, and `errors` is empty.
- Whole project broken: `errors` is non-empty, or multiple entries in `files` have errors, not just `projects/template/system-model.c4`.
