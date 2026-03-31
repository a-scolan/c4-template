A minimal `projects/template/likec4.config.json` can point at the shared specs by adding them to `include`:

```json
{
  "name": "template",
  "include": [
    "../shared/*.c4",
    "./*.c4"
  ]
}
```

This keeps the template project small while reusing the `.c4` files from `projects/shared/`.

When multiple `likec4.config.json` files exist in one workspace, LikeC4 assigns each `.c4` file to the project whose config includes that file. In practice:

- each config defines a project root and its own include patterns
- a `.c4` file belongs to the project whose include rules match it
- files matched only by `projects/template/likec4.config.json` are part of the template project
- shared files can be reused by another project only if that project’s config explicitly includes them

So the deciding factor is not just folder location by itself, but whether that project config resolves and includes the `.c4` file in its source set.