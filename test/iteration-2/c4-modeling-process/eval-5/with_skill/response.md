Follow this sequence without skipping steps:

1. **Revalidate the active project first** because this is a multi-project workspace and the shared specs have changed. Start with **`understand-project-structure`** so you confirm the active project, shared definitions, valid kinds, and current view organization.
2. **Check the existing structural baseline** before adding detail: make sure the C1 boundary and C2 container model still make sense after the shared-spec changes.
3. **Only then add the C3 view**, and only because it is justified by the need for sensitive internal detail. Keep the progression **C1 → C2 → C3** rather than jumping straight into components as if the earlier levels no longer matter.
4. Use specialized skills for the C3 work:
   - **`create-element`** for component declarations or adjustments
   - **`create-relationship`** for the internal interactions
   - **`design-view`** for the actual C3 static view
5. After the structural work is stable, document the nominal user scenario with **`create-sequence-view`** in **`views 'Use Cases'`**.
6. Finish with **`test-model`** to verify that the updated structure and views are coherent and render correctly.

So the order is: **revalidate project/shared specs → confirm C1/C2 baseline → add the selective C3 view → document the user scenario as a dynamic view → run final validation**.