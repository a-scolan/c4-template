Approach it in this order:

1. Start with **`understand-project-structure`**.
   - Re-establish the valid project structure, shared specs, allowed kinds, relationship types, and view organization before editing anything.
2. Reconfirm the **C1** framing.
   - Make sure the system boundary, actors, and external dependencies are still correct.
3. Then design the **C2** view.
   - Define or refine the runtime containers and the main interactions between them.
4. Hand off the detailed work to specialized skills:
   - **`create-element`** for container declarations
   - **`create-relationship`** for typed relationships
   - **`design-view`** for the static C2 view itself
5. Only consider **C3** later if a container truly needs deeper internal detail.
6. Finish with **`test-model`** to validate the result.

So the flow is: **reload project context → confirm C1 → build C2 → delegate detailed edits to the right skills**.