Run the validation command, not a layout/snapshot check:

```bash
npx likec4 validate projects/template/system-model.c4 --format json
```

What to inspect in the JSON output:

- The **top-level success/status field** tells you whether the validation run as a whole passed or failed.
- The **per-diagnostic file path field** (the path attached to each error/issue/diagnostic entry) tells you which file actually triggered the failure.

Interpretation:

- If the run failed **and every diagnostic path is `projects/template/system-model.c4`**, then only your edited file failed validation.
- If the run failed **and diagnostics point at other files too**, or the failure is reported at the **project/config level rather than a single file path**, then the project is broken more broadly than just your file.

So in practice, use the top-level overall result together with each diagnostic’s file path to distinguish **single-file failure** from **whole-project failure**.