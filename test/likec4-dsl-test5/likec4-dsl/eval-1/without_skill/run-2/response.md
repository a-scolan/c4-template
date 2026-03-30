Minimal `projects/template/likec4.config.json` snippet:

```json
{
  "name": "template",
  "include": [
    "./**/*.c4",
    "../shared/**/*.c4"
  ]
}
```

How file-to-project resolution works with multiple configs:
- Each `likec4.config.json` defines one project root.
- `include`/`exclude` globs are resolved relative to that config file.
- A `.c4` file belongs to a project when it matches that project’s includes (and is not excluded).
- If a file is matched by multiple project configs, it is included in each matching project context.Minimal `projects/template/likec4.config.json` snippet:

```json
{
  "name": "template",
  "include": [
    "./**/*.c4",
    "../shared/**/*.c4"
  ]
}
```

How file-to-project resolution works with multiple configs:
- Each `likec4.config.json` defines one project root.
- `include`/`exclude` globs are resolved relative to that config file.
- A `.c4` file belongs to a project when it matches that project’s includes (and is not excluded).
- If a file is matched by multiple project configs, it is included in each matching project context.