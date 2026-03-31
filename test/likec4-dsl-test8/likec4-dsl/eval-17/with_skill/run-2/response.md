`backend.api` fails because cross-file references are **not** resolved relative to the nesting from another file. LikeC4 merges `model { ... }` blocks across files, but lexical scope does not carry over across files: in `ops.c4`, `backend.api` is treated as a top-level path starting from `backend`, and there is no top-level element named `backend`.

For cross-file references, use the full FQN.

```likec4
cloud.backend.api -> cloud.db
```