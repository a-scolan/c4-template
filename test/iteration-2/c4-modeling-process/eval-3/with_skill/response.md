Do it in this order:

1. **Re-establish the workspace rules first** by using **`understand-project-structure`**. In an unfamiliar LikeC4 workspace, you should confirm the project structure, shared specs, valid kinds, and view organization before editing anything.
2. **Refresh the C1 picture**: make sure the system boundary, actors, and external systems are still clear. Do not jump straight into detailed edits.
3. **Then work on C2**: decide which runtime containers belong in the model and how they interact.
4. For the detailed edits, hand off to the specialized skills:
   - **`create-element`** for adding or adjusting containers
   - **`create-relationship`** for choosing and defining the right interactions
   - **`design-view`** for constructing the C2 view itself
5. Only consider **C3 later**, and only for containers that truly need deeper internal detail.

So the right flow is: **understand the project structure → confirm C1 → design C2 → use the specialized creation/view skills for the detailed work**.