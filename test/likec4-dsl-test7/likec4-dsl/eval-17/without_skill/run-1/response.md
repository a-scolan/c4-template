`backend.api` is unresolved in `ops.c4` because references are resolved by model scope, not by filename.

- In `base.c4`, `api` is nested under `cloud.backend`, so its full id is `cloud.backend.api`.
- In another file (`ops.c4`), writing `backend.api` does **not** mean “the `backend` inside `cloud`”. It is interpreted as a top-level path starting at `backend`, which does not exist.
- LikeC4 merges files into one model, but it does not carry a per-file namespace that would make `backend.api` resolve to `cloud.backend.api`.

Use FQNs for cross-file relationships:

`cloud.backend.api -> cloud.db`