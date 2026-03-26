`backend.api` is resolved relative to the current scope/file context, not magically to `cloud.backend` across files. In `ops.c4`, that short name is unresolved unless that scope is active there.

Use fully qualified IDs in cross-file relationships:

```likec4
model {
  cloud.backend.api -> cloud.db
}
```