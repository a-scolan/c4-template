Follow this order without skipping steps:

1. Start with **`understand-project-structure`**.
   - Revalidate the active project in `projects/template`, the shared specs, valid kinds, relationships, and view organization after the shared-spec changes.
2. Reconfirm the existing **C1 → C2** foundation.
   - Make sure the system boundary and container structure still support the detail you want to add.
3. Only then add the **C3** view.
   - Do it only because this is a sensitive container that deserves deeper internal detail.
4. Hand off the detailed structural work to:
   - **`create-element`** for component declarations
   - **`create-relationship`** for typed internal relationships
   - **`design-view`** for the static C3 view
5. Document the nominal user scenario separately with **`create-sequence-view`** in **`views 'Use Cases'`**.
6. Run **`test-model`** after the structure and views are complete.

So the sequence is: **revalidate project context and shared specs → confirm C1/C2 → add targeted C3 detail → add the user scenario as a dynamic view → validate**.