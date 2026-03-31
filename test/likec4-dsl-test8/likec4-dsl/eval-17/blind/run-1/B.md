`backend.api` fails in `ops.c4` because short nested names are not shared as cross-file symbols. In `base.c4`, `backend` is nested inside `cloud`, so the service’s real identifier is `cloud.backend.api`. Across files, LikeC4 requires the full FQN for nested elements; lexical/file-local short references like `backend.api` are not resolved from another file.

Correct cross-file relationship:

```likec4
cloud.backend.api -> cloud.db
```