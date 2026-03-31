`backend.api` fails because LikeC4 merges `model {}` blocks across files, but **name resolution does not inherit lexical/container scope across files**.

In `base.c4`, `api` is not a top-level symbol. It is nested under `cloud.backend`, so its fully qualified name is:

- `cloud.backend.api`

When `ops.c4` says:

```likec4
backend.api -> cloud.db
```

LikeC4 tries to resolve `backend.api` from `ops.c4`'s own scope. There is no top-level `backend` element there, so `backend.api` is unresolved. This is why imports are not the fix here: the issue is not file inclusion, but that **cross-file references to nested elements must use full FQNs**.

The corrected cross-file relationship is:

```likec4
cloud.backend.api -> cloud.db
```

That is valid **only if** the database element is actually defined with FQN `cloud.db`. If the database is nested somewhere else, use its real full FQN as well.