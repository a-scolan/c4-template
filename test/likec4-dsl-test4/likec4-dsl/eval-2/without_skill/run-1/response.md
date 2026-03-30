# LikeC4 CLI: Export filtered views as dark PNGs

To export only views matching `overview*` as dark PNGs into `./images`, flattened, for the current project, run:

```bash
likec4 export png --filter "overview*" --theme dark --output ./images --flat
```

## Parameter breakdown

| Flag | Value | Purpose |
|------|-------|---------|
| `--filter "overview*"` | glob pattern | Restricts export to views whose ID starts with `overview` |
| `--theme dark` | `dark` | Renders diagrams with the dark color theme |
| `--output ./images` | `./images` | Destination directory for the PNG files |
| `--flat` | (flag) | Flattens the output — all PNGs land directly in `./images` rather than mirroring the source directory structure |

## Project path

The project path argument is **optional** when running the command from inside the project directory (i.e., the directory containing `likec4.config.json` or the `.c4` / `.likec4` source files). LikeC4 will auto-discover the project from the current working directory.

If you need to target a project in a different location, append the path explicitly:

```bash
likec4 export png --filter "overview*" --theme dark --output ./images --flat ./path/to/project
```

> **Note:** Flag names (`--filter`, `--flat`, `--theme`) should be verified against your installed LikeC4 version (`likec4 export png --help`), as exact flag names can differ between releases.
