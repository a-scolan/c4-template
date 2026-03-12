Use `Container_Api`.

- `Container_Api` is the exact declared kind in `projects/shared/spec-containers.c4`.
- `Container_API` is not declared there, so it is not a valid repository kind.
- `Container` is valid, but it is the generic fallback. If the backend is an API/service, `Container_Api` is the precise match.

For logical model relationships, the declared kinds are in `projects/shared/spec-global.c4`: `uses`, `calls`, `async`, `reads`, and `writes`.

Toward a database, the repository examples use `reads` and `writes` rather than inventing a separate verb. See:

- `projects/template/system-model.c4`
- `projects/spec-showcase/containers.c4`

So the safe answer is:

- backend kind: `Container_Api`
- database interactions in the model: `reads` and `writes`
- other valid logical kinds in this taxonomy: `uses`, `calls`, `async`

Do not use undeclared names such as `Container_API`, `query`, or `invokes`.