Use `Container_Api` as the exact backend API kind.

- Valid exact kind: `Container_Api`
- Lookalike to reject: `Container_API`
- Generic option exists: `Container`

For database relationships in logical modeling, use logical kinds (especially `reads` and `writes`; also `calls/async/uses` are valid).

Do not swap in deployment protocol kinds for logical behavior edges.

Verify by checking:

- `projects/shared/spec-containers.c4` for kinds
- `projects/shared/spec-global.c4` for logical relationships
- `projects/shared/spec-deployment.c4` for deployment-only relationships