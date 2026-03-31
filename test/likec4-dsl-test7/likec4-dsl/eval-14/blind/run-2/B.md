`styles { theme dark }` fails because both parts are in the wrong place for LikeC4 DSL files:

- `styles` is not a valid top-level DSL block in `.c4` model files.
- `theme dark` is not a DSL statement; theme selection is a project config concern.

A minimal valid **DSL-scope styling** alternative is to use a top-level styling statement that is actually allowed in `.c4`:

```likec4
style * {
  color "#9FB3C8"
}
```

If the real intent is a **project-level dark theme**, put it in `likec4.config.json`, e.g.:

```json
{
  "theme": "dark"
}
```