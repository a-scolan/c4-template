`backend.api` is unresolved in `ops.c4` because cross-file references are resolved by absolute element identity (FQN), not by another file’s local lexical path; outside the `cloud` scope, `backend` is not a top-level symbol.

Use the relationship with fully qualified names:

```likec4
cloud.backend.api -> cloud.db
```