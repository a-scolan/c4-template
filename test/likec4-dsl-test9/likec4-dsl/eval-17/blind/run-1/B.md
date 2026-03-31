## Why the reference fails

`backend.api` is **not** a cross-file name. It is a **relative identifier**.

LikeC4 merges model files into one model, but reference resolution is still based on the **current scope**, not on the file where an element was originally declared.

In `base.c4`, this declaration:

- `cloud = system { backend = container { api = service } }`

creates the element with the full qualified name:

- `cloud.backend.api`

When you write this in `ops.c4` at top level:

- `backend.api -> cloud.db`

LikeC4 tries to resolve `backend.api` from the **root scope** of that statement. That means it looks for:

- root element `backend`
- child `api` under it

But no root element named `backend` exists. The real path is under `cloud`, so the reference is unresolved.

## Why imports are not the fix

This is not an import problem. The files are part of the same model, but **relative references do not automatically inherit the parent scope from another file**.

So across files, if you reference an element from outside its parent block, use its **FQN**.

## Correct relationship

```likec4
cloud.backend.api -> cloud.db
```

That works because both endpoints are addressed by their full qualified names.