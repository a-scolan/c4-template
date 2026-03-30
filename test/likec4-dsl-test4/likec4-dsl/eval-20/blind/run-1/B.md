# Validate Two Specific Files Without Layout Drift Checks

## Command

```bash
likec4 validate --no-layout-drift projects/template/system-model.c4 projects/template/system-views.c4
```

If the CLI does not support positional file arguments directly, use:

```bash
likec4 validate --files projects/template/system-model.c4,projects/template/system-views.c4 --no-layout-drift
```

Or with a glob/include pattern scoped to the template project folder:

```bash
likec4 validate --include "projects/template/system-*.c4" --no-layout-drift
```

## How to Confirm Both Files Were Filtered in JSON Output

Run with JSON output format:

```bash
likec4 validate --no-layout-drift --format json projects/template/system-model.c4 projects/template/system-views.c4
```

In the JSON output, look for a `files` (or `sources`) array at the top level. Each validated file should appear as an entry. For example:

```json
{
  "files": [
    "projects/template/system-model.c4",
    "projects/template/system-views.c4"
  ],
  "errors": [],
  "warnings": []
}
```

To confirm both files were included:

1. Parse the JSON output (e.g., with `jq`):
   ```bash
   likec4 validate --no-layout-drift --format json \
     projects/template/system-model.c4 \
     projects/template/system-views.c4 \
   | jq '.files'
   ```
2. Verify the array contains exactly the two expected paths: `projects/template/system-model.c4` and `projects/template/system-views.c4`.
3. If neither file appears in the JSON `files` array, the filter was not applied correctly — check the CLI flags or file path arguments.
4. Absence of `errors` referencing other project files (e.g., `projects/spec-showcase/`) also confirms the scope was correctly limited.
