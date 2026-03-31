You can point the template project to shared specs with a minimal config like this:

```json
{
  "name": "template",
  "include": {
    "paths": [
      "../shared/**/*.c4",
      "./**/*.c4"
    ]
  }
}
```

How LikeC4 picks the project for a `.c4` file when multiple configs exist:

- Each `likec4.config.json` defines a project root (the folder containing that config).
- LikeC4 resolves files to the **nearest matching project context** based on config location and that project’s include/exclude rules.
- A file is part of a project only if it matches that project’s `include` scope (and is not excluded).
- If several projects could match, the one with the most specific/closest scope to the file path wins (practically: nearest config boundary + matching include patterns).
- So with `projects/template/likec4.config.json`, using `../shared/**/*.c4` explicitly brings shared files into the `template` project.