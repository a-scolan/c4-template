```
npx likec4 export png --theme dark --output ./images --views "overview*" --flat
```

- `--theme dark` — renders with the dark colour scheme.
- `--output ./images` — destination directory.
- `--views "overview*"` (or `--filter "overview*"` depending on CLI version) — glob filter applied against view IDs; only views whose ID starts with `overview` are exported.
- `--flat` — writes all PNG files directly into `./images` with no subdirectory per view.
