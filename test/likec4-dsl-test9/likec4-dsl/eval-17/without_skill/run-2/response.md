In LikeC4, element references are resolved by **identifier scope**, not by “same project file set means short names are globally visible”.

`base.c4` defines a nested hierarchy:

- `cloud`
- `cloud.backend`
- `cloud.backend.api`

So `api` is **not** a top-level element. It exists only as the child of `cloud.backend`.

That is why this reference in `ops.c4` fails:

- `backend.api -> cloud.db`

## Why it fails exactly

Across files, LikeC4 still resolves references against the model’s element ids. A nested element must be referenced by its **fully qualified name** unless you are inside a scope where the shorter name is valid.

In `ops.c4`, `backend.api` is interpreted as:

- top-level `backend`
- child `api` under that top-level `backend`

But no top-level `backend` exists. The actual element id is:

- `cloud.backend.api`

So the reference is unresolved because `backend.api` is missing its root parent `cloud`.

## Correct cross-file relationship

Use FQNs on both sides:

`cloud.backend.api -> cloud.db`

If `db` is also nested under `cloud`, that is the correct cross-file relationship form. The key rule is: **across files, do not rely on shortened nested ids; use the full element path from the root element.**
