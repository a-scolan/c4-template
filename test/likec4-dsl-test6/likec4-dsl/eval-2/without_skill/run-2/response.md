Use this command:

```bash
npx likec4 export png --views "overview*" --theme dark --output ./images --flat
```

Notes:

- `--views "overview*"` limits export to views whose ids/names match `overview*`.
- `--theme dark` renders the dark theme.
- `--output ./images` writes into `./images`.
- `--flat` avoids nested per-view folders.

Project path note:

- If you are already in the project context, or the current project can be inferred unambiguously, the project path is optional.
- If you are at the repo root and want to force a specific project in a multi-project workspace, add the project path explicitly, for example:

```bash
npx likec4 export png --project projects/template --views "overview*" --theme dark --output ./images --flat
```