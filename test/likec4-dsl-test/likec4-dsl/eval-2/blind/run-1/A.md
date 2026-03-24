```bash
npx likec4 export png --theme dark --flat -f "overview*" -o ./images projects/template
```

- `--theme dark`: dark background PNGs
- `--flat`: all files output to the same `./images` directory (no subdirectories)
- `-f "overview*"`: glob filter — only views whose ID matches `overview*`
- `-o ./images`: output directory
- `projects/template`: path to the project
