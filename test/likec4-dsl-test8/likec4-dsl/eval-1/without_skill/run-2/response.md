A minimal `projects/template/likec4.config.json` can look like this:

```json
{
  "name": "template",
  "include": {
    "paths": [
      "./**/*.c4",
      "../shared/**/*.c4"
    ]
  }
}
```

Notes:

- Paths are resolved relative to the config file, so `../shared/**/*.c4` pulls in files from `projects/shared/`.
- `./**/*.c4` keeps the local project files in `projects/template/` included too.

When multiple `likec4.config.json` files exist in one workspace, LikeC4 treats each config file as a separate project root.

In practice:

- A `.c4` file is normally associated with the project whose config is the closest enclosing config for that file.
- If a project config explicitly includes files outside its own folder, those files are also loaded as sources for that project.
- That is how a `shared` folder can be reused: it does not need its own project config if other projects include it explicitly.
- If the same shared files are included by more than one project, they can be reused by each included project rather than being automatically assigned to only one sibling config.

So the mental model is: **config location defines project boundaries by default, and `include.paths` lets a project opt into extra `.c4` files such as shared specs.**