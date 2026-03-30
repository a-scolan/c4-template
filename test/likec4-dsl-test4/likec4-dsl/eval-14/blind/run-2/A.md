# Why the snippet fails

`styles` is not a valid top-level statement in LikeC4 DSL.  
The only allowed top-level blocks are: `import`, `specification`, `model`, `deployment`, `views`, and `global`.  
The parser will reject any file whose root-level block is named anything else, including `styles`.

---

## (1) Minimal valid `.c4` alternative — DSL-scope styling

Use `global { styleGroup ... }` (a valid top-level block) to define reusable style rules, then apply them in views with `global style`:

```likec4
global {
  styleGroup darkTheme {
    style * { color muted }
  }
}

views {
  view index {
    include *
    global style darkTheme
  }
}
```

Alternatively, a local style rule placed inside `views { }` but outside any individual view applies to **all** views in that block without needing a named group:

```likec4
views {
  style * { color muted }

  view index {
    include *
  }
}
```

Both forms use only the allowed top-level keywords (`global`, `views`).

---

## (2) Minimal `likec4.config.json` for a project-level dark theme

Project-level theme customization lives in the `styles.theme.colors` and `styles.defaults` keys of the config file. There is no boolean `theme: "dark"` switch; instead you override the named color tokens:

```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "my-project",
  "styles": {
    "theme": {
      "colors": {
        "primary": "#BB86FC",
        "secondary": "#03DAC6"
      }
    },
    "defaults": {
      "border": "solid"
    }
  }
}
```

This applies the color overrides to **every** diagram generated for the project, without touching any `.c4` file.
