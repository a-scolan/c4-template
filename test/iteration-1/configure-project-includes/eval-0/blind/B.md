Keep the template config minimal and preserve these fields:

- `$schema`
- `name`
- `title`
- `include`
- `imageAliases`

For `projects/payments/likec4.config.json`, use paths relative to that project folder:

- `include.paths: ["../shared"]`
- `imageAliases: { "@": "../shared/images/" }`

A good starting shape is:

- `$schema`: keep the schema URL from the template
- `name`: change to your project identifier
- `title`: change to your project title
- `include.paths`: keep `../shared`
- `imageAliases`: keep `"@": "../shared/images/"`

Do not switch these to workspace-root or absolute paths. The config should resolve shared specs and images from the project directory, so `../shared` and `../shared/images/` are the safe references to keep imports working.