Across files, local names are not shared lexically; unresolved `backend` in `ops.c4` happens because cross-file references must use FQNs.

Correct relationship:

```likec4
model {
  cloud.backend.api -> cloud.db
}
```