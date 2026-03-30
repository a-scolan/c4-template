# Why `backend.api -> cloud.db` fails and how to fix it

## Root cause

In LikeC4, when you write a relationship outside the element definition block, **all identifiers must be fully-qualified names (FQNs) relative to the model root**. There is no implicit "current scope" or namespace resolution that makes a bare name like `backend` resolve to `cloud.backend`.

In `ops.c4`, the identifier `backend` is not defined at the top level of *that* file. It is a nested element inside `cloud` (defined in `base.c4`). LikeC4 parses each file, but the identifier resolution for relationships always starts from the **global model root**. So `backend.api` means "a top-level element named `backend`, with a child named `api`" — which does not exist. The validator correctly reports an unresolved reference.

Similarly, `cloud.db` would only resolve if `db` is actually defined as a child of `cloud` somewhere in the model; if it is not yet defined, that is a separate unresolved reference, but the structural issue with `backend.api` is the one described here.

## The fix: use full FQNs

Replace the relationship in `ops.c4` with the fully-qualified paths from the model root:

```c4
// ops.c4
cloud.backend.api -> cloud.db
```

This resolves correctly because:
- `cloud` is a top-level element (defined in `base.c4`).
- `cloud.backend` is its child container.
- `cloud.backend.api` is the nested service element.
- `cloud.db` is the target element, also addressed from the root.

LikeC4 merges all `.c4` files in the project into a single model, so elements defined in `base.c4` are fully accessible by their FQN in `ops.c4` without any import — but you must always use the complete path from the root.
