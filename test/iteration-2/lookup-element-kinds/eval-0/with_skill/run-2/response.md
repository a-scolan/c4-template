Use `Container_Api` for a backend API container in this workspace.

- ✅ Exact declared kind: `Container_Api`
- ❌ Reject lookalike: `Container_API`
- ✅ Generic fallback exists: `Container` (less specific)

For database interactions in the logical model, valid relationship kinds are from the model taxonomy:

- `reads`
- `writes`
- also valid generally: `calls`, `async`, `uses`

How to verify in the active workspace:

1. Confirm exact kind spellings in `projects/shared/spec-containers.c4`.
2. Confirm logical relationships in `projects/shared/spec-global.c4`.
3. Keep deployment relationships (`https`, `tcp`, `sql`, etc.) in deployment modeling only.

Avoid guessing by English label; use exact declared identifiers only.