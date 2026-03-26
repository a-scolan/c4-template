Invalid. LikeC4 does not allow relationships between parent and child elements.

Minimal corrected pattern:

```likec4
model {
  cloud = system "Cloud" {
    backend = container "Backend"
    db = container "Database"

    backend -> db "reads/writes"
  }
}
```