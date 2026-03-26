# Customize C2 View: Keep User on the Left Without Brittle Rank Directives

Based on the `customize-view` skill guidance ("prefer `autoLayout` before rank, favor one obvious anchor"):

```likec4
views 'C2' {
  view containers_c2 {
    include *

    autoLayout LeftRight

    include user with { rank source }
  }
}
```

**Key principle applied:**  
The skill says: *"Start with `autoLayout` alone. Add `rank` only if the preview is still hard to read."*  
*"Favor one obvious anchor at a time."*

- `autoLayout LeftRight` sets the axis.
- `rank source` on `user` is the single, obvious anchor — the user is clearly the initiating element.
- Nothing else is rank-constrained; the layout engine handles the rest.

**Avoid:** Adding `rank sink` on every output or `rank same` to align siblings — this over-specifies the layout and tends to break as the model evolves.
