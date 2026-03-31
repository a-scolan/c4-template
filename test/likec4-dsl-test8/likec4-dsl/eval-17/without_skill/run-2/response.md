`backend.api` fails in `ops.c4` because it is **not** a fully qualified name. In LikeC4, files contribute to the same model, but they do **not** share a carried-over lexical scope from another file.

`base.c4` defines this hierarchy:

- `cloud`
- `cloud.backend`
- `cloud.backend.api`

When `ops.c4` contains:

```likec4
backend.api -> cloud.db
```

the resolver reads `backend.api` from the top level of `ops.c4`. At that location, `backend.api` is treated as a **relative** reference, so LikeC4 looks for a top-level `backend` element and then its child `api`. That path does not exist, because `backend` is nested under `cloud`, not at the root.

So the exact reason is:

1. `backend.api` is a relative path.
2. Relative paths are resolved from the current scope of the file/block where they are written.
3. `ops.c4` is not inside the `cloud` scope.
4. Therefore `backend.api` does **not** resolve to `cloud.backend.api` across files.

Imports would not be the right fix here, because the problem is **name resolution**, not file visibility.

Use the element’s **FQN** instead:

```likec4
cloud.backend.api -> cloud.db
```

That is the correct cross-file relationship, assuming `cloud.db` is a real element in the model. If `db` has not been defined under `cloud`, then `cloud.db` must also be created first.