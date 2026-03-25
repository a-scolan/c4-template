`backend.api` fails in `ops.c4` because LikeC4 references are resolved by lexical scope, and across files you don’t automatically inherit the nested scope from where an element was originally declared. In `base.c4`, `backend` exists only as `cloud.backend` (nested under `cloud`), so `backend.api` is not a globally resolvable name in another file.

For cross-file references, use fully qualified names (FQNs):

```likec4
model {
  cloud.backend.api -> cloud.db
}
```

That works because both endpoints are resolved from the project-global hierarchy using their full dot path.