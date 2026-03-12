Use `Container_Api`.

- `Container_Api` is the exact declared kind for an API/service in this repository.
- `Container_API` is not declared, so reject it.
- `Container` is valid, but it is only the generic base kind; prefer `Container_Api` when the backend is actually an API.

For logical relationships toward a database, the declared model kinds are:

- `calls`
- `async`
- `reads`
- `writes`
- `uses`

For database access, `reads` and `writes` are usually the most precise choices. Do not invent undeclared model relationships such as `query` or `invokes`.

How to verify it in this repository:

1. Check `projects/shared/spec-containers.c4` for the exact container kind declarations.
2. Check `projects/shared/spec-global.c4` for the logical-model relationship declarations.
3. If MCP is available, `read-project-summary` can confirm the currently loaded taxonomy.
