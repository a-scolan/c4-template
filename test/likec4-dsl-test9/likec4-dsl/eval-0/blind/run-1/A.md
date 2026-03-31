# Answer

Run this from the repo root:

`npx likec4 validate --config projects/template/likec4.config.json projects/template/system-model.c4 --json`

That uses the **validate** command, so you get syntax + semantic/model validation only, without any layout-drift concerns.

To tell whether **only that file** failed or whether the **project is broken more broadly**, inspect the JSON diagnostics rather than just the top-level pass/fail flag:

- `diagnostics[].location.path` — which file each diagnostic belongs to
- `diagnostics[].severity` — treat `"error"` entries as failures
- top-level `ok` / overall status — tells you whether the validation run failed at all, but **not** whether the failure is isolated to one file

Interpret it like this:

- **Only `projects/template/system-model.c4` failed**: every diagnostic with `severity: "error"` has `location.path: "projects/template/system-model.c4"`
- **The whole project is broken**: you also see `severity: "error"` diagnostics whose `location.path` points at other files

So the key scope signal is the per-diagnostic file path field, not the top-level boolean alone.
