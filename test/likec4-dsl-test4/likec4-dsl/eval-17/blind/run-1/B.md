# Why `backend.api -> cloud.db` Fails Across Files

## Root Cause

In LikeC4, element references in relationships are always resolved relative to the **current file's scope**, not globally. When you write `backend.api -> cloud.db` in `ops.c4`, the parser looks for a top-level element named `backend` in the scope visible to that file. However, `backend` is not a top-level element — it is a **child of `cloud`** (i.e., `cloud.backend`). Its fully-qualified name (FQN) is `cloud.backend`, and the api inside it is `cloud.backend.api`.

There is no implicit "bring all nested elements into scope" across files. Each reference must be resolvable from the root of the model using the full dotted path. Writing `backend.api` is ambiguous and will fail because `backend` does not exist at the top level.

Additionally, `cloud.db` does not appear in the `base.c4` definition you described, so that reference would also be unresolved unless `db` is defined elsewhere as a child of `cloud`.

## Corrected Cross-File Relationship Using FQNs

```c4
// ops.c4
cloud.backend.api -> cloud.db
```

- `cloud.backend.api` — fully-qualified path: `cloud` (system) → `backend` (container) → `api` (service)
- `cloud.db` — fully-qualified path: `cloud` (system) → `db` (whatever element type it is)

Both sides of the relationship use FQNs starting from the model root, which is unambiguous regardless of which file the relationship is declared in.
