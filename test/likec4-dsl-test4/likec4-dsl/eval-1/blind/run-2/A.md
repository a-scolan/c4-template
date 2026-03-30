# LikeC4 Multi-Project Config with Shared Specs

## Minimal `likec4.config.json` for `projects/template/`

```json
{
  "name": "template",
  "include": [
    ".",
    "../shared"
  ]
}
```

The `include` array lists directories (relative to the config file) whose `.c4` files are parsed as part of this project. By adding `"../shared"`, all spec files under `projects/shared/` are included in the `template` project.

## How LikeC4 assigns a `.c4` file to a project

LikeC4 scans the workspace for `likec4.config.json` files. Each config file defines a project rooted at its own directory. A `.c4` file is assigned to the project whose config explicitly includes it — either because it sits inside the config's directory (default inclusion) or because its path is covered by an entry in `include`.

When a file is covered by multiple configs (e.g. a shared spec included by several projects), LikeC4 loads it independently into each project that references it; it does **not** create a shared singleton. Each project gets its own parsed model.

Key rules:
- **Closest config wins for default inclusion**: without an explicit `include`, a project owns the files in its own directory tree.
- **Explicit `include` paths extend ownership**: paths listed in `include` are resolved relative to the config file.
- **No implicit cross-project sharing**: files under `projects/shared/` belong to the `shared` project by default; to reuse them in `template`, you must explicitly list `"../shared"` in `template`'s config.
