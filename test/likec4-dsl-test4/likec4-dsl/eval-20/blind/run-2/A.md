# Validate Two Specific Files Without Layout Drift Checks

## Command

```bash
likec4 check projects/template/system-model.c4 projects/template/system-views.c4 --no-layout --output json
```

If the CLI does not support positional file arguments, use the project directory with a filter flag (exact flag names depend on the CLI version):

```bash
likec4 check --files projects/template/system-model.c4,projects/template/system-views.c4 --no-layout --output json
```

Or, if the tool validates by project and you want to skip layout checks only:

```bash
likec4 validate --no-layout-checks --format json projects/template/system-model.c4 projects/template/system-views.c4
```

## How to Confirm Both Files Were Filtered in JSON Output

In the JSON output, look for a top-level `files` (or `sources` / `validatedFiles`) array. Each entry should list the file path that was validated. For example:

```json
{
  "validatedFiles": [
    "projects/template/system-model.c4",
    "projects/template/system-views.c4"
  ],
  "errors": [],
  "warnings": []
}
```

**Confirmation steps:**

1. Check that the `validatedFiles` (or equivalent) array contains **exactly two entries**: `projects/template/system-model.c4` and `projects/template/system-views.c4`.
2. Verify no other `.c4` files appear in that array — if additional files are listed, the filter was not applied correctly.
3. Confirm there is no `layoutDrift` or `layout` key in the output (or that it is `null`/absent), proving layout drift checks were skipped.
4. If the JSON has a `checkedCount` or `totalFiles` field, it should equal `2`.

## Notes

- `--no-layout` / `--no-layout-checks` suppresses layout drift validation so only structural/semantic errors are reported.
- If the CLI validates an entire project by default, passing explicit file paths scopes validation to only those files.
- Always check the exact flag names with `likec4 --help` or `likec4 check --help` for your installed version, as flag names may vary between releases.
