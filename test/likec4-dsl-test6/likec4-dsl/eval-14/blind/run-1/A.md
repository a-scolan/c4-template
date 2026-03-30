`styles { theme dark }` fails because `styles`/`theme` is not a valid top-level DSL form in `.c4` files.

A minimal valid DSL styling alternative is to use an allowed top-level style declaration:

```likec4
global style myStyle {
  color red
}
```

If your intent is a **project-level dark theme**, put that in `likec4.config.json` instead:

```json
{
  "theme": "dark"
}
```