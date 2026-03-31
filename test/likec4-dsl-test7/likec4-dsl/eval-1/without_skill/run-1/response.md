A minimal `projects/template/likec4.config.json` can look like this:

```json
{
  "extends": "../shared/spec-global.c4",
  "include": ["./**/*.c4"]
}
```

If you need multiple shared spec files, use an array in `extends`.

When multiple LikeC4 config files exist in a workspace, a `.c4` file is associated with the **nearest config in its directory ancestry** (the config whose folder contains that file). In practice, each config defines a project rooted at its folder, and files are resolved relative to that project root unless explicitly included from elsewhere.
