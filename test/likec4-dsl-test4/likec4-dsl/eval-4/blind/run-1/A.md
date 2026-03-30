(1) This styling belongs in the **view definition** itself (i.e., inside the `view` block in a `.c4` views file), not in the model elements or the `specification` block.

(2) Minimal view snippet:

```likec4
view highlighted_backend {
  include *

  style * {
    color muted
  }

  style cloud.backend.* {
    color primary
  }
}
```

`style *` mutes all elements first, then `style cloud.backend.*` overrides with a visible color, so only the backend components stand out.
