Run the validator from the repo root with the file path as the target and JSON output enabled:

`npx likec4 validate projects/template/system-model.c4 --output json`

What to look at in the JSON:

- `status` — overall result for the validation run.
- `files` — per-file validation results.
- `files["projects/template/system-model.c4"]` — whether your edited file specifically failed.
- `files["projects/template/system-model.c4"].errors` — syntax/semantic errors for only that file.
- `summary.errorCount` — total errors across the whole validation run.

How to tell file-only failure vs project-wide breakage:

- If `files["projects/template/system-model.c4"].errors` is non-empty **and** other entries in `files` have no errors, then only your file failed.
- If `summary.errorCount` is greater than the error count in `files["projects/template/system-model.c4"].errors`, or other `files[...]` entries also contain errors, then the project has broader problems.

This validates syntax and semantics only; it does not check layout drift.