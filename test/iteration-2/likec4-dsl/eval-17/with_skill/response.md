**Why the error occurs**

LikeC4 uses lexical scoping for identifier resolution. The rule from the skill is explicit: *'To reference across files, FQN must be used.'* and *'Nested elements can be referenced in this file by id, but from other files only using FQN.'*

In `base.c4` the hierarchy is:
```
cloud          ← top-level, FQN = cloud
  backend      ← nested inside cloud, FQN = cloud.backend
    api        ← nested inside backend, FQN = cloud.backend.api
```

Only `cloud` is a top-level identifier visible project-wide by its short name. `backend` and `api` are nested — they are only resolvable by their short names *within* `base.c4`'s own lexical scope.

In `ops.c4`, writing `backend.api -> cloud.db` asks the parser to resolve `backend` as a known name in `ops.c4`'s scope. There is no top-level element named `backend` in the project (`cloud` is the top-level), so the reference is unresolved. Even if `backend` were found, `backend.api` would be treated as a two-segment FQN starting at a top-level named `backend`, which does not exist.

**Corrected relationship using FQNs**

```likec4
model {
  cloud.backend.api -> cloud.db
}
```

Both endpoints use their full dot-separated FQN anchored at the project-level root (`cloud`), which is the only form guaranteed to resolve across files.
