To export only views matching `overview*` as dark PNGs into `./images`, flattened, for the current project, run:

```bash
likec4 export png --theme dark --output ./images --flat --filter "overview*"
```

**Flags explained:**

| Flag | Purpose |
|------|---------|
| `png` | Export format |
| `--theme dark` | Use dark color theme |
| `--output ./images` | Destination directory |
| `--flat` | Flatten output (no subdirectories per view) |
| `--filter "overview*"` | Glob pattern to select only views whose ID starts with `overview` |

**Project path:** The project path argument is optional when running from the project root directory (where `likec4.config.json` is located). If you need to target a specific project folder, append it as a positional argument:

```bash
likec4 export png --theme dark --output ./images --flat --filter "overview*" ./path/to/project
```

> **Note:** The exact flag names (`--filter`, `--flat`, `--theme`) should be verified against your installed LikeC4 CLI version (`likec4 export png --help`), as CLI flags can vary between versions. The `--filter` flag in particular may accept glob patterns or regex depending on the version.
