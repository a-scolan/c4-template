## Why `backend.api` is an unresolved reference in `ops.c4`

LikeC4 uses **lexical scoping**: short identifiers like `backend` and `api` are only in scope within the block where they are defined. In `base.c4`, `backend` is defined as a nested child of `cloud`, not as a top-level identifier. When writing in `ops.c4`, you are at the top-level scope — only `cloud` is directly accessible there. The name `backend` does not exist at that level, so `backend.api` cannot be resolved.

The SKILL rule: *"Nested elements can be referenced in this file by id, but from other files only using FQN, i.e. parentid.childid"*

## Corrected cross-file relationship (no import statements)

Use the full FQN starting from the top-level element:

```likec4
model {
  cloud.backend.api -> cloud.db "calls"
}
```

`cloud.backend.api` is the correct FQN because `cloud` is the top-level element, `backend` is its direct child, and `api` is a child of `backend`.
