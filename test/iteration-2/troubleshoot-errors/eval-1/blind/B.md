The break is caused by **two different conceptual problems**.

1. **`system -> system.api` is the wrong interaction shape for a dynamic view.** A dynamic view shows time-ordered interactions between participants. It should **not** model a parent calling its own child. `system.api` is contained inside `system`, so `system -> system.api` is trying to turn containment into an interaction.

2. **`rank same user, system.api` is also invalid in this shape.** `rank same` only works for elements that share the **same parent context**. A top-level actor like `user` and a nested element like `system.api` are not siblings, so that constraint is not valid.

The clean fix is:

- Remove the parent→child step.
- Rewrite the scenario using the **real participating peers**.
  - If the user talks directly to the API, use `user -> system.api`.
  - If the web app calls the API, use `user -> system.webapp` and then `system.webapp -> system.api`.
- Remove `rank same user, system.api`, or only use `rank same` for siblings such as `system.webapp, system.api`.

So the real cause is **not a vague layout bug**. It is:
- a **conceptual dynamic-view violation** (`parent -> own child`), and
- a **misused rank constraint** (`rank same` across different parent contexts).