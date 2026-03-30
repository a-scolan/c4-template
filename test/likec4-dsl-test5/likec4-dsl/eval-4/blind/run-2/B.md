(1) This styling belongs directly in the target **view definition** (view-local styles), not in the model/specification.

(2) Minimal snippet:

```likec4
view backend_focus of cloud {
  include *

  style * {
    color muted
  }

  style cloud.backend.* {
    color primary
  }
}
```# Answer

## Part 1 — Where the styling belongs

This styling belongs inside the **view definition itself** (view-local `style` rules), not in the model elements or the specification.

## Part 2 — Minimal view snippet

```likec4
view backend_highlight {
  include *

  style * {
    color muted
  }

  style cloud.backend.* {
    color primary
  }
}
```

The first `style *` rule mutes every element included by `include *`. The second `style cloud.backend.*` rule then overrides that for all elements whose fully-qualified name matches `cloud.backend.*`, restoring them to the default (or any explicit) color so they stand out against the muted background.
