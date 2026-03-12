Use `Container_Api` if the backend is an API/service. `Container_API` is **not** declared in this workspace, and plain `Container` is only the generic base kind.

For logical-model relationships toward a database, the declared relationship taxonomy is:
- `uses`
- `calls`
- `async`
- `reads`
- `writes`

For a database specifically, `reads` and `writes` are usually the best fit; `uses` is the generic fallback. Do not invent undeclared kinds such as `query` or `invokes`.

How to verify in this workspace:
1. Read `projects/shared/spec-containers.c4` and look for `element Container_Api`.
2. Read `projects/shared/spec-global.c4` and look for the declared model relationships.
3. `projects/shared/SPEC_CHEATSHEET.md` summarizes the same taxonomy in one place.
