Use:

`npx likec4 export --format png --theme dark --views "overview*" --output ./images --flatten`

Project path note: in this context it is optional if your current working directory is already the target project root; otherwise pass the project path/selector explicitly (for example with the CLI’s project option).# LikeC4 CLI Export Command

## Command

```sh
likec4 export png --output ./images --theme dark --filter "overview*" --flat
```

## Explanation of flags

| Flag | Value | Purpose |
|---|---|---|
| `export png` | — | Export views as PNG files |
| `--output ./images` | `./images` | Destination directory for generated PNGs |
| `--theme dark` | `dark` | Render with the dark colour theme |
| `--filter "overview*"` | glob pattern | Include only views whose ID matches `overview*` |
| `--flat` | — | Write all PNGs directly into the output directory (no sub-folder hierarchy) |

## Project path argument

The `[path]` positional argument (pointing to the project folder or `likec4.config.json`) is **optional**.  
When the command is run from the project root (the directory that contains `likec4.config.json`), it can be omitted entirely, as shown above.

If you need to target a project that is not the current working directory, append the path explicitly:

```sh
likec4 export png ./projects/template --output ./images --theme dark --filter "overview*" --flat
```
