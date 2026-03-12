There are two distinct problems here.

1. `system -> system.api` in a dynamic view
   - That is a parent-to-child interaction.
   - In LikeC4 dynamic views, a parent should not "call" its own child. The dynamic flow should show the real participant that performs the action, such as `user -> system.api`.

2. `rank same user, system.api`
   - `rank same` only works for elements that share the same parent context.
   - `user` is an external actor and `system.api` is nested inside `system`, so they are not siblings. That is why the rank constraint is invalid.

Clean fix:
- Replace the parent-child step with the real initiating interaction, for example `user -> system.api`.
- Remove that `rank same` rule, or only use `rank same` for true siblings under the same parent.
- If you want to show the system boundary, keep that in a structural view; the dynamic view should focus on the sequence of real interactions.
