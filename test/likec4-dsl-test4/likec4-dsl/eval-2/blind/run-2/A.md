## Answer

```bash
bunx likec4 export png --theme dark --flat -f "overview*" -o ./images [project-dir]
```

**Flag breakdown:**
- `--theme dark` — render in dark theme
- `--flat` — flatten output (all PNGs in a single directory, no subdirectories)
- `-f "overview*"` — glob filter: only export views whose ID matches `overview*`
- `-o ./images` — output directory

**Is `[project-dir]` optional here?**  
Yes. The `project-dir` argument is always optional for `export png`. When omitted, LikeC4 uses the current working directory as the project root. Only specify it if you are running the command from a directory that is not the project root (e.g., running from a monorepo root where the project lives in `projects/template/`).

**Example with explicit project path (if needed):**
```bash
bunx likec4 export png --theme dark --flat -f "overview*" -o ./images projects/template
```

**Reminder:** if the workspace already has `likec4` as a dependency, check `package.json` and pin the version if it is below `1.53.0`:
```bash
bunx likec4@1.53.0 export png --theme dark --flat -f "overview*" -o ./images
```
