Minimal `projects/template/likec4.config.json` snippet:

```json
{
  "name": "template",
  "include": ["./*.c4", "../shared/*.c4"]
}
```

Project ownership is resolved from config matching rules in the workspace: a `.c4` file belongs to the project whose config/include scope matches that file; with overlaps, the config rooted closest to the file path is used.