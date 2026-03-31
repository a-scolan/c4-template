# Minimal config

```json
{
	"$schema": "https://likec4.dev/schemas/config.json",
	"name": "template",
	"title": "Template",
	"include": {
		"paths": ["../shared"]
	}
}
```

LikeC4 assigns each `.c4` file to the project defined by the **nearest config file in the directory hierarchy** (`likec4.config.json`, `.likec4rc`, etc.). So a file under `projects/template/` belongs to the `projects/template/likec4.config.json` project, while shared files are reused by pointing `include.paths` at `../shared`.
