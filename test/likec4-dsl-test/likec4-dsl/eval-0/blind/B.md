Run from the repo root:

```bash
npx likec4 validate --json --no-layout --file projects/template/system-model.c4 projects/template 2>/dev/null
```

`--no-layout` skips layout drift and runs only syntax + semantic validation. `--file` restricts error reporting to the specified file.

Key JSON fields in the output:
- `filteredFiles`: should be 1 — self-check that your file was found and evaluated.
- `filteredErrors`: number of errors in your file. If 0, your file is clean.
- `totalErrors`: total errors across the whole project. If `filteredErrors` is 0 but `totalErrors` is high, the rest of the project is broken — not your file's problem.
- `valid`: overall project validity; `false` whenever any error exists anywhere in the project.

Diagnosis rule: `filteredErrors == 0 && totalErrors > 0` → only your file is clean; `filteredErrors > 0` → your file has issues.
