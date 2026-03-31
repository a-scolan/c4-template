`backend.api` fails because LikeC4 merges `model { ... }` blocks across files **after** parsing, but reference resolution is still **lexical per file**. In `base.c4`, `backend` is **not** a top-level symbol; it is the child of `cloud`, so its real name is the FQN `cloud.backend`, and `api` is `cloud.backend.api`.

That file-local/container scope does **not** carry into `ops.c4`. So in `ops.c4`, `backend.api` is treated as a lookup starting from a top-level `backend`, which does not exist, and validation reports it as unresolved.

So the cross-file rule is:

- short nested references like `backend.api` only work inside the file/scope where `backend` is already in lexical scope
- across files, use the **full FQN from the root**

Corrected cross-file relationship using FQNs:

```likec4
cloud.backend.api -> cloud.backend.db
```

If your database is actually a **direct child of `cloud`** rather than a child of `backend`, then the target FQN would be `cloud.db`, but the source still must be fully qualified:

```likec4
cloud.backend.api -> cloud.db
```