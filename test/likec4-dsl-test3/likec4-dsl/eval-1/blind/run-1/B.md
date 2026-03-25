Use this minimal `projects/template/likec4.config.json`:

```json
{
  "name": "template",
  "title": "Template",
  "extends": "../../projects/shared/spec-*.c4",
  "include": {
    "paths": ["./**/*.c4"]
  }
}
```

How LikeC4 decides project ownership when multiple configs exist:

- Each `likec4.config.json` defines a separate project scope (rooted at that config file’s folder).
- A `.c4` file belongs to a project if it is discovered by that project’s source rules (`include` / `exclude`, plus any inherited/extended sources).
- With multiple configs in one workspace, ownership is not “global first match”; it is evaluated per project configuration.
- So the same physical `.c4` file can be reused by another project only when that project explicitly references it (for example via `extends` or include paths pointing to it).
- In your case, `projects/template` remains its own project, while shared specs under `projects/shared/` are reused because the template config explicitly extends them.