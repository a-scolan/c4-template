Use `Container_Api` for a backend API container in this workspace.

- ✅ Exact declared kind: `Container_Api`
- ❌ Reject lookalike: `Container_API`
- ✅ Generic fallback exists: `Container` (less specific)

For database interactions in the logical model, valid relationship kinds are from the model taxonomy:

- `reads`
- `writes`
- also valid generally: `calls`, `async`, `uses`

Typical database semantics should be `reads`/`writes`, not protocol-level deployment kinds.

How to verify safely in the active workspace:

1. Check the project’s declared kinds/relationships.
2. Confirm exact spelling in `projects/shared/spec-containers.c4` (`Container_Api`, `Container_Database`).
3. Confirm logical relationships in `projects/shared/spec-global.c4` (`calls`, `async`, `reads`, `writes`, `uses`).
4. Keep deployment relationships separate (`https`, `tcp`, `sql`, etc. in `spec-deployment.c4`).

Rule of thumb: in logical model edges, use behavior (`calls`), put protocol in technology; in deployment edges, use transport/protocol kinds.