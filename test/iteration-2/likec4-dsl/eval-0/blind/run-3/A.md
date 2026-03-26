`npx likec4 validate --project projects/template --files projects/template/system-model.c4 --json --no-layout`

Use `files[].path` + `files[].errors` to see which file failed. If only `projects/template/system-model.c4` has errors, it is file-local. If many files fail (or a top-level/global error section is populated), the project is broadly broken.