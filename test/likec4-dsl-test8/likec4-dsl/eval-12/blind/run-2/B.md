1. **Support status**
   - `include * with { color red }`: **not supported** in a `deployment view`.
   - `global style myTheme`: **not supported** as a `deployment view` construct.

2. **Supported alternative**
   If you want styling inside a `deployment view`, use a **separate local `style` rule** in the view body. That is a supported deployment-view construct, and it is **not** the same thing as `with { ... }` on `include`, and **not** `global style`.

3. **Minimal corrected snippet**

```likec4
deployment view prod {
  include *

  style prod.web {
    color red
  }
}
```

Replace `prod.web` with the actual deployment node or deployed instance you want to style.