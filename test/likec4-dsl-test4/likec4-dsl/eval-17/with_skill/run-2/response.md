## Why the unresolved reference occurs

LikeC4 uses **lexical scoping**: nested element identifiers are only in scope within the file (lexical context) where they were defined. Short names like `backend` and `api` exist only within the `cloud` element's body in `base.c4`.

When `ops.c4` references `backend.api`, it tries to resolve `backend` as a top-level name in the project. But `backend` is **not** a top-level element — it is a child of `cloud` defined in `base.c4`. It never enters the global namespace, so `ops.c4` cannot see it under that short name.

From the DSL rule: *"Nested elements can be referenced in this file by id, but from other files only using FQN, i.e. `parentid.childid`."*

## Corrected cross-file relationship using FQNs

`cloud` is a top-level element and is globally accessible from any file. Its nested elements are reachable via their FQN (dot-separated path from the top-level ancestor).

```likec4
// ops.c4
model {
  cloud.backend.api -> cloud.db
}
```

- `cloud.backend.api` — full FQN: top-level `cloud` → child `backend` → child `api`
- `cloud.db` — full FQN for the target

Using FQNs for both endpoints makes both references globally resolvable across files without any import statements.
