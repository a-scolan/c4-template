`backend.api` fails across files because LikeC4 references use lexical scoping: in `ops.c4`, the bare reference is resolved from that file’s scope, and there is no top-level `backend` there. Nested elements defined under `cloud` in another file are not addressable cross-file by a partial path, so you must use the full FQN.

```likec4
cloud.backend.api -> cloud.db
```