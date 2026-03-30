(1) This styling belongs in the **view definition** (view-local style rules), not in the model or specification.

(2) Minimal snippet:

```c4
view backend_focus of cloud {
  include *

  style * {
    color muted
  }

  style cloud.backend.* {
    color primary
  }
}
```# Eval-4 Response

## Part 1 — Where the styling belongs

This styling belongs inside the **view definition block** (as inline view-level style rules), not in the model elements nor in the specification.

## Part 2 — Minimal view snippet

```likec4
view highlightBackend {
  include *

  style * {
    color muted
  }

  style cloud.backend.* {
    color primary
  }
}
```
