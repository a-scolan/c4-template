In `view backend of cloud.backend { include * }`, `*` expands according to scoped-view wildcard semantics:

- **Base include set:** `*` selects `cloud.backend` itself plus its **direct children** (one level deep — not recursive descendants via `**`), together with all relationships between those elements.

- **Neighboring/derived visibility:** Because `include *` also captures every relationship connected to `cloud.backend` and its direct children, any external element at the other end of one of those relationships (incomers from outside the subtree, outgoers to outside the subtree) can also become visible — pulled in automatically through the matched relationship.

---

Minimal snippet that keeps `include *` and explicitly adds incoming and outgoing relationships around `cloud.backend`:

```likec4
view backend of cloud.backend {
  include *
  include * -> cloud.backend
  include cloud.backend -> *
}
```

- `* -> cloud.backend` — matches all relationships from any element to `cloud.backend` (incoming), and includes the source elements.
- `cloud.backend -> *` — matches all relationships from `cloud.backend` to any element (outgoing), and includes the target elements.
