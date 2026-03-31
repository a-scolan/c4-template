# Why `backend.api` is unresolved in `ops.c4`

`backend.api` is **not** a global name. It is only a **relative path**.

In `base.c4`, `backend` is declared **inside** `cloud`:

- `cloud`
	- `backend`
		- `api`

So the full identity of `api` is:

- `cloud.backend.api`

When you write this in another file (`ops.c4`):

- `backend.api -> cloud.db`

LikeC4 resolves `backend.api` from the **current top-level model scope of that file**, not from inside the `cloud` block declared in `base.c4`.

That means it looks for:

- top-level `backend`
	- child `api`

But no top-level `backend` exists, because `backend` is nested under `cloud`. So the reference is unresolved.

This is why the fix is **not** an import statement: the issue is not file inclusion, but **name resolution**. Across files, if you are not already inside the same enclosing element scope, you must reference nested elements by their **FQN** (fully qualified name).

# Correct cross-file relationship

Use the full source name:

`cloud.backend.api -> cloud.db`

So the corrected relationship in `ops.c4` is:

- `cloud.backend.api -> cloud.db`

In short: across files, nested elements are not automatically addressable by short relative names such as `backend.api`; use the full path from the root, i.e. the FQN.
