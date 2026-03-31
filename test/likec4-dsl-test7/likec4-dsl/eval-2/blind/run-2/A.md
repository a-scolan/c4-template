Run:

```bash
likec4 export --views "overview*" --format png --theme dark --output ./images --flatten
```

If you want to be explicit about project path, add it (for current project):

```bash
likec4 export . --views "overview*" --format png --theme dark --output ./images --flatten
```

The project path is optional when you run the command from the project root.