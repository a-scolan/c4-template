```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "template",
  "include": {
    "paths": ["../shared"]
  }
}
```

When multiple LikeC4 config files exist in the workspace, each config defines a separate project, and a `.c4` file belongs to the project of the **nearest config file in its directory hierarchy**.

So in this case:

- `projects/template/*.c4` belongs to the project defined by `projects/template/likec4.config.json`.
- A `.c4` file under some other folder with its own `likec4.config.*` belongs to that other project instead.
- `include.paths` is how the `template` project reuses files from `projects/shared/`; it tells LikeC4 to load those shared `.c4` files into the `template` project as shared input.