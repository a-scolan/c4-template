## Minimal config snippet

```json
{
  "extends": ["../shared/spec-*.c4"],
  "include": ["./**/*.c4"]
}
```

Place this in `projects/template/likec4.config.json`.

- `extends` pulls in the shared specification files from `projects/shared/`.
- `include` keeps the project’s own `.c4` files inside `projects/template/`.

## How LikeC4 assigns a `.c4` file to a project

When several `likec4.config.json` files exist in the workspace, LikeC4 resolves a `.c4` file to the **nearest project config by directory ancestry**.

In practice:

- a `.c4` file under `projects/template/` belongs to the project defined by `projects/template/likec4.config.json`
- a `.c4` file under another folder with its own config belongs to that other project
- shared files can still be reused by a project when they are referenced through `extends` or included explicitly

So the project is determined primarily by **where the file lives relative to config files**, not by whichever config happens to be loaded first. Shared specs are reused because the template project config points at them.