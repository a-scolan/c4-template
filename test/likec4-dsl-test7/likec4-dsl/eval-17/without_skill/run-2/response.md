`backend.api` fails in `ops.c4` because name resolution is lexical, not global-by-file. Across files, LikeC4 merges the model, but unqualified/partially qualified identifiers are still resolved from the current scope. In `ops.c4`, `backend` is not a top-level element, so `backend.api` cannot be resolved there.

For cross-file relationships, reference elements by fully qualified names (FQNs) from the root:

`cloud.backend.api -> cloud.db`

(If `db` is also nested under `backend`, then it should be `cloud.backend.db`.)
