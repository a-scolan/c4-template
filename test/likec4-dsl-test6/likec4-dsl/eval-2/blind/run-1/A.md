Use:

```bash
npx likec4 export png --view "overview*" --theme dark --output ./images --flat
```

If your workspace has multiple projects (or you are not running from the target project root), pass the project path explicitly, e.g.:

```bash
npx likec4 export png --project ./projects/template --view "overview*" --theme dark --output ./images --flat
```

So yes: project path can be optional when current working directory already resolves the intended project.