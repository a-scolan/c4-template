This happens because LikeC4 resolves references in a single merged model namespace, but unqualified names are still resolved from the current scope; in `ops.c4` at top level, `backend.api` means “top-level `backend` with child `api`”, which does not exist.

Use fully qualified names from the root element path:

```likec4
cloud.backend.api -> cloud.db
```
# Cross-File Reference: Unresolved `backend.api`

## Why the error occurs

In `base.c4`:

```c4
cloud = system {
  backend = container {
    api = service
  }
}
```

The identifiers here are **shorthand names scoped to their lexical block**. Within the block, `backend` and `api` are local. Their **fully qualified names (FQNs)** in the global model namespace are:

| Shorthand | FQN |
|-----------|-----|
| `cloud`   | `cloud` |
| `backend` | `cloud.backend` |
| `api`     | `cloud.backend.api` |

In `ops.c4`, LikeC4 resolves names **against the global namespace**. When you write:

```c4
backend.api -> cloud.db
```

the parser looks for a top-level element whose name is `backend`. No such element exists — `backend` only exists as a child of `cloud`. The reference `backend.api` therefore cannot be resolved, producing the "unresolved reference" validation error.

`cloud.db` would also be unresolved unless it is defined somewhere, but the scope issue with `backend.api` is the primary error here.

## Corrected relationship using FQNs

Use the full dot-separated path from the root for both endpoints:

```c4
cloud.backend.api -> cloud.db
```

This unambiguously identifies `api` as the service nested two levels inside `cloud`, and `db` as a direct child of `cloud`, regardless of which file the relationship is written in.
