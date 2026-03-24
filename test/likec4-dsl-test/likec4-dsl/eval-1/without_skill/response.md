Minimal `projects/template/likec4.config.json`:

```json
{
  "name": "template",
  "include": {
    "paths": [
      "**/*.c4",
      "../shared/**/*.c4"
    ]
  }
}
```

How LikeC4 assigns project membership when multiple config files exist:
LikeC4 walks up the directory tree from each `.c4` file and assigns that file to the project whose `likec4.config.json` is the **nearest ancestor**. The config whose directory is closest to the file wins. Files referenced via relative `include.paths` (such as `../shared/**/*.c4`) are explicitly claimed by the config that declares the include, even though they live outside that config's own directory subtree. A shared file will therefore belong to whichever project explicitly includes it; if two projects include the same shared file, it is part of both (LikeC4 supports multi-project workspaces and each project builds its own model graph).
