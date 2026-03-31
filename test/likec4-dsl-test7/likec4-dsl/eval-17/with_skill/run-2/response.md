`cloud.backend.api -> cloud.db`

This fails because LikeC4 resolves references by **lexical scope**, not by “same project file set” relative nesting.

`backend.api` is a **relative reference**. It only resolves when the current scope already sits inside `cloud` (or another scope where `backend` is visible as a local child). In `base.c4`, that kind of shorthand works inside the `cloud { ... }` hierarchy.

But `ops.c4` is parsed in its own file context. At the top level of that file, there is no local `backend` symbol. Even though LikeC4 later merges `model { ... }` blocks across files, cross-file references to nested elements must use their **fully qualified name**.

So the corrected cross-file relationship is:

`cloud.backend.api -> cloud.db`
