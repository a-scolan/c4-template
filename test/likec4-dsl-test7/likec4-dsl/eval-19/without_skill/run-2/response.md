- With `view backend of cloud.backend { include * }`, the base set is the scoped element context: `cloud.backend` and its **direct children** (and nested descendants inside that scope), not the entire workspace model.
- From that base, visibility can still expand via relationships: edges among included nodes are shown, and with explicit incoming/outgoing include rules you can also surface neighboring external elements plus the corresponding incoming/outgoing links (including implied/derived relations where applicable).

```likec4
view backend of cloud.backend {
  include *
  include _ -> cloud.backend
  include cloud.backend -> _
}
```