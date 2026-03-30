## Exact CLI Command

```bash
bunx likec4 export png --theme dark --flat -f "overview*" -o ./images
```

**Project path is optional here.** When omitted, LikeC4 uses the current working directory as the project root. If you need to target a different project directory (e.g. `projects/template`), append it as a positional argument:

```bash
bunx likec4 export png --theme dark --flat -f "overview*" -o ./images projects/template
```

## Flag Breakdown

| Flag | Purpose |
|---|---|
| `--theme dark` | Render all exported PNGs with the dark theme |
| `--flat` | Flatten output — all PNG files go directly into `./images/` (no subdirectories) |
| `-f "overview*"` | Filter: export only views whose ID matches the glob `overview*` (alias: `--filter`) |
| `-o ./images` | Output directory (alias: `--outdir`) |

## Notes

- Use your workspace's package manager instead of `bunx` if available (`pnpx`, `npx`). If `likec4` is already a project dependency, check that its version is ≥ 1.53.0 and pin it if needed: `bunx likec4@1.53.0 export png ...`.
- `--out-dir` is **not** a valid flag — use `-o` or `--outdir`.
- The export command requires Playwright for PNG rendering.
