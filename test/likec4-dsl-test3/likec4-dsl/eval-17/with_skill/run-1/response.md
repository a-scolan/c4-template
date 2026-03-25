`backend.api` fails in `ops.c4` because LikeC4 name resolution is lexical and file-local by scope: `backend` is **not** a top-level symbol in that file. It is nested under `cloud` (as `cloud.backend`), and cross-file references should use an unambiguous FQN.

So in another file, reference the service as `cloud.backend.api` (not `backend.api`).

Correct cross-file relationship:

```likec4
model {
  cloud.backend.api -> cloud.db
}
```

Why this works:
- `cloud.backend.api` is the full path (FQN) to the nested element defined in `base.c4`.
- `cloud.db` is also an FQN.
- FQNs are the safe/expected way to reference elements across files in a merged LikeC4 project.