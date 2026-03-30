# Eval 14 — Response

## Why `styles { theme dark }` fails

`styles` is **not a valid top-level statement** in the LikeC4 DSL. The only allowed top-level statements are:

```
import | specification | model | deployment | views | global
```

There is no `styles { ... }` block and no `theme` keyword in the DSL grammar. The parser will reject this file immediately with an unknown top-level statement error.

---

## (1) Minimal valid `.c4` alternative — styling inside DSL scope

The correct DSL mechanism for reusable theme-like styling is a **global style group** defined in `global { ... }` and applied per view with `global style`:

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

If the intent is to apply the style to every view in a block without repeating `global style`, use a **local style rule** outside any individual `view {}` inside the `views {}` block:

```likec4
views {
  style * { color muted }

  view index {
    include *
  }
}
```

Both use only valid top-level DSL statements (`global` and `views` respectively). There is no `theme dark` toggle at the DSL level — color and appearance overrides are the available mechanism.

---

## (2) Minimal `likec4.config.json` for project-level theme customization

Project-level color theming belongs in the config file under the `styles.theme.colors` key:

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
    }
  }
}
```

This is the only supported mechanism for project-level theme customization. There is no `theme: "dark"` preset in the config schema; dark-style palettes must be expressed as explicit color values under `styles.theme.colors`.
