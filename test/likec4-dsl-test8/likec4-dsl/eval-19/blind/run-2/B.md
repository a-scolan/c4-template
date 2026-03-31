- `*` in a scoped view starts from the scoped element and its **direct children**. So in `view backend of cloud.backend { include * }`, the base include set is `cloud.backend` plus the elements exactly one level below it, not the entire model and not every deeper descendant by default.
- From that scoped base, LikeC4 can still surface adjacent context: elements connected by incoming or outgoing relationships to the visible scoped nodes, plus the corresponding direct or derived relationships that become visible around that scoped content.

```likec4
view backend of cloud.backend {
  include *
  include * -> cloud.backend
  include cloud.backend -> *
}
```