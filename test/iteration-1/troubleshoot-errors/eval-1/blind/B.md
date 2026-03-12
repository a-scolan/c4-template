The breakage comes from **two different conceptual errors**.

1. **`mySystem -> mySystem.api` is the wrong interaction**
   - `mySystem` is the parent system boundary.
   - `mySystem.api` is a child container inside that boundary.
   - In a dynamic view, the interaction should be between actual runtime participants, not a parent boundary calling its own child.
   - So the source should usually be something like `user` or `mySystem.webapp`, not `mySystem`.

2. **`rank same user, mySystem.api` is also invalid in principle**
   - `rank same` only works for elements that share the same parent.
   - `user` is a top-level actor.
   - `mySystem.api` is nested under `mySystem`.
   - They do not live at the same level, so forcing them into the same rank is the wrong layout constraint.

3. **What to fix**
   - Replace `mySystem -> mySystem.api` with the real runtime step you mean, for example:
     - `user -> mySystem.webapp`, or
     - `mySystem.webapp -> mySystem.api`
   - If you use `rank same`, apply it only to siblings, such as `mySystem.webapp` and another `mySystem.*` element.
   - Keep `user` in a separate source rank instead of forcing it into the same rank as an internal container.

So the real cause is not a rendering glitch. It is a **bad interaction model** plus a **misused rank constraint**.