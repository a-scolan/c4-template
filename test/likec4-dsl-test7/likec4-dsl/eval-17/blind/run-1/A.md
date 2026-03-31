`backend.api` is unresolved because LikeC4 does **not** carry nested element scope across files. In `base.c4`, `backend` is not a top-level symbol; it exists only under the top-level element `cloud`, so its full identity is `cloud.backend`, and `api` is `cloud.backend.api`.

Across files, references must use **FQNs** for nested elements. Only the top-level element name (`cloud`) is directly addressable from another file; `backend.api` by itself is only meaningful inside the lexical scope where `backend` is already in scope.

So in `ops.c4`, this cross-file relationship must use the full source path:

```likec4
model {
  cloud.backend.api -> cloud.db
}
```

If `db` is also nested under `cloud`, this is the correct cross-file relationship because both ends are referenced by their fully qualified names.