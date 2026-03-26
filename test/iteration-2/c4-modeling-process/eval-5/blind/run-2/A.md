Follow this order without skipping:

1. **Re-sync project constraints first**
   - Because shared specs changed, start with **`understand-project-structure`** to confirm valid kinds, relationships, and project boundaries.

2. **Ensure C1/C2 are still coherent**
   - Verify the target container for the new C3 is correctly positioned and still valid after spec changes.

3. **Add the sensitive C3 view (selective C3 only)**
   - Use **`create-element`** / **`create-relationship`** for component-level detail,
   - then **`design-view`** to build/refine the C3 view.

4. **Document the nominal user scenario**
   - Use **`create-sequence-view`** in `views 'Use Cases'` for temporal flow.

5. **Validate end-to-end**
   - Use **`test-model`** to check references, kinds, relationships, and rendering.

This keeps the top-down process intact: stabilize structure first, then behavior over time.